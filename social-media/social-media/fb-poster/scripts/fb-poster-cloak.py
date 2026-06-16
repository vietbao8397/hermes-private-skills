import os
import sys
import json
import time
import argparse

# This script requires cloakbrowser: pip install cloakbrowser
try:
    from cloakbrowser import launch
except ImportError:
    print(json.dumps({"success": False, "error": "Library 'cloakbrowser' not found. Install with: pip install cloakbrowser"}))
    sys.exit(1)

def post_to_facebook(content_file, state_file, image_file=None, headless=True):
    # Read content and strip frontmatter
    with open(content_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            content = parts[2].strip()

    steps = []
    browser = None
    try:
        # Launch Cloak Browser (Stealth Chromium)
        browser = launch(
            headless=headless,
            humanize=True  # Human-like interaction (Bezier curves, etc.)
        )
        steps.append("browser_launched_with_cloak")
        
        # storage_state must be passed to context, not launch
        context = browser.new_context(
            storage_state=state_file,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        # Visit Facebook
        page.goto("https://www.facebook.com/", wait_until="domcontentloaded", timeout=60000)
        time.sleep(5) # Give it a moment to load
        
        # Open Composer
        composer_opened = False
        photo_selectors = [
            'div[role="button"]:has-text("Ảnh/Video")',
            'div[role="button"]:has-text("Photo/video")',
            'div[aria-label="Ảnh/video"]',
            'div[aria-label="Photo/video"]'
        ]
        
        for selector in photo_selectors:
            try:
                if page.is_visible(selector, timeout=5000):
                    if image_file and os.path.exists(image_file):
                        with page.expect_file_chooser() as fc_info:
                            page.click(selector)
                        file_chooser = fc_info.value
                        file_chooser.set_files(image_file)
                        steps.append("image_attached")
                    else:
                        page.click(selector)
                    composer_opened = True
                    steps.append("composer_opened")
                    break
            except:
                continue

        if not composer_opened:
            text_selectors = [
                'span:has-text("bạn đang nghĩ gì thế?")',
                'span:has-text("Bạn đang nghĩ gì?")'
            ]
            for selector in text_selectors:
                try:
                    if page.is_visible(selector, timeout=5000):
                        page.click(selector)
                        composer_opened = True
                        steps.append("composer_opened")
                        break
                except:
                    continue

        if not composer_opened:
            raise Exception("Facebook home loaded but could not find the post composer (Login likely expired)")

        # Fill content
        editor_selector = 'div[role="dialog"] div[contenteditable="true"]'
        page.wait_for_selector(editor_selector, state="visible", timeout=10000)
        time.sleep(2)
        page.fill(editor_selector, content)
        steps.append("content_typed")
        
        # Click Next
        next_selectors = [
            'div[aria-label="Tiếp"][role="button"]',
            'div[aria-label="Next"][role="button"]'
        ]
        for selector in next_selectors:
            try:
                if page.is_visible(selector, timeout=3000):
                    page.click(selector)
                    steps.append("next_clicked")
                    break
            except:
                continue

        # Click Post
        post_selectors = [
            'div[aria-label="Post"][role="button"]',
            'div[aria-label="Đăng"][role="button"]'
        ]
        posted = False
        for selector in post_selectors:
            try:
                # Ensure the Post button is not disabled
                page.wait_for_selector(f"{selector}:not([aria-disabled='true'])", timeout=5000)
                page.click(selector)
                posted = True
                steps.append("post_clicked")
                break
            except:
                continue
        
        if not posted:
            raise Exception("Clicked Next but could not find/click the Post button")

        # Wait for dialog to close
        page.wait_for_selector('div[role="dialog"]', state="hidden", timeout=15000)
        steps.append("post_confirmed")
        
        # Save updated state
        context.storage_state(path=state_file)
        print(json.dumps({"success": True, "steps": steps}))
        
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e), "steps": steps}))
    finally:
        if browser:
            browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Path to content.md")
    parser.add_argument("--state", required=True, help="Path to fb_state.json")
    parser.add_argument("--image", required=False, help="Path to image file")
    parser.add_argument("--headed", action="store_true", help="Run in headed mode")
    args = parser.parse_args()
    
    post_to_facebook(args.file, args.state, args.image, headless=not args.headed)
