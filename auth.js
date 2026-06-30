(function () {
  'use strict';

  /* ============================================================
   * Authentication Architecture
   * ============================================================
   *
   * Provides the Auth API surface (stable, will not change).
   * GitHub OAuth flow is active – token exchange requires a
   * serverless worker (see workers/auth-worker.js).
   *
   * To deploy the worker:
   *   1. Copy workers/auth-worker.js to a Cloudflare Worker
   *   2. Add your GITHUB_CLIENT_SECRET as an env variable
   *   3. Set workerUrl below to the deployed worker URL
   *
   * Email auth is stubbed – wire up a provider when ready.
   * ============================================================ */

  var AUTH_KEY = 'auth';

  var AUTH_CONFIG = {
    github: {
      clientId: 'Ov23liMMYiMlgYzGg2Ht',
      redirectUri: window.location.origin + '/auth/callback/',
      scope: 'read:user',
      workerUrl: 'https://auth-worker.harpertoken-welcome.workers.dev'
    }
  };

  function defaultState() {
    return { user: null };
  }

  function getState() {
    try {
      return JSON.parse(localStorage.getItem(AUTH_KEY)) || defaultState();
    } catch (e) {
      return defaultState();
    }
  }

  function setState(state) {
    localStorage.setItem(AUTH_KEY, JSON.stringify(state));
  }

  function clearState() {
    localStorage.removeItem(AUTH_KEY);
  }

  function generateState() {
    var arr = new Uint8Array(16);
    crypto.getRandomValues(arr);
    var state = Array.from(arr).map(function (b) {
      return b.toString(16).padStart(2, '0');
    }).join('');
    sessionStorage.setItem('auth_state', state);
    return state;
  }

  function getStoredState() {
    return sessionStorage.getItem('auth_state');
  }

  function clearStoredState() {
    sessionStorage.removeItem('auth_state');
  }

  function escapeHtml(str) {
    var div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
  }

  /* === Public API === */

  window.Auth = {
    _config: AUTH_CONFIG,
    getUser: function () {
      return getState().user;
    },

    isSignedIn: function () {
      return !!getState().user;
    },

    signIn: function (provider) {
      if (provider === 'github') {
        var cfg = AUTH_CONFIG.github;
        if (!cfg.workerUrl) {
          alert('GitHub sign-in is not yet configured. ' +
                'Deploy the auth worker and set workerUrl in auth.js.');
          return;
        }
        var state = generateState();
        sessionStorage.setItem('auth_return_to', window.location.pathname);
        var url = 'https://github.com/login/oauth/authorize'
          + '?client_id=' + encodeURIComponent(cfg.clientId)
          + '&redirect_uri=' + encodeURIComponent(cfg.redirectUri)
          + '&scope=' + encodeURIComponent(cfg.scope)
          + '&state=' + encodeURIComponent(state);
        window.location.href = url;
        return;
      }

      if (provider === 'email' || provider === 'email-signin') {
        alert('Email-based sign-in is coming soon. In the meantime, use GitHub.');
        return;
      }
    },

    signOut: function () {
      clearState();
      updateUI();
      if (window.location.pathname === '/auth/') {
        window.location.reload();
      }
    },

    _setUser: function (user) {
      setState({ user: user });
      updateUI();
    },

    init: function () {
      updateUI();
    },

    _getStoredState: getStoredState,
    _clearStoredState: clearStoredState
  };

  /* === UI Updates === */

  function updateUI() {
    var link = document.querySelector('.nav-auth-link');
    if (!link) return;

    var user = window.Auth.getUser();
    if (user) {
      link.textContent = escapeHtml(user.name || user.login || 'Account');
    } else {
      link.textContent = 'Sign in';
    }
  }

  /* Bootstrap */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', window.Auth.init);
  } else {
    window.Auth.init();
  }
})();
