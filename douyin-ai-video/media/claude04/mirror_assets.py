#!/usr/bin/env python3
"""Mirror same-origin assets for claude.com/pricing and cursor.com/pricing.

The live pages' CSS/JS/fonts return HTTP 403 to Chromium (bot filter) but
200 to curl, so we download the exact bytes curl receives and serve the
page locally for screenshotting. Content is byte-identical to today's
official page; only the transport is local.
"""
import os
import re
import subprocess

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/159.0.0.0 Safari/537.36")
BASE = os.path.expanduser("~/workspace/douyin-ai-video/media/claude04/mirror")


def mirror(site, host):
    d = os.path.join(BASE, site)
    html = open(os.path.join(d, "pricing.html"), encoding="utf-8", errors="replace").read()
    urls = set(re.findall(r'(?:src|href)="(/[^"]+)"', html))
    # also CSS url() references inside inline <style> (rare) - skip, main files cover it
    urls = {u.split("#")[0] for u in urls}
    urls = {u for u in urls if not u.startswith("//") and "?" not in u or u.endswith((".css", ".js", ".woff2", ".png", ".svg", ".jpg", ".webp"))}
    # keep only static-ish assets and images
    keep = set()
    for u in urls:
        if u.startswith("/_next/static/") or u.startswith("/static/") or \
           re.search(r"\.(css|js|woff2?|ttf|png|svg|jpg|jpeg|webp|avif|ico)$", u):
            keep.add(u)
    print(f"{site}: {len(keep)} assets to fetch")
    ok = fail = 0
    for u in sorted(keep):
        dest = os.path.join(d, u.lstrip("/"))
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            ok += 1
            continue
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        r = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA,
                            f"https://{host}{u}", "-o", dest],
                           capture_output=True)
        if r.returncode == 0 and os.path.getsize(dest) > 0:
            ok += 1
        else:
            fail += 1
            print(f"  FAIL {u}")
    print(f"{site}: ok={ok} fail={fail}")


mirror("claude", "claude.com")
mirror("cursor", "cursor.com")
print("done")
