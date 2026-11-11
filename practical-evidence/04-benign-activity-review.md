# 04 — Benign Activity Review (When the Alert Is My Own Team)

**Type:** false-positive study · **Evidence:** mail dataset and alert-rule behaviour
**Verdict:** Benign — authorised internal activity · **Skills:** alert tuning, false-positive control

---

## Context

Not every alert should become an incident. While reviewing mail data I found internal messages requesting
creation of a system account, sent from a security-team mailbox to an operations mailbox, with a reply
twenty minutes later. A rule that fires on "account creation" would open an incident for our own test team.

## What I did

1. Read the sender, recipient, subject and timestamps of both messages.
2. Checked that both parties sit in the internal domain.
3. Compared the pattern against a real account-creation attack from case 03.
4. Listed the checks that separate the two.
5. Wrote a tuning plan with the risk of each change.

## The comparison that decided it

| Aspect | Benign case | Real attack case |
| :--- | :--- | :--- |
| Starting point | Internal mail request | Web request with an operating-system command |
| Who asks | Internal security mailbox | External attacker |
| Approval | Request and reply in a thread | None |
| Timing | Working hours | Late evening, single attempt |
| Corroboration | Internal parties agree | Unknown external infrastructure |

Same outcome — an account is created — completely different path. That is the whole lesson.

## Result

**Benign.** The activity is authorised internal testing. The right action is to tune the rule, not to
delete it.

## Tuning plan I proposed

| Change | Effect | Risk |
| :--- | :--- | :--- |
| Lower severity when the sender is an internal security mailbox **and** authentication passes | Removes queue noise | Spoofed internal address — mitigate with authentication checks |
| Require a change ticket for account-creation requests | Turns a guess into a check | Needs ticket-system integration |
| Keep full severity for external senders | Preserves detection | None |
| Send auto-closed alerts to the SOC lead monthly | Audit trail | Low |

The dangerous version of this rule is "auto-close everything internal". An attacker who can spoof the
internal address gets a free pass. Authentication has to pass before anything closes itself.

## Limits

- The message body was not visible, so the account name and the approval ticket are unknown.
- The judgement rests on sender, domain, subject and the request-and-reply pattern.
- There was no false-positive ticket in my account to test against; this is a tuning study based on real
  mail records, not a closed case.

## What I learned

A false positive is not a failure of the analyst; it is information about the rule. The cost is real
though: every unnecessary alert spends analyst time and teaches users to ignore warnings. Tuning is
security work, not paperwork.

## Skills demonstrated

`false-positive analysis` · `rule tuning` · `authenticated-sender reasoning` · `risk assessment` ·
`documentation`
