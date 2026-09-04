import sys
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from app.data.ref_aircraft_specs import get_aircraft_spec, AIRCRAFT_SPECS


def test_aircraft_specs():
    assert len(AIRCRAFT_SPECS) >= 10
    
    spec_739 = get_aircraft_spec("Boeing 737-900ER")
    assert spec_739 is not None
    assert spec_739["range_miles"] == 2950
    assert "UA" in spec_739["key_operators"]
    
    spec_a321 = get_aircraft_spec("Airbus A321neo")
    assert spec_a321 is not None
    assert spec_a321["range_miles"] == 4000
    assert "DL" in spec_a321["key_operators"]

    spec_e175 = get_aircraft_spec("Embraer E175")
    assert spec_e175 is not None
    assert spec_e175["category"] == "Regional Jet"


if __name__ == "__main__":
    test_aircraft_specs()
    print("✅ Aircraft specifications tests passed!")
