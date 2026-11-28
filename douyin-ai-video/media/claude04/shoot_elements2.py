#!/usr/bin/env python3
"""Locate pricing rows/footnotes and take viewport screenshots after scrolling."""
import os
from playwright.sync_api import sync_playwright

OUT = os.path.expanduser("~/workspace/douyin-ai-video/media/claude04/shots")

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu", "--disable-http2"],
        proxy={"server": "http://127.0.0.1:18080"},
    )
    ctx = browser.new_context(
        viewport={"width": 1440, "height": 1000},
        ignore_https_errors=True,
        user_agent=("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/159.0.0.0 Safari/537.36"),
    )

    # --- Claude pricing: find $0 / $20 price texts in main content ---
    page = ctx.new_page()
    page.goto("https://claude.com/pricing", wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(2500)
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)
    hits = page.evaluate("""() => {
        const out = [];
        for (const el of document.querySelectorAll('body *')) {
            if (el.children.length > 0) continue;
            const t = (el.textContent || '').trim();
            if (/^\\$\\s?0$/.test(t) || /^\\$\\s?20/.test(t) || t === 'Free' || t === 'Pro') {
                const r = el.getBoundingClientRect();
                if (r.width > 10 && r.height > 8) {
                    out.push({text: t.slice(0, 40), y: Math.round(r.y + window.scrollY)});
                }
            }
        }
        return out.slice(0, 25);
    }""")
    for h in hits:
        print("claude:", h)
    # scroll to first $0 hit and screenshot viewport
    y0 = next((h["y"] for h in hits if h["text"].startswith("$0")), None)
    if y0 is not None:
        page.evaluate(f"window.scrollTo(0, {max(0, y0 - 250)})")
        page.wait_for_timeout(800)
        page.screenshot(path=os.path.join(OUT, "claude-free.png"))
        print("saved claude-free.png at scroll", max(0, y0 - 250))
    page.close()

    # --- Cursor pricing: find $30 ---
    page = ctx.new_page()
    page.goto("https://cursor.com/pricing", wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(2500)
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)
    hits = page.evaluate("""() => {
        const out = [];
        for (const el of document.querySelectorAll('body *')) {
            if (el.children.length > 0) continue;
            const t = (el.textContent || '').trim();
            if (/\\$30/.test(t) || t === 'Premium') {
                const r = el.getBoundingClientRect();
                if (r.width > 10 && r.height > 8) {
                    out.push({text: t.slice(0, 50), y: Math.round(r.y + window.scrollY)});
                }
            }
        }
        return out.slice(0, 25);
    }""")
    for h in hits:
        print("cursor:", h)
    y0 = next((h["y"] for h in hits if "$30" in h["text"]), None)
    if y0 is not None:
        page.evaluate(f"window.scrollTo(0, {max(0, y0 - 250)})")
        page.wait_for_timeout(800)
        page.screenshot(path=os.path.join(OUT, "cursor-premium.png"))
        print("saved cursor-premium.png at scroll", max(0, y0 - 250))
    page.close()

    # --- Antigravity pricing: search for 4.6 / November / footnote ---
    page = ctx.new_page()
    page.goto("https://antigravity.google/pricing", wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(2500)
    txt = page.evaluate("() => document.body.innerText")
    import re
    for m in re.finditer(r"4\.6", txt):
        print("antigravity 4.6 ctx:", repr(txt[max(0, m.start()-120):m.end()+120]))
    for pat in ["November 30", "Nov 30", "11/30", "11-30", "remov", "until"]:
        for m in re.finditer(pat, txt, re.I):
            print(f"antigravity {pat!r}:", repr(txt[max(0, m.start()-100):m.end()+100]))
            break
    print("antigravity page text len:", len(txt))
    page.close()
    browser.close()
print("done")
