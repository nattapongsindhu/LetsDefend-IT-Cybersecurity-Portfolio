# 03 — Phishing and Email Headers

## The idea in one paragraph

A phishing investigation is mostly a question about trust: did this message really come from who it
claims, and did the user act on it? The header answers the first question, the logs answer the second.
Everything else — the pretty template, the urgent wording, the fake invoice — is context that helps me
explain the case to someone else, not proof.

## The fields I read first

| Field | What it tells me | Red flag example |
| :--- | :--- | :--- |
| From | The display name the user sees | A known brand with a misspelled domain |
| Return-Path | Where bounces go | Different domain from the From header |
| Reply-To | Where a reply actually lands | Free mail domain for a corporate message |
| Received | The chain of servers that touched it | A first hop that does not match the sender's brand |
| Authentication-Results | SPF, DKIM, DMARC outcome | All three failing, or no result at all |
| Message-ID | Where it was generated | A consumer mail host for an enterprise sender |

The header chain is read bottom-up: the last `Received` line is closest to the sender. When the chain does
not line up with the story in the body, I trust the chain.

## What makes me suspicious before I open anything

1. **Lookalike spelling.** Extra letters, doubled characters, a hyphen where the brand has none.
2. **Free mail for business mail.** A supplier using a consumer mailbox is unusual at scale.
3. **Pressure language.** "Urgent", "final notice", "account suspended" is designed to skip thinking.
4. **A password-protected archive.** The scanner cannot open it, so the file arrives untouched.
5. **A link and an attachment that resolve to the same thing.** Clicking or opening both lead to the same
   payload; blocking one is not enough.
6. **A business document that does not fit the relationship.** An invoice from a company we never bought
   from, an order sheet nobody requested.

## Attachments: what I check and why

| Type | Why it matters | What I look for |
| :--- | :--- | :--- |
| `.docm`, `.xlsm` | Macro-enabled by design | Macro present, auto-run entry point, child processes |
| `.zip`, `.rar` | Hides content from scanners | Password-protected, single file inside, unusual size |
| `.iso`, `.img` | Mounts as a disk | Autorun content, hidden executables |
| `.html` | Local page that can carry script | Credential form posting to an external host |
| `.lnk` | Shortcut with arguments | A command line with a remote path |

A macro document is not automatically malicious. The question is what the macro does: does it start a
script host, does it write a file, does it reach the network? A macro that formats a table is business as
usual. A macro that starts `cscript.exe` is not.

## Turning the mail into a case

The mail alone is not an incident. The incident begins when the user acts. So the next three questions
are always the same:

1. **Was the message delivered?** Device action on the mail row: allowed or blocked.
2. **Did anyone download the payload?** Proxy or web log, with the user name and process name.
3. **Did anything run?** Endpoint telemetry, or the firewall row showing the process talking out.

In the case I wrote up as evidence, the mail was allowed, the proxy showed a browser download from a file
hosting URL, and the firewall showed the dropped binary connecting to a hosting IP on a non-standard port.
Three sources, one sentence each, and the case was closed as a true positive.

## What I got wrong at first

I judged the mail by how it looked. A well-made lure with a clean layout and a real brand logo looked
"probably fine" to me, and an ugly plain-text mail looked suspicious. That is backwards: attackers
reuse professional templates, and internal systems send ugly plain mail every day. The header and the
logs do not care how the mail looks.

## Habits I keep

- Copy the header fields into the report before reading the body. It stops me from being led by the story.
- Check the sender domain against the brand by reading it character by character. My eyes skip doubled
  letters.
- Treat "allowed" as the interesting outcome.
- Write the user's action into the timeline with a timestamp. "The user clicked" is not evidence; "the
  user's browser fetched this URL at this time" is.
