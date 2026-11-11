# 06 — Logs, SIEM and Incident Response

## The idea in one paragraph

Logs are the memory of a system. A SIEM is a way to ask questions across those memories at once. Incident
response is what happens when the answer is bad. The three fit together in one direction: the incident
defines the question, the question defines the search, and the search decides what the response can
honestly claim.

## The log types I learned to read

| Source | What it records | Field that usually matters |
| :--- | :--- | :--- |
| Firewall | Allowed and denied network sessions | Action, source, destination, port, process |
| Proxy | Web requests from users and applications | URL, user, process, action |
| VPN | Remote access sessions | User, source IP, duration, bytes |
| DNS | Name resolutions | Query name, client, response |
| Web server | Requests to the application | Method, path, status, size, user agent |
| Windows security | Authentication and authorisation | Event ID, account, logon type |
| EDR | Process and file activity | Parent process, command line, hash |
| Mail gateway | Message delivery | Sender, recipient, subject, action, attachment |

Two rows from different sources that share an IP or a timestamp are worth more than ten rows from one.

## Building a search that answers the question

I start from a decision, not from a query. Three decisions cover most triage:

1. **Did this happen?** Search for the artefact the alert named — a hash, a URL, a file name.
2. **How far did it go?** Pivot on the host IP across firewall and proxy, then on the destination IP across
   all hosts.
3. **Is anyone else affected?** Take the indicator and search it backwards across the whole estate.

A useful habit: write the question in the report before the query. When the query returns something
unexpected, the written question keeps me from drifting.

## Splunk, in the way I actually use it

| Step | What I do |
| :--- | :--- |
| Scope | Pick the index and the time window before anything else |
| Filter | Narrow by the most selective field first |
| Count | `stats count by field` to find the outliers instead of reading rows |
| Compare | Look for a field value that appears once when everything else appears a thousand times |
| Save | Turn the search into an alert only after it has proved useful twice |

The last line matters. A search I used once is a question I had. A search I used twice is a detection
candidate.

## Incident response, without the poster version

The textbook order is prepare, identify, contain, eradicate, recover, lessons learned. In practice the
steps overlap, and containment decisions are made with incomplete information. What actually helped me:

| Step | What it meant in my cases |
| :--- | :--- |
| Identify | Prove execution first; everything else depends on that |
| Contain | Decide whether the host must come off the network, and say so even if I cannot do it |
| Eradicate | Remove the persistence, not just the file — a run key survives a deleted binary |
| Recover | Verify the host no longer resolves or reaches the C2, then watch it |
| Learn | Write the detection that would have caught it an hour earlier |

## The two questions that decide a case

**"Was anything stopped?"** If a control blocked the payload, the incident is a control success with a
report attached. If nothing was stopped, the incident is a compromise.

**"What can I prove myself?"** Everything else goes in the report as a recommendation, a limitation, or an
open question. Separating those three categories is the difference between a report that holds up in a
review and one that falls apart.

## What I got wrong at first

I wrote conclusions before writing evidence. My first report said "the host was likely compromised" without
a single row under it. A reviewer's question — "which log line says that?" — reorganised how I work. Now the
evidence section is written first and the conclusion is one sentence at the top that summarises it.

## Report skeleton I reuse

```text
1. What happened, in three sentences
2. The alert and what fired it
3. Evidence table: source, time, what it proves
4. Analysis: what I think it means
5. Verdict: true or false positive, one line why
6. What I did and what I could not do
7. What should happen next, with priority
8. Limits and open questions
```

The last section is not padding. It is the part that makes the other seven believable.
