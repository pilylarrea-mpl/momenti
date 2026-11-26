#!/bin/bash
h="$1"; D=/tmp/claude-0/-home-user-momenti/f8db058d-6b86-53e9-be25-77324683de3f/scratchpad/data/crawl
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
[ -s "$D/$h.done" ] && exit 0
curl -sL -m 40 -A "$UA" -o "$D/$h.home.html" "https://$h/" 
for p in 1 2 3 4 5 6 7 8; do
  code=$(curl -sL -m 60 -A "$UA" -o "$D/$h.$p.json" -w "%{http_code}" "https://$h/products.json?limit=250&page=$p")
  sz=$(stat -c%s "$D/$h.$p.json" 2>/dev/null || echo 0)
  if [ "$code" != "200" ] || [ "$sz" -lt 500 ]; then rm -f "$D/$h.$p.json"; break; fi
  head -c 12 "$D/$h.$p.json" | grep -q '{"products"' || { rm -f "$D/$h.$p.json"; break; }
done
echo "$code" > "$D/$h.done"
