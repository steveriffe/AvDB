"""
Unit test for historical airline alliance timelines and brand logos
"""
import sys
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from app.utils.alliances import (
    get_carrier_alliance,
    get_alliance_carriers,
    get_all_alliances_for_year,
    get_carrier_logo_url,
    get_carrier_alliance_timeline
)

def test_alliance_transitions():
    # SAS: Star Alliance 1997 -> SkyTeam 2024
    sk_2023 = get_carrier_alliance("SK", 2023)
    assert sk_2023 is not None
    assert sk_2023["alliance_name"] == "Star Alliance"

    sk_2025 = get_carrier_alliance("SK", 2025)
    assert sk_2025 is not None
    assert sk_2025["alliance_name"] == "SkyTeam"

    # Aer Lingus: oneworld 2000-2007 -> Independent
    ei_2005 = get_carrier_alliance("EI", 2005)
    assert ei_2005 is not None
    assert ei_2005["alliance_name"] == "oneworld"

    ei_2015 = get_carrier_alliance("EI", 2015)
    assert ei_2015 is None

    # Continental: Wings (2002) -> SkyTeam (2006) -> Star (2010)
    co_2002 = get_carrier_alliance("CO", 2002)
    assert co_2002 is not None and co_2002["alliance_name"] == "Wings Alliance"

    co_2006 = get_carrier_alliance("CO", 2006)
    assert co_2006 is not None and co_2006["alliance_name"] == "SkyTeam"

    co_2010 = get_carrier_alliance("CO", 2010)
    assert co_2010 is not None and co_2010["alliance_name"] == "Star Alliance"

    # US Airways: Star (2008) -> oneworld (2014)
    us_2008 = get_carrier_alliance("US", 2008)
    assert us_2008 is not None and us_2008["alliance_name"] == "Star Alliance"

    us_2014 = get_carrier_alliance("US", 2014)
    assert us_2014 is not None and us_2014["alliance_name"] == "oneworld"

    # Logos
    as_logo = get_carrier_logo_url("AS")
    assert as_logo is not None and "Alaska_Airlines" in as_logo

    # Timeline
    sk_timeline = get_carrier_alliance_timeline("SK")
    assert len(sk_timeline) == 2
    assert sk_timeline[0]["alliance_name"] == "Star Alliance"
    assert sk_timeline[1]["alliance_name"] == "SkyTeam"

    print("✅ All historical alliance transition tests passed!")

if __name__ == "__main__":
    test_alliance_transitions()

