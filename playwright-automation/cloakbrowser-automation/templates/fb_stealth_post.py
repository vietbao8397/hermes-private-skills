import os
import sys
import json
import time

# Ensure custom venv is in path
sys.path.insert(0, "/opt/data/cloak-venv/lib/python3.13/site-packages")

from cloakbrowser import launch

def post_pattern(content_file, state_file):
    # Pattern for stealth social media posting
    browser = launch(
        headless=True,
        humanize=True, # Critical for bot detection bypass
    )
    
    # storage_state goes in new_context
    context = browser.new_context(
        storage_state=state_file,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    
    page = context.new_page()
    # ... navigation and interaction ...
    # Use page.keyboard.type(text, delay=100) for human-like speed
    browser.close()
