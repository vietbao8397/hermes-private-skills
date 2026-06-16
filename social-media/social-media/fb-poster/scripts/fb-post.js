const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright-core');

// Parse CLI args
const args = process.argv.slice(2);
let fileArg = '';
let imageArg = '';
let isDryRun = false;

for (let i = 0; i < args.length; i++) {
    if (args[i] === '--file' && i + 1 < args.length) fileArg = args[i + 1];
    if (args[i] === '--image' && i + 1 < args.length) imageArg = args[i + 1];
    if (args[i] === '--dry-run') isDryRun = true;
}

if (!fileArg) {
    console.error(JSON.stringify({ success: false, error: "Missing --file parameter" }));
    process.exit(1);
}

// Read and strip frontmatter from content
let content = fs.readFileSync(fileArg, 'utf8');
if (content.startsWith('---')) {
    const endOfFrontmatter = content.indexOf('---', 3);
    if (endOfFrontmatter !== -1) {
        content = content.substring(endOfFrontmatter + 3).trim();
    }
}

(async () => {
    let browser;
    try {
        browser = await chromium.launch({
            headless: true, 
            executablePath: '/opt/data/home/.agent-browser/browsers/chrome-148.0.7778.167/chrome',
            args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
        });
        
        const context = await browser.newContext({
            storageState: '/opt/data/fb-content/fb_state.json',
            userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport: { width: 1280, height: 720 }
        });
        
        const page = await context.newPage();
        const steps = ["browser_launched"];
        
        await page.goto('https://www.facebook.com/', { waitUntil: 'domcontentloaded', timeout: 60000 });
        await page.waitForTimeout(5000); 
        
        // Buoc 1: Mo composer
        const photoBtnFeed = [
            'div[role="button"]:has-text("Ảnh/Video")',
            'div[role="button"]:has-text("Photo/video")',
            'div[aria-label="Ảnh/video"]',
            'div[aria-label="Photo/video"]'
        ];

        let composerOpened = false;
        for (const selector of photoBtnFeed) {
            try {
                await page.waitForSelector(selector, { state: 'visible', timeout: 5000 });
                if (imageArg && fs.existsSync(imageArg)) {
                    const fileChooserPromise = page.waitForEvent('filechooser');
                    await page.click(selector);
                    const fileChooser = await fileChooserPromise;
                    await fileChooser.setFiles(imageArg);
                    steps.push("image_attached");
                } else {
                    await page.click(selector);
                }
                composerOpened = true;
                steps.push("composer_opened");
                break;
            } catch (e) { }
        }

        if (!composerOpened) {
            const createPostSelectors = [
                'span:has-text("bạn đang nghĩ gì thế?")',
                'span:has-text("Bạn đang nghĩ gì?")'
            ];
            for (const selector of createPostSelectors) {
                try {
                    await page.waitForSelector(selector, { state: 'visible', timeout: 5000 });
                    await page.click(selector);
                    composerOpened = true;
                    steps.push("composer_opened");
                    break;
                } catch (e) { }
            }
        }
        
        if (!composerOpened) throw new Error("Khong tim thay nut tao bai");

        // Buoc 2: Dien noi dung
        const editorSelector = 'div[role="dialog"] div[contenteditable="true"]';
        await page.waitForSelector(editorSelector, { state: 'visible', timeout: 10000 });
        await page.waitForTimeout(2000); 
        await page.locator(editorSelector).fill(content);
        steps.push("content_typed");
        
        // Buoc 3: Tiep tuc
        const nextBtnSelectors = [
            'div[aria-label="Tiếp"][role="button"]',
            'div[aria-label="Next"][role="button"]'
        ];
        for (const selector of nextBtnSelectors) {
            try {
                await page.waitForSelector(selector + ':not([aria-disabled="true"])', { timeout: 3000 });
                await page.click(selector);
                steps.push("next_clicked");
                break;
            } catch (e) { }
        }

        // Buoc 4: Dang
        const postBtnSelectors = [
            'div[aria-label="Post"][role="button"]',
            'div[aria-label="Đăng"][role="button"]'
        ];
        let posted = false;
        for (const selector of postBtnSelectors) {
            try {
                await page.waitForSelector(selector + ':not([aria-disabled="true"])', { timeout: 5000 });
                await page.click(selector);
                posted = true;
                steps.push("post_clicked");
                break;
            } catch (e) { }
        }
        
        if (!posted) throw new Error("Khong bam duoc nut Dang");
        await page.waitForSelector('div[role="dialog"]', { state: 'hidden', timeout: 15000 });
        steps.push("post_confirmed");
        await context.storageState({ path: '/opt/data/fb-content/fb_state.json' });
        console.log(JSON.stringify({ success: true, steps }));
        
        await browser.close();
    } catch (err) {
        if (browser) await browser.close();
        console.error(JSON.stringify({ success: false, error: err.message }));
        process.exit(1);
    }
})();