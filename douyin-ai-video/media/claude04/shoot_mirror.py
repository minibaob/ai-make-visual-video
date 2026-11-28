#!/usr/bin/env python3
"""Screenshot pricing rows from the local mirror + Antigravity footnote (live)."""
import os
from playwright.sync_api import sync_playwright

OUT = os.path.expanduser("~/workspace/douyin-ai-video/media/claude04/shots")

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu",
              "--disable-http2"],
        proxy={"server": "http://127.0.0.1:18080", "bypass": "127.0.0.1,localhost"},
    )
    ctx = browser.new_context(
        viewport={"width": 1440, "height": 1000},
        ignore_https_errors=True,
        user_agent=("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/159.0.0.0 Safari/537.36"),
    )

    def shot(name, url, needle_fn, clip_h=760):
        page = ctx.new_page()
        try:
            page.goto(url, wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(3000)
            info = page.evaluate("""() => {
                return {sheets: document.styleSheets.length,
                        h: document.body.scrollHeight};
            }""")
            print(f"{name}: stylesheets={info['sheets']} pageH={info['h']}")
            y = page.evaluate(needle_fn)
            print(f"{name}: target y={y}")
            if y is not None:
                page.screenshot(path=os.path.join(OUT, f"{name}.png"),
                                full_page=True,
                                clip={"x": 0, "y": max(0, y - 120),
                                      "width": 1440, "height": clip_h})
                print(f"  saved {name}.png")
        except Exception as e:
            print(f"{name}: FAILED {type(e).__name__}: {e}", flush=True)
        page.close()

    # Claude Free $0 card (local mirror, real CSS/JS)
    shot("claude-free", "http://127.0.0.1:8901/pricing.html",
         """() => {
            const els=[...document.querySelectorAll('body *')].filter(e=>e.children.length===0 && e.textContent.trim()==='Free');
            if(!els.length) return null;
            const r=els[0].getBoundingClientRect(); return Math.round(r.y+window.scrollY);
         }""")
    # Cursor Premium $30 (local mirror)
    shot("cursor-premium", "http://127.0.0.1:8902/pricing.html",
         """() => {
            const els=[...document.querySelectorAll('body *')].filter(e=>e.children.length===0 && /\\$30/.test(e.textContent));
            if(!els.length) return null;
            const r=els[0].getBoundingClientRect(); return Math.round(r.y+window.scrollY);
         }""")
    # Antigravity footnote (live page, styles load fine)
    shot("antigravity-footnote", "https://antigravity.google/pricing",
         """() => {
            const els=[...document.querySelectorAll('body *')].filter(e=>e.children.length===0 && /Will be removed on November 30/.test(e.textContent));
            if(!els.length) return null;
            const r=els[0].getBoundingClientRect(); return Math.round(r.y+window.scrollY);
         }""", clip_h=1000)
    browser.close()
print("done")
