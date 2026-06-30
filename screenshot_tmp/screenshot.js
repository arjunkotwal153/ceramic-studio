const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({
        headless: "new",
        defaultViewport: {
            width: 1920,
            height: 1080
        }
    });
    
    const page = await browser.newPage();
    
    // Disable animations for the screenshot if needed, or wait for them to finish
    await page.goto('http://localhost:8000', { waitUntil: 'networkidle0' });
    
    // Wait a little bit extra to ensure 3d assets or animations are fully loaded/rendered
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    // Take a screenshot of the hero section or the whole visible part
    // Typically the hero section takes up the screen height, so a viewport screenshot is good
    await page.screenshot({ path: '../images/hero_screenshot.png' });
    
    await browser.close();
})();
