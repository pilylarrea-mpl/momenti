/* First-party acquisition evidence. A social browser or fbclid alone is not proof of an ad. */
(function () {
  'use strict';
  const key = 'momenti_acquisition_v1';
  const fields = ['utm_source','utm_medium','utm_campaign','utm_content','utm_term','campaign_id','adset_id','ad_id'];
  const q = new URLSearchParams(location.search), touch = {at:new Date().toISOString()};
  fields.forEach(k => { const v=q.get(k); if(v) touch[k]=v.slice(0,200); });
  try { touch.referrer = document.referrer ? new URL(document.referrer).hostname : ''; } catch (_) { touch.referrer=''; }
  touch.social_click = q.has('fbclid');
  const medium=(touch.utm_medium||'').toLowerCase();
  touch.channel = /^(paid|paid_social|cpc|ppc|paid-social)$/.test(medium) ? 'paid_social' : /^(organic|organic_social|social_organic)$/.test(medium) ? 'organic_social' : (touch.utm_source || touch.referrer || touch.social_click || /Instagram|FBAN|FBAV|TikTok/i.test(navigator.userAgent)) ? 'unknown' : 'direct';
  touch.evidence = touch.utm_medium ? 'tagged_link' : touch.social_click ? 'social_click_only' : touch.referrer ? 'referrer_only' : 'none';
  let saved={};
  try { saved=JSON.parse(sessionStorage.getItem(key)||'{}'); } catch (_) {}
  // Only retain acquisition across sessions after advertising consent.
  let consent=false;
  try { consent=localStorage.getItem('momenti_ad_consent_v1')==='granted';
    if(consent && !saved.first) { const old=JSON.parse(localStorage.getItem(key)||'{}');
      if(old.first && Date.now()-Date.parse(old.first.at)<90*86400000) saved=old;
    }
  } catch (_) {}
  if(!saved.first) saved.first=touch;
  if(touch.utm_source || touch.utm_medium || touch.referrer || touch.social_click || !saved.last) saved.last=touch;
  try { sessionStorage.setItem(key,JSON.stringify(saved)); } catch (_) {}
  window.momentiAttribution = () => {
    try { if(localStorage.getItem('momenti_ad_consent_v1')==='granted') localStorage.setItem(key,JSON.stringify(saved));
      else localStorage.removeItem(key); } catch (_) {}
    return {version:1,first:saved.first,last:saved.last};
  };
  window.momentiAttribution();
})();
