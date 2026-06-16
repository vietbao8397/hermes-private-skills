---
name: fb-poster
description: Đăng bài tự động lên Facebook cá nhân bằng Playwright DOM automation. Đọc POST_LOG.md, tìm bài PENDING, đăng qua CLI tool, cập nhật LOG.
---

# Facebook Auto-Poster

Đăng bài tự động lên trang cá nhân Facebook thông qua Playwright DOM automation.

## Kiến trúc

- **CLI Tool (Standard)**: `node /opt/tools/fb-poster/fb-post.js`
- **CLI Tool (Cloak/Stealth)**: `python3 /opt/data/skills/social-media/social-media/fb-poster/scripts/fb-poster-cloak.py`
- **Content Dir**: `/opt/data/fb-content/`
- **LOG File**: `/opt/data/fb-content/POST_LOG.md`

## Workflow đăng bài

### Bước 1: Chọn công cụ
*   Nếu môi trường yêu cầu độ ẩn danh cao (vượt Cloudflare/Bot detection), hãy sử dụng công cụ **Cloak/Stealth**.
*   Công cụ Cloak yêu cầu thư viện `cloakbrowser` (`pip install cloakbrowser`).

### Bước 2: Đọc LOG
...
### Bước 4: Đăng bài

**Text + Ảnh (Sử dụng Cloak Browser):**
```bash
python3 /opt/data/skills/social-media/social-media/fb-poster/scripts/fb-poster-cloak.py --file "/opt/data/fb-content/<folder>/content.md" --state "/opt/data/fb-content/fb_state.json" --image "/opt/data/fb-content/<folder>/image.jpg"
```

