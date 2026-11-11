# 01 — SOC Fundamentals

## The idea in one paragraph

A Security Operations Center is a team plus a process. The team watches alerts that come out of a SIEM,
an EDR, a mail gateway and a firewall. The process decides who owns an alert, how long they may hold it,
and what a finished investigation looks like. The technology matters, but the process is what stops work
from falling between shifts. A SOC without a process is a group of people staring at dashboards.

## The tiers, in my words

| Tier | Job | What "done" means for them |
| :--- | :--- | :--- |
| Tier 1 | Triage. Decide if the alert is real and urgent. | The alert is either escalated with a reason or closed with a reason |
| Tier 2 | Investigate. Build the timeline, scope the impact. | The scope is known and containment is decided |
| Tier 3 | Hunt and improve. Look for what the alerts missed. | A new detection rule or a confirmed gap |
| Engineering | Keep the sensors and pipelines healthy. | Logs arrive, parsers work, rules fire |

The boundary I care about is Tier 1 versus Tier 2. Tier 1 answers "is this real?". Tier 2 answers "how
far did it go?". Mixing the two is how a queue either backs up or leaks.

## The alert lifecycle

```text
alert fires -> queue -> owner takes it -> investigation -> verdict -> closed -> review
```

Three points in that line cause most of the trouble.

**Ownership.** An alert with no owner is nobody's problem. The moment someone takes it, someone else
stops looking at it. That is a feature, not a bug.

**Verdict.** A closed alert without a reason is worse than an open one, because it looks finished.
Every closure should say true positive or false positive, and one sentence why.

**Review.** The review step is where the SOC learns. If the same alert closes as a false positive every
week, the rule needs tuning, not more analyst attention.

## The tool stack and what each one answers

| Tool | Question it answers | What it is bad at |
| :--- | :--- | :--- |
| SIEM | What happened across the estate? | Deep endpoint detail |
| EDR | What ran on this host? | What happened outside the host |
| Mail gateway | What arrived in the mailbox? | What happened after the click |
| Firewall and proxy | Where did traffic go? | Why it went there |
| Sandbox | What does this file do? | Anything after it stops running |
| Threat intel | Is this indicator known bad? | Anything new |

None of these is enough alone. In my cases, the mail gateway proved delivery, the proxy proved the
download, and the firewall proved the outbound connection. Three tools, one story.

## Pivot points I use first

1. **Host to network.** Take the host IP from the alert and search the proxy and firewall for it.
2. **Network to host.** Take the destination IP and ask which hosts talked to it. That is how I found a
   second victim in one case.
3. **File to behaviour.** Take the hash into a sandbox and compare its behaviour to the alert.
4. **Time to context.** Widen the window by an hour on both sides; most incidents have a step before the
   alert and a step after it.

## What I got wrong at first

I treated the alert text as the truth. It is not. The alert is one sensor's opinion in one sentence. In
my third case the alert said "download attempt" and I nearly closed it as blocked, until the proxy log
showed the file had already reached the disk. The alert was about the attempt; the log was about the
outcome.

## Terms worth keeping straight

| Term | Meaning |
| :--- | :--- |
| True positive | The activity happened and is unwanted |
| False positive | The rule fired but the activity is acceptable |
| Benign true positive | The activity happened but is authorised, such as a red-team test |
| Detection gap | Something happened and no rule fired |
| Mean time to detect | From the event to the alert |
| Mean time to respond | From the alert to containment |
