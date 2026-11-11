#!/usr/bin/env python3
"""Lint the detection rules in detection-engineering/README.md.

There is no SIEM in this repository, so these tests do not prove a rule fires.
What they prove is that each rule is structurally valid and still tied to the
case it came from: the YAML parses, the required Sigma keys exist, the ATT&CK
tags are well formed, and the SPL and KQL blocks still reference the tables the
rule depends on.

Run: python -m unittest discover -s detection-engineering/tests -p "test_*.py"
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

import yaml

README = Path(__file__).resolve().parents[1] / "README.md"
TEXT = README.read_text(encoding="utf-8")

REQUIRED_SIGMA_KEYS = {"title", "logsource", "detection", "level"}
VALID_LEVELS = {"informational", "low", "medium", "high", "critical"}
ATTACK_TAG = re.compile(r"^attack\.(t\d{4}(\.\d{3})?|[a-z-]+)$")


def fenced_blocks(language: str) -> list[str]:
    pattern = re.compile(rf"```{language}\n(.*?)```", re.DOTALL)
    return [block.strip() for block in pattern.findall(TEXT)]


class TestSigmaRule(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        blocks = fenced_blocks("yaml")
        assert blocks, "no yaml block found in the detection README"
        cls.raw = blocks[0]
        cls.rule = yaml.safe_load(cls.raw)

    def test_yaml_parses_to_mapping(self) -> None:
        self.assertIsInstance(self.rule, dict)

    def test_required_keys(self) -> None:
        missing = REQUIRED_SIGMA_KEYS - set(self.rule)
        self.assertFalse(missing, f"missing required Sigma keys: {sorted(missing)}")

    def test_has_condition(self) -> None:
        self.assertIn("condition", self.rule["detection"])

    def test_level_is_valid(self) -> None:
        self.assertIn(self.rule["level"], VALID_LEVELS)

    def test_logsource_is_specific(self) -> None:
        logsource = self.rule["logsource"]
        self.assertIn("category", logsource, "a Sigma rule without a category matches too much")

    def test_attack_tags_are_well_formed(self) -> None:
        tags = [t for t in self.rule.get("tags", []) if str(t).startswith("attack.")]
        self.assertTrue(tags, "at least one ATT&CK tag is required")
        for tag in tags:
            self.assertRegex(tag, ATTACK_TAG)

    def test_lists_a_false_positive_section(self) -> None:
        self.assertIn("falsepositives", self.rule, "every rule needs its known noise written down")

    def test_references_lead_to_the_case(self) -> None:
        """The rule must point at portfolio evidence, not just at ATT&CK."""
        text = " ".join(self.rule.get("references", []))
        self.assertIn("../practical-evidence/", text)


class TestSplRule(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        blocks = fenced_blocks("spl")
        assert blocks, "no spl block found"
        cls.rule = blocks[0]

    def test_targets_a_named_index(self) -> None:
        self.assertIn("index=", self.rule)

    def test_uses_an_aggregation(self) -> None:
        self.assertIn("stats", self.rule, "without stats this is a search, not a detection")

    def test_has_a_threshold(self) -> None:
        self.assertRegex(self.rule, r"where attempts >= \d+")

    def test_excludes_common_ports(self) -> None:
        self.assertRegex(self.rule, r"NOT \(dest_port IN \([0-9, ]+\)\)")


class TestKqlRule(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        blocks = fenced_blocks("kusto")
        assert blocks, "no kusto block found"
        cls.rule = blocks[0]

    def test_uses_mail_and_device_tables(self) -> None:
        self.assertIn("EmailEvents", self.rule)
        self.assertIn("DeviceNetworkEvents", self.rule)

    def test_correlates_on_time(self) -> None:
        self.assertIn("between", self.rule, "a correlation rule must bound the time window")

    def test_states_its_own_weakness(self) -> None:
        """The README must warn that the join key is a placeholder."""
        self.assertIn("placeholder", TEXT)


if __name__ == "__main__":
    unittest.main()
