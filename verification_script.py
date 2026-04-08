import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 414, "height": 896})
        await page.goto('file:///app/index.html')
        await page.wait_for_timeout(2000) # Wait 2 seconds

        # Scroll down to trigger scroll-based animations
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

        await page.wait_for_timeout(3000) # Wait 3 more seconds for GSAP animations

        await page.screenshot(path='/app/verification.png', full_page=True)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
