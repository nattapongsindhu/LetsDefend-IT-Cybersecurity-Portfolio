# Changelog

All notable changes to this portfolio. Dates are the day the change was published.

The format follows the spirit of [Keep a Changelog](https://keepachangelog.com/): sections are grouped by
what changed, not by file.

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
