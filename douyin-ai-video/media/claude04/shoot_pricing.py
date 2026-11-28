#!/usr/bin/env python3
"""Screenshot the three pricing pages for Douyin AI video 04 (Claude Code).

Uses Playwright Chromium (unpatched build) via the local no-auth CONNECT
forwarder on 127.0.0.1:18080 (see /tmp/localproxy.py). ignore_https_errors
because the egress proxy MITMs TLS with the Hatch CA.
"""
import os
from playwright.sync_api import sync_playwright

OUT = os.path.expanduser("~/workspace/douyin-ai-video/media/claude04/shots")
os.makedirs(OUT, exist_ok=True)

PAGES = [
    ("claude-pricing", "https://claude.com/pricing"),
    ("cursor-pricing", "https://cursor.com/pricing"),
    ("antigravity-models", "https://antigravity.google/models"),
]

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu",
              "--hide-scrollbars"],
        proxy={"server": "http://127.0.0.1:18080"},
    )
    ctx = browser.new_context(
        viewport={"width": 1440, "height": 1000},
        ignore_https_errors=True,
        user_agent=("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/159.0.0.0 Safari/537.36"),
    )
    for name, url in PAGES:
        page = ctx.new_page()
        try:
            page.goto(url, wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(3000)
            page.screenshot(path=os.path.join(OUT, f"{name}-full.png"),
                            full_page=True)
            print(f"{name}: OK, height={page.evaluate('document.body.scrollHeight')}", flush=True)
        except Exception as e:
            print(f"{name}: FAILED {type(e).__name__}: {e}", flush=True)
        page.close()
    browser.close()
print("done")
