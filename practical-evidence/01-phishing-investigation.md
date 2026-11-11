# 01 — Phishing Investigation (Mail Lure to Stealer C2)

**Type:** live alert case · **Platform:** LetsDefend · **Verdict:** True Positive
**Skills:** email header analysis, log correlation, IOC extraction, containment planning

---

## Context

A mail reached a user's mailbox with the subject *Free Coffee Voucher*. It carried a password-protected
zip and a "Redeem Now" link. The mail filter allowed it through. The alert asked a simple question: was
this a real threat, and did anything happen after delivery?

## What I did

1. Read the alert fields: sender, recipient, subject, sender IP, and the device action.
2. Opened the message in the mail console to check the body, the link, and the attachment.
3. Compared the link target and the attachment name. Both pointed at the same file on a public object
   store.
4. Searched the proxy and firewall logs for the recipient's host address.
5. Traced the process that downloaded the file and the process that made the outbound connection.
6. Wrote the verdict, the recommended actions, and the limits into the case note.

## Evidence

| Source | What it showed |
| :--- | :--- |
| Mail gateway | Message delivered from a lookalike domain through a relay IP, action **allowed** |
| Proxy | The user's browser fetched the archive from an object-storage URL |
| Firewall | The dropped binary opened a TCP session to a hosting IP on a non-standard port |
| Endpoint | The dropped binary had several shell children, far more than the application needed |

The mail was the delivery. The proxy row was the download. The firewall row was the compromise. Three
sources, three sentences, one conclusion.

## Result

**True positive.** The chain was: phishing mail, password-protected archive, user execution, malware
beacon to an external host. The case was closed with a written note covering the chain, the indicators,
and the recommended containment.

## Recommended actions I recorded

- Isolate the host from the network.
- Reset the user's credentials and revoke active sessions, because stealers read saved browser data.
- Block the destination IP and the delivery URL at the proxy and at DNS.
- Search mail and proxy logs for the same sender, subject and URL to find other recipients.
- Hunt the binary hash across all endpoints.

I could not perform the isolation myself; the endpoint console available to me listed no hosts. The
report says that in plain words instead of describing an action I did not take.

## Limits

- The mail headers were not fully visible in the interface, so I did not assert SPF, DKIM or DMARC results.
- The process identifiers and hash came from the course walkthrough for this alert; the platform accepted
  those answers, and the network rows above are ones I read myself.
- The log store available to me is a demonstration data set, so the timestamps are historical rather than
  live.

## What I would do differently

I would check the mailbox rules before the endpoint. Attackers who deliver mail often add a hidden
forwarding rule, and that takes thirty seconds to check. I only thought of it after closing the case.

## Skills demonstrated

`email header analysis` · `phishing triage` · `proxy and firewall log correlation` · `process lineage
reading` · `IOC extraction` · `containment planning` · `bilingual incident write-up`
