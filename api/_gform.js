// Sends one answer to the Google Form that collects pre-orders and House List sign-ups.
// Paste the form's pre-filled link here (Get pre-filled link, type x in the answer, Copy link).
// The form must be open to anyone: no sign-in, no verified emails, no one-response limit.
const GFORM_LINK = 'https://docs.google.com/forms/d/e/1FAIpQLSeONbYOnSwdN1Uki36nq-w7KDfATfEsdxRLsXfywLD4ObGAkA/viewform?usp=pp_url&entry.1860604233=x';

module.exports = async function toGoogle(text) {
  const m = GFORM_LINK.match(/forms\/d\/e\/([^/]+)\/viewform.*?[?&](entry\.\d+)=/);
  if (!m) return false;
  try {
    const r = await fetch(`https://docs.google.com/forms/d/e/${m[1]}/formResponse`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ [m[2]]: text }).toString(),
    });
    // Google answers 200 only when the response is recorded; a sign-in wall answers 401.
    if (!r.ok) console.error('Google Form refused the response:', r.status);
    return r.ok;
  } catch (e) {
    console.error('Google Form unreachable:', e);
    return false;
  }
};
