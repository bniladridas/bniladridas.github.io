(function () {
  'use strict';

  var index = [];
  var input, resultsEl, emptyEl;
  var selectedIdx = -1;
  var currentResults = [];
  var searchContainer;

  function escapeHtml(str) {
    var d = document.createElement('div');
    d.appendChild(document.createTextNode(str));
    return d.innerHTML;
  }

  function highlightMatch(text, query) {
    if (!query) return escapeHtml(text);
    var terms = query.toLowerCase().split(/\s+/).filter(Boolean);
    var lower = text.toLowerCase();
    var result = [];
    var last = 0;

    for (var i = 0; i < lower.length; i++) {
      for (var t = 0; t < terms.length; t++) {
        var term = terms[t];
        if (lower.slice(i, i + term.length) === term) {
          if (i > last) {
            result.push(escapeHtml(text.substring(last, i)));
          }
          result.push('<mark>' + escapeHtml(text.slice(i, i + term.length)) + '</mark>');
          i += term.length - 1;
          last = i + 1;
          break;
        }
      }
    }
    if (last < text.length) {
      result.push(escapeHtml(text.substring(last)));
    }
    return result.join('');
  }

  function snippet(text, query, maxLen) {
    maxLen = maxLen || 120;
    if (!query) return escapeHtml(text.substring(0, maxLen));

    var lower = text.toLowerCase();
    var qLower = query.toLowerCase();
    var idx = lower.indexOf(qLower);

    if (idx === -1) return highlightMatch(text.substring(0, maxLen), query);

    var start = Math.max(0, idx - Math.floor((maxLen - qLower.length) / 2));
    var end = Math.min(text.length, start + maxLen);

    if (start > 0) {
      start = text.indexOf(' ', start - 20);
      if (start < 0) start = Math.max(0, idx - 40);
    }
    if (end < text.length) {
      end = text.lastIndexOf(' ', end + 20);
      if (end < start) end = Math.min(text.length, start + maxLen);
    }

    var prefix = start > 0 ? '\u2026' : '';
    var suffix = end < text.length ? '\u2026' : '';
    return prefix + highlightMatch(text.substring(Math.max(0, start), end), query) + suffix;
  }

  function buildSearch() {
    var navRight = document.querySelector('.nav-right');
    if (!navRight) {
      /* Fallback: try old nav container */
      navRight = document.querySelector('nav .container');
    }
    if (!navRight) return;

    searchContainer = document.createElement('div');
    searchContainer.className = 'nav-search';

    searchContainer.innerHTML =
      '<button class="nav-search-btn" aria-label="Search"></button>' +
      '<span class="nav-search-field">' +
        '<input type="search" class="nav-search-input" placeholder="Search\u2026" aria-label="Search" autocomplete="off" spellcheck="false">' +
        '<kbd class="nav-search-key">/</kbd>' +
      '</span>' +
      '<div class="nav-search-dropdown" role="listbox" hidden></div>' +
      '<div class="nav-search-empty" role="status" hidden><p>Nothing matched your search.</p></div>';

    navRight.appendChild(searchContainer);

    input = searchContainer.querySelector('.nav-search-input');
    resultsEl = searchContainer.querySelector('.nav-search-dropdown');
    emptyEl = searchContainer.querySelector('.nav-search-empty');
    var searchBtn = searchContainer.querySelector('.nav-search-btn');

    function runSearch(query) {
      if (!query || index.length === 0) return [];

      var terms = query.toLowerCase().split(/\s+/).filter(Boolean);
      var results = [];
      var seen = {};

      index.forEach(function (page) {
        var titleLower = page.title.toLowerCase();
        var allTermsMatchTitle = terms.every(function (t) { return titleLower.indexOf(t) !== -1; });

        if (allTermsMatchTitle) {
          var key = page.url;
          if (!seen[key]) {
            seen[key] = true;
            results.push({
              url: page.url,
              title: page.title,
              breadcrumb: page.breadcrumb,
              snippet: page.summary || page.sections && page.sections[0] && page.sections[0].content.substring(0, 120) || '',
              score: 10
            });
          }
        }
      });

      index.forEach(function (page) {
        var sections = page.sections || [];
        sections.forEach(function (section) {
          var headingLower = (section.heading || '').toLowerCase();
          var contentLower = (section.content || '').toLowerCase();
          var allTermsMatchHeading = terms.every(function (t) { return headingLower.indexOf(t) !== -1; });
          var allTermsMatchContent = terms.every(function (t) { return contentLower.indexOf(t) !== -1; });

          if (allTermsMatchHeading || allTermsMatchContent) {
            var key = page.url + '#' + section.heading;
            if (seen[key]) return;
            seen[key] = true;

            var score = allTermsMatchHeading ? 5 : 1;
            var ctx = section.content;
            if (ctx.length > 150) {
              var matchIdx = ctx.toLowerCase().indexOf(terms[0]);
              if (matchIdx > 50) {
                var start = ctx.lastIndexOf(' ', matchIdx - 50);
                if (start < 0) start = Math.max(0, matchIdx - 50);
                ctx = (start > 0 ? '\u2026' : '') + ctx.substring(start, start + 150) + (ctx.length > start + 150 ? '\u2026' : '');
              }
            }

            results.push({
              url: page.url,
              title: page.title,
              breadcrumb: page.breadcrumb + ' / ' + section.heading,
              snippet: ctx,
              score: score
            });
          }
        });
      });

      results.sort(function (a, b) { return b.score - a.score; });
      return results.slice(0, 12);
    }

    function renderResults(results, query) {
      if (results.length === 0) {
        resultsEl.innerHTML = '';
        resultsEl.hidden = true;
        emptyEl.hidden = false;
        return;
      }

      emptyEl.hidden = true;
      resultsEl.hidden = false;

      var html = '';
      results.forEach(function (r) {
        html +=
          '<div class="nav-search-result" role="option" aria-selected="false" data-url="' +
            escapeHtml(r.url) + '">' +
            '<div class="nav-search-result-breadcrumb">' + escapeHtml(r.breadcrumb) + '</div>' +
            '<div class="nav-search-result-snippet">' + snippet(r.snippet, query) + '</div>' +
          '</div>';
      });
      resultsEl.innerHTML = html;

      var resultDivs = resultsEl.querySelectorAll('.nav-search-result');
      resultDivs.forEach(function (el) {
        el.addEventListener('click', function () {
          window.location.href = el.getAttribute('data-url');
        });
        el.addEventListener('mouseenter', function () {
          var idx = Array.prototype.indexOf.call(el.parentNode.children, el);
          selectedIdx = idx;
          resultDivs.forEach(function (r, i) {
            r.classList.toggle('nav-search-result-selected', i === selectedIdx);
            r.setAttribute('aria-selected', i === selectedIdx ? 'true' : 'false');
          });
        });
      });
    }

    /* Input events */
    input.addEventListener('input', function () {
      var query = input.value.trim();
      if (!query) {
        closeDropdown();
        return;
      }
      currentResults = runSearch(query);
      renderResults(currentResults, query);
      selectedIdx = -1;
    });

    input.addEventListener('focus', function () {
      searchContainer.classList.add('nav-search-focused');
      if (input.value.trim()) {
        currentResults = runSearch(input.value.trim());
        renderResults(currentResults, input.value.trim());
      }
    });

    input.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        if (resultsEl.hidden || currentResults.length === 0) return;
        selectedIdx = Math.min(selectedIdx + 1, currentResults.length - 1);
        updateSelection();
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        if (resultsEl.hidden || currentResults.length === 0) return;
        if (selectedIdx <= 0) {
          selectedIdx = -1;
          clearSelection();
          return;
        }
        selectedIdx = Math.max(selectedIdx - 1, 0);
        updateSelection();
      } else if (e.key === 'Enter') {
        e.preventDefault();
        if (selectedIdx >= 0 && selectedIdx < currentResults.length) {
          navigateTo(currentResults[selectedIdx]);
        } else if (currentResults.length > 0) {
          navigateTo(currentResults[0]);
        }
      } else if (e.key === 'Escape') {
        e.preventDefault();
        closeDropdown();
        input.blur();
      }
    });

    input.addEventListener('blur', function () {
      /* Delay so click on a result registers before we hide */
      setTimeout(function () {
        closeDropdown();
        searchContainer.classList.remove('nav-search-focused');
      }, 200);
    });

    searchBtn.addEventListener('click', function () {
      input.focus();
    });

    function updateSelection() {
      var items = resultsEl.querySelectorAll('.nav-search-result');
      items.forEach(function (el, i) {
        el.classList.toggle('nav-search-result-selected', i === selectedIdx);
        el.setAttribute('aria-selected', i === selectedIdx ? 'true' : 'false');
      });
      if (selectedIdx >= 0 && items[selectedIdx]) {
        items[selectedIdx].scrollIntoView({ block: 'nearest' });
      }
    }

    function clearSelection() {
      var items = resultsEl.querySelectorAll('.nav-search-result');
      items.forEach(function (el) {
        el.classList.remove('nav-search-result-selected');
        el.setAttribute('aria-selected', 'false');
      });
    }

    function navigateTo(result) {
      closeDropdown();
      var url = result.url;
      if (result.anchor) url += result.anchor;
      window.location.href = url;
    }

    function closeDropdown() {
      resultsEl.innerHTML = '';
      resultsEl.hidden = true;
      emptyEl.hidden = true;
      selectedIdx = -1;
      currentResults = [];
    }

    /* Global '/' key to focus search */
    document.addEventListener('keydown', function (e) {
      if (e.key === '/' && input !== document.activeElement) {
        var tag = e.target.tagName;
        if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return;
        e.preventDefault();
        input.focus();
      }
    });
  }

  /* Load index */
  fetch('/search-index.json')
    .then(function (r) { return r.json(); })
    .then(function (data) { index = data; })
    .catch(function () {
      var emptyMsg = document.querySelector('.nav-search-empty p');
      if (emptyMsg) emptyMsg.textContent = 'Search is temporarily unavailable.';
    });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', buildSearch);
  } else {
    buildSearch();
  }
})();
