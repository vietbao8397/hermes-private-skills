---
name: cloakbrowser-setup
description: |
  Setup and troubleshooting guide for CloakBrowser — a stealth Chromium browser
  with 57 C++ patches that passes Cloudflare, reCAPTCHA, BrowserScan, and
  FingerprintJS bot detection. Use this skill when setting up CloakBrowser as a
  browser backend in Hermes, troubleshooting detection issues, or configuring
  stealth browsing for scraping/automation tasks.
---

# CloakBrowser Setup Guide

## What is CloakBrowser?

CloakBrowser is a **source-patched Chromium** browser designed to bypass bot detection systems. Unlike fingerprint-spoofing tools that work at the JavaScript level, CloakBrowser patches Chromium's C++ source code directly, making detections nearly impossible.

### Key Features
- **57 C++ patches** on Chromium source
- Passes: Cloudflare Turnstile, reCAPTCHA v3, BrowserScan, FingerprintJS, CreepJS
- Built-in `humanize=True` mode (Bézier mouse curves, per-character keyboard)
- Proxy support with automatic GeoIP timezone/locale
- Works via standard **Playwright Python API**

## Installation

### 1. Install the package
```bash
pip install cloakbrowser
```

### 2. Binary downloads automatically
On first launch, CloakBrowser downloads its patched Chromium binary (~200 MB). This is automatic and cached.

### 3. Enable in Hermes
Add to your `.env` file:
```bash
CLOAKBROWSER_ENABLED=true
```

### 4. Verify
```bash
python -c "from cloakbrowser import launch; b = launch(); p = b.new_page(); p.goto('https://bot.sannysoft.com'); print(p.title()); b.close()"
```

## Configuration

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `CLOAKBROWSER_ENABLED` | `false` | Enable CloakBrowser as browser backend |
| `CLOAKBROWSER_PROXY` | (none) | Proxy URL (socks5://user:pass@host:port) |
| `CLOAKBROWSER_HUMANIZE` | `false` | Enable human-like mouse/keyboard |
| `CLOAKBROWSER_HEADLESS` | `true` | Run in headless mode |
| `CLOAKBROWSER_GEOIP` | `false` | Auto timezone/locale from proxy IP |

## Routing Priority

When CloakBrowser is enabled, it takes priority in the browser tool routing:

```
1. BROWSER_CDP_URL → Direct CDP connection (user override)
2. CLOAKBROWSER_ENABLED=true → CloakBrowser (stealth Chromium)
3. CAMOFOX_URL → Camofox (stealth Firefox)
4. Cloud provider → Browserbase/BrowserUse/Firecrawl
5. Default → agent-browser CLI (local Chromium)
```

## Troubleshooting

### Binary download fails
```bash
# Manual download
python -c "from cloakbrowser.utils import download_browser; download_browser()"
```

### Multi-tab crashes (Known Issue #254)
CloakBrowser has a known issue with blank tabs when opening multiple tabs.
**Workaround**: Use single-tab mode (default in Hermes).

### "CloakBrowser is not installed" error
```bash
pip install cloakbrowser
# Verify: python -c "import cloakbrowser; print('OK')"
```

### Detection still failing
1. Enable humanize: `CLOAKBROWSER_HUMANIZE=true`
2. Add proxy: `CLOAKBROWSER_PROXY=socks5://...`
3. Enable GeoIP: `CLOAKBROWSER_GEOIP=true`

## Docker Usage

In Docker, ensure the CloakBrowser package is installed:
```dockerfile
# Add to your Dockerfile after the base pip install
RUN uv pip install --no-cache-dir cloakbrowser
```

Or install at runtime:
```bash
docker exec <container> pip install cloakbrowser
```

## CloakBrowser vs Camofox

| Feature | CloakBrowser | Camofox |
|---------|-------------|---------|
| Engine | Chromium | Firefox |
| Method | C++ source patches | JS fingerprint spoofing |
| API | Playwright Python API | REST API (separate server) |
| Setup | `pip install` | Clone + npm start |
| Humanize | Built-in | Via config |
| Detection bypass | Very high | High |
| Stability | Good (some multi-tab issues) | Good |
