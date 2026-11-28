import os
from playwright.sync_api import sync_playwright
OUT = os.path.expanduser("~/workspace/douyin-ai-video/media/claude04/shots")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox","--disable-dev-shm-usage","--disable-gpu","--disable-http2"], proxy={"server":"http://127.0.0.1:18080","bypass":"127.0.0.1,localhost"})
    ctx = browser.new_context(viewport={"width":1440,"height":1000}, ignore_https_errors=True, user_agent=("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/159.0.0.0 Safari/537.36"))
    for name, url, btn in [
        ("claude-free", "http://127.0.0.1:8901/pricing.html", "Reject all cookies"),
        ("cursor-premium", "http://127.0.0.1:8902/pricing.html", "Reject All"),
    ]:
        page = ctx.new_page()
        page.goto(url, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(3000)
        try:
            page.get_by_text(btn, exact=True).click(timeout=5000)
            page.wait_for_timeout(1200)
            print(name, "cookie dialog dismissed")
        except Exception as e:
            print(name, "no cookie button:", str(e)[:80])
        y = page.evaluate("""() => {
            const els=[...document.querySelectorAll('body *')].filter(e=>e.children.length===0 && (e.textContent.trim()==='Free' || /\\$30/.test(e.textContent)));
            if(!els.length) return null;
            const r=els[0].getBoundingClientRect(); return Math.round(r.y+window.scrollY);
        }""")
        print(name, "target y=", y)
        page.screenshot(path=os.path.join(OUT, f"{name}.png"), full_page=True, clip={"x":0,"y":max(0,y-120),"width":1440,"height":760})
        page.close()
    browser.close()
print("done")
