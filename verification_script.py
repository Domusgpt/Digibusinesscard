import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 414, "height": 896})

        page.on("console", lambda msg: print(f"Browser console: {msg.text}"))
        page.on("pageerror", lambda err: print(f"Browser error: {err}"))

        await page.goto('file:///app/index.html')
        await page.wait_for_timeout(4000) # Wait 4 seconds for GSAP animations

        await page.screenshot(path='/app/verification.png', full_page=True)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
