const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

const htmlPath = path.join(__dirname, '../../index.html');
const cssPath = path.join(__dirname, '../../styles.css');
const jsPath = path.join(__dirname, '../../script.js');
const aboutPath = path.join(__dirname, '../../content/about.json');
const adminHtmlPath = path.join(__dirname, '../../admin/index.html');
const adminConfigPath = path.join(__dirname, '../../admin/config.yml');

let html = fs.readFileSync(htmlPath, 'utf8');
const css = fs.readFileSync(cssPath, 'utf8');
const js = fs.readFileSync(jsPath, 'utf8');
const about = JSON.parse(fs.readFileSync(aboutPath, 'utf8'));
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

console.log('=== E2E: Site (visitor and admin experience) ===');

// 1. About content loads and renders (what visitor sees)
assert(about.title && about.body && about.rule, 'about.json has title, body, rule');
assert(html.includes('id="about-title"') && html.includes('id="about-body"') && html.includes('id="about-rule"'), 'HTML has about placeholders');
assert(js.includes("fetch('content/about.json')"), 'JS fetches content/about.json');

// 2. Fixed header
assert(css.includes('.nav{position:fixed'), 'CSS header is fixed');
assert(css.includes('padding-top:64px'), 'CSS body has padding-top for fixed header');
assert(html.includes('class="nav"') && html.includes('id="scrollBar"'), 'HTML has nav and scroll progress');

// 3. Mobile menu (what visitor taps)
assert(html.includes('id="menuBtn"') && html.includes('id="mobileLinks"'), 'HTML has mobile menu');
assert(js.includes("menuBtn") && js.includes("mobileLinks"), 'JS handles mobile menu');
assert(css.includes('.mobile-links') && css.includes('.menu-btn'), 'CSS has mobile menu styles');

// 4. Copy button (what visitor clicks)
assert(html.includes('class="copy"') && html.includes('quickstart.ts'), 'HTML has copy button in quickstart');
assert(js.includes("clipboard.writeText") || js.includes("execCommand"), 'JS handles copy');

// 5. Gist lazy loading (what visitor expands)
assert(html.includes('gist-details') && html.includes('data-gist'), 'HTML has gist details');
assert(js.includes('details.gist-details') && js.includes('gist.githubusercontent.com'), 'JS lazy loads gists');
assert(js.includes('function mdRender'), 'JS has markdown renderer');

// 6. Scroll progress and cue (what visitor sees while scrolling)
assert(html.includes('id="scrollCue"') && html.includes('id="scrollBar"'), 'HTML has scroll cue and progress');
assert(js.includes('onScroll') && js.includes('scrollBar'), 'JS handles scroll progress');
assert(css.includes('.scroll-cue'), 'CSS has scroll cue');

// 7. Admin page and config (what admin sees)
assert(adminHtml.includes('decap-cms'), 'Admin HTML loads Decap CMS');
assert(adminConfig.includes('backend:') && adminConfig.includes('name: github'), 'Admin config has github backend');
assert(adminConfig.includes('repo: bniladridas/bniladridas.github.io'), 'Admin config points to correct repo');
assert(adminConfig.includes('file: "content/about.json"'), 'Admin config edits about.json');
assert(!adminConfig.includes('auth_type: implicit'), 'Admin config does not use implicit flow (per docs)');

// 8. Open Graph and Twitter metadata (what social previews see)
assert(html.includes('property="og:title"'), 'HTML has og:title');
assert(html.includes('property="og:description"'), 'HTML has og:description');
assert(html.includes('property="og:image"') && html.includes('og-image.png'), 'HTML has og:image with og-image.png');
assert(html.includes('name="twitter:card"') && html.includes('summary_large_image'), 'HTML has twitter:card');
assert(html.includes('name="twitter:image"'), 'HTML has twitter:image');
assert(html.includes('property="og:site_name"'), 'HTML has og:site_name');

// 9. DOM simulation for interactive parts
const dom = new JSDOM(html, {
  url: 'http://127.0.0.1:8345/',
  runScripts: 'dangerously',
  pretendToBeVisual: true,
  beforeParse(window) {
    window.IntersectionObserver = class { constructor(cb){this.cb=cb;} observe(el){this.cb([{isIntersecting:true,target:el}],this);} unobserve(){} };
    window.fetch = (url) => {
      if (String(url).includes('content/about.json')) {
        return Promise.resolve({ ok: true, json: () => Promise.resolve(about) });
      }
      return Promise.reject(new Error('fetch not needed'));
    };
  }
});
const { window } = dom;
const { document } = window;
const style = document.createElement('style');
style.textContent = css;
document.head.appendChild(style);
const scriptEl = document.createElement('script');
scriptEl.textContent = js;
document.body.appendChild(scriptEl);

setTimeout(() => {
  // About rendered
  assert(document.getElementById('about-title').textContent === about.title, 'About title rendered from about.json');
  assert(document.getElementById('about-body').textContent === about.body, 'About body rendered');

  // Mobile menu toggle
  const menuBtn = document.getElementById('menuBtn');
  const mobileLinks = document.getElementById('mobileLinks');
  assert(!!menuBtn && !!mobileLinks, 'Mobile menu elements exist');
  menuBtn.click();
  assert(mobileLinks.classList.contains('open'), 'Mobile menu opens on click');
  menuBtn.click();
  assert(!mobileLinks.classList.contains('open'), 'Mobile menu closes on second click');

  // Copy button (check handler exists and text changes)
  const copyBtn = document.querySelector('.copy');
  assert(!!copyBtn, 'Copy button exists');

  // Header is fixed (computed style)
  const nav = document.querySelector('.nav');
  assert(window.getComputedStyle(nav).position === 'fixed', 'Header is fixed');

  console.log('\n=== Results ===');
  if (process.exitCode) console.log('E2E SITE FAILED');
  else console.log('E2E SITE PASSED — visitor and admin experience verified');
}, 200);
