(function () {
  var nav = document.querySelector('nav');
  if (nav) {
    var links = nav.querySelectorAll('a');
    var current = window.location.pathname.replace(/\/$/, '') || '/';
    links.forEach(function (link) {
      var href = link.getAttribute('href');
      link.removeAttribute('aria-current');
      if (href === '/') {
        if (current === '/') {
          link.setAttribute('aria-current', 'page');
        }
      } else if (href && current.indexOf(href.replace(/\/$/, '')) === 0) {
        link.setAttribute('aria-current', 'page');
      }
    });
  }

  // Keyboard shortcuts
  var shortcutMap = {
    'h': '/',
    'a': '/agents/',
    'm': '/methodology/',
    'b': '/about/',
    'e': '/ethos/',
    's': '/auth/'
  };

  // Build shortcuts panel
  var panel = document.createElement('div');
  panel.className = 'shortcuts-panel';
  panel.setAttribute('role', 'dialog');
  panel.setAttribute('aria-label', 'Keyboard shortcuts');
  panel.tabIndex = -1;
  panel.innerHTML =
    '<div class="shortcuts-panel-inner">' +
      '<h2 class="shortcuts-title">Keyboard shortcuts</h2>' +
      '<div class="shortcuts-section">' +
        '<h3 class="shortcuts-section-title">Navigation</h3>' +
        '<dl class="shortcuts-list">' +
          '<dt><kbd>H</kbd></dt><dd>Home</dd>' +
          '<dt><kbd>A</kbd></dt><dd>Agents</dd>' +
          '<dt><kbd>M</kbd></dt><dd>Methodology</dd>' +
          '<dt><kbd>B</kbd></dt><dd>About</dd>' +
          '<dt><kbd>E</kbd></dt><dd>Ethos</dd>' +
          '<dt><kbd>S</kbd></dt><dd>Sign in</dd>' +
        '</dl>' +
      '</div>' +
      '<div class="shortcuts-section">' +
        '<h3 class="shortcuts-section-title">General</h3>' +
        '<dl class="shortcuts-list">' +
          '<dt><kbd>/</kbd></dt><dd>Search</dd>' +
          '<dt><kbd>?</kbd></dt><dd>Show shortcuts</dd>' +
          '<dt><kbd>Esc</kbd></dt><dd>Close</dd>' +
        '</dl>' +
        '<p class="shortcuts-note">Hold <kbd>Alt</kbd> (<kbd>\u2325</kbd>) to reveal navigation shortcuts.</p>' +
      '</div>' +
    '</div>';
  document.body.appendChild(panel);

  var panelInner = panel.querySelector('.shortcuts-panel-inner');
  panel.addEventListener('click', function(e) {
    if (!panelInner.contains(e.target)) closePanel();
  });

  function openPanel() {
    panel.classList.add('open');
    panel.focus();
  }

  function closePanel() {
    panel.classList.remove('open');
  }

  // Add keycap hints to nav links
  if (nav) {
    var navLinks = nav.querySelectorAll('a:not(.logo-link)');
    navLinks.forEach(function(link) {
      var href = link.getAttribute('href');
      var key = null;
      for (var k in shortcutMap) {
        if (shortcutMap[k] === href) { key = k; break; }
      }
      if (key) {
        var hint = document.createElement('span');
        hint.className = 'nav-key-hint';
        hint.textContent = '[' + key.toUpperCase() + ']';
        hint.setAttribute('aria-hidden', 'true');
        link.appendChild(document.createTextNode(' '));
        link.appendChild(hint);
      }
    });
  }

  // Alt key reveals keyboard hints
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Alt') {
      document.documentElement.classList.add('alt-hints');
    }
  });
  document.addEventListener('keyup', function(e) {
    if (e.key === 'Alt') {
      document.documentElement.classList.remove('alt-hints');
    }
  });

  // Global keyboard handler
  document.addEventListener('keydown', function(e) {
    if (e.altKey) return;
    var tag = e.target.tagName;
    if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return;

    var isPanelOpen = panel.classList.contains('open');

    if (e.key === 'Escape') {
      if (isPanelOpen) {
        e.preventDefault();
        closePanel();
        return;
      }
      if (overlay && overlay.classList.contains('open')) {
        closeLightbox();
        return;
      }
      return;
    }

    if (e.key === '?' || (e.shiftKey && e.key === '/')) {
      e.preventDefault();
      if (isPanelOpen) closePanel();
      else openPanel();
      return;
    }

    if (isPanelOpen) return;

    var key = e.key.toLowerCase();
    if (shortcutMap[key]) {
      e.preventDefault();
      window.location.href = shortcutMap[key];
      return;
    }

    // Arrow key navigation for ranking list
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      var rankingList = document.getElementById('ranking-list');
      if (rankingList && rankingList.contains(e.target)) {
        e.preventDefault();
        var items = rankingList.querySelectorAll('li a');
        var idx = Array.prototype.indexOf.call(items, e.target);
        if (e.key === 'ArrowDown' && idx < items.length - 1) items[idx + 1].focus();
        else if (e.key === 'ArrowUp' && idx > 0) items[idx - 1].focus();
        return;
      }

      var agentTable = document.getElementById('agent-table');
      if (agentTable && agentTable.contains(e.target)) {
        e.preventDefault();
        var rows = agentTable.querySelectorAll('tbody tr');
        var curRow = e.target.closest('tr');
        var rowIdx = Array.prototype.indexOf.call(rows, curRow);
        if (e.key === 'ArrowDown' && rowIdx < rows.length - 1) {
          var nextLink = rows[rowIdx + 1].querySelector('a');
          if (nextLink) nextLink.focus();
        } else if (e.key === 'ArrowUp' && rowIdx > 0) {
          var prevLink = rows[rowIdx - 1].querySelector('a');
          if (prevLink) prevLink.focus();
        }
        return;
      }
    }
  });

  var rankingEl = document.getElementById('ranking-list');
  var agentTable = document.getElementById('agent-table');
  var sortControls = document.getElementById('sort-controls');

  function formatDate(d) {
    var parts = d.split('-');
    var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    return months[parseInt(parts[1],10)-1] + ' ' + parts[0];
  }

  function verdictClass(v) {
    var map = {
      'Daily driver': 'status-daily',
      'Frequently used': 'status-frequent',
      'Useful in specific situations': 'status-useful',
      'Occasionally used': 'status-occasional',
      'Watching its progress': 'status-watching'
    };
    return map[v] || 'status-watching';
  }

  function renderRanking(list) {
    if (!rankingEl) return;
    var html = '';
    list.forEach(function(a, i) {
      html += '<li>' +
        '<span><span class="rank-number">' + (i+1) + '</span> <a href="' + a.path + '">' + a.name + '</a></span>' +
        '<span class="rank-label">' + a.verdict + '</span>' +
      '</li>';
    });
    rankingEl.innerHTML = html;

    // Make ranking list items navigable with arrow keys
    rankingEl.setAttribute('role', 'list');
  }

  function renderAgentTable(list) {
    if (!agentTable) return;
    var tbody = agentTable.querySelector('tbody');
    if (!tbody) return;
    var html = '';
    list.forEach(function(a) {
      html += '<tr tabindex="-1">' +
        '<td><a href="' + a.path + '">' + a.name + '</a><br><span class="text-small">' + a.developer + '</span></td>' +
        '<td><span class="status-indicator ' + verdictClass(a.verdict) + '"></span>' + a.verdict + '</td>' +
        '<td>' + a.versionReviewed + '</td>' +
        '<td>' + formatDate(a.lastUpdated) + '</td>' +
      '</tr>';
    });
    tbody.innerHTML = html;
  }

  function sortedBy(arr, key) {
    var copy = arr.slice();
    copy.sort(function(a, b) {
      if (key === 'lastUpdated' || key === 'addedDate') {
        return b[key].localeCompare(a[key]);
      }
      return 0;
    });
    return copy;
  }

  if (sortControls && agentTable) {
    var btns = sortControls.querySelectorAll('.sort-btn');
    btns.forEach(function(btn) {
      btn.addEventListener('click', function() {
        btns.forEach(function(b) { b.classList.remove('active'); b.setAttribute('aria-pressed', 'false'); });
        btn.classList.add('active');
        btn.setAttribute('aria-pressed', 'true');
        var sort = btn.getAttribute('data-sort');
        var list;
        if (sort === 'ranking') {
          list = agents;
        } else if (sort === 'recent') {
          list = sortedBy(agents, 'lastUpdated');
        } else if (sort === 'new') {
          list = sortedBy(agents, 'addedDate');
        } else {
          list = agents;
        }
        renderAgentTable(list);
      });
    });
    var defaultBtn = sortControls.querySelector('.sort-btn.active');
    if (defaultBtn) {
      defaultBtn.setAttribute('aria-pressed', 'true');
    }
  }

  // Lightbox
  var overlay = document.createElement('div');
  overlay.className = 'lightbox-overlay';
  overlay.setAttribute('role', 'dialog');
  overlay.setAttribute('aria-label', 'Image expanded view');
  overlay.tabIndex = -1;
  document.body.appendChild(overlay);
  var overlayImg = document.createElement('img');
  overlay.appendChild(overlayImg);

  var lastFocused;

  overlay.addEventListener('click', function() { closeLightbox(); });

  function closeLightbox() {
    overlay.classList.remove('open');
    if (lastFocused) { lastFocused.focus(); lastFocused = null; }
  }

  var figures = document.querySelectorAll('figure img');
  figures.forEach(function(img) {
    img.addEventListener('click', function() {
      overlayImg.src = img.src;
      overlayImg.alt = img.alt;
      lastFocused = img;
      overlay.classList.add('open');
      overlay.focus();
    });
  });

  if (rankingEl) {
    renderRanking(agents);
  }

  if (agentTable) {
    renderAgentTable(agents);
  }

  // Add [?] trigger to footer
  var footerColophon = document.querySelector('.footer-colophon');
  if (footerColophon) {
    var hintBtn = document.createElement('button');
    hintBtn.className = 'shortcuts-trigger';
    hintBtn.setAttribute('aria-label', 'Keyboard shortcuts');
    hintBtn.textContent = '?';
    footerColophon.appendChild(document.createTextNode(' \u00b7 '));
    footerColophon.appendChild(hintBtn);
    hintBtn.addEventListener('click', function (e) {
      e.preventDefault();
      openPanel();
    });
  }
})();