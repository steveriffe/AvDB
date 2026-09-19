"""
Unit Tests for AvDB Frequent Flyer Program (FFP) Reference Data & Bilateral Partnerships
Validates program metadata, status tier hierarchies, elite qualification, bilateral partnership webs,
and vector logo availability for all 11 major and predecessor US airlines.
"""
import sys
from pathlib import Path

# Add project root
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from app.data.ref_ffp_partnerships import (
    PROGRAMS,
    CARRIER_TO_PROGRAM,
    BILATERAL_PARTNERSHIPS,
    CURATED_CASE_STUDIES,
    get_all_programs,
    get_program_by_id,
    get_program_by_carrier,
    get_tiers_for_program,
    get_partnerships_for_year,
    get_partnerships_for_carrier,
    get_active_programs_for_year,
    get_curated_case_studies,
)
from app.data.ref_logos_svg import get_vector_logo_data_uri


def test_required_programs_exist():
    """Verify all 11 specified programs and their historical predecessors are cataloged."""
    expected_carriers = {"AS", "NW", "CO", "HP", "US", "TW", "DL", "AA", "UA", "EA", "PA"}
    found_carriers = {p["carrier_code"] for p in PROGRAMS.values()}
    
    missing = expected_carriers - found_carriers
    assert not missing, f"Missing required carrier loyalty programs: {missing}"

    # Verify CARRIER_TO_PROGRAM mapping covers all expected
    for carrier in expected_carriers:
        assert carrier in CARRIER_TO_PROGRAM, f"Carrier {carrier} missing from CARRIER_TO_PROGRAM lookup"
        prog = get_program_by_carrier(carrier)
        assert prog is not None, f"get_program_by_carrier('{carrier}') returned None"
        assert prog["carrier_code"] == carrier


def test_program_schema_and_status_tiers():
    """Verify each program schema integrity and elite tier hierarchy completeness."""
    for prog_id, prog in PROGRAMS.items():
        assert "program_id" in prog
        assert "program_name" in prog
        assert "carrier_code" in prog
        assert "carrier_name" in prog
        assert "founded_year" in prog
        assert isinstance(prog["founded_year"], int)
        assert "is_active" in prog
        assert "currency_name" in prog
        assert "lineage_summary" in prog
        assert len(prog["lineage_summary"]) > 50, f"Lineage summary too brief for {prog_id}"

        # Status tiers
        tiers = prog.get("status_tiers", [])
        assert len(tiers) >= 2, f"Program {prog_id} must have at least 2 status tiers (got {len(tiers)})"

        prev_level = 0
        for tier in tiers:
            assert "tier_name" in tier
            assert "tier_level" in tier
            assert tier["tier_level"] > prev_level, f"Tier levels must increase monotonically in {prog_id}"
            prev_level = tier["tier_level"]

            assert "upgrade_window" in tier
            assert len(tier["upgrade_window"]) > 0
            assert "bonus_miles_pct" in tier
            assert tier["bonus_miles_pct"] >= 0
            assert "baggage_allowance" in tier
            assert "lounge_access" in tier
            assert "priority_services" in tier


def test_bilateral_partnerships_completeness():
    """Verify bilateral partnership dataset captures historical webs and required key scenarios."""
    assert len(BILATERAL_PARTNERSHIPS) >= 15, f"Expected at least 15 bilateral partnerships, found {len(BILATERAL_PARTNERSHIPS)}"

    # Check key required historical scenarios:
    # 1. Alaska Airlines simultaneous multi-carrier independence (CO, NW, DL, AA)
    as_partners = get_partnerships_for_carrier("AS")
    as_partner_codes = {p["carrier_1"] if p["carrier_2"] == "AS" else p["carrier_2"] for p in as_partners}
    assert "CO" in as_partner_codes, "Missing Alaska-Continental partnership"
    assert "NW" in as_partner_codes, "Missing Alaska-Northwest partnership"
    assert "DL" in as_partner_codes, "Missing Alaska-Delta partnership"
    assert "AA" in as_partner_codes, "Missing Alaska-American partnership"

    # 2. America West & Continental Phoenix Axis
    hp_co = [p for p in BILATERAL_PARTNERSHIPS if (p["carrier_1"] == "HP" and p["carrier_2"] == "CO") or (p["carrier_1"] == "CO" and p["carrier_2"] == "HP")]
    assert len(hp_co) == 1, "Missing America West & Continental partnership"
    assert hp_co[0]["start_year"] == 1994
    assert hp_co[0]["end_year"] == 2002
    assert hp_co[0]["elite_reciprocity"] is True

    # 3. Continental & Northwest Wings Alliance
    co_nw = [p for p in BILATERAL_PARTNERSHIPS if (p["carrier_1"] == "CO" and p["carrier_2"] == "NW") or (p["carrier_1"] == "NW" and p["carrier_2"] == "CO")]
    assert len(co_nw) == 1, "Missing Continental & Northwest Wings Alliance"
    assert co_nw[0]["start_year"] == 1998
    assert co_nw[0]["end_year"] == 2008
    assert co_nw[0]["elite_reciprocity"] is True

    # 4. Delta & Alaska Seattle Hub Battle / Split
    dl_as = [p for p in BILATERAL_PARTNERSHIPS if (p["carrier_1"] == "DL" and p["carrier_2"] == "AS") or (p["carrier_1"] == "AS" and p["carrier_2"] == "DL")]
    assert len(dl_as) == 1, "Missing Delta & Alaska partnership"
    assert dl_as[0]["end_year"] == 2017

    # 5. US Airways BA -> Star Alliance -> oneworld
    us_partnerships = get_partnerships_for_carrier("US")
    us_p_ids = {p["partnership_id"] for p in us_partnerships}
    assert "US_BA_1993_1999" in us_p_ids, "Missing US Airways-British Airways alliance"
    assert "US_STAR_2004_2014" in us_p_ids, "Missing US Airways-Star Alliance era"
    assert "US_ONEWORLD_2014_2015" in us_p_ids, "Missing US Airways-oneworld integration"

    # 6. Eastern & Continental Texas Air OnePass
    ea_co = [p for p in BILATERAL_PARTNERSHIPS if (p["carrier_1"] == "EA" and p["carrier_2"] == "CO") or (p["carrier_1"] == "CO" and p["carrier_2"] == "EA")]
    assert len(ea_co) == 1, "Missing Eastern & Continental Texas Air OnePass"
    assert ea_co[0]["start_year"] == 1987
    assert ea_co[0]["end_year"] == 1991


