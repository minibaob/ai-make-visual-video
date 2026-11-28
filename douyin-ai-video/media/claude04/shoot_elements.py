#!/usr/bin/env python3
"""Element-targeted screenshots for video 04: pricing rows + Antigravity footnote."""
import os
from playwright.sync_api import sync_playwright

OUT = os.path.expanduser("~/workspace/douyin-ai-video/media/claude04/shots")
os.makedirs(OUT, exist_ok=True)

JOBS = [
    # (name, url, text to find, clip height)
    ("claude-free", "https://claude.com/pricing", "Free", 800),
    ("claude-pro", "https://claude.com/pricing", "Pro", 800),
    ("cursor-premium", "https://cursor.com/pricing", "Premium", 800),
    ("antigravity-pricing", "https://antigravity.google/pricing", "Claude", 900),
    ("antigravity-home", "https://antigravity.google/", "Claude", 900),
]

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"],
        proxy={"server": "http://127.0.0.1:18080"},
    )
    ctx = browser.new_context(
        viewport={"width": 1440, "height": 1000},
        ignore_https_errors=True,
        user_agent=("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/159.0.0.0 Safari/537.36"),
    )
    for name, url, needle, clip_h in JOBS:
        page = ctx.new_page()
        try:
            page.goto(url, wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(2500)
            page.keyboard.press("Escape")
            page.wait_for_timeout(500)
            # find visible elements whose own text starts with the needle
            info = page.evaluate("""(needle) => {
                const out = [];
                const els = document.querySelectorAll('body *');
                for (const el of els) {
                    if (el.children.length > 0) continue;
                    const t = (el.textContent || '').trim();
                    if (t === needle || t.startsWith(needle + ' ') || t.startsWith(needle + '\\n')) {
                        const r = el.getBoundingClientRect();
                        if (r.width > 20 && r.height > 10) {
                            out.push({text: t.slice(0, 60), x: r.x, y: r.y + window.scrollY,
                                      w: r.width, h: r.height});
                        }
                    }
                }
                return out.slice(0, 12);
            }""", needle)
            print(f"== {name} ({url}): {len(info)} matches")
            for m in info:
                print("   ", m)
            if info:
                y = max(0, int(info[0]["y"]) - 120)
                page.screenshot(path=os.path.join(OUT, f"{name}.png"),
                                clip={"x": 0, "y": y, "width": 1440,
                                      "height": min(clip_h, 3000)})
                print(f"    saved {name}.png at y={y}")
        except Exception as e:
            print(f"{name}: FAILED {type(e).__name__}: {e}", flush=True)
        page.close()
    browser.close()
print("done")
