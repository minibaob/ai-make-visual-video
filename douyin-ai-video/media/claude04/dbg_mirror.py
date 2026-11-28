from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--no-sandbox","--disable-dev-shm-usage","--disable-gpu","--disable-http2"], proxy={"server":"http://127.0.0.1:18080","bypass":"127.0.0.1,localhost"})
    ctx = b.new_context(viewport={"width":1440,"height":1000}, ignore_https_errors=True)
    page = ctx.new_page()
    fails = []
    page.on("requestfailed", lambda r: fails.append(("FAIL", r.url[:100], str(r.failure)[:60])))
    page.on("response", lambda r: fails.append((r.status, r.url[:100], "")) if r.status >= 400 else None)
    page.goto("http://127.0.0.1:8901/claude/pricing.html", wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(4000)
    print("failed requests:", len(fails))
    for f in fails[:15]: print("  ", f)
    print(page.evaluate("""() => {
        const els=[...document.querySelectorAll('*')].filter(e=>e.children.length===0 && e.textContent.trim()==='Free');
        const el = els[0]; const cs = getComputedStyle(el);
        let rules = 0; for (const sh of document.styleSheets) { try { rules += sh.cssRules.length; } catch(e){} }
        // find nearest ancestor with a class containing card/plan
        let a = el.parentElement, chain = [];
        for (let i=0;i<6 && a;i++){ chain.push(a.tagName+'.'+(a.className.baseVal!==undefined?'svg':String(a.className).slice(0,80))); a=a.parentElement; }
        return {font: cs.fontFamily, size: cs.fontSize, weight: cs.fontWeight, color: cs.color,
                rules, sheets: document.styleSheets.length, chain};
    }"""))
    b.close()
