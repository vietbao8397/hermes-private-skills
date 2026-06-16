const fs = require('fs');
const { chromium } = require('playwright-core');

// Parse CLI args
const args = process.argv.slice(2);
let fileArg = '';
let imageArg = '';

for (let i = 0; i < args.length; i++) {
    if (args[i] === '--file' && i + 1 < args.length) fileArg = args[i + 1];
    if (args[i] === '--image' && i + 1 < args.length) imageArg = args[i + 1];
}

(async () => {
    let browser;
    try {
        browser = await chromium.launch({
            headless: true, 
            executablePath: '/opt/data/home/.agent-browser/browsers/chrome-148.0.7778.167/chrome',
            args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
        });
        const context = await browser.newContext({ storageState: '/opt/data/fb-content/fb_state.json' });
        const page = await context.newPage();
        
        let content = fs.readFileSync(fileArg, 'utf8').replace(/^---[\s\S]*?---\s*/, '').trim();
        await page.goto('https://www.facebook.com/', { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(5000); 

        // Mở composer
        const openBtn = 'span:has-text("bạn đang nghĩ gì thế?"), div[aria-label="Tạo bài viết"]';
        await page.click(openBtn);
        
        // Điền text
        const editor = 'div[role="dialog"] div[contenteditable="true"]';
        await page.waitForSelector(editor);
        await page.locator(editor).fill(content);
        
        // Bấm Tiếp
        const nextBtn = 'div[aria-label="Tiếp"], div[role="button"]:has-text("Tiếp")';
        await page.click(nextBtn);
        
        // Bấm Đăng
        const postBtn = 'div[aria-label="Đăng"], div[role="button"]:has-text("Đăng")';
        await page.waitForSelector(postBtn + ':not([aria-disabled="true"])');
        await page.click(postBtn);
        
        await page.waitForSelector('div[role="dialog"]', { state: 'hidden' });
        console.log(JSON.stringify({ success: true }));
        await browser.close();
    } catch (err) {
        if (browser) await browser.close();
        console.error(JSON.stringify({ success: false, error: err.message }));
        process.exit(1);
    }
})();