# Windows & MSYS Playwright Troubleshooting

This guide captures advanced diagnostics and workarounds for running browser automation (Playwright, Cloak Browser, Stealth Chromium) on Windows hosts, particularly when dealing with MSYS/Git-bash environments, symlinked virtualenvs, and Python version conflicts.

## 1. MSYS Symlink Resolution Error (WinError 1920)
### Problem
On Windows, virtual environments created inside Git-bash or MSYS2 (e.g., `cloak-venv`) may use MSYS-style symbolic links for the `python` executable in `bin/`. 
Executing this file directly from native Windows Python or Windows subprocess APIs raises:
`[WinError 1920] The file cannot be accessed by the system`

### Workaround
Do NOT run the symlinked `bin/python` binary. Instead:
1. Run the script using the host's native Windows Python executable (`sys.executable` of the active virtual environment).
2. Append the target virtualenv's `site-packages` directory to `sys.path` inside your script:
```python
import sys
sys.path.append(r"C:\Users\Admin\.hermes\cloak-venv\lib\python3.13\site-packages")
```

---

## 2. ABI Binary Conflicts & ImportError on Greenlet
### Problem
When appending the `site-packages` of a different Python version (e.g., Python 3.13) into the search path of your active Python version (e.g., Python 3.12), compiled binary C-extensions (like `greenlet` or `playwright`) will fail to import:
`ImportError: No module named 'greenlet._greenlet'`

### Solution
1. Install compatible binary wheels directly into the host virtual environment using `uv`:
```bash
uv pip install --python <active_venv_path> playwright
```
This compiles and installs the compatible versions of `greenlet` and `playwright` locally.
2. In your python scripts, use **`sys.path.append()`** instead of `sys.path.insert(0,)` to load external dependencies. This ensures that the active Python environment's native compiled binaries are resolved first, while the pure Python libraries (e.g., `cloakbrowser`) are successfully resolved from the appended folder.

---

## 3. WebUI Image Gateway Cache Bypassing
### Problem
When you save an edited or cropped image over the exact same local file path, the WebUI rendering engine may still display the old uncropped image due to internal image-path caching.

### Solution
Always save the modified image under a **new unique filename** (e.g., append `_beautified_v2_solid` or a unique suffix) before returning it as a `MEDIA:` tag:
```python
# Save with a unique name
beautified_path = r"C:\Users\Admin\workspace\screenshot_beautified_v2_solid.png"
# Return in response
# MEDIA:C:\Users\Admin\workspace\screenshot_beautified_v2_solid.png
```

---

## 4. Flattening Transparent Drop-Shadows (PIL)
### Problem
When creating modern "Beautified" cards with drop shadows on solid backgrounds using PIL, some transparency (alpha channel) might leak around the soft shadow edges, showing as empty or broken pixels in standard Jpeg/PNG viewers.

### Solution
Convert the final composited canvas from `RGBA` to **`RGB`** mode before saving to merge and flatten any alpha channel completely against the solid background:
```python
# Flatten to Solid RGB
final_rgb = canvas.convert("RGB")
final_rgb.save(output_path, "PNG") # No transparent pixels will remain
```

---

## 5. Facebook Automation & Stealth Posting (Playwright)
### Problem
When automating postings on Facebook using Playwright/Cloak Browser, several dynamic layout-related blockers often arise:
- **Notification Pop-up Overlays:** Unread notifications panels or other home-screen dropdown overlays can remain open by default in saved sessions (`fb_state.json`), completely covering the composer input and intercepting click events.
- **React Hydration Click Failures:** Clicking the post composer trigger button immediately after page load can succeed in the DOM, but because React's event-handlers are not yet hydrated, the click is ignored and the publishing dialog never opens.
- **Multi-step "Tiếp" (Next) Button:** Modern Facebook uses a multi-step wizard. An active blue "Tiếp" (Next/Continue) button appears at the bottom of the composer dialog, which must be clicked before the final "Đăng" (Post) button is rendered.
- **Aria-Disabled Upload Waiting:** The "Tiếp" or "Đăng" button is visually disabled (`aria-disabled="true"`) while a high-resolution image uploads. Trying to click it immediately causes errors.

### Solution (Stealth Posting Playbook)
1. **Direct Profile Navigation:** Bypass all homepage popups, overlays, and notification panels by navigating the browser directly to the user's personal timeline profile page instead of the home page:
   `https://www.facebook.com/profile.php?id=<user_id>`
2. **Hydration Stabilization:** Wait for the page load, and then execute a stable click sequence:
   ```python
   # Locate, scroll, hover, wait, and click
   composer_selector = 'div[role="button"]:has-text("Bạn đang nghĩ gì")'
   page.wait_for_selector(composer_selector, state="visible", timeout=60000)
   locator = page.locator(composer_selector)
   locator.scroll_into_view_if_needed()
   time.sleep(1)
   locator.hover()
   time.sleep(3) # Wait 3 seconds to guarantee React event handlers are hydrated!
   locator.click(force=True) # Click with force to open dialog
   ```
3. **Multi-step Click Wizard:** Always check and click the "Tiếp" button inside the dialog first, sleep for 3 seconds, and then click the final "Đăng" button:
   ```python
   # Click 'Tiếp' first
   page.click('div[role="dialog"] div[aria-label="Tiếp"][role="button"]', force=True)
   time.sleep(3)
   # Click 'Đăng' with a generous timeout (30-45s) for image upload completion
   page.wait_for_selector('div[aria-label="Đăng"][role="button"]:not([aria-disabled="true"])', timeout=45000)
   page.click('div[aria-label="Đăng"][role="button"]', force=True)
   ```
