# Opens the real extension panel in Chrome, fills a package and walks the guided copy.
import asyncio, pathlib
from playwright.async_api import async_playwright
EXT = str(pathlib.Path(__file__).resolve().parent.parent / 'extension')
PKG = {"artist":"Daniele M","type":"ep","releaseTitle":"Notte Minore","releaseDate":"2026-12-20","primaryGenre":"R&B/Soul","secondaryGenre":"Electronic","language":"Italian",
 "tracks":[{"title":"Vetro","songwriters":[{"first":"Daniele","last":"Marsico"}]},{"title":"Luci Basse","explicit":True,"songwriters":[{"first":"Daniele","last":"Marsico"}]}]}
async def main():
  async with async_playwright() as p:
    ctx = await p.chromium.launch_persistent_context('/tmp/rc-profile', executable_path='/usr/bin/google-chrome', headless=True,
      args=[f'--disable-extensions-except={EXT}', f'--load-extension={EXT}', '--headless=new', '--no-sandbox', '--lang=it'], permissions=['clipboard-read','clipboard-write'], locale='it-IT')
    sw = ctx.service_workers[0] if ctx.service_workers else await ctx.wait_for_event('serviceworker')
    await sw.evaluate('p => chrome.storage.local.set({pkg: p})', PKG)
    pg = await ctx.new_page()
    await pg.set_viewport_size({'width':380,'height':1100})
    await pg.goto(f'chrome-extension://{sw.url.split("/")[2]}/panel/panel.html')
    await pg.wait_for_timeout(300)
    await pg.click('#tabUp')
    for _ in range(3):
      print('BTN:', await pg.inner_text('#next')); await pg.click('#next'); await pg.wait_for_timeout(1000)
      print('  clipboard =', await pg.evaluate('navigator.clipboard.readText()'))
    print('BTN:', await pg.inner_text('#next'))
    await pg.screenshot(path='upload.png', full_page=True)
    await ctx.close()
asyncio.run(main())
