"""
AvDB Fleet Specifications & BTS Description Resolution Tests
Validates technical engineering parameters, operator alignments, verified photography,
and fuzzy BTS description matching for the expanded McDonnell Douglas and Douglas fleet families.
"""
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from app.data.ref_aircraft_specs import get_aircraft_spec, AIRCRAFT_SPECS


class TestFleetSpecs(unittest.TestCase):
    """Test suite for expanded McDonnell Douglas / Douglas fleet specifications."""

    def test_dc9_spec_and_matching(self):
        """Verify DC-9 Family technical specifications and BTS description matching."""
        # 1. Direct dictionary inspection
        self.assertIn("McDonnell Douglas DC-9 Family", AIRCRAFT_SPECS)
        spec = AIRCRAFT_SPECS["McDonnell Douglas DC-9 Family"]
        self.assertEqual(spec["family"], "McDonnell Douglas Series")
        self.assertEqual(spec["category"], "Mainline Narrowbody")
        self.assertEqual(spec["seats_typical"], "90 - 135 seats")
        self.assertEqual(spec["engines"], "Pratt & Whitney JT8D series")
        self.assertIn("NW", spec["key_operators"])
        self.assertIn("DL", spec["key_operators"])
        self.assertIn("EA", spec["key_operators"])
        self.assertIn("CO", spec["key_operators"])
        self.assertIn("OZ", spec["key_operators"])
        self.assertIn("RC", spec["key_operators"])
        self.assertIn("FL", spec["key_operators"])
        self.assertTrue(spec["photo_url"].startswith("https://"))
        self.assertIn("CC", spec["photo_license"])
        self.assertTrue(len(spec["photo_credit"]) > 0)

        # 2. Fuzzy matching typical BTS and historical labels
        test_labels = [
            "DC-9",
            "DC9",
            "D9S",
            "DC-9-30",
            "DC-9-10",
            "DC-9-50",
            "DC9-30",
            "DC9-50",
            "D93",
            "D95",
            "McDonnell Douglas DC-9",
            "Douglas DC-9-30",
            "McDonnell Douglas DC-9-10/20/30/40/50",
        ]
        for label in test_labels:
            matched = get_aircraft_spec(label)
            self.assertIsNotNone(matched, f"Failed to match DC-9 label: '{label}'")
            self.assertEqual(
                matched["engines"],
                "Pratt & Whitney JT8D series",
                f"Label '{label}' did not resolve to DC-9 Family",
            )

    def test_md90_spec_and_matching(self):
        """Verify MD-90 technical specifications and BTS description matching."""
        self.assertIn("McDonnell Douglas MD-90", AIRCRAFT_SPECS)
        spec = AIRCRAFT_SPECS["McDonnell Douglas MD-90"]
        self.assertEqual(spec["family"], "McDonnell Douglas Series")
        self.assertEqual(spec["category"], "Mainline Narrowbody")
        self.assertEqual(spec["seats_typical"], "150 - 172 seats")
        self.assertEqual(spec["engines"], "IAE V2500-D5")
        self.assertIn("DL", spec["key_operators"])
        self.assertIn("QQ", spec["key_operators"])
        self.assertIn("SK", spec["key_operators"])
        self.assertTrue(spec["photo_url"].startswith("https://"))
        self.assertIn("CC", spec["photo_license"])

        test_labels = [
            "MD-90",
            "MD90",
            "MD-90-30",
            "MD90-30",
            "McDonnell Douglas MD-90",
            "Boeing MD-90",
            "MD-90 (MD90)",
        ]
        for label in test_labels:
            matched = get_aircraft_spec(label)
            self.assertIsNotNone(matched, f"Failed to match MD-90 label: '{label}'")
            self.assertEqual(
                matched["engines"],
                "IAE V2500-D5",
                f"Label '{label}' did not resolve to MD-90",
            )

    def test_dc10_spec_and_matching(self):
        """Verify DC-10 technical specifications and BTS description matching."""
        self.assertIn("McDonnell Douglas DC-10", AIRCRAFT_SPECS)
        spec = AIRCRAFT_SPECS["McDonnell Douglas DC-10"]
        self.assertEqual(spec["family"], "McDonnell Douglas Series")
        self.assertEqual(spec["category"], "Mainline Widebody Trijet")
        self.assertEqual(spec["seats_typical"], "250 - 380 seats")
        self.assertIn("CF6", spec["engines"])
        self.assertIn("JT9D", spec["engines"])
        self.assertIn("AA", spec["key_operators"])
        self.assertIn("UA", spec["key_operators"])
        self.assertIn("NW", spec["key_operators"])
        self.assertIn("CO", spec["key_operators"])
        self.assertIn("FX", spec["key_operators"])
        self.assertTrue(spec["photo_url"].startswith("https://"))
        self.assertIn("CC", spec["photo_license"])

        test_labels = [
            "DC-10",
            "DC10",
            "D10",
            "DC-10-10",
            "DC-10-30",
            "DC-10-40",
            "DC10-30",
            "McDonnell Douglas DC-10",
            "Douglas DC-10",
            "DC-10-30/40",
            "DC-10 (D10)",
        ]
        for label in test_labels:
            matched = get_aircraft_spec(label)
            self.assertIsNotNone(matched, f"Failed to match DC-10 label: '{label}'")
            self.assertEqual(
                matched["category"],
                "Mainline Widebody Trijet",
                f"Label '{label}' did not resolve to DC-10",
            )
            self.assertIn("AA", matched["key_operators"])

    def test_md11_spec_and_matching(self):
        """Verify MD-11 technical specifications and BTS description matching."""
        self.assertIn("McDonnell Douglas MD-11", AIRCRAFT_SPECS)
        spec = AIRCRAFT_SPECS["McDonnell Douglas MD-11"]
        self.assertEqual(spec["family"], "McDonnell Douglas Series")
        self.assertEqual(spec["category"], "Mainline Widebody Trijet")
        self.assertEqual(spec["seats_typical"], "285 - 410 seats / Freighter")
        self.assertEqual(spec["engines"], "GE CF6-80C2 / PW4460")
        self.assertIn("DL", spec["key_operators"])
        self.assertIn("AA", spec["key_operators"])
        self.assertIn("FX", spec["key_operators"])
        self.assertIn("K4", spec["key_operators"])
        self.assertIn("KL", spec["key_operators"])
        self.assertIn("SR", spec["key_operators"])
        self.assertTrue(spec["photo_url"].startswith("https://"))
        self.assertIn("CC", spec["photo_license"])

        test_labels = [
            "MD-11",
            "MD11",
            "M11",
            "MD-11F",
            "MD11F",
            "McDonnell Douglas MD-11",
            "Boeing MD-11",
            "McDonnell Douglas MD-11F",
            "MD-11 (M11)",
        ]
        for label in test_labels:
            matched = get_aircraft_spec(label)
            self.assertIsNotNone(matched, f"Failed to match MD-11 label: '{label}'")
            self.assertEqual(
                matched["engines"],
                "GE CF6-80C2 / PW4460",
                f"Label '{label}' did not resolve to MD-11",
            )

    def test_collision_prevention(self):
        """Ensure DC-9 does not collide with DC-10, and MD-80/717 remain distinct."""
        # DC-10 vs DC-9 collision checks
        dc10_matched = get_aircraft_spec("DC-10")
        self.assertEqual(dc10_matched["category"], "Mainline Widebody Trijet")
        self.assertNotEqual(dc10_matched["engines"], "Pratt & Whitney JT8D series")

        dc10_label2 = get_aircraft_spec("DC10")
        self.assertEqual(dc10_label2["category"], "Mainline Widebody Trijet")

        d10_label = get_aircraft_spec("D10")
        self.assertEqual(d10_label["category"], "Mainline Widebody Trijet")

        # DC-9 check
        dc9_matched = get_aircraft_spec("DC-9")
        self.assertEqual(dc9_matched["category"], "Mainline Narrowbody")
        self.assertEqual(dc9_matched["engines"], "Pratt & Whitney JT8D series")

        # DC-9 Super 80 must resolve to MD-80 Series
        super80 = get_aircraft_spec("DC-9 Super 80")
        self.assertEqual(super80["first_flight"], 1979)
        self.assertEqual(super80["engines"], "Pratt & Whitney JT8D-217/219")

        # MD-88 check
        md88 = get_aircraft_spec("MD-88")
        self.assertEqual(md88["engines"], "Pratt & Whitney JT8D-217/219")

        # 717 check
        b717 = get_aircraft_spec("Boeing 717-200")
        self.assertEqual(b717["engines"], "Rolls-Royce BR715")


if __name__ == "__main__":
    unittest.main()
