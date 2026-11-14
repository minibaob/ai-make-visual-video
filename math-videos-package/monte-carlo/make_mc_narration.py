"""Generate Monte Carlo narration with edge-tts through the Hatch egress proxy.

Two VM-specific fixes (both discovered 2026-11-11):
1. edge-tts uses certifi's CA bundle, which lacks the Hatch Sandbox Egress CA
   that MITMs TLS here -> rebuild its SSL context from the runtime bundle.
2. The egress proxy password rotates -> read the proxy URL fresh from the
   environment in this same process, never hardcode it.
"""
import asyncio
import os
import ssl

import edge_tts.communicate as comm

comm._SSL_CTX = ssl.create_default_context(
    cafile="/run/hatch/egress-tls/ca-bundle.pem"
)

SEGMENTS = [
    "随机往正方形里撒点，居然能算出圆周率。",
    "正方形里画一个内切圆，数一数，落在圆里的点有多少。",
    "圆里的点，除以总点数，再乘以四，就约等于派。",
    "点撒得越多，这个数就越接近三点一四。",
    "这就是蒙特卡洛方法，随机，也能算出派。一千六百个点，算出来三点一五。",
]

VOICE = "zh-CN-XiaoxiaoNeural"
OUT = os.path.expanduser("~/workspace/imagine_media/mc-narration")


async def main():
    proxy = os.environ.get("https_proxy") or os.environ.get("HTTPS_PROXY")
    assert proxy, "no https_proxy in environment"
    for i, text in enumerate(SEGMENTS, 1):
        path = os.path.join(OUT, f"seg{i}.mp3")
        communicate = comm.Communicate(text, VOICE, proxy=proxy)
        with open(path, "wb") as f:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    f.write(chunk["data"])
        print(f"seg{i} -> {path} ({os.path.getsize(path)} bytes)")


asyncio.run(main())
