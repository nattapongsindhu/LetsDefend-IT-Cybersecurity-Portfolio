# Changelog

All notable changes to this portfolio. Dates are the day the change was published.

The format follows the spirit of [Keep a Changelog](https://keepachangelog.com/): sections are grouped by
what changed, not by file.

---

## [1.2.1] — 2026-11-11

Follow-up fixes after a second review of v1.2.0.

### Fixed

- **Attachment password removed from both mail screenshots.** The password line is cropped from
  `01-mail-evidence.png` and `02-mail-body.png`, and the screenshots README now records the crop.
- **Stale claim in the skills table.** "6 reports in this repository" replaced with "5 case summaries and
  1 Python tool", matching the rest of the README.

### Changed

- **SPL rule now has a bounded time window** (`earliest=-15m latest=now`) and the redundant port-range
  clause is gone. Without a window the search was a scan.
- **Every rule carries a status line**: draft, not tested against real telemetry, tuning required.
- **Two new rule-lint tests**: one fails if the SPL window becomes unbounded, one fails if the redundant
  port clause returns. Rule lint is now 17 tests.

### Added

- **LetsDefend transcript screenshot** in `certificates/`, with the platform numbers recorded in the README:
  2,160 points, SLA 51, 100 % success rate, and the alert-type radar that shows the breadth of work.

### Notes

- CI scans `.md`, `.py` and `.log`. It cannot read text inside a PNG, so image redaction stays a manual step
  in the pre-publish checklist.

---
## [1.2.0] — 2026-11-11

Review-driven release. An external review scored the repository 74/100 and listed six high-impact gaps; this
release closes all six.

### Added

- **Evidence tables in every case** — timeline, IOC list and a case-specific MITRE ATT&CK table with
  evidence, source, confidence and a detection opportunity per technique.
- **Detection engineering library** — one Sigma rule, one SPL rule, one KQL rule, each tied to a case, each
  with its tuning problem written down.
- **Rule lint tests** — 15 unit tests that parse the rules and fail if the structure or the ATT&CK tags break.
- **Screenshots** — five real captures, cropped so no answer panel is published.
- **Architecture page** — the seven-step investigation workflow as a Mermaid diagram.
- **CI workflow** — unit tests plus a secret-pattern scan on every push.
- **Analyzer unit tests** — nine tests covering parsing, payload detection and the "no secrets in the sample"
  rule.
- **Sample analyzer output** committed as evidence.

### Changed

- README evidence counts corrected: "6 investigation reports" became **5 case summaries, 1 tool, 3 rules**.
- `SECURITY-CHECK.md` last-check date corrected from a future date to 2026-11-11.
- Repository layout section updated with the new folders.

### Fixed

- A password-like string inside the synthetic sample log replaced with `PASSWORD_REDACTED`. A regression test
  now fails if it returns.
- The CI secret scan no longer flags its own documentation.

### Notes

- Git history was not rewritten. The old commit still contains the synthetic string; the reasoning is
  documented in `SECURITY-CHECK.md` §6.

---

## [1.1.0] — 2026-11-11

### Added

- MIT license for the code, with a license-scope section separating code from written content.
- Repository topics and a skill badge bar.
- LetsDefend profile link, pointing at the account the path was completed on.

### Changed

- Header facts rendered as a table instead of run-on lines.
- Sister-portfolio link corrected to point at the public TryHackMe repository.

---

## [1.0.0] — 2026-11-11

First public release.

### Added

- Ten-section README covering purpose, learning path, skills, tools, study notes, evidence, certificates,
  lessons, next steps and the security check.
- Six study notes: SOC fundamentals, kill chain and ATT&CK, phishing and headers, web attacks, malware and
  document analysis, logs and incident response.
- Five case summaries: phishing, web attack log analysis, macro document to C2, benign activity review,
  campaign reconstruction.
- Python log analyzer with a synthetic sample log.
- `SECURITY-CHECK.md` with the pre-publish checklist and the commands used to run it.
