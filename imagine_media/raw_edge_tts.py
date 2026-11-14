"""Minimal raw-socket edge-tts client.

Why this exists (2026-11-11): the VM's egress proxy MITMs TLS (Hatch Egress CA)
and strips the `Connection: Upgrade` header from the 101 response, so aiohttp
rejects the websocket handshake ("Invalid connection header"). This client does
the same edge-tts protocol over a raw socket and validates only the 101 status
and the `Upgrade: websocket` header. Message formats are copied from the
installed edge-tts package; only the transport is custom.
"""
import base64
import os
import socket
import ssl
import struct
import sys
from urllib.parse import urlparse

from edge_tts.communicate import (
    connect_id,
    date_to_string,
    escape,
    get_headers_and_data,
    mkssml,
    remove_incompatible_characters,
    ssml_headers_plus_data,
)
from edge_tts.constants import SEC_MS_GEC_VERSION, WSS_HEADERS, WSS_URL
from edge_tts.data_classes import TTSConfig
from edge_tts.drm import DRM

CA_BUNDLE = "/run/hatch/egress-tls/ca-bundle.pem"
TARGET = "speech.platform.bing.com"


def _recv_exact(sock, n):
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("socket closed while reading")
        buf += chunk
    return buf


def _read_http_headers(sock):
    buf = b""
    while b"\r\n\r\n" not in buf:
        chunk = sock.recv(4096)
        if not chunk:
            raise ConnectionError("socket closed during handshake")
        buf += chunk
    head, rest = buf.split(b"\r\n\r\n", 1)
    return head.decode("utf-8", "replace"), rest


def _send_frame(sock, payload: bytes, opcode=0x1):
    mask = os.urandom(4)
    masked = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
    header = bytes([0x80 | opcode])
    n = len(payload)
    if n < 126:
        header += bytes([0x80 | n])
    elif n < 65536:
        header += bytes([0x80 | 126]) + struct.pack(">H", n)
    else:
        header += bytes([0x80 | 127]) + struct.pack(">Q", n)
    sock.sendall(header + mask + masked)


def _recv_frame(sock):
    b0, b1 = _recv_exact(sock, 2)
    fin = bool(b0 & 0x80)
    opcode = b0 & 0x0F
    masked = bool(b1 & 0x80)
    length = b1 & 0x7F
    if length == 126:
        length = struct.unpack(">H", _recv_exact(sock, 2))[0]
    elif length == 127:
        length = struct.unpack(">Q", _recv_exact(sock, 8))[0]
    if masked:
        key = _recv_exact(sock, 4)
    payload = _recv_exact(sock, length)
    if masked:
        payload = bytes(b ^ key[i % 4] for i, b in enumerate(payload))
    return fin, opcode, payload


def _recv_message(sock):
    """Return (opcode, full payload), handling fragmentation and ping."""
    parts = []
    opcode = None
    while True:
        fin, op, payload = _recv_frame(sock)
        if op == 0x9:  # ping -> pong
            _send_frame(sock, payload, opcode=0xA)
            continue
        if op == 0x8:  # close
            raise ConnectionError("server closed the websocket")
        if op in (0x1, 0x2):
            opcode = op
        parts.append(payload)
        if fin:
            return opcode, b"".join(parts)


