# 04 — Web Attacks

## The idea in one paragraph

Most web attacks are the same three moves in different clothes: send something the application did not
expect, make the application treat data as code or as a command, and then use whatever the application is
allowed to do. A defender cannot read every request, so the skill is knowing which few requests are worth
reading — the ones where input reaches something dangerous.

## The families I learned, and the log evidence for each

| Attack | The idea | What stands out in a web log |
| :--- | :--- | :--- |
| SQL injection | Input becomes part of a query | Quote characters, `UNION`, `OR 1=1`, error responses |
| Cross-site scripting | Input becomes script in someone else's browser | Script tags or event handlers in parameters |
| Command injection | Input becomes an OS command | Shell metacharacters, `system(`, `whoami`, `net user` |
| Directory traversal | Input becomes a path | `../` sequences, config file names |
| Local or remote file inclusion | Input becomes an include target | File paths, remote URLs in a parameter |
| IDOR | Input becomes someone else's record | Sequential IDs, one user reading another's data |
| Brute force | Volume against one endpoint | Hundreds of POSTs to the same login path |
| Open redirect | Input becomes a destination | A URL parameter that changes where the browser goes |

## Reading a log as a sequence, not a list

A single 200 response tells me almost nothing. A sequence tells a story. In the log-analysis case I wrote
up, the sequence was unmistakable once I sorted by time and user agent:

1. A scanner walked the site with a recognisable user agent and test labels.
2. A directory brute-force tool guessed thousands of paths in minutes.
3. A login page received 134 POSTs in a burst.
4. The authenticated portal appeared immediately after.
5. A parameter carried an operating-system command, twice.
6. The last request created a local account.

Each step is weak evidence alone. Together they are a full intrusion, and I could prove it without any
endpoint data.

## Fields that earn their place

| Field | Why I care |
| :--- | :--- |
| Source IP | Who is talking, and how many others share that IP |
| Request line | Method plus path — the actual action |
| Status code | Success, denial, or redirect; the redirect often follows a successful login |
| Response size | A sudden jump can mean a page that returned data it should not have |
| User agent | Separates scanners from people faster than anything else |
| Referer | Shows the path the user took, which helps order events |

## Detections worth building

- Requests whose URI contains OS command syntax or shell metacharacters.
- More than N POSTs to the same login path from one IP in a short window.
- A 200 on an admin path from an IP that failed login repeatedly just before.
- Requests for configuration files, backup files, or shell history.
- Scanner user agents appearing from internal addresses.

None of these needs a threat-intel feed. They need the log and a threshold.

## What I got wrong at first

I looked for suspicious strings and ignored volume. The brute-force phase in my case did not contain a
single strange character; it was 134 identical, perfectly well-formed POSTs. The signal was the count.
Since then I always compute "how many times from this IP to this path" before reading individual lines.

## The defensive lesson I keep

A web server runs with an identity. Whatever that identity can read, the attacker can read once command
execution is achieved. So the blast radius of a web attack is set by the service account, the file
permissions, and the secrets stored next to the application — not by the vulnerability score. When I read
a report that says "injection on a low-value page", my first question is what the service account can
reach.
