const puppeteer = require('puppeteer');
const path = require('path');
const validUrl = require('valid-url');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  // Set the viewport size
  await page.setViewport({ width: 1024, height: 1024 });

  // Get the URL from the command-line arguments
  const urlOrPath = process.argv[2];

  if (!urlOrPath) {
    console.error('Please provide a valid URL or file path as a command-line argument.');
    process.exit(1);
  }

  // Determine if the input is a valid URL or a local file path
  const isUrl = validUrl.isWebUri(urlOrPath);
  const target = isUrl ? urlOrPath : `file://${path.resolve(urlOrPath)}`;

  // Navigate to the specified URL or local file
  await page.goto(target);

  // Take a screenshot
  await page.screenshot({ path: 'screenshot.png' });

  // Close the browser
  await browser.close();
})();