def synth(text, voice, out_path, rate="+0%", volume="+0%", pitch="+0Hz"):
    proxy = urlparse(os.environ.get("https_proxy") or os.environ.get("HTTPS_PROXY"))
    assert proxy.hostname, "no https_proxy in environment"
    auth = base64.b64encode(f"{proxy.username}:{proxy.password}".encode()).decode()

    raw = socket.create_connection((proxy.hostname, proxy.port or 3128), timeout=20)
    raw.sendall(
        f"CONNECT {TARGET}:443 HTTP/1.1\r\n"
        f"Host: {TARGET}:443\r\n"
        f"Proxy-Authorization: Basic {auth}\r\n"
        "Proxy-Connection: Keep-Alive\r\n\r\n".encode()
    )
    head, _ = _read_http_headers(raw)
    if " 200 " not in head.split("\r\n")[0]:
        raise ConnectionError(f"proxy CONNECT failed: {head.splitlines()[0]}")

    ctx = ssl.create_default_context(cafile=CA_BUNDLE)
    sock = ctx.wrap_socket(raw, server_hostname=TARGET)
    # 2026-11-13: raised from 30s — the WS handshake timed out twice at 30s
    # while the proxy path itself was fine (curl reached the host in <1s).
    sock.settimeout(90)

    url = (
        f"{WSS_URL}&ConnectionId={connect_id()}"
        f"&Sec-MS-GEC={DRM.generate_sec_ms_gec()}"
        f"&Sec-MS-GEC-Version={SEC_MS_GEC_VERSION}"
    )
    path = url[len(f"wss://{TARGET}"):]
    headers = DRM.headers_with_muid(WSS_HEADERS)
    key = base64.b64encode(os.urandom(16)).decode()
    # Build the header block as a dict so nothing is duplicated (WSS_HEADERS
    # already carries Sec-WebSocket-Version; a duplicate made the server 400).
    hdrs = dict(headers)
    hdrs.setdefault("Accept", "*/*")
    hdrs["Upgrade"] = "websocket"
    hdrs["Connection"] = "Upgrade"
    hdrs["Sec-WebSocket-Key"] = key
    req_lines = [f"GET {path} HTTP/1.1", f"Host: {TARGET}"]
    req_lines += [f"{k}: {v}" for k, v in hdrs.items()]
    req_lines += ["", ""]
    sock.sendall("\r\n".join(req_lines).encode())
    head, _ = _read_http_headers(sock)
    status = head.split("\r\n")[0]
    if " 101 " not in status:
        raise ConnectionError(f"websocket handshake failed: {status}")
    # NOTE: deliberately NOT checking the Connection header -- the egress
    # proxy strips it. Only the Upgrade header is verified.
    lower = head.lower()
    if "upgrade: websocket" not in lower:
        raise ConnectionError(f"handshake 101 without Upgrade header: {head}")

    tc = TTSConfig(voice, rate, volume, pitch, "SentenceBoundary")
    config_msg = (
        f"X-Timestamp:{date_to_string()}\r\n"
        "Content-Type:application/json; charset=utf-8\r\n"
        "Path:speech.config\r\n\r\n"
        '{"context":{"synthesis":{"audio":{"metadataoptions":'
        '{"sentenceBoundaryEnabled":"true","wordBoundaryEnabled":"false"},'
        '"outputFormat":"audio-24khz-48kbitrate-mono-mp3"}}}}\r\n'
    )
    _send_frame(sock, config_msg.encode("utf-8"), opcode=0x1)

    clean = escape(remove_incompatible_characters(text))
    ssml = mkssml(tc, clean)
    _send_frame(
        sock,
        ssml_headers_plus_data(connect_id(), date_to_string(), ssml).encode("utf-8"),
        opcode=0x1,
    )

    audio = bytearray()
    while True:
        opcode, payload = _recv_message(sock)
        if opcode == 0x1:
            header_len = payload.find(b"\r\n\r\n")
            params, _ = get_headers_and_data(payload, header_len)
            path = params.get(b"Path")
            if path == b"turn.end":
                break
            continue
        if opcode == 0x2:
            if len(payload) < 2:
                continue
            header_length = int.from_bytes(payload[:2], "big")
            params, data = get_headers_and_data(payload, header_length)
            if params.get(b"Path") != b"audio":
                continue
            if data:
                audio.extend(data)
    try:
        sock.close()
    except Exception:
        pass
    if not audio:
        raise RuntimeError("no audio received")
    with open(out_path, "wb") as f:
        f.write(bytes(audio))
    return len(audio)


# Shortened 2026-11-11: first draft ran 27.0s total; each segment must fit its
# 4s window, so every line is <=18 chars. Rate +10% for short-video pacing.
RATE = "+10%"
SEGMENTS = [
    "随机往正方形里撒点，能算出圆周率。",
    "正方形里画个圆，数数圆里的点。",
    "圆里点数除以总数，再乘四，就是派。",
    "点撒得越多，这个数越接近三点一四。",
    "蒙特卡洛，1600 个点，算出 3.15。",
]

if __name__ == "__main__":
    out_dir = os.path.expanduser("~/workspace/imagine_media/mc-narration")
    os.makedirs(out_dir, exist_ok=True)
    for i, text in enumerate(SEGMENTS, 1):
        path = os.path.join(out_dir, f"seg{i}.mp3")
        n = synth(text, "zh-CN-XiaoxiaoNeural", path, rate=RATE)
        print(f"seg{i} OK: {n} bytes -> {path}")
