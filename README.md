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

Both forms post to the site's own functions (`api/preorder`, `api/subscribe`), which deliver each submission to:

1. **The Google Form** in `api/_gform.js` (one Paragraph question). To swap forms, get its pre-filled link (type `x` as the answer) and paste it into `GFORM_LINK` there. Link the form to a Google Sheet, and turn on email notifications in its Responses tab.
2. **Email via Resend**, when `RESEND_API_KEY` and `ORDER_EMAIL` are set (see above).

The site only tells a customer "received" when at least one of these really took it. Otherwise it shows them a message to copy and send to you, so nothing is lost silently.

The Google Form must be open to anyone: in **Publish** settings, responders must be "Anyone with the link", and in **Settings → Responses** there must be no sign-in, no verified email collection and no one-response limit. A form that requires sign-in rejects every submission.

## Edit the site

Near the top of the `<script>` in `index.html`:

- `HANDLE`, `INSTAGRAM`, `TIKTOK`, `CONTACT_EMAIL`
- `COLLECTION`: the collection name
- `FIRST_BATCH`: `'open'` takes $100 deposits for that bag, `'full'` shows the first batch as full
- `DEPOSIT_LINK`: a $100 Stripe Payment Link per bag, shown right after the pre-order form
- The `P` list holds every bag: name, price, description, images
