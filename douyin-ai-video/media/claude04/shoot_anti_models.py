import os
from playwright.sync_api import sync_playwright
OUT = os.path.expanduser("~/workspace/douyin-ai-video/media/claude04/shots")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox","--disable-dev-shm-usage","--disable-gpu","--disable-http2"], proxy={"server":"http://127.0.0.1:18080","bypass":"127.0.0.1,localhost"})
    ctx = browser.new_context(viewport={"width":1440,"height":1000}, ignore_https_errors=True, user_agent=("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/159.0.0.0 Safari/537.36"))
    page = ctx.new_page()
    page.goto("https://antigravity.google/pricing", wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(2500)
    # free-tier models list: first "Claude Sonnet 4.6" occurrence
    y = page.evaluate("""() => {
        const els=[...document.querySelectorAll('body *')].filter(e=>e.children.length===0 && /Claude Sonnet 4\\.6/.test(e.textContent));
        if(!els.length) return null;
        const r=els[0].getBoundingClientRect(); return Math.round(r.y+window.scrollY);
    }""")
    print("Claude Sonnet 4.6 y =", y)
    # also locate the free-tier plan heading above it for context
    y2 = page.evaluate("""() => {
        const els=[...document.querySelectorAll('body *')].filter(e=>e.children.length===0 && /^(Free|For Individuals)/.test(e.textContent.trim()));
        return els.slice(0,5).map(e=>{const r=e.getBoundingClientRect(); return {t:e.textContent.trim(), y:Math.round(r.y+window.scrollY)};});
    }""")
    print("headings:", y2)
    if y:
        page.screenshot(path=os.path.join(OUT, "antigravity-models.png"), full_page=True, clip={"x":0,"y":max(0,y-420),"width":1440,"height":900})
        print("saved antigravity-models.png")
    page.close(); browser.close()
print("done")
