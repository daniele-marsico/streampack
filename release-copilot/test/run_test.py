# Loads the real extension in Chrome, serves the mock form as distrokid.com, fills it.
import asyncio, json, sys, pathlib
from playwright.async_api import async_playwright
EXT = str(pathlib.Path(__file__).resolve().parent.parent / 'extension')
HTML = (pathlib.Path(__file__).parent / 'distrokid-mock.html').read_text()
PKG = {"artist":"Daniele M","type":"ep","releaseTitle":"Notte Minore","releaseDate":"2026-12-20","label":"","primaryGenre":"R&B/Soul","secondaryGenre":"Electronic","language":"Italian","aiUsage":"none",
 "tracks":[{"title":"Vetro","songwriters":[{"first":"Daniele","last":"Marsico"}],"explicit":False,"instrumental":False},
           {"title":"Luci Basse","songwriters":[{"first":"Daniele","last":"Marsico"}],"explicit":True,"instrumental":False}]}
async def main():
  async with async_playwright() as p:
    ctx = await p.chromium.launch_persistent_context('/tmp/rc-profile', executable_path='/usr/bin/google-chrome', headless=True,
      args=[f'--disable-extensions-except={EXT}', f'--load-extension={EXT}', '--headless=new', '--no-sandbox'])
    sw = ctx.service_workers[0] if ctx.service_workers else await ctx.wait_for_event('serviceworker')
    await sw.evaluate('p => chrome.storage.local.set({pkg: p, "overrides:distrokid.com": {}})', PKG)
    await ctx.route('https://distrokid.com/**', lambda r: r.fulfill(body=HTML, content_type='text/html'))
    page = await ctx.new_page()
    await page.goto('https://distrokid.com/new/')
    await page.wait_for_selector('#rc-root', state='attached', timeout=8000)
    fab = page.locator('#rc-root').locator('css=#fab')
    await fab.click()
    # pick files in the copilot panel
    await page.locator('#rc-root').locator('css=input[data-k="cover"]').set_input_files(files=[{"name":"cover.jpg","mimeType":"image/jpeg","buffer":b"x"}])
    await page.locator('#rc-root').locator('css=input[data-k="audio:0"]').set_input_files(files=[{"name":"vetro.wav","mimeType":"audio/wav","buffer":b"x"}])
    await page.locator('#rc-root').locator('css=#fill').click()
    await page.wait_for_timeout(500)
    vals = await page.evaluate('''() => { const o={}; document.querySelectorAll('form input,form select').forEach(e=>{
      const k=e.name||e.id||e.getAttribute('aria-label'); if(e.type==='radio'){ if(e.checked) o[e.name]=e.value } else if(e.type==='file'){o[k]=e.files.length?e.files[0].name:''} else o[k+(o[k]!==undefined?'#2':'')]=e.value}); return o }''')
    print(json.dumps(vals, indent=1))
    rep = await page.locator('#rc-root').locator('css=ul').inner_text()
    print(rep)
    # point out the unknown field for "Album title", then it must fill it
    await page.locator('#rc-root').locator('css=button[data-pick="release.releaseTitle"]').click()
    await page.click('#weird')
    await page.wait_for_timeout(400)
    print('WEIRD after pick:', await page.input_value('#weird'))
    await page.screenshot(path='shot.png', full_page=True)
    # panel page renders
    pg = await ctx.new_page()
    await pg.goto(f'chrome-extension://{sw.url.split("/")[2]}/panel/panel.html')
    await pg.wait_for_timeout(500)
    print('CHECKS:', await pg.locator('#checks').inner_text())
    await pg.set_viewport_size({'width':380,'height':1400})
    await pg.screenshot(path='panel.png', full_page=True)
    await ctx.close()
asyncio.run(main())