def test_temporal_queries_and_filters():
    """Verify temporal year filtering dynamically identifies active programs and partnerships."""
    # In 1990: Eastern (EA) and Pan Am (PA) should be active; US Airways active; Northwest active.
    active_1990 = {p["carrier_code"] for p in get_active_programs_for_year(1990)}
    assert "EA" in active_1990, "Eastern should be active in 1990"
    assert "PA" in active_1990, "Pan Am should be active in 1990"
    assert "CO" in active_1990, "Continental should be active in 1990"

    # In 2024: EA, PA, TW, HP, NW, CO, US should NOT be active
    active_2024 = {p["carrier_code"] for p in get_active_programs_for_year(2024)}
    historical_carriers = {"EA", "PA", "TW", "HP", "NW", "CO", "US"}
    overlap = active_2024.intersection(historical_carriers)
    assert not overlap, f"Historical carriers marked active in 2024: {overlap}"
    assert {"AA", "DL", "UA", "AS"}.issubset(active_2024)

    # Partnerships in 2000 for Alaska Airlines
    as_2000 = get_partnerships_for_year(2000, carrier_code="AS")
    as_2000_partners = {p["carrier_1"] if p["carrier_2"] == "AS" else p["carrier_2"] for p in as_2000}
    # In 2000, Alaska was simultaneously partnered with CO, NW, and AA!
    assert "CO" in as_2000_partners, "Alaska should have active CO partnership in 2000"
    assert "NW" in as_2000_partners, "Alaska should have active NW partnership in 2000"
    assert "AA" in as_2000_partners, "Alaska should have active AA partnership in 2000"


def test_curated_case_studies():
    """Verify curated case studies are properly structured and detailed."""
    cases = get_curated_case_studies()
    assert len(cases) >= 5, f"Expected at least 5 case studies, got {len(cases)}"
    for cs in cases:
        assert "case_id" in cs
        assert "title" in cs
        assert "subtitle" in cs
        assert "narrative" in cs
        assert "key_takeaways" in cs
        assert len(cs["key_takeaways"]) >= 2
        assert len(cs["narrative"]) > 200, f"Case study {cs['case_id']} narrative too short"


def test_vector_logos_for_all_ffp_carriers():
    """Verify vector SVG logo data URIs generate crisply for every loyalty carrier."""
    carriers = ["AS", "NW", "CO", "HP", "US", "TW", "DL", "AA", "UA", "EA", "PA"]
    for c in carriers:
        uri = get_vector_logo_data_uri(c)
        assert uri.startswith("data:image/svg+xml;base64,"), f"Invalid SVG data URI for {c}"
        assert len(uri) > 100, f"Data URI suspiciously short for {c}"


if __name__ == "__main__":
    print("Testing FFP reference data and bilateral partnerships...")
    test_required_programs_exist()
    print("✅ test_required_programs_exist passed")
    test_program_schema_and_status_tiers()
    print("✅ test_program_schema_and_status_tiers passed")
    test_bilateral_partnerships_completeness()
    print("✅ test_bilateral_partnerships_completeness passed")
    test_temporal_queries_and_filters()
    print("✅ test_temporal_queries_and_filters passed")
    test_curated_case_studies()
    print("✅ test_curated_case_studies passed")
    test_vector_logos_for_all_ffp_carriers()
    print("✅ test_vector_logos_for_all_ffp_carriers passed")
    print("🎉 All FFP partnership unit tests passed successfully!")
