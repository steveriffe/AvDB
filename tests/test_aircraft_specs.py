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

    # McDonnell Douglas additions
    spec_dc9 = get_aircraft_spec("DC-9-30")
    assert spec_dc9 is not None
    assert "NW" in spec_dc9["key_operators"]
    assert spec_dc9["engines"] == "Pratt & Whitney JT8D series"

    spec_md90 = get_aircraft_spec("MD90")
    assert spec_md90 is not None
    assert "DL" in spec_md90["key_operators"]
    assert spec_md90["engines"] == "IAE V2500-D5"

    spec_dc10 = get_aircraft_spec("DC-10-30")
    assert spec_dc10 is not None
    assert "AA" in spec_dc10["key_operators"]
    assert spec_dc10["category"] == "Mainline Widebody Trijet"

    spec_md11 = get_aircraft_spec("MD11")
    assert spec_md11 is not None
    assert "FX" in spec_md11["key_operators"]
    assert spec_md11["category"] == "Mainline Widebody Trijet"


if __name__ == "__main__":
    test_aircraft_specs()
    print("✅ Aircraft specifications tests passed!")
