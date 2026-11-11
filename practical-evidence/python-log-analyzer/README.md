# Python Log Analyzer

A small command-line tool I wrote to speed up first-pass triage of a web access log. It answers one
question: **where should I start reading?**

It is deliberately simple — standard library only, no dependencies, one file. That is the point: a tool I
can run on any machine, including a locked-down jump host, in the first five minutes of an investigation.

## What it does

| Section | Output |
| :--- | :--- |
| [1] Volume | Request count, unique sources, share of the busiest source |
| [2] Top sources | Ranked by request count, with a bar for quick eyeballing |
| [3] Tool user agents | Matches known scanner and tool user-agent strings |
| [4] Top paths | Which endpoints are being hit most |
| [5] Status codes | Distribution of responses, including error spikes |
| [6] Login POSTs | POST counts to login-like paths per source (brute-force hint) |
| [7] Attack payloads | Requests whose decoded query string matches injection, traversal, XSS, sensitive-file, or account-creation patterns |

URL-encoded payloads are decoded before matching, so `%3Cscript%3E` and `%20UNION%20SELECT` are caught the
same as their plain forms.

## Usage

```bash
python analyze.py sample_access.log
python analyze.py sample_access.log --top 5
python analyze.py sample_access.log --json     # machine-readable output
```

## Real output on the included sample

The sample log is synthetic and included for demonstration: a normal shopper, a scanner, a brute-force
burst, an injection attempt, and a traversal attempt.

```text
==================================================================
 ACCESS LOG TRIAGE  file=28 requests, 5 source IPs
==================================================================

[1] VOLUME
    parsable requests : 28
    skipped lines     : 0
    unique sources    : 5
    busiest source    : 203.0.113.42 (60.7% of all requests)

[2] TOP 6 SOURCE ADDRESSES
        17  ############################  203.0.113.42
         7  ############  10.0.4.11
         2  ###  10.0.4.13
         1  ##  10.0.4.12
         1  ##  10.0.4.14

[3] USER AGENTS THAT ARE TOOLS
         2  curl/8.4.0
         1  Mozilla/5.00 (Nikto/2.1.6) (Evasions:None) (Test:sitefiles)
         1  Mozilla/5.00 (Nikto/2.1.6) (Evasions:None) (Test:004729)
         1  Mozilla/5.00 (Nikto/2.1.6) (Evasions:None) (Test:map_codes)
         1  Mozilla/5.00 (Nikto/2.1.6) (Evasions:None) (Test:002989)

[4] TOP 6 PATHS
         6  /shop/login.php
         4  /shop/product.php
         3  /shop/index.php
         3  /shop/cart.php
         3  /shop/portal.php
         1  /

[5] STATUS CODES
        12  200
         7  404
         5  401
         2  403
         1  302
         1  500

[6] POST REQUESTS TO LOGIN-LIKE PATHS
         6  203.0.113.42   (brute-force hint when this is high in a short window)

[7] REQUESTS WITH ATTACK-LIKE PAYLOADS (8)
    203.0.113.42     GET   sensitive-file       /.git/config
    203.0.113.42     GET   sensitive-file       /.env
    203.0.113.42     GET   os-command           /shop/portal.php?msg=%22%22%3Bsystem(%27whoami%27)
    203.0.113.42     GET   os-command,account-creation /shop/portal.php?msg=%22%22%3Bsystem(%27net%20user%20backup%...
    10.0.4.12        GET   sql-injection        /shop/index.php?id=1%20UNION%20SELECT%20username,password%20
    10.0.4.13        GET   path-traversal,sensitive-file /shop/product.php?file=../../../../etc/passwd

==================================================================
 Read order: start with [7], then [3] and [6], then the busiest source in [2].
==================================================================
```

## How I read the output

1. **Start at [7].** A request that carries `system(` or `net user` is almost never a normal user.
2. **Then [3].** Scanner user agents arriving from an internal address are more interesting than the same
   agent hitting a public site.
3. **Then [6].** Six POSTs in six seconds is a brute force; six spread over a day is a forgotten password.
4. **Then [2].** One source that owns 60 % of the traffic is the story. Read that source's lines first.

## What it does not do

- It does not understand application context: `/search?q=<script>` may be a reflection test or a real
  attempt, and the tool cannot tell.
- It does not score severity. Every finding is a prompt to read, not a verdict.
- It does not parse every log format. Apache and Nginx combined logs work; JSON logs do not.
- It does not replace a SIEM. It is for the case where a log file lands in front of me and there is no
  search interface yet.

## Why I built it

During a log-analysis exercise I found myself running the same five shell pipelines by hand: count the
sources, count the user agents, count the paths, count the login POSTs, grep the payloads. Repeating that
by hand is slow and easy to get wrong. Writing it once made the step repeatable, and writing the regex
patterns made me think about what an attack payload actually looks like.

## Files

| File | Purpose |
| :--- | :--- |
| `analyze.py` | The tool (Python 3.8+, standard library only) |
| `sample_access.log` | Synthetic sample log used in the output above |

## Safety

The included log is synthetic. No real customer data, no internal hostnames, and no credentials appear in
this folder. The account name that appears inside one injection payload is a dummy value created for the
sample.
