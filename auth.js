// auth.js - shared sign-in plumbing for the Hayes Systems client
// account pages (client-accounts-2026-11 Card B). One small plain
// script, no build; every page carries its own markup and a few lines
// of page logic on top of this. The API origin literal matches
// fub-app.html exactly so the sandbox origin rewrite keeps working.
//
// Surface: API, post(path, body), me(), next(default), goto(path),
// fail(r), badTicket(), wireShow(), busy(). Every network helper
// RESOLVES with {status, j} and never rejects, so a transport failure
// can never blank a page: callers paint a plain message instead.
var API = 'https://ops.hayessystems.com';

function $(id){ return document.getElementById(id); }

function show(id, text){
  var el = $(id);
  if (!el) return;
  el.textContent = text || '';
  el.classList.remove('hide');
}

function clearMsg(id){
  var el = $(id);
  if (!el) return;
  el.textContent = '';
  el.classList.add('hide');
}

// Plain failure copy for transport trouble, throttling and server
// errors. A 401 is page business (signed out, or a wrong password) and
// is handled by the page, never here. Returns true when the failure
// was handled and painted.
function fail(r){
  if (!r || r.status === 0) {
    show('authErr', 'We could not reach Hayes Systems just now. Check'
      + ' your connection and try again.');
    return true;
  }
  if (r.status === 429) {
    show('authErr', (r.j && r.j.message)
      || 'Too many requests. Wait a moment and try again.');
    return true;
  }
  if (r.status >= 500) {
    show('authErr', (r.j && r.j.message)
      || 'Sign-in is unavailable just now. Try again in a few minutes.');
    return true;
  }
  return false;
}

// POST with the session cookie along (credentials include). Always
// resolves {status, j}; a broken body parses as j = null.
function post(path, body){
  return fetch(API + path, {
    method: 'POST',
    credentials: 'include',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(body || {})
  }).then(function(r){
    return r.json().catch(function(){ return null; })
      .then(function(j){ return {status: r.status, j: j}; });
  }).catch(function(){ return {status: 0, j: null}; });
}

// GET /api/auth/me with the session cookie along. 401 means signed
// out; the page decides what that means for it.
function me(){
  return fetch(API + '/api/auth/me', {credentials: 'include'})
    .then(function(r){
      return r.json().catch(function(){ return null; })
        .then(function(j){ return {status: r.status, j: j}; });
    }).catch(function(){ return {status: 0, j: null}; });
}

// A ?next value is honoured only when it is a same-site absolute path:
// it must start with "/" and must not start with "//" (protocol
// relative) or contain a backslash (browsers fold those into "//").
// Anything else falls back to the default.
function next(defaultPath){
  var v = '';
  try { v = new URLSearchParams(location.search).get('next') || ''; }
  catch (e) {}
  if (v && v.charAt(0) === '/' && v.charAt(1) !== '/'
      && v.indexOf('\\') < 0) return v;
  return defaultPath;
}

function goto(path){ location.assign(path); }

// The shared dead-link state (BRIEF 5.5): one message, two doors. The
// page decides whether its form stays usable (login keeps it).
function badTicket(){
  var el = $('badTicket');
  if (el) el.classList.remove('hide');
}

// "Show" toggle for a password field. Paste is never blocked.
function wireShow(btnId, inputId){
  var b = $(btnId), i = $(inputId);
  if (!b || !i) return;
  b.addEventListener('click', function(){
    var reveal = i.type === 'password';
    i.type = reveal ? 'text' : 'password';
    b.textContent = reveal ? 'Hide' : 'Show';
  });
}

// Busy state keeps the button's box intact (the ghl-app Refresh tags
// lesson): the label stays, only the small spinner runs.
function busy(btn, on, label){
  if (!btn) return;
  btn.disabled = on;
  btn.innerHTML = on
    ? '<span class="spin-sm"></span>' + label : label;
}
