import os
from playwright.sync_api import sync_playwright
OUT = os.path.expanduser("~/workspace/douyin-ai-video/media/claude04/shots")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox","--disable-dev-shm-usage","--disable-gpu","--disable-http2"], proxy={"server":"http://127.0.0.1:18080","bypass":"127.0.0.1,localhost"})
    ctx = browser.new_context(viewport={"width":1440,"height":1000}, ignore_https_errors=True, user_agent=("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/159.0.0.0 Safari/537.36"))
    page = ctx.new_page()
    page.goto("https://antigravity.google/pricing", wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(2500)
    hits = page.evaluate("""() => {
        const out = [];
        for (const el of document.querySelectorAll('body *')) {
            const t = (el.textContent || '');
            if (t.includes('Claude Sonnet 4.6') && t.length < 80) {
                const r = el.getBoundingClientRect();
                if (r.width > 20 && r.height > 5) out.push({tag: el.tagName, text: t.trim().slice(0,70), y: Math.round(r.y + window.scrollY), h: Math.round(r.height)});
            }
        }
        return out.slice(0, 10);
    }""")
    for h in hits: print(h)
    if hits:
        y = hits[0]["y"]
        page.screenshot(path=os.path.join(OUT, "antigravity-models.png"), full_page=True, clip={"x":0,"y":max(0,y-460),"width":1440,"height":900})
        print("saved antigravity-models.png at", max(0, y-460))
    page.close(); browser.close()
print("done")
