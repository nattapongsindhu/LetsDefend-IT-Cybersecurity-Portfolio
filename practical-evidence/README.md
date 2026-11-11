# Practical Evidence

Work I produced during and after the learning path. Each file is an **evidence summary**: the situation,
what I did, what the evidence showed, what the result was, and what I could not verify.

The full investigation reports stay in my private working repository. These summaries are written for a
public audience: enough detail to judge the work, no answers to anything still active, no flags, no
credentials.

| # | Evidence | Type | Outcome |
| :---: | :--- | :--- | :--- |
| 01 | [Phishing investigation](01-phishing-investigation.md) | Live alert case | True positive — mail lure delivered a stealer that beaconed out |
| 02 | [Web attack analysis](02-web-attack-analysis.md) | Log analysis challenge | Full attack chain reconstructed from a 12,557-line access log |
| 03 | [Macro document to C2](03-macro-document-to-c2.md) | Live alert case | True positive — macro workbook, script host, C2, persistence |
| 04 | [Benign activity review](04-benign-activity-review.md) | False-positive study | Tuning plan for an alert that fires on internal red-team work |
| 05 | [Campaign reconstruction](05-campaign-reconstruction.md) | Multi-host incident | Three hosts, one campaign, two confirmed outcomes |
| 06 | [Python log analyzer](python-log-analyzer/) | Tool I built | CLI that parses access logs and surfaces scanners and injection payloads |

## Why these five cases

I did not pick the easiest alerts. I picked the ones that taught me something different:

- **01** taught me that a mail rule can be right and still useless, because the attachment scanner cannot
  open a password-protected archive.
- **02** taught me that volume is a signal; the brute-force phase contained no strange characters.
- **03** taught me that the file is not the attack, the behaviour after the file is.
- **04** taught me that a rule which fires on my own security team is a rule I have to tune, not delete.
- **05** taught me that two alerts an evening apart can be one campaign, and that a DNS row can find a
  victim nobody reported.

## What each summary contains

```text
- Context: what the alert or challenge was
- What I did: the steps, in order
- Evidence: the rows, fields and artefacts that mattered
- Result: the verdict and the reasoning
- Limits: what I could not check, and why
- Skills demonstrated: the short list a recruiter can scan
```
