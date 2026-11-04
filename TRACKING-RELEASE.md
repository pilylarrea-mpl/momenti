# Acquisition tracking release — 4 November 2026

Status: implemented and tested locally; NOT deployed. Branch fix/lead-attribution, commit ce1e548, based on origin/main 54d5a1a. Existing project verified: pramara2016-5492s-projects/momenti-site. Production staging was rejected by automatic approval review pending explicit website-release approval. No ad changes.

Changes: first/latest touch UTM fields and separate campaign/adset/ad identifiers captured on landing and included in successful Priority II and House List records. House List landing URL limit raised from 200 to 4096 characters. Untagged Instagram/referrer/fbclid evidence stays unknown; it never proves organic or paid. Direct revisits retain source in session; consent-granted return visits retain acquisition for at most 90 days. Shared same-email request guard prevents duplicate popup/footer submissions in one page. Meta Lead and CompleteRegistration remain separate, success-only, consent gated. No customer identifiers added to Meta payloads.

Classification is first-party link evidence, not Meta attribution or proof of incremental causality. Reports must show paid-tagged, organic-tagged, direct, and unknown separately; Meta-reported events in a separate column. Dedupe genuine contacts by normalized email within each form category, and separately across categories. Existing historical unknown sources cannot be retroactively recovered.

Organic profile destinations prepared (not live until release; profile links not yet changed):
- Instagram: https://www.houseofmomenti.com/instagram
- TikTok: https://www.houseofmomenti.com/tiktok
Each redirects to a platform-specific organic_social tagged landing. Story/collaboration links must use their own utm_content to preserve placement evidence. Existing four approved image ads already use paid_social and unique contents per recorded exact-ID audit; do not change live ad URLs without approval. Reverify every active ad URL before declaring full account coverage.

Validation: node --test tests/*.test.cjs, 13 passing. Includes navigation, paid vs organic, unknown social traffic, storage failure, consent/expiry, server classification, success-only pixel events, request deduplication. No real signup, email send, test lead, or payment generated. Live browser/API-to-Sheet verification remains after approved release. Do not claim CAPI or durable server idempotency implemented: current guard is page-level, and server-side delivery retries still need durable storage before safe implementation. No consent bypass.

Next: approve website release; stage production without domain switch, verify assets and non-mutating invalid-input responses, promote exact tested build; then verify tagged profile destinations and ask for/perform approved profile-link change. Coordinate reporting taxonomy with Momenti Desk. Broader CAPI requires consent-compatible design and event-ID deduplication; never silently send hashed contact data under existing policy that excludes contact fields.
