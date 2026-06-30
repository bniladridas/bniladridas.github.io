/**
 * Cloudflare Worker – GitHub OAuth Token Exchange
 *
 * Deploy this worker to handle the code→token exchange securely.
 * The GitHub client_secret stays server-side.
 *
 * Deploy:
 *   1. npm install -g wrangler
 *   2. wrangler deploy workers/auth-worker.js --name auth-worker
 *   3. wrangler secret put GITHUB_CLIENT_SECRET
 *   4. Set AUTH_CONFIG.github.workerUrl in auth.js to the deployed URL
 *
 * Environment variables (set via `wrangler secret put` or dashboard):
 *   GITHUB_CLIENT_SECRET – required
 */

var CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type'
};

addEventListener('fetch', function (event) {
  event.respondWith(handleRequest(event.request));
});

async function handleRequest(request) {
  if (request.method === 'OPTIONS') {
    return new Response(null, {
      headers: CORS_HEADERS
    });
  }

  if (request.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), {
      status: 405,
      headers: Object.assign({ 'Content-Type': 'application/json', 'Allow': 'POST' }, CORS_HEADERS)
    });
  }

  var body;
  try {
    body = await request.json();
  } catch (e) {
    return new Response(JSON.stringify({ error: 'Invalid JSON' }), {
      status: 400,
      headers: Object.assign({ 'Content-Type': 'application/json' }, CORS_HEADERS)
    });
  }

  var code = body.code;
  var clientId = body.client_id;
  var redirectUri = body.redirect_uri;

  if (!code) {
    return new Response(JSON.stringify({ error: 'Missing authorization code' }), {
      status: 400,
      headers: Object.assign({ 'Content-Type': 'application/json' }, CORS_HEADERS)
    });
  }

  var clientSecret = GITHUB_CLIENT_SECRET;
  if (!clientSecret) {
    return new Response(JSON.stringify({ error: 'Server misconfigured' }), {
      status: 500,
      headers: Object.assign({ 'Content-Type': 'application/json' }, CORS_HEADERS)
    });
  }

  /* Exchange code for access token */
  var tokenRes = await fetch('https://github.com/login/oauth/access_token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    },
    body: JSON.stringify({
      client_id: clientId,
      client_secret: clientSecret,
      code: code,
      redirect_uri: redirectUri
    })
  });

  var tokenData = await tokenRes.json();

  if (tokenData.error) {
    return new Response(JSON.stringify({
      error: tokenData.error,
      error_description: tokenData.error_description
    }), {
      status: 400,
      headers: Object.assign({ 'Content-Type': 'application/json' }, CORS_HEADERS)
    });
  }

  var accessToken = tokenData.access_token;

  /* Fetch user info */
  var userRes = await fetch('https://api.github.com/user', {
    headers: {
      'Authorization': 'Bearer ' + accessToken,
      'Accept': 'application/vnd.github.v3+json',
      'User-Agent': 'palmshed-auth'
    }
  });

  if (!userRes.ok) {
    return new Response(JSON.stringify({ error: 'Failed to fetch user info' }), {
      status: 502,
      headers: Object.assign({ 'Content-Type': 'application/json' }, CORS_HEADERS)
    });
  }

  var userData = await userRes.json();

  /* Fetch primary email if not public */
  var email = userData.email || '';
  if (!email) {
    var emailRes = await fetch('https://api.github.com/user/emails', {
      headers: {
        'Authorization': 'Bearer ' + accessToken,
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'palmshed-auth'
      }
    });
    if (emailRes.ok) {
      var emails = await emailRes.json();
      var primary = emails.find(function (e) { return e.primary && e.verified; });
      if (primary) email = primary.email;
    }
  }

  return new Response(JSON.stringify({
    login: userData.login,
    name: userData.name,
    email: email,
    avatar_url: userData.avatar_url
  }), {
    headers: Object.assign({ 'Content-Type': 'application/json' }, CORS_HEADERS)
  });
}
