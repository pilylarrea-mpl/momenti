/* MOMENTI · website proposal · motion and interactions */
(function () {
  'use strict';
  /* always start at the top of a page (Pily: the page jumped to the bottom on her phone) */
  try { if ('scrollRestoration' in history) history.scrollRestoration = 'manual'; } catch (e) {}
  if (!location.hash) { window.scrollTo(0, 0); window.addEventListener('load', function () { window.scrollTo(0, 0); }); }
  var d = document, html = d.documentElement, body = d.body;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia('(pointer: fine)').matches;
  var phone = function () { return window.innerWidth <= 760; };
  var $ = function (s, c) { return (c || d).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || d).querySelectorAll(s)); };
  var store = {
    get: function (k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { sessionStorage.setItem(k, v); } catch (e) {} }
  };

  /* The opening film. When the Runway film exists, put its files here; the site plays it once per visit
     and dissolves into the hero. Until then the no-film opening runs. */
  var FILM = { desktop: '', phone: '' };
  /* Stripe payment links per piece (Pily is creating them). Empty = preview state. */
  var STRIPE_LINK = 'https://buy.stripe.com/4gM3cw72Q8Mjfama0Pbo400'; /* Pily's reserve link, 18 Nov */
  var STRIPE = { 'havana-1958': STRIPE_LINK, 'miami-1959': STRIPE_LINK, 'new-york-1977': STRIPE_LINK, 'tokyo-1979': STRIPE_LINK, 'monaco': STRIPE_LINK };
  /* measurement (js/tracking.js, js/attribution.js, Vercel Analytics); ad pixels only fire after consent */
  function adTrack(n, d, once) { try { if (window.momentiTrack) window.momentiTrack(n, d, once); } catch (_) {} }
  function logStep(n) { try { var p = '/~/' + n; window.va('pageview', { route: p, path: p }); } catch (_) {} }
  (function () { var q = new URLSearchParams(location.search), ua = navigator.userAgent, src = (q.get('utm_source') || q.get('s') || (/Instagram/.test(ua) ? 'instagram' : /musical_ly|Bytedance|TikTok/i.test(ua) ? 'tiktok' : /FBAN|FBAV/.test(ua) ? 'facebook' : '')).toLowerCase().replace(/[^a-z0-9-]/g, '');
    try { if (src && !sessionStorage.getItem('m_from')) { sessionStorage.setItem('m_from', src); logStep('from/' + src); } } catch (_) {} })();
  function cameFrom() { var f = ''; try { f = sessionStorage.getItem('m_from') || ''; } catch (_) {} var ref = ''; try { ref = document.referrer ? new URL(document.referrer).hostname : ''; } catch (_) {}
    return { attribution: window.momentiAttribution ? window.momentiAttribution() : null, from: f || 'direct', ref: ref, landed: location.pathname + location.search }; }
  if (body.dataset.piece) { adTrack('product_view', { content_id: body.dataset.piece, content_type: 'product' }, body.dataset.piece); logStep('piece/' + body.dataset.piece); }
  /* send a sign-up to the House List backend (api/subscribe.js) */
  function send(email, topics) { var o = cameFrom(); o.email = email; o.topics = topics;
    return fetch('/api/subscribe', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(o) }).then(function (r) { if (r.ok) { logStep('house-list'); adTrack('house_list_signup', { source: topics[0] || 'house_list' }); } return r.ok; }).catch(function () { return false; }); }

  /* ---------- curtain + page transitions ---------- */
  function ready() { var go = function () { body.classList.add('ready'); }; requestAnimationFrame(go); setTimeout(go, 450); /* never leave the curtain down */ }
  window.addEventListener('pageshow', function (e) { if (e.persisted) { unlockAll(); body.classList.remove('leaving'); body.classList.add('ready'); } });
  /* one place that undoes every lock: menu, reserve sheet, smooth-scroll lock */
  function unlockAll() {
    var m = d.querySelector('.menu'); if (m) m.classList.remove('open');
    body.classList.remove('res-open');
    if (typeof sm !== 'undefined') sm.lock = false;
  }
  d.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a || a.target || e.metaKey || e.ctrlKey || e.shiftKey) return;
    var href = a.getAttribute('href');
    if (!href || href.charAt(0) === '#' || /^(mailto|tel|http)/.test(href)) return;
    if (a.dataset.arrive) store.set('arrive', a.dataset.arrive);
    var here = location.pathname.split('/').pop() || 'index.html';
    if (href.split('#')[0] === here && href.indexOf('#') > -1) return;
    e.preventDefault();
    /* a link to the page you're already on: close any menu or sheet and go to the top, never fade out */
    if (href.split('#')[0] === here) { unlockAll(); window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); return; }
    body.classList.add('leaving');
    setTimeout(function () { body.classList.remove('leaving'); }, 2500); /* never leave the curtain down */
    setTimeout(function () { location.href = href; }, reduce ? 0 : 360);
  });

  /* ---------- smooth wheel scrolling (desktop only) ---------- */
  var sm = { y: window.scrollY, t: window.scrollY, on: false, lock: false };
  if (fine && !reduce) {
    window.addEventListener('wheel', function (e) {
      if (sm.lock || e.ctrlKey || Math.abs(e.deltaX) > Math.abs(e.deltaY)) return;
      if (e.target.closest && e.target.closest('.sheet,.menu')) return;
      e.preventDefault();
      if (!sm.on) { sm.y = sm.t = window.scrollY; }
      var max = d.documentElement.scrollHeight - window.innerHeight;
      sm.t = Math.max(0, Math.min(max, sm.t + e.deltaY * (e.deltaMode === 1 ? 32 : 1)));
      if (!sm.on) { sm.on = true; requestAnimationFrame(step); }
    }, { passive: false });
  }
  function step() {
    sm.y += (sm.t - sm.y) * 0.11;
    if (Math.abs(sm.t - sm.y) < 0.5) { sm.y = sm.t; sm.on = false; }
    window.scrollTo(0, sm.y);
    if (sm.on) requestAnimationFrame(step);
  }

  /* ---------- reveals ---------- */
  html.classList.add('js');
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
  $$('.rv,.rv-img,.rv-lines').forEach(function (el) { io.observe(el); });

  /* ---------- nav: photo/solid/hide on scroll ---------- */
  var nav = $('.nav'), lastY = 0;
  function navState() {
    var y = window.scrollY;
    if (!nav) return;
    var dark = $$('[data-nav-photo]').some(function (s) { var r = s.getBoundingClientRect(); return r.top <= 30 && r.bottom > 40; });
    nav.classList.toggle('on-photo', dark && y > 0 ? true : dark);
    nav.classList.toggle('solid', y > 60 && !dark);
    nav.classList.toggle('hidden', y > 300 && y > lastY + 2 && !body.classList.contains('res-open'));
    if (y < lastY - 2) nav.classList.remove('hidden');
    lastY = y;
  }

  /* ---------- parallax (images and the line-up drift) ---------- */
  var par = $$('[data-par]');
  function parallax() {
    if (reduce) return;
    var vh = window.innerHeight;
    par.forEach(function (el) {
      if (phone() && el.dataset.parDesk) { el.style.transform = ''; return; }
      var r = el.parentElement.getBoundingClientRect();
      if (r.bottom < -200 || r.top > vh + 200) return;
      var k = parseFloat(el.dataset.par);
      var c = (r.top + r.height / 2 - vh / 2);
      el.style.transform = 'translate3d(0,' + (c * k).toFixed(1) + 'px,0)';
    });
  }
  var ticking = false;
  window.addEventListener('scroll', function () {
    if (!ticking) { ticking = true; requestAnimationFrame(function () { navState(); parallax(); ticking = false; }); }
  }, { passive: true });
  window.addEventListener('resize', parallax);

  /* ---------- menu ---------- */
  var menu = $('.menu');
  $$('[data-menu]').forEach(function (b) {
    b.addEventListener('click', function (e) { e.preventDefault(); if (!menu) return; menu.classList.toggle('open'); sm.lock = menu.classList.contains('open') || body.classList.contains('res-open'); });
  });
  $$('.menu [data-pic]').forEach(function (a) {
    a.addEventListener('mouseenter', function () {
      $$('.menu .pic img').forEach(function (i) { i.classList.toggle('on', i.dataset.k === a.dataset.pic); });
    });
  });
  d.addEventListener('keydown', function (e) { if (e.key === 'Escape') { if (menu) menu.classList.remove('open'); sm.lock = false; closeSheet(); } });

  /* ---------- email forms (front-end preview) ---------- */
  $$('form.join').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var v = f.querySelector('input').value;
      if (!/.+@.+\..+/.test(v)) { f.querySelector('input').value = ''; f.querySelector('input').placeholder = 'That email doesn’t look right.'; return; }
      var inHouse = /join/.test(location.pathname);
      send(v, [inHouse ? 'the house' : 'the letter']).then(function (ok) { if (ok) f.classList.add('ok'); else { f.querySelector('input').value = ''; f.querySelector('input').placeholder = 'Something went wrong. Try again?'; } });
    });
  });

  /* the House forms (your moment, joining): front-end preview, nothing is sent */
  $$('form.nom').forEach(function (f) {
    var file = $('input[type=file]', f), fake = $('.fake', f);
    if (file && fake) file.addEventListener('change', function () { if (file.files[0]) fake.textContent = file.files[0].name; });
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var em = $('input[type=email]', f);
      if (!/.+@.+\..+/.test(em.value)) { em.value = ''; em.placeholder = 'That email doesn’t look right.'; em.focus(); return; }
      var parts = Array.prototype.slice.call(f.querySelectorAll('input:not([type=email]):not([type=file]), textarea')).map(function (x) { return (x.getAttribute('name') || x.getAttribute('placeholder') || '') + ': ' + x.value; }).filter(function (t) { return !/: $/.test(t); }).join(' | ').slice(0, 900);
      send(em.value, ['the house', parts ? 'moment · ' + parts : 'joined']).then(function (ok) { if (ok) f.classList.add('ok'); else { em.value = ''; em.placeholder = 'Something went wrong. Try again?'; } });
    });
  });

  /* ---------- accordions ---------- */
  $$('.acc .h').forEach(function (h) {
    h.addEventListener('click', function () { h.parentElement.classList.toggle('open'); h.setAttribute('aria-expanded', h.parentElement.classList.contains('open')); });
  });

  /* ---------- the Grand Tour line-up (home strip + The Grand Tour page): floating bags, drag with inertia ---------- */
  var tw = $('.track-wrap');
  if (tw && fine) {
    var tr = $('.track', tw), cards = $$('.card,.flt', tr), barI = $('.drag-bar i'), cnt = $('.drag-bar .count');
    var x = 0, tx = 0, v = 0, down = false, sx = 0, sxx = 0, moved = 0, lastX = 0;
    var lagK = [0, 0.9, 0.35, 1.25, 0.6], lags = [0, 0, 0, 0, 0], px = 0;
    function maxX() { return Math.max(0, tr.scrollWidth - tw.clientWidth); }
    function render() {
      x += (tx - x) * 0.12;
      tr.style.transform = 'translate3d(' + (-x).toFixed(1) + 'px,0,0)';
      var vel = x - px; px = x;
      if (!reduce) cards.forEach(function (c, i) { var t = Math.max(-18, Math.min(18, vel * lagK[i % 5] * 1.6)); lags[i] += (t - lags[i]) * 0.12; c.style.transform = 'translate3d(' + lags[i].toFixed(1) + 'px,0,0)'; });
      var m = maxX(), p = m ? x / m : 0;
      if (barI) barI.style.left = (p * 80) + '%';
      if (cnt) cnt.textContent = '0' + Math.min(5, Math.round(p * 4) + 1) + ' / 05';
      requestAnimationFrame(render);
    }
    requestAnimationFrame(render);
    tw.addEventListener('pointerdown', function (e) { down = true; moved = 0; sx = e.clientX; sxx = tx; lastX = e.clientX; v = 0; tw.classList.add('drag'); });
    window.addEventListener('pointermove', function (e) {
      if (!down) return;
      moved = Math.max(moved, Math.abs(e.clientX - sx));
      v = lastX - e.clientX; lastX = e.clientX;
      tx = Math.max(-60, Math.min(maxX() + 60, sxx - (e.clientX - sx)));
    });
    window.addEventListener('pointerup', function () {
      if (!down) return; down = false; tw.classList.remove('drag');
      tx = Math.max(0, Math.min(maxX(), tx + v * 14));
    });
    tw.addEventListener('click', function (e) { if (moved > 6) { e.preventDefault(); e.stopPropagation(); } }, true);
    tw.addEventListener('dragstart', function (e) { e.preventDefault(); });
    tw.addEventListener('wheel', function (e) {
      if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) { e.preventDefault(); tx = Math.max(0, Math.min(maxX(), tx + e.deltaX)); }
    }, { passive: false });
  } else if (tw) {
    var dl = $('.drag-bar .lab'); if (dl && dl.textContent === 'Drag') dl.textContent = 'Swipe';
    var bi = $('.drag-bar i'), ct = $('.drag-bar .count');
    tw.addEventListener('scroll', function () {
      var m = tw.scrollWidth - tw.clientWidth, p = m ? tw.scrollLeft / m : 0;
      if (bi) bi.style.left = (p * 80) + '%';
      if (ct) ct.textContent = '0' + Math.min(5, Math.round(p * 4) + 1) + ' / 05';
    }, { passive: true });
  }

  /* ---------- piece gallery dots (phone) ---------- */
  var gal = $('.gal');
  if (gal) {
    var dots = $$('.dots i');
    gal.addEventListener('scroll', function () {
      var i = Math.round(gal.scrollLeft / gal.clientWidth);
      dots.forEach(function (dd, k) { dd.classList.toggle('on', k === i); });
    }, { passive: true });
  }

  /* ---------- reserve sheet ---------- */
  var sheet = $('.sheet');
  function openSheet(e) {
    if (!sheet) return; /* no sheet on this page: let the link do its normal thing, lock nothing */
    if (e) e.preventDefault();
    if (menu) menu.classList.remove('open');
    body.classList.add('res-open'); sm.lock = true;
    if (nav) nav.classList.remove('hidden');
    var pc = body.dataset.piece; if (pc) { adTrack('preorder_start', { content_id: pc, content_type: 'product', mode: 'reserve' }, pc); logStep('reserve/' + pc); }
  }
  function closeSheet() { body.classList.remove('res-open'); sm.lock = !!(menu && menu.classList.contains('open')); }
  $$('[data-reserve]').forEach(function (b) { b.addEventListener('click', openSheet); });
  $$('[data-close], .veil').forEach(function (b) { b.addEventListener('click', closeSheet); });
  if (sheet) {
    var hold = $('[data-hold]', sheet);
    if (hold) hold.addEventListener('click', function (e) {
      e.preventDefault();
      var link = STRIPE[body.dataset.piece];
      adTrack('preorder_submit', { content_id: body.dataset.piece, content_type: 'product', mode: 'reserve' }); logStep('reserve-link/' + body.dataset.piece);
      if (link) { location.href = link + (link.indexOf('?') < 0 ? '?' : '&') + 'client_reference_id=' + encodeURIComponent(body.dataset.piece); return; }
      sheet.classList.add('done');
    });
    var alt = $('.alt', sheet);
    var tell = $('[data-tell]', sheet);
    if (tell) tell.addEventListener('click', function (e) { e.preventDefault(); alt.classList.add('asking'); var i = $('input', alt); if (i) i.focus(); });
    var tf = $('form', alt);
    if (tf) tf.addEventListener('submit', function (e) { e.preventDefault(); var ti = tf.querySelector('input'); if (ti && /.+@.+\..+/.test(ti.value)) send(ti.value, ['back: ' + body.dataset.piece]); alt.classList.remove('asking'); alt.classList.add('ok'); $('.tell-txt', alt).innerHTML = '<span class="it" style="font-size:18px">Done. You’ll hear when it’s back, and not before.</span>'; $('.tell-txt', alt).style.display = 'block'; });
    if (location.hash === '#reserve') setTimeout(openSheet, 500);
  }

  /* ---------- the signature: the car finds its clasp ----------
     The photograph fills the screen, the camera pushes in on its car, a match cut lands on the
     same car sitting on the clasp, and the camera pulls back to the bag in the gallery. */
  function arrival() {
    var a = window.ARRIVE, slug = body.dataset.piece;
    var want = store.get('arrive') === slug || /[?&]arrive/.test(location.search);
    store.set('arrive', '');
    if (!a || !want || reduce) return false;
    var target = $('.gal .a');
    if (!target) return false;
    window.scrollTo(0, 0);
    var vw = window.innerWidth, vh = window.innerHeight;
    var ov = d.createElement('div'); ov.className = 'arrive';
    var rA = a.printH / a.printW, rB = 1396 / 2000;
    // A: the photograph, covering the screen
    var bw = vw, bh = vw * rA; if (bh < vh) { bh = vh; bw = vh / rA; }
    var bx = (vw - bw) / 2, by = (vh - bh) / 2;
    var A = d.createElement('div'); A.className = 'box';
    A.style.cssText = 'left:' + bx + 'px;top:' + by + 'px;width:' + bw + 'px;height:' + bh + 'px;opacity:0';
    A.innerHTML = '<img src="' + a.print + '" alt="">';
    // B: the bag, at its final place in the gallery
    var r = target.getBoundingClientRect();
    var B = d.createElement('div'); B.className = 'box';
    B.style.cssText = 'left:' + r.left + 'px;top:' + r.top + 'px;width:' + r.width + 'px;height:' + r.height + 'px;opacity:0';
    B.innerHTML = '<img src="' + a.master + '" alt="">';
    ov.appendChild(A); ov.appendChild(B); body.appendChild(ov);
    // push in on the photograph's car (the photograph keeps covering the screen)
    var c = a.car, k = a.clasp;
    var z = phone() ? 2.1 : 2.3;
    var WA = bw * z, HA = bh * z;
    var ccx = (c[0] + c[2]) / 2, ccy = (c[1] + c[3]) / 2;
    var L = vw / 2 - ccx * WA, T = vh * 0.52 - ccy * HA;
    L = Math.min(0, Math.max(vw - WA, L)); T = Math.min(0, Math.max(vh - HA, T));
    var zA = 'translate3d(' + (L - bx) + 'px,' + (T - by) + 'px,0) scale(' + z + ')';
    var cx = L + ccx * WA, cy = L === L ? T + ccy * HA : 0, tw = (c[2] - c[0]) * WA;
    // the bag, zoomed so its clasp car sits exactly where the street car was
    var WB = tw / (k[2] - k[0]), HB = WB * rB;
    var zB = 'translate3d(' + (cx - (k[0] + k[2]) / 2 * WB - r.left) + 'px,' + (cy - (k[1] + k[3]) / 2 * HB - r.top) + 'px,0) scale(' + (WB / r.width) + ')';
    B.style.transform = zB;
    var go = function (el, tf, dur, ease) { el.style.transition = 'transform ' + dur + 'ms ' + (ease || 'cubic-bezier(.22,.61,.12,1)') + ',opacity 420ms ease'; if (tf !== null) el.style.transform = tf; };
    requestAnimationFrame(function () { go(A, null, 0); A.style.opacity = 1; });
    setTimeout(function () { go(A, zA, 1300, 'cubic-bezier(.55,.05,.35,1)'); }, 450);          // the push-in
    setTimeout(function () { go(B, null, 0); B.style.opacity = 1; }, 1650);                     // the match cut
    setTimeout(function () { A.style.opacity = 0; go(B, 'none', 1250); }, 2050);                  // the pull-back
    setTimeout(function () { ov.style.background = 'transparent'; ov.classList.add('fade'); }, 3250);
    setTimeout(function () { ov.remove(); }, 3800);
    return true;
  }

  /* ---------- home opening (no-film fallback; the film slot is ready) ---------- */
  function opening() {
    var op = $('.opening');
    if (!op) return;
    var seen = store.get('opened');
    if (seen || reduce) { op.remove(); body.classList.remove('pre'); return; }
    store.set('opened', '1');
    var src = phone() ? FILM.phone : FILM.desktop;
    if (src) {
      var f = $('.film'); f.style.display = 'block';
      var vid = f.querySelector('video'); vid.src = src; vid.play();
      vid.addEventListener('ended', function () { f.style.transition = 'opacity .9s'; f.style.opacity = 0; setTimeout(function () { f.remove(); }, 900); });
      op.remove(); body.classList.remove('pre');
      return;
    }
    setTimeout(function () { op.classList.add('show'); }, 150);
    setTimeout(function () { op.classList.add('gone'); body.classList.remove('pre'); }, 1250);
    setTimeout(function () { op.remove(); }, 2300);
  }

  /* ---------- go ---------- */
  ready();
  if (body.classList.contains('home')) {
    var first = !store.get('opened') && !reduce;
    if (!first) body.classList.remove('pre');
    opening();
    var h = $('.hero .rv-lines'); if (h) setTimeout(function () { h.classList.add('in'); }, first ? 1500 : 300);
  }
  arrival();
  navState(); parallax();
})();
