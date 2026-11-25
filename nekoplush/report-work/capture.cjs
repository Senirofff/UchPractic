const {chromium}=require('C:/Program Files/WindowsApps/OpenAI.CodexPrimaryRuntime.v26-1123-915-0_26.1123.915.0_x64__3k8sg7r9htsxt/dependencies/node/node_modules/playwright');
const fs=require('fs');
(async()=>{
const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
const page=await browser.newPage({viewport:{width:1500,height:900},deviceScaleFactor:1.5});
let errors=[];page.on('pageerror',e=>errors.push(e.message));
await page.goto('http://127.0.0.1:5173/'); await page.locator('img').last().waitFor();
await page.evaluate(()=>Promise.all([...document.images].map(i=>i.decode())));
await page.screenshot({path:'report-work/01-catalog.png',fullPage:true});
const buttons=page.getByRole('button');
for(let i=0;i<3;i++) await buttons.nth(0).click();
await buttons.nth(1).click();
const values=await page.locator('.quantity').allTextContents();
if(JSON.stringify(values)!==JSON.stringify(['Выбрано: 3','Выбрано: 1','Выбрано: 0','Выбрано: 0','Выбрано: 0']))throw Error(values);
await page.mouse.move(1490,890);await page.screenshot({path:'report-work/02-counts.png',fullPage:true});
await page.setViewportSize({width:1000,height:1000});
if(await page.locator('.product-grid').evaluate(e=>getComputedStyle(e).gridTemplateColumns.split(' ').length)!==3)throw Error('grid');
await page.setViewportSize({width:650,height:1100});
if(await page.locator('.product-grid').evaluate(e=>getComputedStyle(e).gridTemplateColumns.split(' ').length)!==2)throw Error('grid');
await page.setViewportSize({width:390,height:850});
await page.reload();await page.evaluate(()=>Promise.all([...document.images].map(i=>i.decode())));
if(await page.locator('.quantity').first().textContent()!=='Выбрано: 0') throw Error('reload');
await page.screenshot({path:'report-work/03-mobile.png'});
const checks={quantities:values,cards:await page.locator('.product-card').count(),mobileNoOverflow:await page.evaluate(()=>document.documentElement.scrollWidth===innerWidth),errors};
fs.writeFileSync('report-work/browser-checks.json',JSON.stringify(checks,null,2));
const escape=s=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
for(const [name,file] of [['04-app','src/App.jsx'],['05-card','src/components/ProductCard.jsx'],['06-css','src/styles.css'],['07-main','src/main.jsx']]){
 let code=fs.readFileSync(file,'utf8');if(name==='06-css')code=code.slice(code.indexOf('.product-grid {'),code.indexOf('.product-card img'));
 await page.setViewportSize({width:1120,height:900});
 await page.setContent(`<html><meta charset="utf-8"><style>body{margin:0;background:#f6f7f9;color:#263345;font-family:Consolas,monospace}header{padding:20px 30px;background:#e8ebef;font:20px Segoe UI}pre{font-size:19px;line-height:1.55;padding:24px 30px;margin:0;white-space:pre-wrap}b{color:#526b22}</style><header>${file}</header><pre>${escape(code)}</pre></html>`);
 const height=await page.locator('pre').evaluate(e=>Math.ceil(e.getBoundingClientRect().bottom));
 await page.setViewportSize({width:1120,height});
 await page.screenshot({path:`report-work/${name}.png`,fullPage:true});
}
console.log(checks);await browser.close();
})();
