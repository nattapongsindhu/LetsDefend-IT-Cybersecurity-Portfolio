# Certificates

This folder holds the certificate images earned through the learning paths, plus the credential links.

## Status

Certificate images are being added as they are downloaded from the platform dashboards. The table below
is the register; when an image is added, the file column is filled in.

| Certificate / Badge | Platform | Issued | Image | Verify |
| :--- | :--- | :--- | :--- | :--- |
| SOC Analyst Learning Path | LetsDefend | 2026 | [transcript screenshot](letsdefend-transcript.png) | [gnopattan](https://app.letsdefend.io/user/gnopattan) |
| Pre Security | TryHackMe | 2026 | *pending download* | [THM profile](https://tryhackme.com/p/nattapongsindhu) |
| SOC Level 1 | TryHackMe | 2026 | *pending download* | [THM profile](https://tryhackme.com/p/nattapongsindhu) |

## LetsDefend transcript, in numbers

The screenshot in this folder is the platform transcript for the account the path was completed on.

| Metric | Value |
| :--- | ---: |
| Score | **2,160 points** |
| SLA | **51** |
| Success rate | **100 %** |
| Investigated alert types | Exchange, Proxy, Mobile, Threat Intel, Malware, Ransomware, Brute Force, Web Attack, Generic, Unauthorized Access, LOLBin, Data Leakage, Persistence, C2, Privilege Escalation, APT Group |
| Most recent badge | Brute Force — 11 Nov 2026 |

The radar chart is the useful part for a reviewer: it shows the breadth of alert types actually worked, not
just a single score.

## How to add an image

1. Download the certificate from the platform dashboard as PNG or PDF.
2. If it is a PDF, export page one to PNG at 1600 px wide.
3. Crop to the certificate border, keep the text readable.
4. Name the file with the platform and path, for example `letsdefend-soc-analyst-path.png`.
5. Place it in this folder and update the table above.
6. Check that the image contains no session token, email address you do not want public, or dashboard
   chrome from the browser.

## Naming convention

```text
letsdefend-<path-name>.png
tryhackme-<path-name>.png
badge-<name>.png
```

Lowercase, hyphens instead of spaces, no dates in the filename — the table carries the date.

## Note on verification

A certificate image can be edited; a profile link cannot. That is why every row links to the platform
profile as the primary source of truth, with the image as supporting evidence.
