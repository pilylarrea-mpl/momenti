# Momenti

The Momenti website: the Havana film, the title sequence, Collection I, The House, Client Services, pre-orders and the House List.

It's a static site (`index.html`, `img/`, `vid/`) plus two small Vercel functions in `api/`.

## Deploy on Vercel

1. vercel.com → **Add New → Project** → import `momenti` → **Deploy**. Leave every build setting on its default.
2. **Settings → Environment Variables**, then redeploy:
   - `RESEND_API_KEY`: from resend.com (free plan is fine).
   - `ORDER_EMAIL`: the inbox that receives every pre-order and House List sign-up.
   - `FROM_EMAIL` (optional): a sender on your own domain once it's verified in Resend, e.g. `Momenti <orders@yourdomain.com>`.
   - `RESEND_AUDIENCE_ID` (optional): a Resend audience, so House List sign-ups collect there for newsletters.
3. **Settings → Domains** to add your domain.

## Where pre-orders and sign-ups go

The simplest way: a Google Form with one Paragraph question. Get its pre-filled link (type `x` as the answer) and paste it into `GFORM_LINK` in `index.html`. Every pre-order and House List sign-up then arrives as a form response, and you can link the form to a Google Sheet.

The Resend setup above is optional once the Google Form is in.

## Edit the site

Near the top of the `<script>` in `index.html`:

- `HANDLE`, `INSTAGRAM`, `TIKTOK`, `CONTACT_EMAIL`
- `COLLECTION`: the collection name
- `FIRST_BATCH`: `'open'` takes $100 deposits for that bag, `'full'` shows the first batch as full
- `DEPOSIT_LINK`: a $100 Stripe Payment Link per bag, shown right after the pre-order form
- The `P` list holds every bag: name, price, description, images