```

Tìm dòng có trạng thái `⏳ PENDING`. Nếu không có → thông báo "Không có bài nào cần đăng."

### Bước 2: Đọc nội dung bài viết

```bash
read_file /opt/data/fb-content/<folder-name>/content.md
```

File `content.md` có frontmatter:
```yaml
---
title: Tiêu đề bài viết
created: 2026-04-25
---
```
Nội dung bài viết nằm sau frontmatter.

### Bước 3: Kiểm tra ảnh

Kiểm tra có file ảnh trong folder hay không:
```bash
terminal: ls /opt/data/fb-content/<folder-name>/
```
Ảnh có thể là: `image.jpg`, `image.png`, `image.webp`, hoặc tên bất kỳ có extension ảnh.

### Bước 4: Đăng bài

**Lưu ý về UI Facebook**: Facebook thường yêu cầu xác nhận 2 bước: Bấm **Tiếp (Next)** trước, sau đó mới bấm **Đăng (Post)** trong cửa sổ tiếp theo.

**Khuyên dùng `--file` cho tiếng Việt** (tránh lỗi encoding qua CLI args).

**Timeout Quan Trọng**: Khi sử dụng CloakBrowser (chế độ humanize), việc gõ văn bản và tải ảnh lên có thể mất vài phút. Luôn sử dụng timeout ít nhất **300-600 giây** để tránh bị ngắt quãng giữa chừng.

**Quyền riêng tư (Privacy)**: Việc tự động chọn "Chỉ mình tôi" (Only me) rất dễ lỗi do selector (`aria-label*="Chỉnh sửa đối tượng"`) không ổn định. Luôn kiểm tra lại bài viết sau khi đăng để đảm bảo đúng quyền riêng tư.

**Text + Ảnh (đọc từ file):**
```bash
terminal: node /opt/data/fb-content/fb-post.js --file "/opt/data/fb-content/<folder>/content.md" --image "/opt/data/fb-content/<folder>/image.jpg"
```

### Cookie Auth (Headless/WSL)
Nếu môi trường không có GUI (thiếu X server/DISPLAY), không thể login thủ công. Sử dụng cookie `c_user` và `xs` từ trình duyệt máy cá nhân để tạo `fb_state.json`:
1. Mở F12 > Application > Cookies > facebook.com.
2. Copy giá trị `c_user` và `xs`.
3. Tạo file `fb_state.json` theo định dạng Playwright storageState.

## Selector Tham Khảo (2026)
| Thành phần | Selector |
|------------|----------|
| Nút mở Composer | `span:has-text("bạn đang nghĩ gì thế?")`, `div[aria-label="Tạo bài viết"]` |
| Khung nhập liệu | `div[role="dialog"] div[contenteditable="true"]` |
| Nút Tiếp (Next) | `div[aria-label="Tiếp"]`, `div[role="button"]:has-text("Tiếp")` |
| Nút Đăng (Post) | `div[aria-label="Đăng"]`, `div[role="button"]:has-text("Đăng")` |

> **Lưu ý**: `--file` tự động strip frontmatter (--- ... ---) và chỉ lấy nội dung bài viết.

**Output là JSON:**
```json
{"success": true, "dryRun": false, "steps": ["browser_launched", "composer_opened", "content_typed", "post_clicked", "post_confirmed"]}
```

### Bước 5: Cập nhật LOG

Nếu thành công: đổi `⏳ PENDING` → `✅ POSTED` và thêm timestamp.
Nếu thất bại: đổi `⏳ PENDING` → `❌ FAILED` và ghi lỗi.

Dùng `patch` tool để sửa đúng dòng trong `POST_LOG.md`.

### Bước 6: Thông báo

```bash
send_message telegram: "✅ Đã đăng bài Facebook: <tiêu đề>"
```
hoặc
```bash
send_message telegram: "❌ Đăng bài thất bại: <tiêu đề> — Lỗi: <error message>"
```

## POST_LOG.md Format

```markdown
| # | Folder | Tiêu đề | Trạng thái | Ngày đăng | Ghi chú |
|---|--------|---------|-----------|----------|---------|
| 1 | bai-viet-1 | Tiêu đề 1 | ✅ POSTED | 2026-04-25 08:00 | OK |
| 2 | bai-viet-2 | Tiêu đề 2 | ⏳ PENDING | — | Chờ đăng |
| 3 | bai-viet-3 | Tiêu đề 3 | ❌ FAILED  | 2026-04-25 12:00 | Lỗi upload |
```

## Quy tắc an toàn

1. **Tối đa 1 bài mỗi lần gọi** — luôn chỉ đăng 1 bài PENDING đầu tiên
2. **Timeout 120 giây** cho mỗi lần đăng
3. **Giãn cách tối thiểu 2 giờ** giữa các bài (kiểm tra cột "Ngày đăng")
4. **Không thử lại bài FAILED** — cần user kiểm tra thủ công
5. **Dry run trước khi đăng thật** nếu user yêu cầu test

### Cloak Browser Integration (Python)
For high-stealth posting, use the Python version of the poster with CloakBrowser.
**Tip**: Use `page.keyboard.type(content, delay=100)` to simulate real typing, which triggers Facebook's editor correctly while maintaining stealth.

**Session Recovery**:
If logged out, update `fb_state.json` with fresh `c_user` and `xs` cookies from a logged-in browser.

| Lỗi | Nguyên nhân | Xử lý |
|-----|------------|-------|
| Lỗi | Nguyên nhân | Xử lý |
|-----|------------|-------|
| Chrome profile chưa login | Profile hết session | Lấy `c_user` và `xs` từ browser cá nhân để tạo `fb_state.json`. |
| Không tìm thấy composer | Facebook đổi UI | Thử selector `span:has-text("bạn đang nghĩ gì thế?")`. |
| Nút Đăng bị ẩn | Cần qua bước trung gian | Facebook yêu cầu bấm nút **Tiếp** (Next) trước khi hiện nút Đăng. |
| Image upload failed | File không tồn tại | Kiểm tra path ảnh. Với Drive, dùng `curl -L "URL_UC" -o file.jpg`. |

## Đồng bộ hóa & Di chuyển giữa các máy (Git Sync)

Để đồng bộ hóa skill này sang một máy tính cài Hermes khác:

### 1. Ở máy nguồn (WSL/Linux):
* Cấu hình SSH Keys (`id_ed25519_github`) cho GitHub và phân quyền hợp lệ (`600` cho keys, `700` cho thư mục `.ssh`).
* **Lỗi Dubious Ownership:** Nếu gặp lỗi sở hữu thư mục trên WSL, thêm thư mục vào danh sách an toàn:
  ```bash
  git config --global --add safe.directory /opt/data/skills/social-media/social-media/fb-poster
  ```
* Khởi tạo và đẩy lên Private Repo:
  ```bash
  git init
  git remote add origin git@github.com:vietbao8397/hermes-private-skills.git
  git branch -M main
  git add .
  git commit -m "feat: add fb-poster skill with scripts"
  git push -u origin main
  ```

### 2. Ở máy đích (Hermes mới):
* Di chuyển vào thư mục quản lý skill (thường là `~/.hermes/skills/`).
* Nhân bản (clone) repo về máy mới:
  ```bash
  git clone git@github.com:vietbao8397/hermes-private-skills.git fb-poster
  ```

