const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

const htmlPath = path.join(__dirname, '../../index.html');
const cssPath = path.join(__dirname, '../../styles.css');
const jsPath = path.join(__dirname, '../../script.js');

let html = fs.readFileSync(htmlPath, 'utf8');
const css = fs.readFileSync(cssPath, 'utf8');
const js = fs.readFileSync(jsPath, 'utf8');

// Remove the script tag to avoid duplicate execution in jsdom
html = html.replace('<script src="script.js"></script>', '');

function assert(cond, msg) {
  if (!cond) {
    console.error('✗', msg);
    process.exitCode = 1;
  } else {
    console.log('✓', msg);
  }
}

console.log('=== E2E: Theme switch ===');

// 1. Static checks
assert(html.includes('theme-ball'), 'HTML has theme-ball');
assert((html.match(/theme-ball/g)||[]).length === 2, 'HTML has 2 theme balls');
assert(html.includes('data-theme="new"') && html.includes('data-theme="prev"'), 'HTML has both data-theme values');
assert(css.includes('html[data-theme="prev"]'), 'CSS has prev theme override');
assert(css.includes('.theme-ball.active'), 'CSS has active state');
assert(js.includes('theme-ball'), 'JS has theme logic');
assert(js.includes('localStorage'), 'JS uses localStorage');

// 2. JS DOM simulation
const dom = new JSDOM(html, {
  url: 'http://127.0.0.1:8345/',
  runScripts: 'dangerously',
  pretendToBeVisual: true,
  beforeParse(window) {
    window.IntersectionObserver = class {
      constructor(cb) { this.cb = cb; }
      observe(el) { this.cb([{isIntersecting: true, target: el}], this); }
      unobserve() {}
    };
    window.fetch = () => Promise.reject(new Error('fetch not needed'));
  }
});

const { window } = dom;
const { document } = window;

// Inject CSS
const style = document.createElement('style');
style.textContent = css;
document.head.appendChild(style);

// Inject JS (only once, since we removed the HTML script tag)
const scriptEl = document.createElement('script');
scriptEl.textContent = js;
document.body.appendChild(scriptEl);

// JSDOM fires DOMContentLoaded async, wait a tick
setTimeout(() => {
  const htmlEl = document.documentElement;
  const balls = document.querySelectorAll('.theme-ball');
  console.log('Found balls:', balls.length);
  assert(balls.length === 2, 'DOM has 2 balls');

  // Initial state should be new (default)
  const initialTheme = htmlEl.getAttribute('data-theme');
  console.log('Initial data-theme:', initialTheme);
  assert(initialTheme === 'new', `Initial theme is new (got ${initialTheme})`);

  const activeBefore = document.querySelector('.theme-ball.active');
  assert(activeBefore && activeBefore.dataset.theme === 'new', 'Initially new ball is active');

  // Click prev
  const prevBall = document.querySelector('.theme-ball[data-theme="prev"]');
  assert(!!prevBall, 'Prev ball exists');
  prevBall.click();

  const afterTheme = htmlEl.getAttribute('data-theme');
  console.log('After click data-theme:', afterTheme);
  assert(afterTheme === 'prev', `After click, data-theme is prev (got ${afterTheme})`);

  const activeAfter = document.querySelector('.theme-ball.active');
  assert(activeAfter && activeAfter.dataset.theme === 'prev', 'After click, prev ball is active');

  // Check computed style or CSS variable (basic)
  const prevBg = window.getComputedStyle(htmlEl).getPropertyValue('--bg').trim();
  console.log('Computed --bg after prev:', prevBg);

  // Click new again
  const newBall = document.querySelector('.theme-ball[data-theme="new"]');
  newBall.click();
  assert(htmlEl.getAttribute('data-theme') === 'new', 'After second click, back to new');
  assert(document.querySelector('.theme-ball.active').dataset.theme === 'new', 'New ball active again');

  const saved = window.localStorage.getItem('theme');
  console.log('localStorage theme:', saved);
  assert(saved === 'new', `localStorage saved new (got ${saved})`);

  console.log('\n=== Results ===');
  if (process.exitCode) console.log('E2E FAILED');
  else console.log('E2E PASSED — theme switch works');
}, 200);
