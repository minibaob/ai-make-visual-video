from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--no-sandbox","--disable-dev-shm-usage","--disable-gpu", "--disable-http2"], proxy={"server":"http://127.0.0.1:18080"})
    ctx = b.new_context(viewport={"width":1440,"height":1000}, ignore_https_errors=True)
    page = ctx.new_page()
    fails = []
    page.on("requestfailed", lambda r: fails.append((r.url[:110], r.failure or "")))
    page.on("response", lambda r: fails.append((r.url[:110], f"HTTP {r.status}")) if r.status >= 400 else None)
    page.goto("https://claude.com/pricing", wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(8000)
    print("failed/non-2xx requests:")
    for u, f in fails[:25]: print("  ", f, u)
    print("stylesheets:", page.evaluate("document.styleSheets.length"))
    print("Free heading font:", page.evaluate("""() => { const els=[...document.querySelectorAll('*')].filter(e=>e.children.length===0 && e.textContent.trim()==='Free'); if(!els.length) return 'not found'; const cs=getComputedStyle(els[0]); return cs.fontFamily+' / '+cs.fontSize+' / '+cs.fontWeight; }"""))
    b.close()
