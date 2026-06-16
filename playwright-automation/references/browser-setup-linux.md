# Cài đặt Trình duyệt trên WSL/Linux cho Hermes Agent

Khi chạy trong môi trường hạn chế hoặc mới (như WSL), công cụ `browser_navigate` có thể thất bại với lỗi "Chrome not found".

## Quy trình Khắc phục

1. **Cài đặt binaries**:
   Sử dụng `agent-browser` CLI (thường có sẵn qua npx):
   ```bash
   npx agent-browser install
   ```

2. **Cấu hình Đường dẫn cho Hermes**:
   Hermes thường tìm kiếm browser trong `/opt/data/.agent-browser/browsers`. Nếu `agent-browser` cài đặt vào thư mục home của user, cần tạo liên kết:
   ```bash
   mkdir -p /opt/data/.agent-browser
   ln -s /opt/data/home/.agent-browser/browsers /opt/data/.agent-browser/browsers
   ```

3. **Thư viện hệ thống**:
   Nếu trình duyệt crash do thiếu `.so` files:
   ```bash
   npx agent-browser install --with-deps
   ```

## Kiểm tra
Sau khi cài đặt, hãy thử:
```bash
browser_navigate --url https://www.google.com
```
Nếu thành công, bạn sẽ nhận được snapshot của trang web.
