const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({
        headless: "new"
    });
    const page = await browser.newPage();
    
    // Set to mobile viewport
    await page.setViewport({ width: 375, height: 667 });
    
    await page.goto('http://127.0.0.1:8080');
    
    const hasHorizontalScroll = await page.evaluate(() => {
        return document.documentElement.scrollWidth > document.documentElement.clientWidth;
    });
    
    console.log(`Has horizontal scroll: ${hasHorizontalScroll}`);
    if (hasHorizontalScroll) {
        const overflowElements = await page.evaluate(() => {
            const elements = document.querySelectorAll('*');
            const result = [];
            for (let el of elements) {
                if (el.scrollWidth > el.clientWidth) {
                    result.push(el.tagName + (el.id ? '#' + el.id : '') + (el.className ? '.' + el.className : ''));
                }
            }
            return result;
        });
        console.log("Elements with overflow:", overflowElements);
    }
    
    await browser.close();
})();
