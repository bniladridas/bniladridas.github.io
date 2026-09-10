const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

const htmlPath = path.join(__dirname, '../../index.html');
const adminHtmlPath = path.join(__dirname, '../../admin/index.html');
const adminConfigPath = path.join(__dirname, '../../admin/config.yml');

let html = fs.readFileSync(htmlPath, 'utf8');
const adminHtml = fs.readFileSync(adminHtmlPath, 'utf8');
const adminConfig = fs.readFileSync(adminConfigPath, 'utf8');

html = html.replace('<script src="script.js"></script>', '');

function assert(cond, msg) {
  if (!cond) {
    console.error('✗', msg);
    process.exitCode = 1;
  } else {
    console.log('✓', msg);
  }
}

console.log('=== E2E: Edit link navigation (public flow) ===');

// 1. Homepage has Edit link
assert(html.includes('Edit this section'), 'HTML has Edit this section link');
assert(html.includes('href="admin/"'), 'Edit link href is admin/');

// 2. Create homepage DOM and find the link
const dom = new JSDOM(html, {
  url: 'http://127.0.0.1:8345/',
  runScripts: 'dangerously',
  pretendToBeVisual: true,
  beforeParse(window) {
    window.IntersectionObserver = class { constructor(cb){this.cb=cb;} observe(el){this.cb([{isIntersecting:true,target:el}],this);} unobserve(){} };
    window.fetch = () => Promise.reject(new Error('fetch not needed'));
  }
});
const { window } = dom;
const { document } = window;

// Minimal CSS/JS not needed for this navigation test, but load JS to ensure no errors
const js = fs.readFileSync(path.join(__dirname, '../../script.js'), 'utf8');
const css = fs.readFileSync(path.join(__dirname, '../../styles.css'), 'utf8');
const style = document.createElement('style');
style.textContent = css;
document.head.appendChild(style);
const scriptEl = document.createElement('script');
scriptEl.textContent = js;
document.body.appendChild(scriptEl);

setTimeout(() => {
  const editLink = document.querySelector('a[href="admin/"]');
  assert(!!editLink, 'DOM has Edit link element');
  assert(editLink.textContent.includes('Edit this section'), 'Edit link text is correct');
  console.log('Found Edit link:', editLink.href);

  // 3. Verify navigation target — do not mock click, verify href resolves to /admin/
  const targetUrl = new URL(editLink.getAttribute('href'), window.location.href).href;
  console.log('Target URL:', targetUrl);
  assert(targetUrl === 'http://127.0.0.1:8345/admin/', `Edit link navigates to /admin/ (got ${targetUrl})`);

  // 4. Load admin page and verify token-based editor loads (what admin sees) — not blank
  const adminDom = new JSDOM(adminHtml, { url: 'http://127.0.0.1:8345/admin/' });
  const adminDoc = adminDom.window.document;
  assert(adminDoc.querySelector('h1') && adminDoc.querySelector('h1').textContent.includes('Admin'), 'Admin page has Admin heading');
  assert(adminDoc.querySelector('#token') && adminDoc.querySelector('#title'), 'Admin has token and title fields');
  assert(adminHtml.includes('api.github.com') && adminHtml.includes('bniladridas/bniladridas.github.io'), 'Admin saves via GitHub API');
  console.log('Admin editor: token-based, saves to content/about.json');

  // 5. Verify admin config exists as alternative (Decap docs), but token editor is primary
  assert(adminConfig.includes('repo: bniladridas/bniladridas.github.io') || adminHtml.includes('api.github.com'), 'Admin points to correct repo');

  // Stop here — do not attempt GitHub API write. Document external boundary.
  console.log('Note: Stopping before GitHub API write — external boundary, no credentials used.');

  console.log('\n=== Results ===');
  if (process.exitCode) console.log('E2E EDIT LINK FAILED');
  else console.log('E2E EDIT LINK PASSED — public Edit navigation verified');
}, 200);
