# Security and Privacy Check

This repository is public. Before publishing, and after every content change, it is checked against the
list below. The point is not to pass a checkbox; it is to make sure nothing from a lab, a mailbox, or a
credential ends up indexed by a search engine.

**Last check:** 2026-11-11 · **Result:** pass

---

## 1. The checklist

| # | Check | Why it matters | Result |
| :---: | :--- | :--- | :---: |
| 1 | API keys and tokens | A leaked key can be used immediately | pass |
| 2 | Passwords, even in examples | People reuse patterns | pass |
| 3 | Flags and room answers | Publishing answers breaks the platform rules and marks me as unreliable | pass |
| 4 | Walkthroughs of active rooms | Same as above | pass |
| 5 | Personal data (home address, phone, ID numbers) | Privacy | pass |
| 6 | Other people's names and emails | Consent | pass |
| 7 | Employer or client data | Confidentiality | pass |
| 8 | Internal hostnames and private IPs from real networks | Attack surface disclosure | pass |
| 9 | Session cookies or dashboard tokens in screenshots | Account takeover | pass |
| 10 | Absolute paths that reveal a username on my machine | Minor, but noisy | pass |

## 2. How the check is done

### 2.1 Pattern scan

```bash
# secrets and credentials
grep -rniE "(api[_-]?key|secret|token|password|passwd|bearer|authorization:)" . --include="*.md" --include="*.py" --include="*.log"

# flags and answer markers
grep -rniE "(flag\{|thm\{|htb\{|letsdefend\{|answer:|correct answer)" . --include="*.md"

# private IP ranges (should only be lab ranges, and only as evidence context)
grep -rnE "(10\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}|192\.168\.[0-9]{1,3}\.[0-9]{1,3}|172\.(1[6-9]|2[0-9]|3[01])\.[0-9]{1,3}\.[0-9]{1,3})" . --include="*.md" --include="*.log"

# email addresses
grep -rnE "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}" . --include="*.md"
```

### 2.2 What is allowed on purpose

| Item | Why it stays |
| :--- | :--- |
| Documentation IP ranges (`203.0.113.0/24`, `198.51.100.0/24`, `192.0.2.0/24`) | They are reserved for examples and belong to nobody |
| Private lab ranges (`10.0.4.0/24`) in the sample log | Synthetic demonstration data I created |
| Example domains (`shop.local`) | Clearly fictional |
| Dummy account name inside an injection sample | Created for the demo log, not a real account |
| Hashes from public malware reports | Public indicators, useful as evidence |

### 2.3 Screenshot review

Any image added to this repository is opened at full size and checked for:

- browser chrome showing a session token, an email address, or a bookmarks bar,
- an avatar or account menu with a real name I do not want published,
- platform-side answer panels or "correct" indicators,
- a file path that shows my Windows username.

If an image fails, it is cropped or re-taken; it is never published "for now".

## 3. What is intentionally excluded

| Excluded content | Reason |
| :--- | :--- |
| Full investigation reports from my private repository | They contain host-level detail and long analyst notes; the public version is the evidence summary |
| Room answers and question walkthroughs | Platform rules, and it would misrepresent the work as memorisation |
| Lab credentials and machine addresses | No public value, some risk |
| Anything from a real employer or client | Never public without written permission |

## 4. Re-running the check

Before any push that adds content:

```text
1. Run the three grep commands above.
2. Open every new image at full size.
3. Read the new markdown for names, paths, keys and answers.
4. Update the date and result at the top of this file.
```

A one-line commit message is enough for a typo fix, but any new evidence file gets the full check.

## 5. Known limitations

- Pattern matching finds strings, not context. A word like "token" appears legitimately in a sentence
  about sessions; each hit is read, not just counted.
- This repository is not scanned by an automated secret scanner on every push. The check is manual and
  documented here so it is repeatable.
- If a secret is ever committed by mistake, removing the file is not enough: the history keeps it. The
  correct response is to revoke the credential first, then rewrite history.
---

## 6. Changes made after the first public review

The first public version of this repository was reviewed and two issues were raised. Both are fixed.

| Issue | Fix | Commit |
| :--- | :--- | :--- |
| A password-like string appeared inside the synthetic sample log | Replaced with `PASSWORD_REDACTED`, and a unit test now fails if it comes back | this commit |
| The "last check" date was in the future | Corrected to 2026-11-11 | this commit |

### Note on Git history

The string was synthetic — an account name and a fake password I invented for the demonstration log — but
it still looked like a credential. The file is now redacted, and the test suite asserts that the pattern
cannot return.

The old commit still contains the original string. Rewriting history would change every commit hash in a
repository that a reviewer may already have cloned, so it was left intact and documented here instead. If
you are auditing this repository: the value was never a working credential, and nothing in this repository
ever connected to a live system.

### Automated check

From this commit onwards, `.github/workflows/ci.yml` runs on every push and blocks the build if it finds:

- credential-like patterns: API key assignments, secret assignments, long bearer tokens and password assignments,
- flag and answer markers used by the training platforms.

The check is a grep, not a scanner with entropy analysis. It catches the mistakes I am likely to make; it
does not prove the repository is clean.