import os
import sys

# Custom venv site-packages path
venv_site_packages = "/opt/data/cloak-venv/lib/python3.13/site-packages"
if venv_site_packages not in sys.path:
    sys.path.insert(0, venv_site_packages)

try:
    from cloakbrowser import launch
    print("--- Initializing Cloak Browser ---")
    
    # Launch in headless mode for testing
    browser = launch(headless=True)
    page = browser.new_page()
    
    print("--- Navigating to Sannysoft Bot Test ---")
    page.goto("https://bot.sannysoft.com", wait_until="networkidle")
    
    title = page.title()
    print(f"Page title: {title}")
    
    screenshot_path = "/opt/data/cloak_test_result.png"
    page.screenshot(path=screenshot_path)
    print(f"Screenshot saved to: {screenshot_path}")
    
    browser.close()
    print("--- Test completed successfully ---")
    
except Exception as e:
    print(f"Test failed: {e}")
    sys.exit(1)
