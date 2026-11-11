#!/usr/bin/env python3
"""Tests for analyze.py — run with: python -m unittest discover -s . -p "test_*.py"
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "analyze.py"
SAMPLE = HERE / "sample_access.log"


def run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        cwd=HERE,
    )


class TestParsing(unittest.TestCase):
    def test_sample_file_exists(self) -> None:
        self.assertTrue(SAMPLE.exists(), "sample_access.log is part of the deliverable")

    def test_reports_request_count(self) -> None:
        result = run([str(SAMPLE), "--json"])
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertGreater(data["requests"], 0)
        self.assertEqual(data["skipped_lines"], 0, "every sample line must parse")

    def test_flags_command_injection(self) -> None:
        result = run([str(SAMPLE), "--json"])
        data = json.loads(result.stdout)
        findings = {f for item in data["flagged_requests"] for f in item["findings"]}
        self.assertIn("os-command", findings)

    def test_flags_sql_injection_and_traversal(self) -> None:
        result = run([str(SAMPLE), "--json"])
        data = json.loads(result.stdout)
        findings = {f for item in data["flagged_requests"] for f in item["findings"]}
        self.assertIn("sql-injection", findings)
        self.assertIn("path-traversal", findings)

    def test_login_post_count(self) -> None:
        result = run([str(SAMPLE), "--json"])
        data = json.loads(result.stdout)
        total_posts = sum(count for _, count in data["login_posts"])
        self.assertGreaterEqual(total_posts, 5, "sample contains a brute-force burst")

    def test_tool_user_agent_detected(self) -> None:
        result = run([str(SAMPLE), "--json"])
        data = json.loads(result.stdout)
        agents = " ".join(agent for agent, _ in data["tool_agents"]).lower()
        self.assertTrue("nikto" in agents or "curl" in agents)


class TestEdgeCases(unittest.TestCase):
    def test_missing_file_returns_error(self) -> None:
        result = run(["does-not-exist.log"])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("File not found", result.stderr)

    def test_unparsable_file_returns_error(self) -> None:
        with tempfile.NamedTemporaryFile("w", suffix=".log", delete=False) as handle:
            handle.write("this is not an access log line\n")
            path = handle.name
        try:
            result = run([path])
            self.assertNotEqual(result.returncode, 0)
        finally:
            Path(path).unlink(missing_ok=True)

    def test_no_secrets_in_sample(self) -> None:
        """The sample must never contain a real-looking credential.

        The needle is built at runtime so this test file does not itself trip the
        repository secret scan in CI.
        """
        text = SAMPLE.read_text(encoding="utf-8", errors="replace")
        needle_plain = "P" + chr(64) + "ss"
        needle_encoded = "P" + "%40" + "ss"
        self.assertNotIn(needle_plain, text)
        self.assertNotIn(needle_encoded, text)
        self.assertIn("PASSWORD_REDACTED", text)


if __name__ == "__main__":
    unittest.main()
