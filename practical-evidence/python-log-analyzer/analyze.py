#!/usr/bin/env python3
"""Access-log analyser for first-pass web attack triage.

Reads an Apache/Nginx "combined" style access log and prints a short triage report:

    1. volume overview
    2. top source addresses
    3. user-agent split (tools vs people)
    4. busiest request paths
    5. status code distribution
    6. login-endpoint POST counts (brute-force hint)
    7. requests whose query string looks like an attack payload

The goal is to answer "where do I start reading" in a few seconds, not to replace an analyst.

Usage:
    python analyze.py sample_access.log
    python analyze.py sample_access.log --top 5
    python analyze.py sample_access.log --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote

COMBINED = re.compile(
    r'^(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] '
    r'"(?P<method>[A-Z]+) (?P<target>\S+) (?P<proto>[^"]+)" '
    r'(?P<status>\d{3}) (?P<size>\S+) '
    r'"(?P<referer>[^"]*)" "(?P<agent>[^"]*)"'
)

TOOL_AGENTS = (
    "nikto", "sqlmap", "dirb", "gobuster", "wfuzz", "nmap", "masscan",
    "hydra", "curl/", "wget/", "python-requests", "go-http-client", "zgrab",
)

PAYLOAD_PATTERNS = {
    "os-command": re.compile(r"(system\(|exec\(|passthru\(|shell_exec\(|`|\|\s*(nc|bash|sh)\b)", re.I),
    "sql-injection": re.compile(r"(union\s+select|or\s+1=1|sleep\(|benchmark\(|information_schema)", re.I),
    "path-traversal": re.compile(r"(\.\./|\.\.\\|%2e%2e)", re.I),
    "xss": re.compile(r"(<script|onerror\s*=|javascript:)", re.I),
    "sensitive-file": re.compile(r"(\.bash_history|\.git/config|\.env|wp-config\.php|/etc/passwd)", re.I),
    "account-creation": re.compile(r"(net\s+user|useradd|adduser|net\s+localgroup)", re.I),
}

LOGIN_HINT = re.compile(r"(login|signin|auth|session)", re.I)


@dataclass
class Entry:
    ip: str
    time: str
    method: str
    target: str
    status: str
    size: str
    agent: str
    findings: list[str] = field(default_factory=list)


def parse(path: Path) -> tuple[list[Entry], int]:
    entries: list[Entry] = []
    skipped = 0
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            match = COMBINED.match(line.strip())
            if not match:
                skipped += 1
                continue
            entry = Entry(
                ip=match["ip"],
                time=match["time"],
                method=match["method"],
                target=match["target"],
                status=match["status"],
                size=match["size"],
                agent=match["agent"],
            )
            decoded = unquote(entry.target)
            for name, pattern in PAYLOAD_PATTERNS.items():
                if pattern.search(decoded):
                    entry.findings.append(name)
            entries.append(entry)
    return entries, skipped


def is_tool(agent: str) -> bool:
    low = agent.lower()
    return any(token in low for token in TOOL_AGENTS)


def bar(count: int, biggest: int, width: int = 28) -> str:
    if biggest <= 0:
        return ""
    filled = max(1, round(count / biggest * width))
    return "#" * filled


def report(entries: list[Entry], skipped: int, top: int, as_json: bool) -> int:
    if not entries:
        print("No parsable log lines found.", file=sys.stderr)
        return 1

    ips = Counter(e.ip for e in entries)
    agents = Counter(e.agent for e in entries)
    paths = Counter(e.target.split("?")[0] for e in entries)
    statuses = Counter(e.status for e in entries)
    logins = Counter(e.ip for e in entries if e.method == "POST" and LOGIN_HINT.search(e.target))
    flagged = [e for e in entries if e.findings]
    tools = [(a, c) for a, c in agents.items() if is_tool(a)]

    summary = {
        "requests": len(entries),
        "skipped_lines": skipped,
        "unique_ips": len(ips),
        "top_ips": ips.most_common(top),
        "tool_agents": sorted(tools, key=lambda x: -x[1])[:top],
        "top_paths": paths.most_common(top),
        "statuses": statuses.most_common(),
        "login_posts": logins.most_common(top),
        "flagged_requests": [
            {"ip": e.ip, "method": e.method, "target": e.target[:120], "findings": e.findings}
            for e in flagged
        ],
        "busiest_ip_share": round(ips.most_common(1)[0][1] / len(entries) * 100, 1),
    }

    if as_json:
        print(json.dumps(summary, indent=2))
        return 0

    line = "=" * 66
    print(line)
    print(f" ACCESS LOG TRIAGE  file={summary['requests']} requests, {summary['unique_ips']} source IPs")
    print(line)

    print("\n[1] VOLUME")
    print(f"    parsable requests : {len(entries)}")
    print(f"    skipped lines     : {skipped}")
    print(f"    unique sources    : {len(ips)}")
    print(f"    busiest source    : {ips.most_common(1)[0][0]} "
          f"({summary['busiest_ip_share']}% of all requests)")

    print(f"\n[2] TOP {top} SOURCE ADDRESSES")
    biggest = ips.most_common(1)[0][1]
    for ip, count in ips.most_common(top):
        print(f"    {count:>6}  {bar(count, biggest)}  {ip}")

    print(f"\n[3] USER AGENTS THAT ARE TOOLS")
    if tools:
        for agent, count in sorted(tools, key=lambda x: -x[1])[:top]:
            print(f"    {count:>6}  {agent[:70]}")
    else:
        print("    none detected")

    print(f"\n[4] TOP {top} PATHS")
    for path, count in paths.most_common(top):
        print(f"    {count:>6}  {path[:70]}")

    print("\n[5] STATUS CODES")
    for status, count in statuses.most_common():
        print(f"    {count:>6}  {status}")

    print("\n[6] POST REQUESTS TO LOGIN-LIKE PATHS")
    if logins:
        for ip, count in logins.most_common(top):
            print(f"    {count:>6}  {ip}   (brute-force hint when this is high in a short window)")
    else:
        print("    none")

    print(f"\n[7] REQUESTS WITH ATTACK-LIKE PAYLOADS ({len(flagged)})")
    if flagged:
        for entry in flagged[:top]:
            print(f"    {entry.ip:<16} {entry.method:<5} {','.join(entry.findings):<20} {entry.target[:60]}")
    else:
        print("    none")

    print("\n" + line)
    print(" Read order: start with [7], then [3] and [6], then the busiest source in [2].")
    print(line)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="First-pass access log triage.")
    parser.add_argument("logfile", type=Path, help="path to an Apache/Nginx combined access log")
    parser.add_argument("--top", type=int, default=10, help="how many rows per section (default 10)")
    parser.add_argument("--json", action="store_true", help="print JSON instead of tables")
    args = parser.parse_args()

    if not args.logfile.exists():
        print(f"File not found: {args.logfile}", file=sys.stderr)
        return 1

    entries, skipped = parse(args.logfile)
    return report(entries, skipped, args.top, args.json)


if __name__ == "__main__":
    raise SystemExit(main())
