# Canadian recognizers

Pattern recognizers for Canadian personally identifying information. They plug
into the standard Presidio analyzer like any other predefined recognizer and
are meant for de-identification workflows under PIPEDA and Quebec Law 25.

## Recognizers

### CaSinRecognizer — `CA_SIN`

Canadian Social Insurance Number.

Accepted formats:

- `046 454 286` (groups of 3 separated by spaces)
- `046-454-286` (groups of 3 separated by hyphens)
- `046454286` (plain 9 digits)

Grouped forms must use the same separator in both gaps. Every candidate is
checked with the Luhn (Modulus 10) checksum; values that fail the checksum
are discarded, which keeps ordinary 9-digit strings from matching.

Context words: `sin`, `social insurance`, `social insurance number`,
`canada`, plus French equivalents (`nas`, `numéro d'assurance sociale`).

### CaOhipRecognizer — `CA_OHIP`

Ontario Health Insurance Plan health card number: 10 digits followed by a
2-letter version code.

Accepted formats:

- `1234567890 AB` (digits, optional space, version code)
- `1234567890AB` (no space)
- `1234-567-890-AB` (grouped 4-3-3 with hyphens, then version code)

There is no public checksum for OHIP numbers, so detection relies on the
shape of the value plus context words (`ohip`, `health card`,
`version code`, `carte santé`, and others) to raise confidence.

### CaPostalCodeRecognizer — `CA_POSTAL_CODE`

Canadian postal code in FSA + LDU format (`K1A 0B1`). Matching is
case-insensitive, so `k1a0b1` also matches.

Accepted formats:

- `K1A 0B1` (canonical, with space)
- `K1A0B1` (no space, weaker score since the shape is more collision-prone)

The forward sortation area is validated: the first letter must be one of
`ABCEGHJ-NPRSTVXY`, and the letters D, F, I, O, Q, U are never valid in any
letter position. Values like US ZIP codes (`90210`) do not match.

Context words: `postal code`, `postcode`, `zip`, province names, and the
French `code postal`.

## Enabling

These recognizers are registered as predefined country-specific recognizers
(`country_code: ca`) and are disabled by default in
`presidio_analyzer/conf/default_recognizers.yaml`. To use them, instantiate
the classes directly or enable them in your registry configuration.

## Try it in the browser

A client-side demo that mirrors these patterns (SIN with Luhn, OHIP, postal
codes, plus credit cards, phone numbers, and emails) is live as the
[Canadian PII Redaction Sandbox](https://movahedi.ca/tools/pii-redactor/).
Everything runs in the visitor's browser: no backend, no storage, no network
calls.
