"""
Unit test for Flighty CSV ingestion and subfleet taxonomy
"""
import sys
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import app.utils.flighty as flighty

def test_subfleet_classification():
    assert flighty.classify_aircraft("Boeing 737-900ER")["subfleet"] == "Boeing 737-900ER"
    assert flighty.classify_aircraft("Boeing 737-900ER")["generation"] == "737 NextGen"
    assert flighty.classify_aircraft("Boeing 737 MAX 9")["subfleet"] == "Boeing 737 MAX 9"
    assert flighty.classify_aircraft("Boeing 737 MAX 9")["generation"] == "737 MAX"
    assert flighty.classify_aircraft("Airbus A321neo")["subfleet"] == "Airbus A321neo"
    assert flighty.classify_aircraft("Airbus A321neo")["generation"] == "A320neo"
    assert flighty.classify_aircraft("Embraer E175")["subfleet"] == "Embraer E175"
    assert flighty.classify_aircraft("Embraer E175")["category"] == "Regional Jet"

def test_sample_flighty_generation():
    df = flighty.generate_sample_flighty_data()
    assert len(df) == 30
    assert "aircraft_subfleet" in df.columns
    assert "aircraft_generation" in df.columns
    assert "aircraft_family" in df.columns
    assert "origin_lat" in df.columns
    assert "dest_lat" in df.columns
    assert "distance_miles" in df.columns
    deck = flighty.build_flighty_travel_deck(df, home_airport="SEA")
    assert deck is not None
    print(f"✅ Flighty test passed! Parsed {len(df)} flights with {df['aircraft_subfleet'].nunique()} unique subfleets.")

if __name__ == "__main__":
    test_subfleet_classification()
    test_sample_flighty_generation()

