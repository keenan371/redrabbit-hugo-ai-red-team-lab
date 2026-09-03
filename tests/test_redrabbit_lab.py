"""Test-first behavioral coverage for the safe local RedRabbit vs. Hugo lab."""

import json
import tempfile
import unittest
from pathlib import Path

from redrabbit_agent.runner import run_safe_demo


class RedRabbitLabTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_hardened_demo_refuses_every_fixed_safe_test_without_protected_values(self):
        report = run_safe_demo("hardened", self.root)

        self.assertEqual(report["summary"]["total"], 4)
        self.assertEqual(report["summary"]["passed"], 4)
        self.assertEqual(report["summary"]["failed"], 0)
        for result in report["results"]:
            self.assertEqual(result["actual_behavior"], "refuse_and_log")
            self.assertTrue(result["passed"])
            self.assertNotIn("MOCK_SYSTEM_INSTRUCTIONS", result["response"])
            self.assertNotIn("RR-MOCK", result["response"])

    def test_baseline_demo_records_controlled_mock_failures(self):
        report = run_safe_demo("baseline", self.root)

        self.assertEqual(report["summary"]["total"], 4)
        self.assertEqual(report["summary"]["failed"], 4)
        self.assertEqual(report["summary"]["passed"], 0)
        self.assertTrue(all(item["actual_behavior"] == "simulated_disclosure" for item in report["results"]))

    def test_demo_writes_real_jsonl_events_and_result_document(self):
        report = run_safe_demo("hardened", self.root)
        events = self.root / "events" / f"{report['scan_id']}.jsonl"
        results = self.root / "results" / f"{report['scan_id']}.json"

        self.assertTrue(events.exists())
        self.assertTrue(results.exists())
        event_types = [json.loads(line)["event_type"] for line in events.read_text(encoding="utf-8").splitlines()]
        self.assertIn("scan_started", event_types)
        self.assertIn("redrabbit_test_sent", event_types)
        self.assertIn("hugo_decision", event_types)
        self.assertIn("redrabbit_evaluation", event_types)
        self.assertIn("scan_completed", event_types)


if __name__ == "__main__":
    unittest.main()
