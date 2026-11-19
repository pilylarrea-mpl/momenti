(function () {
  'use strict';
  const config = window.MOMENTI_TRACKING || {};
  // 'opt-out' (the new site, Pily 18 Nov): no pop-up; tracking runs unless the visitor declines under Advertising preferences.
  const optOut = window.MOMENTI_CONSENT_MODE === 'opt-out' || config.consent === 'opt-out';
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
      const pv = newId();
      window.fbq('track', 'PageView', {}, { eventID: pv });
      relay('PageView', pv, {});
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
  // Site action -> [Meta event, TikTok event]. Meta standard events where one fits; custom only where none does.
  const events = {
    page_view: ['PageView', ''],                                          // server copy of the PageView sent at start
    product_view: ['ViewContent', 'ViewContent'],                         // a bag page: content_ids = slug, value = price
    preorder_start: ['PreorderStart', 'PreorderStart'],                   // opened the Reserve sheet (sees the price)
    checkout_start: ['InitiateCheckout', 'InitiateCheckout'],             // "Reserve mine": leaving for Stripe
    checkout_cancel: ['CheckoutCancel', 'CheckoutCancel'],                // came back from Stripe without finishing
    card_saved: ['AddPaymentInfo', 'AddPaymentInfo'],                     // Stripe confirmed (server-checked)
    reservation_complete: ['CompleteRegistration', 'CompleteRegistration'], // Stripe confirmed (server-checked)
    purchase: ['Purchase', 'CompletePayment'],                            // only if Stripe really charged money
    lead: ['Lead', 'SubmitForm'],                                         // any email sign-up that the server accepted
    contact: ['Contact', 'Contact'],
    film_engaged: ['FilmEngaged', 'FilmEngaged'],
    social_click: ['SocialClick', 'SocialClick'],
    outbound_click: ['OutboundClick', 'OutboundClick'],
    scroll_depth: ['ScrollDepth', 'ScrollDepth'],
    // older names, kept so older pages keep working
    house_list_signup: ['Lead', 'SubmitForm'],
    preorder_submit: ['Lead', 'SubmitForm'],
    deposit_checkout: ['InitiateCheckout', 'InitiateCheckout']
  };
  const custom = new Set(['preorder_start', 'checkout_cancel', 'film_engaged', 'social_click', 'outbound_click', 'scroll_depth']);
  // Only sent when the server has confirmed them with Stripe (the event ID is the Checkout Session ID).
  const verified = new Set(['card_saved', 'reservation_complete', 'purchase']);
  // Sent to the Conversions API through /api/track with the same event ID. Lead and the Stripe events
  // get their server copy from api/subscribe and api/stripe-confirm / api/stripe-webhook instead.
  const relayed = new Set(['page_view', 'product_view', 'preorder_start', 'checkout_start', 'checkout_cancel', 'contact', 'social_click']);
  // Only these carry a money value (the bag price, or what Stripe really charged); sign-ups never do.
  const valued = new Set(['product_view', 'preorder_start', 'checkout_start', 'card_saved', 'reservation_complete', 'purchase']);
  function newId() {
    try { if (window.crypto && window.crypto.randomUUID) return window.crypto.randomUUID(); } catch (_) {}
    return Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 12);
  }
  function cookie(name) {
    try { const m = document.cookie.match(new RegExp('(?:^|; )' + name + '=([^;]*)')); return m ? decodeURIComponent(m[1]) : undefined; } catch (_) { return undefined; }
  }
  function ids() {
    let fbc = cookie('_fbc');
    try { const c = new URLSearchParams(location.search).get('fbclid'); if (!fbc && c) fbc = 'fb.1.' + Date.now() + '.' + c; } catch (_) {}
    let url; try { url = location.origin + location.pathname; } catch (_) {}
    return { fbp: cookie('_fbp'), fbc: fbc, url: url };
  }
  // What the server needs to send its copy of an event; null when ad tracking is off.
  window.momentiMeta = function (eventId) { if (!allowed || !enabled || !config.metaPixelId) return null; const o = ids(); o.event_id = eventId; return o; };
  window.momentiEventId = newId;
  function relay(eventName, eventId, data) {
    if (!config.metaPixelId) return;
    const o = ids();
    const body = JSON.stringify({ event_name: eventName, event_id: eventId, data: data, fbp: o.fbp, fbc: o.fbc, url: o.url });
    try {
      if (navigator.sendBeacon && navigator.sendBeacon('/api/track', new Blob([body], { type: 'text/plain' }))) return;
    } catch (_) {}
    try { fetch('/api/track', { method: 'POST', headers: { 'Content-Type': 'text/plain' }, body: body, keepalive: true }).catch(function () {}); } catch (_) {}
  }
  function track(name, details, once) {
    if (!allowed || !enabled || !events[name]) return null;
    const d = details || {}, token = once && name + ':' + once;
    if (verified.has(name) && !/^cs_[A-Za-z0-9_]+$/.test(String(d.event_id || ''))) return null;
    if (token && seen.has(token)) return null;
    if (token) seen.add(token);
    // Allow only product/activity fields. Never forward form data, emails or full URLs from the browser.
    const data = {};
    ['content_name', 'content_type', 'content_category', 'mode', 'source', 'destination', 'status'].forEach(k => { if (typeof d[k] === 'string') data[k] = d[k].slice(0, 80); });
    if (d.content_id) data.content_ids = [String(d.content_id)];
    if (valued.has(name) && typeof d.value === 'number' && isFinite(d.value)) { data.value = d.value; data.currency = typeof d.currency === 'string' ? d.currency : 'USD'; }
    if (typeof d.bag_price === 'number') data.bag_price = d.bag_price;
    if (typeof d.percent === 'number') data.percent = d.percent;
    if (name === 'deposit_checkout') { data.value = 100; data.currency = 'USD'; }
    const eventId = typeof d.event_id === 'string' && d.event_id ? d.event_id : newId();
    try { if (config.metaPixelId) window.fbq(custom.has(name) ? 'trackCustom' : 'track', events[name][0], data, { eventID: eventId }); } catch (_) {}
    if (relayed.has(name) && d.server !== false) relay(events[name][0], eventId, data);
    try {
      if (config.tiktokPixelId && events[name][1]) {
        const tiktokData = { ...data };
        if (d.content_id) { tiktokData.content_id = String(d.content_id); delete tiktokData.content_ids; }
        window.ttq.track(events[name][1], tiktokData, { event_id: eventId });
      }
    } catch (_) {}
    return eventId;
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
  allowed = optOut ? read() !== 'denied' : read() === 'granted';
  start();
  function ui() {
    if (!enabled) return;
    const style = document.createElement('style');
    style.textContent = '#adConsent{position:fixed;bottom:16px;left:16px;right:16px;max-width:520px;z-index:10000;background:#F2E8DD;color:#1A1511;padding:20px;border:1px solid #D9CCBC;font:14px/1.5 Arial,sans-serif;box-shadow:0 4px 24px #0002}#adConsent[hidden]{display:none}#adConsent p{margin:0 0 12px}#adConsent button{font:inherit;padding:8px 14px;margin-right:8px;background:transparent;color:inherit;border:1px solid currentColor;cursor:pointer}#adSettings{font:inherit;color:inherit;background:none;border:0;text-decoration:underline;cursor:pointer}';
    document.head.appendChild(style);
    const panel = document.createElement('section'); panel.id = 'adConsent'; panel.setAttribute('aria-label', 'Advertising preferences');
    const vendors = [config.metaPixelId && 'Meta', config.tiktokPixelId && 'TikTok'].filter(Boolean).join(' and ');
    panel.innerHTML = '<p>May we use ' + vendors + ' advertising cookies to measure visits and actions, improve our ads, and show relevant ads?</p><button type="button" data-choice="granted">Allow</button><button type="button" data-choice="denied">Decline</button>';
    panel.hidden = optOut || read() !== null;
    panel.querySelectorAll('button').forEach(b => b.addEventListener('click', () => choose(b.dataset.choice)));
    document.body.appendChild(panel);
    const button = document.createElement('button'); button.id = 'adSettings'; button.type = 'button'; button.textContent = 'Advertising preferences'; button.addEventListener('click', window.momentiAdConsent.open);
    (document.querySelector('footer') || document.body).appendChild(button);
    document.addEventListener('click', e => {
      const link = e.target.closest && e.target.closest('a'); if (!link) return;
      if (link.protocol === 'mailto:') { track('contact', {source: 'email'}); return; }
      const host = String(link.hostname || '').replace(/^www\./, '');
      if (['igLink','ttLink'].includes(link.id) || /(^|\.)(instagram|tiktok)\.com$/.test(host)) {
        track('social_click', {destination: link.id === 'igLink' || /instagram/.test(host) ? 'instagram' : 'tiktok'}); return;
      }
      // Stripe links are tracked as InitiateCheckout by the page itself.
      if (/^https?:$/.test(link.protocol) && host && host !== location.hostname.replace(/^www\./, '') && !/(^|\.)stripe\.com$/.test(host)) track('outbound_click', {destination: host});
    });
    const film = document.getElementById('fv') || document.querySelector('.film video');
    if (film) film.addEventListener('timeupdate', () => { if (film.currentTime >= 5) track('film_engaged', {}, 'film'); });
    // How far down the page people read: once each at 50% and 90%.
    let ticking = false;
    window.addEventListener('scroll', () => {
      if (ticking) return; ticking = true;
      requestAnimationFrame(() => {
        ticking = false;
        const h = document.documentElement, max = h.scrollHeight - window.innerHeight;
        if (max < 400) return;
        const pct = (window.scrollY / max) * 100;
        [50, 90].forEach(p => { if (pct >= p) track('scroll_depth', {percent: p, content_category: location.pathname.replace(/^\/|\.html$/g, '') || 'home'}, 'scroll' + p); });
      });
    }, {passive: true});
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', ui); else ui();
})();
