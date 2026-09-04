import sys
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from app.utils.mergers import (
    get_all_ancestor_codes,
    get_ultimate_successor,
    enrich_historical_route_service
)


def test_merger_ancestor_chains():
    # AA should trace back to US, HP, QQ, and TW
    aa_ancestors = get_all_ancestor_codes("AA")
    assert "US" in aa_ancestors, f"Expected US in AA ancestors, got {aa_ancestors}"
    assert "HP" in aa_ancestors, f"Expected HP in AA ancestors, got {aa_ancestors}"
    assert "QQ" in aa_ancestors, f"Expected QQ in AA ancestors, got {aa_ancestors}"
    assert "TW" in aa_ancestors, f"Expected TW in AA ancestors, got {aa_ancestors}"

    # DL should trace back to NW
    dl_ancestors = get_all_ancestor_codes("DL")
    assert "NW" in dl_ancestors, f"Expected NW in DL ancestors, got {dl_ancestors}"

    # UA should trace back to CO
    ua_ancestors = get_all_ancestor_codes("UA")
    assert "CO" in ua_ancestors, f"Expected CO in UA ancestors, got {ua_ancestors}"

    # Reno Air (QQ) ultimate successor should be AA
    qq_succ = get_ultimate_successor("QQ")
    assert qq_succ is not None and qq_succ["successor_code"] == "AA"

    # America West (HP) ultimate successor should be AA (via US)
    hp_succ = get_ultimate_successor("HP")
    assert hp_succ is not None and hp_succ["successor_code"] == "AA"


def test_historical_route_enrichment():
    # ANC -> DTW previously flown by DL should tag NW/DL due to DTW hub heritage
    anc_dtw = enrich_historical_route_service("ANC", "DTW", 2021, "DL")
    assert "NW/DL" in anc_dtw
    assert "2021" in anc_dtw

    # ANC -> IAH previously flown by UA should tag CO/UA due to IAH hub heritage
    anc_iah = enrich_historical_route_service("ANC", "IAH", 2020, "UA")
    assert "CO/UA" in anc_iah
    assert "2020" in anc_iah

    # Never flown route
    unflown = enrich_historical_route_service("ANC", "MCO", None, None)
    assert "Never Flown Nonstop" in unflown


if __name__ == "__main__":
    test_merger_ancestor_chains()
    test_historical_route_enrichment()
    print("✅ All merger lineage and historical route tests passed!")
