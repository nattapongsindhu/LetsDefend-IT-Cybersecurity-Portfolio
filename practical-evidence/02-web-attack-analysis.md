# 02 — Web Attack Analysis (One Access Log, Four Phases)

**Type:** log analysis challenge · **Artefact:** Apache access log, 12,557 lines
**Verdict:** True Positive — full attack chain · **Skills:** log analysis, timeline building, MITRE mapping

---

## Context

The challenge provided a single web server access log covering 17 minutes and 43 seconds. The task was to
work out what happened, in what order, and whether the attacker succeeded — using nothing but the log.

## What I did

1. Counted source addresses to see who was talking most.
2. Counted user agents to separate tools from people.
3. Grouped requests by path to find the phases of the attack.
4. Counted POST requests to the login endpoint.
5. Checked whether the authenticated area appeared in the log.
6. Extracted command-style parameters to see what the attacker tried to run.
7. Read the last lines of the log for the final action.

## What the log showed

| Phase | What I saw | Why it mattered |
| :--- | :--- | :--- |
| Scanning | A scanner user agent with test labels, hundreds of requests | Reconnaissance, and a fingerprint |
| Directory brute force | Thousands of guessed paths from one tool | Looking for hidden files and admin paths |
| Login brute force | 134 POST requests to one login endpoint in minutes | Credential guessing at volume |
| Access | The authenticated page returned success immediately after | The guessing worked |
| Command injection | A parameter carrying an operating-system command | The web server ran the command |
| Persistence | A final request that created a local account | The attacker intended to return |

One source address made up almost every request in the log; a real user made 29. That single ratio told me
where to look before I read a line of detail.

## Result

**True positive.** I reconstructed a six-step intrusion from one file: reconnaissance, directory brute
force, credential brute force, successful authentication, command execution, and account creation for
persistence. No endpoint data was needed to prove it.

## Why the count mattered more than the content

The brute-force phase contained no strange characters. It was 134 well-formed requests to a normal login
page. If I had searched only for suspicious strings, I would have missed it. Sorting by count is what made
the phase visible, and that is now the first thing I do on any log.

## Recommended actions I recorded

- Disable and delete the created account.
- Reset the service account the web server runs as.
- Take the host off the network and rebuild it from a clean image.
- Rotate application and database secrets reachable from that account.
- Block the source address.
- Remove diagnostic pages that expose version information or accept code.

## Limits

- The log is the only artefact. There is no host telemetry, so I cannot say what the created account did
  afterwards.
- The log window ends at the persistence request; anything later is unknown.
- The target application is deliberately vulnerable, so the value of the exercise is the timeline and the
  reasoning, not the discovery of a novel vulnerability.

## What I learned

A log is not a list of events; it is a sequence with a direction. The same lines sorted by count tell one
story, sorted by time tell another, and sorted by user agent tell a third. The analyst's job is to choose
the sort that answers the question.

## Skills demonstrated

`Apache log analysis` · `user-agent fingerprinting` · `brute-force detection` · `command injection
recognition` · `timeline reconstruction` · `MITRE ATT&CK mapping` · `containment planning`
