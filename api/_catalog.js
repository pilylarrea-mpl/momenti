// Bag slugs and prices (USD), for tracking values. Keep in step with the piece pages.
// Old slugs from the first site map to the new pages.
const PRICES = { 'havana-1958': 520, 'miami-1959': 500, 'new-york-1977': 560, 'tokyo-1995': 580, 'monaco': 600 };
const NAMES = { 'havana-1958': 'Havana 1958', 'miami-1959': 'Miami 1959', 'new-york-1977': 'New York 1977', 'tokyo-1995': 'Tokyo 1995', 'monaco': 'Monaco' };
const OLD = { havana: 'havana-1958', miami: 'miami-1959', nyc: 'new-york-1977', tokyo: 'tokyo-1995', 'tokyo-1979': 'tokyo-1995' };
function slug(v) {
  const s = String(v || '').toLowerCase().split(':')[0].replace(/--optout$/, '');
  return PRICES[s] ? s : OLD[s] || null;
}
module.exports = { PRICES, NAMES, slug };
