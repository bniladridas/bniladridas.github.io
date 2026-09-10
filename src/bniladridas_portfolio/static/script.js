// Mobile menu
const menuBtn = document.getElementById('menuBtn');
const mobileLinks = document.getElementById('mobileLinks');
if (menuBtn && mobileLinks) {
  menuBtn.addEventListener('click', () => mobileLinks.classList.toggle('open'));
  mobileLinks.querySelectorAll('a').forEach((a) =>
    a.addEventListener('click', () => mobileLinks.classList.remove('open'))
  );
}

// Copy buttons
document.querySelectorAll('.copy').forEach((btn) => {
  btn.addEventListener('click', async () => {
    const text = btn.getAttribute('data-copy') || '';
    const done = () => {
      const old = btn.textContent;
      btn.textContent = 'Copied ✓';
      setTimeout(() => (btn.textContent = old), 1400);
    };
    try {
      await navigator.clipboard.writeText(text);
      done();
    } catch {
      const ta = document.createElement('textarea');
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand('copy'); } catch {}
      ta.remove();
      done();
    }
  });
});

// Lazy gist rendering: fetch raw markdown + render inline.
// (gist ".../xxx.js" embeds use document.write, which blanks the page
// when injected after load, so we never inject them.)
function mdEscape(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
function mdInline(s) {
  s = mdEscape(s);
  s = s.replace(/`([^`]+)`/g, '<code>$1</code>');
  s = s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  s = s.replace(/\[([^\]]+)\]\((https?:[^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
  return s;
}
function mdTableRow(cells, head) {
  const t = head ? 'th' : 'td';
  return '<tr>' + cells.map((c) => '<' + t + '>' + mdInline(c.trim()) + '</' + t + '>').join('') + '</tr>';
}
function mdRender(src) {
  const lines = src.replace(/\r/g, '').split('\n');
  let html = '', i = 0, inCode = false, codeLang = '', codeBuf = [], listTag = '';
  const closeList = () => { if (listTag) { html += '</' + listTag + '>'; listTag = ''; } };
  const isDelim = (l) => l.trim().indexOf('-') > -1 && /^\|?[\s:|_-]+\|?$/.test(l.trim());
  const splitRow = (l) => l.trim().replace(/^\||\|$/g, '').split('|');
  while (i < lines.length) {
    const line = lines[i];
    const fence = line.match(/^```(\w*)/);
    if (fence) {
      if (!inCode) { closeList(); inCode = true; codeLang = fence[1]; codeBuf = []; }
      else { inCode = false; html += '<pre><code>' + mdEscape(codeBuf.join('\n')) + '</code></pre>'; }
      i++; continue;
    }
    if (inCode) { codeBuf.push(line); i++; continue; }
    if (/^\|?.*\|.*$/.test(line) && i + 1 < lines.length && isDelim(lines[i + 1])) {
      closeList();
      const head = splitRow(line);
      html += '<div class="table-wrap"><table><thead>' + mdTableRow(head, true) + '</thead><tbody>';
      i += 2;
      while (i < lines.length && lines[i].trim().indexOf('|') > -1) {
        html += mdTableRow(splitRow(lines[i]), false); i++;
      }
      html += '</tbody></table></div>'; continue;
    }
    const h = line.match(/^(#{1,4})\s+(.*)/);
    if (h) { closeList(); html += '<h' + h[1].length + '>' + mdInline(h[2]) + '</h' + h[1].length + '>'; i++; continue; }
    if (/^---+$/.test(line.trim())) { closeList(); html += '<hr>'; i++; continue; }
    if (/^>\s?/.test(line)) { closeList(); html += '<blockquote>' + mdInline(line.replace(/^>\s?/, '')) + '</blockquote>'; i++; continue; }
    const ul = line.match(/^\s*[-*]\s+(.*)/);
    const ol = line.match(/^\s*\d+[.)]\s+(.*)/);
    if (ul || ol) {
      const tag = ul ? 'ul' : 'ol';
      const item = ul ? ul[1] : ol[1];
      if (listTag !== tag) { closeList(); listTag = tag; html += '<' + tag + '>'; }
      html += '<li>' + mdInline(item) + '</li>'; i++; continue;
    }
    closeList();
    if (line.trim() === '') { i++; continue; }
    html += '<p>' + mdInline(line) + '</p>'; i++;
  }
  closeList();
  if (inCode) html += '<pre><code>' + mdEscape(codeBuf.join('\n')) + '</code></pre>';
  return html;
}
document.querySelectorAll('details.gist-details').forEach((d) => {
  let loaded = false;
  d.addEventListener('toggle', async () => {
    if (!d.open || loaded) return;
    loaded = true;
    const summary = d.querySelector('summary[data-gist]');
    const body = d.querySelector('.gist-body');
    if (!summary || !body) return;
    const id = summary.getAttribute('data-gist');
    const file = summary.getAttribute('data-file') || '';
    const pageUrl = 'https://gist.github.com/' + id;
    body.innerHTML = '<p class="muted small">Loading gist…</p>';
    try {
      const res = await fetch('https://gist.githubusercontent.com/' + id + '/raw/' + file, { cache: 'force-cache' });
      if (!res.ok) throw new Error('HTTP ' + res.status);
      const md = await res.text();
      body.innerHTML = '<div class="md-body">' + mdRender(md) + '</div>';
    } catch (e) {
      body.innerHTML =
        '<p class="muted small">Could not load the gist inline. <a href="' +
        pageUrl + '" target="_blank" rel="noopener">Open it on gist.github.com ↗</a></p>';
    }
  });
});

// Scroll cue + progress (clever, quiet)
const scrollBar = document.getElementById('scrollBar');
const scrollCue = document.getElementById('scrollCue');
let ticking = false;
function onScroll() {
  if (!ticking) {
    requestAnimationFrame(() => {
      const max = document.documentElement.scrollHeight - window.innerHeight;
      const pct = max > 0 ? (window.scrollY / max) * 100 : 0;
      if (scrollBar) scrollBar.style.width = pct.toFixed(2) + '%';
      if (scrollCue) {
        if (window.scrollY > 120) scrollCue.classList.add('hidden');
        else scrollCue.classList.remove('hidden');
      }
      ticking = false;
    });
    ticking = true;
  }
}
window.addEventListener('scroll', onScroll, { passive: true });
onScroll();

// Theme switch: two round balls at end, keep both themes
(function() {
  function initTheme() {
    const balls = document.querySelectorAll('.theme-ball');
    if (!balls.length) return;
    const saved = localStorage.getItem('theme');
    const initial = saved || 'new';
    document.documentElement.setAttribute('data-theme', initial);
    balls.forEach((b) => b.classList.toggle('active', b.dataset.theme === initial));
    balls.forEach((ball) => {
      ball.addEventListener('click', () => {
        const t = ball.dataset.theme;
        document.documentElement.setAttribute('data-theme', t);
        try { localStorage.setItem('theme', t); } catch (e) {}
        balls.forEach((b) => b.classList.toggle('active', b === ball));
      });
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initTheme);
  else initTheme();
})();

// Scroll reveal
const io = new IntersectionObserver(
  (entries) =>
    entries.forEach((e) => {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
        io.unobserve(e.target);
      }
    }),
  { threshold: 0.12 }
);
document.querySelectorAll('.reveal').forEach((el) => io.observe(el));
