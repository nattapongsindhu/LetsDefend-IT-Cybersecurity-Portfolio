# Screenshots

Real captures from the training platform, cropped so that **no answers, flags or session data** are
published. Each image is here to support a specific claim in the case summaries.

| File | Case | What it proves | What was removed |
| :--- | :--- | :--- | :--- |
| `01-mail-evidence.png` | Case 01 | The message was delivered, with sender, recipient, subject and action | Nothing — the panel has no answers |
| `02-mail-body.png` | Case 01 | The body, the "Redeem Now" link and the attachment name | Nothing |
| `03-endpoint-empty.png` | Case 01 | The endpoint console listed no hosts, which is why isolation stayed a recommendation | Nothing |
| `04-soc138-case-report.png` | Case 03 | Case closed with 100 % playbook success and the alert fields (hash, file name, device action) | The answer panel below the crop line |
| `05-soc137-case-report.png` | Case 05 | The blocked host in the same campaign, same report layout | The answer panel below the crop line |

## Why crops

The platform shows a "Playbook Answers" panel under the case fields. Publishing it would hand the answers
to anyone working on the same exercise, and the platform rules do not allow that. The crop keeps the
evidence that matters for a reviewer — that the case existed, was closed, and with what result — and drops
the answer text.

## Redaction rules I applied

1. No flags, no answer text, no "correct" markers.
2. No session tokens, no email addresses of other people, no browser chrome with a logged-in account menu.
3. No hostnames or IPs from real networks; only lab ranges.
4. No file paths that reveal a Windows username.

## What is still missing

The platform cases do not expose raw SIEM queries in a copyable form, so the query text in the case
summaries was written by me to show the logic, not pasted from the console. That is stated in each case
file rather than implied.
