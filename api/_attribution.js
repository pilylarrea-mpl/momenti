// Strictly bounded acquisition fields; never trust a client-supplied source as platform attribution.
const keys=['at','utm_source','utm_medium','utm_campaign','utm_content','utm_term','campaign_id','adset_id','ad_id','referrer','evidence'];
module.exports = value => {
  if(!value || value.version!==1) return 'Acquisition: unknown (legacy submission)';
  const clean = t => {
    if(!t || typeof t!=='object') return null;
    const out={};
    keys.forEach(k=>{if(typeof t[k]==='string') out[k]=t[k].replace(/[\r\n]/g,' ').slice(0,200);});
    const m=(out.utm_medium||'').toLowerCase();
    out.channel=/^(paid|paid_social|cpc|ppc|paid-social)$/.test(m)?'paid_social':/^(organic|organic_social|social_organic)$/.test(m)?'organic_social':t.channel==='direct'&&!out.utm_source&&!out.referrer&&!t.social_click?'direct':'unknown';
    out.social_click=t.social_click===true;
    return out;
  };
  return 'Acquisition evidence: '+JSON.stringify({version:1,first:clean(value.first),last:clean(value.last)});
};
