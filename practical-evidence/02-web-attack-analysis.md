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


---

## Evidence tables

### Timeline

| Time (+03:00) | Phase | Evidence |
| :--- | :--- | :--- |
| 12:35:40 | Log window opens | First request |
| 12:35–12:45 | Scanner activity | Tool user agent with test labels |
| 12:45–12:49 | Directory brute force | Thousands of guessed paths |
| 12:49–12:50 | Login brute force | 134 POST requests to one endpoint |
| 12:50:10 | Authenticated page returned | `200` on the portal |
| 12:50:15 | Session accepted | `302` immediately after |
| ~12:51 | Command execution | Parameter carrying an OS command |
| 12:53:23 | Persistence | Final request creates a local account |

### IOCs

| Type | Value | Note |
| :--- | :--- | :--- |
| Source address | `192.168.199.2` | 99.8 % of requests in the window |
| User agents | scanner string, directory-tool string, Shellshock probe | Tools, not browsers |
| Paths | login endpoint, portal, diagnostic page | Attack surface |
| Payload pattern | `system(` plus `net user` in a parameter | Command injection and account creation |

The full request lines stay out of this public summary. Publishing exact exploit strings adds nothing for a
reviewer and everything for a copy-paste attacker.

### MITRE ATT&CK for this case

| Technique | Evidence in this case | Source | Confidence | Detection opportunity |
| :--- | :--- | :--- | :---: | :--- |
| `T1595` Active scanning | Scanner user agent with hundreds of probes | Access log | High | Alert on known scanner agents from internal ranges |
| `T1083` File and directory discovery | Thousands of guessed paths | Access log | High | Count 404s per source per minute |
| `T1110` Brute force | 134 login POSTs in one minute | Access log | High | Threshold POSTs to login paths |
| `T1190` Exploit public-facing app | Command payload in a parameter | Access log | High | Match command syntax in query strings |
| `T1059` Command interpreter | `system()` call | Access log | High | Same rule as above, higher severity |
| `T1136` Create account | Account creation command | Access log | High | Alert on account-creation strings in web requests |
## Skills demonstrated

`Apache log analysis` · `user-agent fingerprinting` · `brute-force detection` · `command injection
recognition` · `timeline reconstruction` · `MITRE ATT&CK mapping` · `containment planning`