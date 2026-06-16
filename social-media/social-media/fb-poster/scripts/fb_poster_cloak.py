import os
import sys
import json
import time

# Support for CloakBrowser stealth posting
# Installation: uv venv /opt/data/cloak-venv && VIRTUAL_ENV=/opt/data/cloak-venv uv pip install cloakbrowser

venv_site_packages = "/opt/data/cloak-venv/lib/python3.13/site-packages"
if venv_site_packages not in sys.path:
    sys.path.insert(0, venv_site_packages)

try:
    from cloakbrowser import launch
except ImportError:
    print(json.dumps({"success": False, "error": "cloakbrowser not installed in /opt/data/cloak-venv"}))
    sys.exit(1)

def post_to_facebook(content_file, image_file=None, state_path="/opt/data/fb-content/fb_state.json"):
    with open(content_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            content = parts[2].strip()

    browser = None
    try:
        browser = launch(headless=True, humanize=True)
        context = browser.new_context(storage_state=state_path)
        page = context.new_page()
        
        page.goto("https://www.facebook.com/", wait_until="domcontentloaded", timeout=60000)
        time.sleep(5)
        
        # Open Composer
        composer_opened = False
        text_selectors = ['span:has-text("bạn đang nghĩ gì thế?")', 'div[role="button"]:has-text("bạn đang nghĩ gì thế?")']
        
        for selector in text_selectors:
            if page.is_visible(selector, timeout=5000):
                page.click(selector)
                composer_opened = True
                break
        
        if not composer_opened:
            raise Exception("Facebook composer not found (Login expired?)")

        editor_selector = 'div[role="dialog"] div[contenteditable="true"]'
        page.wait_for_selector(editor_selector, state="visible", timeout=15000)
        
        # Human-like typing
        page.focus(editor_selector)
        page.keyboard.type(content, delay=100)
        
        if image_file and os.path.exists(image_file):
            # Logic for adding image inside dialog
            pass 

        # Navigation to Post
        # ... (Refer to full script for 'Next' and 'Post' selectors)
        
        context.storage_state(path=state_path)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        if browser: browser.close()
