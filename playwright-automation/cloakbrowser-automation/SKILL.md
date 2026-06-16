---
name: cloakbrowser-automation
description: |
  Advanced automation using CloakBrowser (Stealth Chromium). Focuses on
  bypassing bot detection, human-like interaction, and cross-platform
  stealth posting (Facebook, etc.).
---

# CloakBrowser Automation

## Overview
CloakBrowser provides source-level patches to Chromium to bypass advanced bot detection (Cloudflare, reCAPTCHA, etc.). This skill covers practical implementation patterns for stealthy automation.

## Implementation Patterns

### 1. Environment Setup (WSL/Protected Systems)
When the main environment is read-only or restricted, use a dedicated venv and inject it:
```python
import sys
# Path to CloakBrowser venv
sys.path.insert(0, "/opt/data/cloak-venv/lib/python3.13/site-packages")
from cloakbrowser import launch
```

### 2. Stealth Configuration
Always use `humanize=True` for social media to simulate real user behavior (Bézier curves, typing delays).

```python
browser = launch(
    headless=True,
    humanize=True,
    # Use storage_state for session persistence
)
context = browser.new_context(storage_state="path/to/state.json")
```

### 3. Human-like Typing
Instead of `page.fill()` (which is instant), use `page.keyboard.type()` with a delay to mimic human speed.

```python
page.focus('selector')
page.keyboard.type("Content here...", delay=100) # 100ms delay per char
```

## Workflows

### Facebook Stealth Posting
See `scripts/fb-poster-cloak.py` for a full implementation that handles:
- Cookie-based authentication (`c_user`, `xs`).
- Privacy settings (e.g., "Only Me").
- Dynamic selector fallbacks for the Facebook Composer.

## Hermes Environment Setup

### Installation in Restricted Environments
If the default venv is read-only (common in Hermes/WSL):
1. Create a custom venv: `uv venv /opt/data/cloak-venv`
2. Install: `VIRTUAL_ENV=/opt/data/cloak-venv uv pip install cloakbrowser`
3. Download binary: `VIRTUAL_ENV=/opt/data/cloak-venv /opt/data/cloak-venv/bin/python3 -c "import cloakbrowser; cloakbrowser.ensure_binary()"`

### NPM Global Prefix (EACCES workaround)
If `/usr/local` is read-only:
```bash
mkdir -p /opt/data/npm-global
npm config set prefix '/opt/data/npm-global'
export PATH=/opt/data/npm-global/bin:$PATH
```

### Hermes config.yaml (when .env is protected)
```yaml
browser:
  engine: cloakbrowser
  cloakbrowser:
    enabled: true
    humanize: true
    headless: true
```

## Facebook-Specific Patterns

### Cookie-Based Authentication
Use `c_user` and `xs` cookies stored in `fb_state.json`. Pass via `browser.new_context(storage_state=...)` — NOT `launch()`.

### Privacy Settings ("Only Me" / "Chỉ mình tôi")
1. After clicking "Next" (Tiếp), wait for the privacy selection button
2. Click the privacy selector: `div[aria-label="Chọn đối tượng"]`
3. Select "Only me": `div[role="menuitem"]:has-text("Chỉ mình tôi")`
4. Click "Post" (Đăng)

### Storage State Pattern
`cloakbrowser.launch()` does **not** accept `storage_state`. Pass it to `browser.new_context()`:
```python
browser = launch(headless=True, humanize=True)
context = browser.new_context(storage_state="path/to/state.json")
```

## Verification
Run `scripts/verify_cloak.py` to validate the CloakBrowser installation and stealth detection bypass.

## Pitfalls
- **Timeout Management**: Tasks involving human-like interaction (typing delays, mouse curves) are significantly slower than standard Playwright actions. For complex workflows like social media posting, use a `timeout` of at least **300-600 seconds** for the terminal/script execution.
- **Session Expiry**: Facebook cookies (`xs`) expire. If you see the login screen, refresh the `fb_state.json` with fresh cookies from a logged-in browser.
- **Selector Changes**: Facebook frequently updates its DOM. Use text-based selectors (e.g., `span:has-text("bạn đang nghĩ gì thế?")`) for better resilience.
