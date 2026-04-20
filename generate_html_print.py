import os
import time
from playwright.sync_api import sync_playwright

def generate_print_cards():
    print_dir = "print"
    os.makedirs(print_dir, exist_ok=True)

    current_dir = os.path.abspath(os.path.dirname(__file__))
    front_url = f"file://{os.path.join(current_dir, 'print_front.html')}"
    back_url = f"file://{os.path.join(current_dir, 'print_back.html')}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Use high device scale factor to ensure 300 DPI equivalent quality
        # 1125x675 with dsf=1 is already standard, but let's make it crispy
        context = browser.new_context(
            viewport={'width': 1125, 'height': 675},
            device_scale_factor=2
        )
        page = context.new_page()

        # Render Front
        print("Rendering front...")
        page.goto(front_url)
        # Wait for web fonts to load
        page.wait_for_load_state("networkidle")
        time.sleep(1) # Extra buffer for fonts
        page.screenshot(path=os.path.join(print_dir, "business_card_front.png"))
        page.pdf(
            path=os.path.join(print_dir, "business_card_front.pdf"),
            width="3.75in",
            height="2.25in",
            print_background=True,
            page_ranges="1"
        )

        # Render Back
        print("Rendering back...")
        page.goto(back_url)
        page.wait_for_load_state("networkidle")
        time.sleep(1)
        page.screenshot(path=os.path.join(print_dir, "business_card_back.png"))
        page.pdf(
            path=os.path.join(print_dir, "business_card_back.pdf"),
            width="3.75in",
            height="2.25in",
            print_background=True,
            page_ranges="1"
        )

        browser.close()
        print("Done!")

if __name__ == "__main__":
    generate_print_cards()
