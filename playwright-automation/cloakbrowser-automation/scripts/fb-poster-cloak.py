import os
import sys
import json
import time

# Thêm venv vào path nếu cần (Sửa đường dẫn cho phù hợp với môi trường)
venv_site_packages = "/opt/data/cloak-venv/lib/python3.13/site-packages"
if venv_site_packages not in sys.path:
    sys.path.insert(0, venv_site_packages)

from cloakbrowser import launch

def post_to_facebook(content_file, image_file=None, privacy="public"):
    """
    Đăng bài lên Facebook bằng CloakBrowser (Stealth Chromium).
    privacy: "public" hoặc "only_me"
    """
    with open(content_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            content = parts[2].strip()

    browser = None
    try:
        browser = launch(headless=True, humanize=True)
        context = browser.new_context(
            storage_state="/opt/data/fb-content/fb_state.json",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        page.goto("https://www.facebook.com/", wait_until="domcontentloaded", timeout=60000)
        time.sleep(5)
        
        # Mở Composer
        composer_opened = False
        text_selectors = [
            'span:has-text("bạn đang nghĩ gì thế?")',
            'span:has-text("Bạn đang nghĩ gì?")',
            'div[role="button"]:has-text("bạn đang nghĩ gì thế?")',
            'div[role="button"]:has-text("Bạn đang nghĩ gì?")'
        ]
        
        for selector in text_selectors:
            try:
                if page.is_visible(selector, timeout=5000):
                    page.click(selector)
                    composer_opened = True
                    break
            except: continue

        if not composer_opened:
            raise Exception("Không tìm thấy nút tạo bài viết")

        # Điền nội dung (Human-like typing)
        editor_selector = 'div[role="dialog"] div[contenteditable="true"]'
        page.wait_for_selector(editor_selector, state="visible", timeout=15000)
        time.sleep(2)
        page.focus(editor_selector)
        page.keyboard.type(content, delay=100)
        
        # Xử lý Privacy (Chỉ mình tôi)
        if privacy == "only_me":
            # Bấm nút chọn đối tượng (thường hiện sau khi có text hoặc trong composer)
            try:
                # Selector này có thể thay đổi, thường là nút có aria-label chứa "Công khai" hoặc "Public"
                page.click('div[aria-label*="đối tượng"], div[aria-label*="audience"]')
                page.click('span:has-text("Chỉ mình tôi"), span:has-text("Only me")')
                page.click('div[aria-label="Xong"], div[aria-label="Done"]')
            except: pass

        # Bấm Tiếp & Đăng
        next_btn = 'div[aria-label="Tiếp"][role="button"], div[aria-label="Next"][role="button"]'
        if page.is_visible(next_btn):
            page.click(next_btn)
            
        post_btn = 'div[aria-label="Post"][role="button"], div[aria-label="Đăng"][role="button"]'
        page.wait_for_selector(f"{post_btn}:not([aria-disabled='true'])", timeout=10000)
        page.click(post_btn)

        page.wait_for_selector('div[role="dialog"]', state="hidden", timeout=15000)
        context.storage_state(path="/opt/data/fb-content/fb_state.json")
        print(json.dumps({"success": True}))
        
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))
    finally:
        if browser: browser.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--image", required=False)
    parser.add_argument("--privacy", default="public")
    args = parser.parse_args()
    post_to_facebook(args.file, args.image, args.privacy)
