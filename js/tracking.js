(function () {
  'use strict';
  const config = window.MOMENTI_TRACKING || {};
  const enabled = Boolean(config.metaPixelId || config.tiktokPixelId);
  const key = 'momenti_ad_consent_v1';
  let allowed = false, started = false;
  const seen = new Set();
  function save(value) { try { localStorage.setItem(key, value); } catch (_) {} }
  function read() { try { return localStorage.getItem(key); } catch (_) { return null; } }
  function script(src) { const s = document.createElement('script'); s.async = true; s.src = src; document.head.appendChild(s); }
  function start() {
    if (started || !enabled || !allowed) return;
    started = true;
    if (config.metaPixelId) {
      if (!window.fbq) {
        const f = window.fbq = function () { f.callMethod ? f.callMethod.apply(f, arguments) : f.queue.push(arguments); };
        window._fbq = f; f.push = f; f.loaded = true; f.version = '2.0'; f.queue = [];
        script('https://connect.facebook.net/en_US/fbevents.js');
      }
      window.fbq('consent', 'grant');
      window.fbq('init', config.metaPixelId);
      window.fbq('track', 'PageView');
    }
    if (config.tiktokPixelId) {
      window.TiktokAnalyticsObject = 'ttq';
      const ttq = window.ttq = window.ttq || [];
      const defer = (target, name) => { target[name] = function () { target.push([name].concat(Array.from(arguments))); }; };
      ['page','track','identify','instances','debug','on','off','once','ready','alias','group','enableCookie','disableCookie','holdConsent','revokeConsent','grantConsent'].forEach(name => { if (!ttq[name]) defer(ttq, name); });
      ttq.load = function (id) {
        const url = 'https://analytics.tiktok.com/i18n/pixel/events.js';
        ttq._i = ttq._i || {}; ttq._i[id] = []; ttq._i[id]._u = url;
        ttq._t = ttq._t || {}; ttq._t[id] = +new Date();
        ttq._o = ttq._o || {}; ttq._o[id] = {};
        script(url + '?sdkid=' + encodeURIComponent(id) + '&lib=ttq');
      };
      ttq.load(config.tiktokPixelId); ttq.grantConsent(); ttq.page();
    }
  }
  const events = {
    product_view: ['ViewContent', 'ViewContent'],
    preorder_start: ['PreorderStart', 'PreorderStart'],
    preorder_submit: ['Lead', 'SubmitForm'],
    house_list_signup: ['CompleteRegistration', 'CompleteRegistration'],
    deposit_checkout: ['InitiateCheckout', 'InitiateCheckout'],
    contact: ['Contact', 'Contact'],
    film_engaged: ['FilmEngaged', 'FilmEngaged'],
    social_click: ['SocialClick', 'SocialClick']
  };
  const custom = new Set(['preorder_start', 'film_engaged', 'social_click']);
  function track(name, details, once) {
    if (!allowed || !enabled || !events[name]) return;
    const d = details || {}, token = once && name + ':' + once;
    if (token && seen.has(token)) return;
    if (token) seen.add(token);
    // Allow only product/activity fields. Never forward form data or full URLs.
    const data = {};
    ['content_name', 'content_type', 'mode', 'source', 'destination'].forEach(k => { if (typeof d[k] === 'string') data[k] = d[k]; });
    if (d.content_id) data.content_ids = [String(d.content_id)];
    if (name === 'deposit_checkout') { data.value = 100; data.currency = 'USD'; }
    try { if (config.metaPixelId) window.fbq(custom.has(name) ? 'trackCustom' : 'track', events[name][0], data); } catch (_) {}
    try {
      if (config.tiktokPixelId) {
        const tiktokData = { ...data };
        if (d.content_id) { tiktokData.content_id = String(d.content_id); delete tiktokData.content_ids; }
        window.ttq.track(events[name][1], tiktokData);
      }
    } catch (_) {}
  }
  window.momentiTrack = track;
  function choose(value) {
    save(value); allowed = value === 'granted';
    if (allowed) {
      if (!started) start();
      else {
        try { if (config.metaPixelId && window.fbq) window.fbq('consent', 'grant'); } catch (_) {}
        try { if (config.tiktokPixelId && window.ttq) window.ttq.grantConsent(); } catch (_) {}
      }
    }
    else {
      try { if (window.fbq) window.fbq('consent', 'revoke'); } catch (_) {}
      try { if (window.ttq) window.ttq.revokeConsent(); } catch (_) {}
    }
    const panel = document.getElementById('adConsent'); if (panel) panel.hidden = true;
  }
  window.momentiAdConsent = { set: choose, open: () => { const panel = document.getElementById('adConsent'); if (panel) panel.hidden = false; } };
  allowed = read() === 'granted';
  start();
  function ui() {
    if (!enabled) return;
    const style = document.createElement('style');
    style.textContent = '#adConsent{position:fixed;bottom:16px;left:16px;right:16px;max-width:520px;z-index:10000;background:#F2E8DD;color:#1A1511;padding:20px;border:1px solid #D9CCBC;font:14px/1.5 Arial,sans-serif;box-shadow:0 4px 24px #0002}#adConsent[hidden]{display:none}#adConsent p{margin:0 0 12px}#adConsent button{font:inherit;padding:8px 14px;margin-right:8px;background:transparent;color:inherit;border:1px solid currentColor;cursor:pointer}#adSettings{font:inherit;color:inherit;background:none;border:0;text-decoration:underline;cursor:pointer}';
    document.head.appendChild(style);
    const panel = document.createElement('section'); panel.id = 'adConsent'; panel.setAttribute('aria-label', 'Advertising preferences');
    const vendors = [config.metaPixelId && 'Meta', config.tiktokPixelId && 'TikTok'].filter(Boolean).join(' and ');
    panel.innerHTML = '<p>May we use ' + vendors + ' advertising cookies to measure visits and actions, improve our ads, and show relevant ads?</p><button type="button" data-choice="granted">Allow</button><button type="button" data-choice="denied">Decline</button>';
    panel.hidden = read() !== null;
    panel.querySelectorAll('button').forEach(b => b.addEventListener('click', () => choose(b.dataset.choice)));
    document.body.appendChild(panel);
    const button = document.createElement('button'); button.id = 'adSettings'; button.type = 'button'; button.textContent = 'Advertising preferences'; button.addEventListener('click', window.momentiAdConsent.open);
    (document.querySelector('footer') || document.body).appendChild(button);
    document.addEventListener('click', e => {
      const link = e.target.closest && e.target.closest('a'); if (!link) return;
      if (link.protocol === 'mailto:') track('contact', {source:'email'});
      if (['igLink','ttLink'].includes(link.id)) track('social_click', {destination:link.id === 'igLink' ? 'instagram' : 'tiktok'});
    });
    const film = document.getElementById('fv');
    if (film) film.addEventListener('timeupdate', () => { if (film.currentTime >= 5) track('film_engaged', {}, 'film'); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', ui); else ui();
})();
