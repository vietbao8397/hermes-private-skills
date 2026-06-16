---
name: playwright-automation
description: Sử dụng kỹ năng này khi bạn cần tự động hóa trình duyệt, thu thập dữ liệu web động, hoặc tương tác với một trang web sử dụng thư viện Python Playwright thông qua công cụ execute_code.
---

# Kỹ năng Tự động hóa Playwright

Kỹ năng này hướng dẫn Hermes cách sử dụng thư viện `playwright` (Python) để điều khiển trình duyệt và hoàn thành các tác vụ web thông qua công cụ `execute_code`. Xem thêm hướng dẫn cài đặt môi trường tại [references/browser-setup-linux.md](references/browser-setup-linux.md).

## Hướng dẫn cốt lõi

1.  **Luôn dùng API Đồng bộ (Sync API):** 
    Luôn bắt đầu mã với `from playwright.sync_api import sync_playwright`. Hãy tránh sử dụng API bất đồng bộ (`asyncio`) để đảm bảo tính ổn định và tránh lỗi event loop khi mã chạy trong môi trường `execute_code`.
    
2.  **Chế độ Headless:** 
    Vì Hermes chạy trong môi trường không có giao diện đồ họa (GUI), **BẮT BUỘC** phải khởi chạy trình duyệt ở chế độ ẩn: `p.chromium.launch(headless=True)`.
    
3.  **Bộ định vị (Locators) mạnh mẽ:** 
    Ưu tiên sử dụng các locator có sẵn của Playwright như `page.get_by_role()`, `page.get_by_text()`, hoặc `page.locator()` thay vì các bộ chọn CSS (CSS selectors) dễ bị gãy.
    
4.  **Cơ chế Chờ (Auto-waiting):** 
    Tận dụng tối đa cơ chế tự động chờ (auto-wait) của Playwright. Hạn chế sử dụng `time.sleep()`. Thay vào đó hãy dùng `page.wait_for_selector()` hoặc `page.wait_for_load_state()`.

## Xử lý sự cố Môi trường (Troubleshooting)

Nếu gặp lỗi "Chrome not found" hoặc lỗi về shared library trên Linux/WSL:
1.  **Cài đặt Chrome**: `npx agent-browser install`
2.  **Cài đặt dependencies**: `npx agent-browser install --with-deps`
3.  **Symlink cho Hermes**: Nếu `browser_navigate` vẫn không tìm thấy, hãy tạo symlink:
    `mkdir -p /opt/data/.agent-browser && ln -s /opt/data/home/.agent-browser/browsers /opt/data/.agent-browser/browsers`
4.  **Lỗi Windows & MSYS**: Xem thêm [references/windows-playwright-troubleshooting.md](references/windows-playwright-troubleshooting.md) để biết cách khắc phục lỗi WinError 1920, lỗi nạp nhị phân greenlet, xung đột môi trường Python 3.12/3.13, và cách xóa cache hiển thị ảnh.

## Mã mẫu (Template)

Dưới đây là một bộ khung chuẩn để bạn có thể sinh mã Python và chạy thông qua `execute_code`:

```python
import json
from playwright.sync_api import sync_playwright

def main():
    try:
        with sync_playwright() as p:
            # Khởi tạo trình duyệt ẩn (headless)
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={'width': 1280, 'height': 720},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            
            # Điều hướng đến trang web
            page.goto("https://example.com")
            
            # (Thực thi các logic của bạn ở đây)
            title = page.title()
            
            # Chụp ảnh màn hình làm bằng chứng nếu cần
            page.screenshot(path="screenshot.png")
            
            # Trả về kết quả dưới dạng JSON để Hermes dễ dàng parse
            result = {
                "status": "success",
                "title": title,
                "message": "Đã thu thập dữ liệu thành công."
            }
            print(json.dumps(result))
            
            # Đóng trình duyệt
            browser.close()
            
    except Exception as e:
        # Bắt lỗi và in ra dưới dạng JSON
        print(json.dumps({"status": "error", "message": str(e)}))

if __name__ == "__main__":
    main()
```

Khi được yêu cầu sử dụng Playwright, bạn hãy tạo ra một đoạn mã Python tương tự như trên và dùng lệnh `terminal` hoặc công cụ tương đương để chạy nó.
