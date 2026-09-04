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

def test_flighty_analytics():
    # Carrier normalization
    assert flighty.normalize_carrier_code("Alaska Airlines", "AS 12") == "AS"
    assert flighty.normalize_carrier_code("United Airlines", "UA 450") == "UA"
    assert flighty.normalize_carrier_code("Delta Air Lines", "DL 1184") == "DL"
    assert flighty.normalize_carrier_code("British Airways", "BA 49") == "BA"

    # Seat placement
    assert flighty.classify_seat_position("2A") == "Window"
    assert flighty.classify_seat_position("15K") == "Window"
    assert flighty.classify_seat_position("7C") == "Aisle"
    assert flighty.classify_seat_position("3D") == "Aisle"
    assert flighty.classify_seat_position("10B") == "Middle"
    assert flighty.classify_seat_position("8E") == "Middle"
    assert flighty.classify_seat_position("Any") == "Unassigned / Open"
    assert flighty.classify_seat_position("") == "Unassigned / Open"

    # Carbon emissions calculation
    co2_econ = flighty.calculate_flight_carbon_footprint(1000, "Economy", "Mainline Narrowbody")
    co2_first = flighty.calculate_flight_carbon_footprint(1000, "First", "Mainline Narrowbody")
    assert co2_first > co2_econ
    assert co2_econ > 0

    # Sample data enrichment assertions
    df = flighty.generate_sample_flighty_data()
    assert "carrier_code" in df.columns
    assert "alliance" in df.columns
    assert "seat_position" in df.columns
    assert "co2_kg" in df.columns
    assert df["co2_kg"].sum() > 0
    assert set(df["alliance"]).issubset({"Star Alliance", "oneworld", "SkyTeam", "Independent / Unaligned"})


if __name__ == "__main__":
    test_subfleet_classification()
    test_sample_flighty_generation()
    test_flighty_analytics()
    print("✅ All Flighty subfleet, alliance, seating, and carbon analytics tests passed!")


