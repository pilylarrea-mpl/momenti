# Meta and TikTok conversions

Meta is configured in `js/tracking-config.js` with Momenti-owned Pixel ID
`1518737959611932`, connected to ad account `823415260132461`. Kaia's Pixel ID
`1458466688971757` must not be used for Momenti. TikTok remains inactive until its
public pixel ID is added later. No secret keys belong in this file.

## Activate

1. In Meta Events Manager, create a web data source / Meta Pixel (or open the
   existing dataset) and copy its Pixel ID. Choose manual installation because
   the site already contains the integration. Put it in `metaPixelId`.
2. In TikTok Ads Manager, open Events Manager, create a website data source / web
   pixel and choose manual installation. Copy the Pixel ID into `tiktokPixelId`.
   Labels may vary by account. Do not install a second copy through another tool.
3. Deploy the changes through the existing Vercel workflow. Pushing main deploys
   to production. These changes have not been pushed or deployed by setup.
4. In each platform's Test Events view, visit the deployed site, allow advertising
   cookies and exercise product views, form opens and submissions. Use an agreed
   test submission: a successful form sends data to the real studio Google Form
   and may send email. Invalid or failed submissions must not convert.
5. Verify event receipt and parameters in both platforms before spending money.
   For Meta choose website Leads with the Lead event as the main optimization
   event. For TikTok choose website lead generation / website conversions with
   SubmitForm where available. Account eligibility and event availability must be
   checked in Ads Manager. Create ads and budgets there; site code does not create
   or publish campaigns.

| Site action | Meta | TikTok | Role |
| --- | --- | --- | --- |
| Page load after consent | PageView | page() | Activity |
| Open a product detail | ViewContent | ViewContent | Interest |
| Open pre-order form | PreorderStart (custom) | PreorderStart (custom) | Interest |
| Successfully delivered pre-order | Lead | SubmitForm | **Main conversion** |
| Successful House List signup | CompleteRegistration | CompleteRegistration | Secondary conversion |
| Click configured deposit payment link | InitiateCheckout | InitiateCheckout | Checkout intent only |
| Click an email link | Contact | Contact | Contact intent |
| Watch at least 5 seconds of the film | FilmEngaged (custom) | FilmEngaged (custom) | Interest |
| Click Instagram or TikTok | SocialClick (custom) | SocialClick (custom) | Interest |

Pre-orders include priority_1 / priority_2 mode and product identifiers, not sales
revenue. Product and form-open events are limited to once per product/mode per
page visit; successful pre-orders are guarded against repeat callback execution.
House List events represent successful submissions, not verified unique people.

## Paid deposits: pending payment-provider connection

Payment links are sent manually and all on-site deposit URLs are currently blank.
There is no reliable payment-success signal in this repository. No Purchase event
is emitted. A pre-order, link click, redirect URL or displayed thank-you message
must not be counted as a paid deposit.

To track deposits, connect the payment provider's verified payment webhook or its
supported native Meta/TikTok conversion integration. The payment flow must retain
a reference to the pre-order and permitted ad attribution identifiers. Report only
confirmed payments, with an idempotent provider transaction/event ID, amount and
currency. This needs the chosen payment provider, its configuration and secure
credentials. Browser and server copies of a payment event must use the same event
ID for platform deduplication. Server-side Conversions API / Events API delivery
has not been added here.

## Visitor choice and scope

Pixels load only after a visitor allows advertising cookies; preferences can be
changed in the footer. Events before permission are discarded. Withdrawal stops
new event calls and invokes the vendors' consent-revocation methods. It does not
erase previously sent data. These custom event payloads allow only activity and
product fields and exclude form names, emails, phone numbers and addresses.
Vendor scripts still collect browser/device and page information under their own
settings. Avoid personal information in landing URLs and review automatic event
and advanced matching settings in both ad accounts to prevent unintended data
collection or duplicate conversions.

Keep changes to both `index.html` and `studio/source/momenti.html`: these pages
already diverged before this change. Do not regenerate the published index over
its existing design without reviewing the differences.

Local checks: `node --test tests/tracking.test.cjs` and
`python3 studio/scripts/build.py /tmp/momenti-built.html` from the repository root.
No live pixel receipt or ad attribution can be verified without IDs and deployment.
