# 03 — Macro Document to C2

**Type:** live alert case · **Platform:** LetsDefend · **Verdict:** True Positive
**Skills:** document analysis, process lineage, C2 identification, persistence analysis

---

## Context

An internal host received a spreadsheet named like a business order sheet. The security stack recorded the
file but did not stop it: the device action was **allowed**. The question was whether the document was
malicious and whether anything ran.

## What I did

1. Read the alert fields: file name, size, hash, host, source address, device action, mapped technique.
2. Confirmed the file type was macro-capable and the name was a business lure.
3. Used a public sandbox report for the same hash to see the behaviour, because my endpoint console showed
   no hosts.
4. Built the execution chain from the sandbox process tree and network tab.
5. Located a second internal host that resolved the same command-and-control domain.
6. Walked the platform playbook to record the verdict and the recommended actions.

## Evidence

| Source | What it showed |
| :--- | :--- |
| Alert pane | Macro-capable workbook, 2.66 MB, allowed, mapped to registry modification |
| Sandbox report | Office process started a script host, which wrote a script file to a temporary folder |
| Sandbox network tab | HTTPS session to a single external host |
| Behaviour | A registry value written for persistence |
| Log search | A second internal host resolving the same C2 domain |

The chain was short: document, macro, script host, dropped script, outbound connection, persistence. Short
chains are the normal case. Malware does not need to be elegant.

## Result

**True positive.** The document ran, the host connected out, and persistence was written. A second host
touched the same infrastructure, which turned a single alert into a campaign — documented separately as
[case 05](05-campaign-reconstruction.md).

## Recommended actions I recorded

- Isolate both hosts.
- Remove the registry run value, not just the dropped file.
- Block the C2 IP and domain at proxy and DNS.
- Block the delivery URL so the same file cannot be fetched again.
- Hunt the hash and the file name across mail and endpoints.
- Disable macros for internet-origin documents by policy.

None of the isolation actions were possible from my console. The report states that as a limitation.

## Limits

- The endpoint console listed no hosts, so I did not observe the process tree on the victim machine myself.
  The chain comes from a public sandbox report of the same hash, and the report names that source.
- I did not re-run the sample in my own lab.
- The log data set is demonstrative, so the timestamps are historical.

## What I learned

The file is not the attack. The attack is what the file starts. I initially focused on the document, and
the interesting evidence was the script host it spawned and the registry value it wrote. Since then I read
the process tree before the file properties.

## Skills demonstrated

`malicious document triage` · `sandbox report reading` · `process lineage analysis` · `C2 identification` ·
`persistence analysis` · `second-victim discovery` · `containment planning`
