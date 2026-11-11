# 02 — Kill Chain and MITRE ATT&CK

## The idea in one paragraph

The cyber kill chain is a story shape: someone researches you, prepares a weapon, delivers it, exploits
something, installs a foothold, opens a channel home, and then acts. MITRE ATT&CK is the same idea
written as a catalogue of observed behaviours, so two analysts can describe the same intrusion with the
same words. The chain helps me tell the story; ATT&CK helps me write it down in a way other tools and
other teams understand.

## The chain phases, with what I look for

| Phase | Plain meaning | Evidence I would expect |
| :--- | :--- | :--- |
| Reconnaissance | Learning about the target | Scanner user agents, directory brute force, port sweeps |
| Weaponisation | Building the payload | Usually invisible from the defender side |
| Delivery | Sending it | Mail rows, download URLs, USB events |
| Exploitation | Making it run | Document macros, script hosts, vulnerable service calls |
| Installation | Staying | Registry run keys, scheduled tasks, new accounts |
| Command and control | Phoning home | Outbound sessions to hosting IPs on odd ports |
| Actions on objectives | Doing the damage | Data access, exfiltration, encryption |

The useful part for a defender is not the neat sequence. Real intrusions skip steps, repeat them, and run
several in parallel. What stays true is that each phase leaves a different kind of evidence, and the
evidence for one phase usually points at the next.

## How I use ATT&CK in an investigation

1. **Map what I can prove.** Not what the alert suggested — what I have a row or artefact for.
2. **Look for the neighbours.** If I can prove execution, I look for delivery before it and persistence
   after it. Adversaries rarely stop at one technique.
3. **Use the technique list as a checklist for gaps.** If I proved command execution but found no
   persistence, either it is absent or I have not looked in the right place yet.

## Techniques that keep appearing in my cases

| Technique | ID | What it looked like |
| :--- | :--- | :--- |
| Phishing: spearphishing link | T1566.002 | A mail with a link and a password-protected archive |
| User execution | T1204 | A user opened a document and enabled macros |
| Command and scripting interpreter | T1059 | `cmd.exe` children, `cscript.exe`, PowerShell |
| Application layer protocol | T1071 | HTTPS beacon to a hosting IP |
| Boot or logon autostart: registry run keys | T1547.001 / T1112 | A run key written after the macro ran |
| Create account | T1136 | A local account created from a web shell |
| Brute force | T1110 | Hundreds of login attempts in minutes |
| Exploit public-facing application | T1190 | Injection through a web parameter |

## Why I stopped memorising IDs

I used to try to remember technique numbers. That is backwards. The technique names describe behaviour,
and the behaviour is what I see in a log. I now search ATT&CK by behaviour — "create account", "registry
run key" — and let the ID come with the description. The ID matters for the report; the behaviour matters
for the investigation.

## The trap I fell into

I mapped everything I could think of, which made my first report look thorough and read like a shopping
list. A reviewer asked one question: "which of these did you actually see?" Only four survived. A short
honest mapping beats a long speculative one.

## Mapping rules I follow now

- One row per technique I can point at evidence for.
- If the evidence is a sandbox report and not my own log, say so in the row.
- If a technique is plausible but unproven, mark it "possible" rather than mixing it with the proven ones.
- Always note the tactic, because that is what a manager reads first.

## What the chain is bad at

The kill chain was written for perimeter intrusions. It says little about cloud identity abuse or
insider data theft, and nothing about living-off-the-land where every step uses a legitimate tool. For
those, ATT&CK's tactic grouping is a better mental model. I use the chain for narrative and ATT&CK for
coverage.
