"""
AvDB Flighty Integration & Aircraft Subfleet Engine
Parses Flighty CSV exports, manages granular aircraft subfleet hierarchies,
and enriches personal flight logs with GPS coordinates and BTS route benchmarks.
"""
import io
import math
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple

# ----------------------------------------------------------------------
# Comprehensive Subfleet & Airframe Taxonomy
# ----------------------------------------------------------------------
# Maps specific aircraft models/ICAO codes to:
# - Family (e.g. Boeing 737)
# - Generation (e.g. 737 NextGen, 737 MAX, 737 Classic)
# - Subfleet (e.g. Boeing 737-900ER, Boeing 737-800, Boeing 737 MAX 8)
# - Category (Mainline Narrowbody, Widebody, Regional Jet, Turboprop)

SUBFLEET_TAXONOMY = {
    # --- Boeing 737 Family ---
    "B731": {"family": "Boeing 737", "generation": "737 Original", "subfleet": "Boeing 737-100", "category": "Mainline Narrowbody"},
    "B732": {"family": "Boeing 737", "generation": "737 Original", "subfleet": "Boeing 737-200", "category": "Mainline Narrowbody"},
    "B733": {"family": "Boeing 737", "generation": "737 Classic", "subfleet": "Boeing 737-300", "category": "Mainline Narrowbody"},
    "B734": {"family": "Boeing 737", "generation": "737 Classic", "subfleet": "Boeing 737-400", "category": "Mainline Narrowbody"},
    "B735": {"family": "Boeing 737", "generation": "737 Classic", "subfleet": "Boeing 737-500", "category": "Mainline Narrowbody"},
    "B736": {"family": "Boeing 737", "generation": "737 NextGen", "subfleet": "Boeing 737-600", "category": "Mainline Narrowbody"},
    "B737": {"family": "Boeing 737", "generation": "737 NextGen", "subfleet": "Boeing 737-700", "category": "Mainline Narrowbody"},
    "B738": {"family": "Boeing 737", "generation": "737 NextGen", "subfleet": "Boeing 737-800", "category": "Mainline Narrowbody"},
    "B739": {"family": "Boeing 737", "generation": "737 NextGen", "subfleet": "Boeing 737-900ER", "category": "Mainline Narrowbody"},
    "B37M": {"family": "Boeing 737", "generation": "737 MAX", "subfleet": "Boeing 737 MAX 7", "category": "Mainline Narrowbody"},
    "B38M": {"family": "Boeing 737", "generation": "737 MAX", "subfleet": "Boeing 737 MAX 8", "category": "Mainline Narrowbody"},
    "B39M": {"family": "Boeing 737", "generation": "737 MAX", "subfleet": "Boeing 737 MAX 9", "category": "Mainline Narrowbody"},
    "B3XM": {"family": "Boeing 737", "generation": "737 MAX", "subfleet": "Boeing 737 MAX 10", "category": "Mainline Narrowbody"},

    # --- Airbus A320 Family ---
    "A318": {"family": "Airbus A320", "generation": "A320ceo", "subfleet": "Airbus A318", "category": "Mainline Narrowbody"},
    "A319": {"family": "Airbus A320", "generation": "A320ceo", "subfleet": "Airbus A319ceo", "category": "Mainline Narrowbody"},
    "A320": {"family": "Airbus A320", "generation": "A320ceo", "subfleet": "Airbus A320ceo", "category": "Mainline Narrowbody"},
    "A321": {"family": "Airbus A320", "generation": "A320ceo", "subfleet": "Airbus A321ceo", "category": "Mainline Narrowbody"},
    "A19N": {"family": "Airbus A320", "generation": "A320neo", "subfleet": "Airbus A319neo", "category": "Mainline Narrowbody"},
    "A20N": {"family": "Airbus A320", "generation": "A320neo", "subfleet": "Airbus A320neo", "category": "Mainline Narrowbody"},
    "A21N": {"family": "Airbus A320", "generation": "A320neo", "subfleet": "Airbus A321neo", "category": "Mainline Narrowbody"},
    "A21X": {"family": "Airbus A320", "generation": "A320neo", "subfleet": "Airbus A321XLR", "category": "Mainline Narrowbody"},

    # --- Airbus A220 Family ---
    "BCS1": {"family": "Airbus A220", "generation": "A220 Series", "subfleet": "Airbus A220-100", "category": "Mainline Narrowbody"},
    "BCS3": {"family": "Airbus A220", "generation": "A220 Series", "subfleet": "Airbus A220-300", "category": "Mainline Narrowbody"},
    "A220": {"family": "Airbus A220", "generation": "A220 Series", "subfleet": "Airbus A220-300", "category": "Mainline Narrowbody"},

    # --- Boeing 757 / 767 / 777 / 787 Widebodies ---
    "B752": {"family": "Boeing 757", "generation": "757 Standard", "subfleet": "Boeing 757-200", "category": "Mainline Narrowbody"},
    "B753": {"family": "Boeing 757", "generation": "757 Standard", "subfleet": "Boeing 757-300", "category": "Mainline Narrowbody"},
    "B762": {"family": "Boeing 767", "generation": "767 Classic", "subfleet": "Boeing 767-200ER", "category": "Widebody"},
    "B763": {"family": "Boeing 767", "generation": "767 Extended", "subfleet": "Boeing 767-300ER", "category": "Widebody"},
    "B764": {"family": "Boeing 767", "generation": "767 Extended", "subfleet": "Boeing 767-400ER", "category": "Widebody"},
    "B772": {"family": "Boeing 777", "generation": "777 Classic", "subfleet": "Boeing 777-200ER", "category": "Widebody"},
    "B77L": {"family": "Boeing 777", "generation": "777 Long Range", "subfleet": "Boeing 777-200LR", "category": "Widebody"},
    "B773": {"family": "Boeing 777", "generation": "777 Classic", "subfleet": "Boeing 777-300", "category": "Widebody"},
    "B77W": {"family": "Boeing 777", "generation": "777 Extended", "subfleet": "Boeing 777-300ER", "category": "Widebody"},
    "B779": {"family": "Boeing 777", "generation": "777X", "subfleet": "Boeing 777-9", "category": "Widebody"},
    "B788": {"family": "Boeing 787", "generation": "787 Dreamliner", "subfleet": "Boeing 787-8", "category": "Widebody"},
    "B789": {"family": "Boeing 787", "generation": "787 Dreamliner", "subfleet": "Boeing 787-9", "category": "Widebody"},
    "B78X": {"family": "Boeing 787", "generation": "787 Dreamliner", "subfleet": "Boeing 787-10", "category": "Widebody"},
    "B744": {"family": "Boeing 747", "generation": "747-400", "subfleet": "Boeing 747-400", "category": "Widebody"},
    "B748": {"family": "Boeing 747", "generation": "747-8", "subfleet": "Boeing 747-8", "category": "Widebody"},

    # --- Airbus A330 / A340 / A350 / A380 Widebodies ---
    "A332": {"family": "Airbus A330", "generation": "A330ceo", "subfleet": "Airbus A330-200", "category": "Widebody"},
    "A333": {"family": "Airbus A330", "generation": "A330ceo", "subfleet": "Airbus A330-300", "category": "Widebody"},
    "A338": {"family": "Airbus A330", "generation": "A330neo", "subfleet": "Airbus A330-800neo", "category": "Widebody"},
    "A339": {"family": "Airbus A330", "generation": "A330neo", "subfleet": "Airbus A330-900neo", "category": "Widebody"},
    "A343": {"family": "Airbus A340", "generation": "A340 Classic", "subfleet": "Airbus A340-300", "category": "Widebody"},
    "A346": {"family": "Airbus A340", "generation": "A340 Extended", "subfleet": "Airbus A340-600", "category": "Widebody"},
    "A359": {"family": "Airbus A350", "generation": "A350 XWB", "subfleet": "Airbus A350-900", "category": "Widebody"},
    "A35K": {"family": "Airbus A350", "generation": "A350 XWB", "subfleet": "Airbus A350-1000", "category": "Widebody"},
    "A388": {"family": "Airbus A380", "generation": "A380 Superjumbo", "subfleet": "Airbus A380-800", "category": "Widebody"},

    # --- Embraer E-Jets ---
    "E170": {"family": "Embraer E-Jet", "generation": "E1 E-Jets", "subfleet": "Embraer E170", "category": "Regional Jet"},
    "E175": {"family": "Embraer E-Jet", "generation": "E1 E-Jets", "subfleet": "Embraer E175", "category": "Regional Jet"},
    "E190": {"family": "Embraer E-Jet", "generation": "E1 E-Jets", "subfleet": "Embraer E190", "category": "Regional Jet"},
    "E195": {"family": "Embraer E-Jet", "generation": "E1 E-Jets", "subfleet": "Embraer E195", "category": "Regional Jet"},
    "E290": {"family": "Embraer E-Jet", "generation": "E2 E-Jets", "subfleet": "Embraer E190-E2", "category": "Regional Jet"},
    "E295": {"family": "Embraer E-Jet", "generation": "E2 E-Jets", "subfleet": "Embraer E195-E2", "category": "Regional Jet"},

    # --- Bombardier / MHI CRJ ---
    "CRJ2": {"family": "Bombardier CRJ", "generation": "CRJ Series", "subfleet": "Bombardier CRJ-200", "category": "Regional Jet"},
    "CRJ7": {"family": "Bombardier CRJ", "generation": "CRJ NextGen", "subfleet": "Bombardier CRJ-700", "category": "Regional Jet"},
    "CRJ9": {"family": "Bombardier CRJ", "generation": "CRJ NextGen", "subfleet": "Bombardier CRJ-900", "category": "Regional Jet"},
    "CRJX": {"family": "Bombardier CRJ", "generation": "CRJ NextGen", "subfleet": "Bombardier CRJ-1000", "category": "Regional Jet"},

    # --- Turboprops ---
    "DH8D": {"family": "De Havilland Dash 8", "generation": "Q-Series", "subfleet": "Dash 8 Q400", "category": "Turboprop / Regional Prop"},
    "AT76": {"family": "ATR 42/72", "generation": "ATR -600", "subfleet": "ATR 72-600", "category": "Turboprop / Regional Prop"},
}

# Key fallback coordinates for prominent airports
AIRPORT_COORDINATES: Dict[str, Tuple[float, float, str, str]] = {
    "SEA": (47.4502, -122.3088, "Seattle-Tacoma International", "Seattle, WA"),
    "SFO": (37.6213, -122.3790, "San Francisco International", "San Francisco, CA"),
    "LAX": (33.9416, -118.4085, "Los Angeles International", "Los Angeles, CA"),
    "SAN": (32.7338, -117.1933, "San Diego International", "San Diego, CA"),
    "PDX": (45.5898, -122.5951, "Portland International", "Portland, OR"),
    "ORD": (41.9742, -87.9073, "Chicago O'Hare International", "Chicago, IL"),
    "MDW": (41.7868, -87.7522, "Chicago Midway International", "Chicago, IL"),
    "DFW": (32.8998, -97.0403, "Dallas/Fort Worth International", "Dallas, TX"),
    "DAL": (32.8481, -96.8512, "Dallas Love Field", "Dallas, TX"),
    "DEN": (39.8561, -104.6737, "Denver International", "Denver, CO"),
    "ATL": (33.6407, -84.4277, "Hartsfield-Jackson Atlanta", "Atlanta, GA"),
    "JFK": (40.6413, -73.7781, "John F. Kennedy International", "New York, NY"),
    "EWR": (40.6895, -74.1745, "Newark Liberty International", "Newark, NJ"),
    "LGA": (40.7769, -73.8740, "LaGuardia Airport", "New York, NY"),
    "BOS": (42.3656, -71.0096, "Boston Logan International", "Boston, MA"),
    "IAD": (38.9531, -77.4565, "Washington Dulles International", "Washington, DC"),
    "DCA": (38.8512, -77.0402, "Ronald Reagan Washington National", "Washington, DC"),
    "MIA": (25.7959, -80.2870, "Miami International", "Miami, FL"),
    "FLL": (26.0742, -80.1506, "Fort Lauderdale-Hollywood", "Fort Lauderdale, FL"),
    "MCO": (28.4312, -81.3081, "Orlando International", "Orlando, FL"),
    "TPA": (27.9755, -82.5332, "Tampa International", "Tampa, FL"),
    "PHX": (33.4373, -112.0078, "Phoenix Sky Harbor", "Phoenix, AZ"),
    "LAS": (36.0840, -115.1537, "Harry Reid International", "Las Vegas, NV"),
    "SLC": (40.7899, -111.9791, "Salt Lake City International", "Salt Lake City, UT"),
    "MSP": (44.8848, -93.2223, "Minneapolis-Saint Paul", "Minneapolis, MN"),
    "DTW": (42.2162, -83.3554, "Detroit Metropolitan", "Detroit, MI"),
    "CLT": (35.2144, -80.9473, "Charlotte Douglas International", "Charlotte, NC"),
    "PHL": (39.8729, -75.2437, "Philadelphia International", "Philadelphia, PA"),
    "BWI": (39.1774, -76.6684, "Baltimore/Washington International", "Baltimore, MD"),
    "AUS": (30.1975, -97.6664, "Austin-Bergstrom International", "Austin, TX"),
    "BNA": (36.1263, -86.6774, "Nashville International", "Nashville, TN"),
    "RDU": (35.8801, -78.7880, "Raleigh-Durham International", "Raleigh, NC"),
    "HNL": (21.3187, -157.9224, "Daniel K. Inouye International", "Honolulu, HI"),
    "OGG": (20.8986, -156.4305, "Kahului Airport", "Kahului, HI"),
    "ANC": (61.1743, -149.9962, "Ted Stevens Anchorage", "Anchorage, AK"),
    "LHR": (51.4700, -0.4543, "London Heathrow", "London, UK"),
    "LGW": (51.1537, -0.1821, "London Gatwick", "London, UK"),
    "CDG": (49.0097, 2.5479, "Paris Charles de Gaulle", "Paris, France"),
    "FRA": (50.0379, 8.5622, "Frankfurt Airport", "Frankfurt, Germany"),
    "AMS": (52.3105, 4.7683, "Amsterdam Airport Schiphol", "Amsterdam, Netherlands"),
    "NRT": (35.7720, 140.3929, "Narita International", "Tokyo, Japan"),
    "HND": (35.5494, 139.7798, "Tokyo Haneda", "Tokyo, Japan"),
}


def classify_aircraft(raw_str: str) -> Dict[str, str]:
    """
    Classifies raw aircraft type strings (e.g. 'Boeing 737-900ER', '737-800',
    'B739', 'A321neo', 'Airbus A320') into exact subfleet, generation, and family.
    """
    s = str(raw_str or "").strip().upper()
    if not s:
        return {
            "family": "Unspecified Aircraft",
            "generation": "Unspecified",
            "subfleet": "Unspecified",
            "category": "Other / Uncategorized"
        }

    # Direct 4-letter ICAO lookup
    for icao, info in SUBFLEET_TAXONOMY.items():
        if s == icao:
            return info

    # Boeing 737 Subfleet matching
    if "737" in s:
        fam = "Boeing 737"
        cat = "Mainline Narrowbody"
        if "MAX 10" in s or "737-10" in s or "MAX10" in s:
            return {"family": fam, "generation": "737 MAX", "subfleet": "Boeing 737 MAX 10", "category": cat}
        elif "MAX 9" in s or "737-9 MAX" in s or "MAX9" in s:
            return {"family": fam, "generation": "737 MAX", "subfleet": "Boeing 737 MAX 9", "category": cat}
        elif "MAX 8" in s or "737-8 MAX" in s or "MAX8" in s or "MAX 8200" in s:
            return {"family": fam, "generation": "737 MAX", "subfleet": "Boeing 737 MAX 8", "category": cat}
        elif "MAX 7" in s or "737-7 MAX" in s or "MAX7" in s:
            return {"family": fam, "generation": "737 MAX", "subfleet": "Boeing 737 MAX 7", "category": cat}
        elif "900ER" in s or "-900ER" in s:
            return {"family": fam, "generation": "737 NextGen", "subfleet": "Boeing 737-900ER", "category": cat}
        elif "900" in s or "-900" in s:
            return {"family": fam, "generation": "737 NextGen", "subfleet": "Boeing 737-900", "category": cat}
        elif "800" in s or "-800" in s:
            return {"family": fam, "generation": "737 NextGen", "subfleet": "Boeing 737-800", "category": cat}
        elif "700" in s or "-700" in s:
            return {"family": fam, "generation": "737 NextGen", "subfleet": "Boeing 737-700", "category": cat}
        elif "600" in s or "-600" in s:
            return {"family": fam, "generation": "737 NextGen", "subfleet": "Boeing 737-600", "category": cat}
        elif "500" in s or "400" in s or "300" in s:
            return {"family": fam, "generation": "737 Classic", "subfleet": f"Boeing 737 Classic", "category": cat}
        elif "MAX" in s:
            return {"family": fam, "generation": "737 MAX", "subfleet": "Boeing 737 MAX (General)", "category": cat}
        else:
            return {"family": fam, "generation": "737 NextGen", "subfleet": "Boeing 737 (General)", "category": cat}

    # Airbus A320 Subfleet matching
    if "321" in s:
        fam = "Airbus A320"
        cat = "Mainline Narrowbody"
        if "XLR" in s:
            return {"family": fam, "generation": "A320neo", "subfleet": "Airbus A321XLR", "category": cat}
        elif "NEO" in s or "21N" in s:
            return {"family": fam, "generation": "A320neo", "subfleet": "Airbus A321neo", "category": cat}
        else:
            return {"family": fam, "generation": "A320ceo", "subfleet": "Airbus A321ceo", "category": cat}
    elif "320" in s:
        fam = "Airbus A320"
        cat = "Mainline Narrowbody"
        if "NEO" in s or "20N" in s:
            return {"family": fam, "generation": "A320neo", "subfleet": "Airbus A320neo", "category": cat}
        else:
            return {"family": fam, "generation": "A320ceo", "subfleet": "Airbus A320ceo", "category": cat}
    elif "319" in s:
        fam = "Airbus A320"
        cat = "Mainline Narrowbody"
        if "NEO" in s:
            return {"family": fam, "generation": "A320neo", "subfleet": "Airbus A319neo", "category": cat}
        else:
            return {"family": fam, "generation": "A320ceo", "subfleet": "Airbus A319ceo", "category": cat}

    # Boeing 787 Dreamliner
    if "787" in s:
        fam = "Boeing 787"
        cat = "Widebody"
        if "-10" in s or "10" in s:
            return {"family": fam, "generation": "787 Dreamliner", "subfleet": "Boeing 787-10", "category": cat}
        elif "-9" in s or "9" in s:
            return {"family": fam, "generation": "787 Dreamliner", "subfleet": "Boeing 787-9", "category": cat}
        else:
            return {"family": fam, "generation": "787 Dreamliner", "subfleet": "Boeing 787-8", "category": cat}

    # Boeing 777
    if "777" in s:
        fam = "Boeing 777"
        cat = "Widebody"
        if "300ER" in s or "300" in s or "77W" in s:
            return {"family": fam, "generation": "777 Extended", "subfleet": "Boeing 777-300ER", "category": cat}
        elif "200LR" in s or "77L" in s:
            return {"family": fam, "generation": "777 Long Range", "subfleet": "Boeing 777-200LR", "category": cat}
        else:
            return {"family": fam, "generation": "777 Classic", "subfleet": "Boeing 777-200ER", "category": cat}

    # Airbus A350
    if "350" in s or "A35" in s:
        fam = "Airbus A350"
        cat = "Widebody"
        if "1000" in s or "35K" in s:
            return {"family": fam, "generation": "A350 XWB", "subfleet": "Airbus A350-1000", "category": cat}
        else:
            return {"family": fam, "generation": "A350 XWB", "subfleet": "Airbus A350-900", "category": cat}

    # Embraer E-Jets
    if "E175" in s or "E-175" in s:
        return {"family": "Embraer E-Jet", "generation": "E1 E-Jets", "subfleet": "Embraer E175", "category": "Regional Jet"}
    elif "E170" in s or "E-170" in s:
        return {"family": "Embraer E-Jet", "generation": "E1 E-Jets", "subfleet": "Embraer E170", "category": "Regional Jet"}
    elif "E190" in s or "E-190" in s:
        return {"family": "Embraer E-Jet", "generation": "E1 E-Jets", "subfleet": "Embraer E190", "category": "Regional Jet"}
    elif "E195" in s or "E-195" in s:
        return {"family": "Embraer E-Jet", "generation": "E1 E-Jets", "subfleet": "Embraer E195", "category": "Regional Jet"}

    # Bombardier CRJ
    if "CRJ" in s:
        fam = "Bombardier CRJ"
        cat = "Regional Jet"
        if "900" in s or "CRJ9" in s:
            return {"family": fam, "generation": "CRJ NextGen", "subfleet": "Bombardier CRJ-900", "category": cat}
        elif "700" in s or "CRJ7" in s:
            return {"family": fam, "generation": "CRJ NextGen", "subfleet": "Bombardier CRJ-700", "category": cat}
        else:
            return {"family": fam, "generation": "CRJ Series", "subfleet": "Bombardier CRJ-200", "category": cat}

    # Default fallback
    return {
        "family": raw_str.strip() or "Other",
        "generation": raw_str.strip() or "Other",
        "subfleet": raw_str.strip() or "Other",
        "category": "Mainline Narrowbody"
    }


def calculate_haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates great-circle distance between two GPS coordinates in miles."""
    r = 3958.8  # Earth radius in statute miles
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(r * c, 1)


def normalize_carrier_code(carrier_str: str, flight_str: str = "") -> str:
    """Normalizes raw airline name or flight number to standard 2-letter IATA code."""
    import re
    from app.data.ref_alliances import CARRIER_LOGOS
    c = str(carrier_str).strip().upper()
    f = str(flight_str).strip().upper()
    
    # 1. Check flight number prefix (e.g. 'AS 12' or 'UA450')
    if f:
        m = re.match(r"^([A-Z0-9]{2})\s*\d+", f)
        if m:
            prefix = m.group(1)
            if prefix in CARRIER_LOGOS or prefix in ["AS", "UA", "DL", "AA", "WN", "B6", "NK", "F9", "HA", "BA", "LH", "AF", "KL", "QF", "SQ", "NH", "JL"]:
                return prefix

    # 2. Check if already 2 letters
    if len(c) == 2 and c.isalpha():
        return c

    # 3. Common airline names
    airline_map = {
        "ALASKA": "AS",
        "HORIZON": "AS",
        "UNITED": "UA",
        "DELTA": "DL",
        "AMERICAN": "AA",
        "SOUTHWEST": "WN",
        "JETBLUE": "B6",
        "SPIRIT": "NK",
        "FRONTIER": "F9",
        "HAWAIIAN": "HA",
        "ALLEGIANT": "G4",
        "BRITISH AIRWAYS": "BA",
        "LUFTHANSA": "LH",
        "AIR FRANCE": "AF",
        "KLM": "KL",
        "VIRGIN": "VS",
        "AIR CANADA": "AC",
        "QANTAS": "QF",
        "SINGAPORE": "SQ",
        "ANA": "NH",
        "JAPAN AIRLINES": "JL",
        "CATHAY": "CX",
        "EMIRATES": "EK",
        "QATAR": "QR",
        "AEROMEXICO": "AM",
        "AVIANCA": "AV",
        "COPA": "CM",
        "IBERIA": "IB",
        "FINNAIR": "AY",
        "SWISS": "LX",
        "AUSTRIAN": "OS",
        "SAS": "SK",
        "TURKISH": "TK"
    }
    for name, code in airline_map.items():
        if name in c:
            return code
            
    return c[:2] if len(c) >= 2 else "UA"


def classify_seat_position(seat_str: str) -> str:
    """Classifies seat identifier into Window, Aisle, Middle, or Unassigned."""
    if not seat_str or pd.isna(seat_str):
        return "Unassigned / Open"
    s = str(seat_str).strip().upper()
    if s in ["ANY", "OPEN", "GENERAL", "UNASSIGNED", "NONE", "NAN", ""]:
        return "Unassigned / Open"
    
    letter = s[-1] if s[-1].isalpha() else ""
    if not letter:
        return "Unassigned / Open"
        
    if letter in ["A", "F", "K"]:
        return "Window"
    elif letter in ["C", "D", "G", "H"]:
        return "Aisle"
    elif letter in ["B", "E", "J"]:
        return "Middle"
    else:
        return "Other"


def calculate_flight_carbon_footprint(distance_miles: float, cabin_class: str = "Economy", category: str = "Mainline Narrowbody") -> float:
    """
    Estimates kg of CO2 emissions for a passenger on a flight segment
    based on stage length, aircraft category, and cabin class multiplier.
    """
    cat_lower = str(category).lower()
    if "widebody" in cat_lower:
        base_rate = 0.115
    elif "regional" in cat_lower:
        base_rate = 0.175
    elif "turboprop" in cat_lower:
        base_rate = 0.145
    else:
        base_rate = 0.135
        
    c_lower = str(cabin_class).lower()
    if "first" in c_lower:
        mult = 3.5
    elif any(k in c_lower for k in ["business", "polaris", "one", "club"]):
        mult = 2.4
    elif any(k in c_lower for k in ["premium", "comfort", "extra", "plus"]):
        mult = 1.4
    else:
        mult = 1.0
        
    return round(float(distance_miles) * base_rate * mult, 1)



def parse_flighty_csv(file_or_content) -> pd.DataFrame:
    """
    Parses Flighty CSV export and enriches it with:
    - Standardized column names
    - Subfleet, Generation, and Family taxonomy
    - Origin/Destination coordinates
    - Geodesic route distances
    """
    if isinstance(file_or_content, pd.DataFrame):
        df = file_or_content.copy()
    elif isinstance(file_or_content, (bytes, bytearray)):
        df = pd.read_csv(io.BytesIO(file_or_content))
    elif isinstance(file_or_content, str):
        df = pd.read_csv(io.StringIO(file_or_content))
    else:
        df = pd.read_csv(file_or_content)

    # Normalize column names: lowercase and replace spaces/underscores
    col_map = {}
    for col in df.columns:
        clean = col.strip().lower().replace(" ", "_").replace("/", "_").replace("-", "_")
        col_map[col] = clean
    df.rename(columns=col_map, inplace=True)

    # Resolve date
    date_col = next((c for c in df.columns if "date" in c), None)
    if date_col:
        df["flight_date"] = pd.to_datetime(df[date_col], errors="coerce").dt.strftime("%Y-%m-%d")
        df["year"] = pd.to_datetime(df[date_col], errors="coerce").dt.year.fillna(2023).astype(int)
    else:
        df["flight_date"] = "2023-01-01"
        df["year"] = 2023

    # Resolve origin
    orig_col = next((c for c in df.columns if c in ["departure", "origin", "from", "departure_iata", "origin_iata"]), None)
    if orig_col:
        df["origin"] = df[orig_col].astype(str).str.strip().str.upper().str[:3]
    else:
        df["origin"] = "SEA"

    # Resolve destination
    dest_col = next((c for c in df.columns if c in ["arrival", "destination", "dest", "to", "arrival_iata", "dest_iata"]), None)
    if dest_col:
        df["dest"] = df[dest_col].astype(str).str.strip().str.upper().str[:3]
    else:
        df["dest"] = "SFO"

    # Resolve carrier
    carr_col = next((c for c in df.columns if c in ["airline", "carrier", "airline_code", "operating_carrier"]), None)
    if carr_col:
        df["carrier"] = df[carr_col].astype(str).str.strip().str.upper()
    else:
        df["carrier"] = "AS"

    # Resolve flight number
    flt_col = next((c for c in df.columns if ("flight" in c and "number" in c) or c == "flight"), None)
    if flt_col:
        df["flight_number"] = df[flt_col].astype(str).str.strip()
    else:
        df["flight_number"] = ""

    # Resolve aircraft type
    act_col = next((c for c in df.columns if any(k in c for k in ["aircraft", "plane", "equipment", "type", "model"])), None)
    if act_col:
        raw_aircraft = df[act_col].astype(str)
    else:
        raw_aircraft = pd.Series(["Boeing 737-900ER"] * len(df))

    # Apply taxonomy classification
    classified = [classify_aircraft(val) for val in raw_aircraft]
    df["raw_aircraft"] = raw_aircraft
    df["aircraft_family"] = [c["family"] for c in classified]
    df["aircraft_generation"] = [c["generation"] for c in classified]
    df["aircraft_subfleet"] = [c["subfleet"] for c in classified]
    df["aircraft_category"] = [c["category"] for c in classified]

    # Resolve seat & cabin
    seat_col = next((c for c in df.columns if "seat" in c and "class" not in c), None)
    df["seat"] = df[seat_col].astype(str).str.strip() if seat_col else ""

    cabin_col = next((c for c in df.columns if "cabin" in c or "class" in c), None)
    df["cabin_class"] = df[cabin_col].astype(str).str.strip() if cabin_col else "Economy"

    # Assign GPS coordinates
    df["origin_lat"] = np.nan
    df["origin_lon"] = np.nan
    df["origin_city"] = ""
    df["origin_name"] = ""

    df["dest_lat"] = np.nan
    df["dest_lon"] = np.nan
    df["dest_city"] = ""
    df["dest_name"] = ""

    for idx, row in df.iterrows():
        o = row["origin"]
        d = row["dest"]
        if o in AIRPORT_COORDINATES:
            lat, lon, name, city = AIRPORT_COORDINATES[o]
            df.at[idx, "origin_lat"] = lat
            df.at[idx, "origin_lon"] = lon
            df.at[idx, "origin_name"] = name
            df.at[idx, "origin_city"] = city
        if d in AIRPORT_COORDINATES:
            lat, lon, name, city = AIRPORT_COORDINATES[d]
            df.at[idx, "dest_lat"] = lat
            df.at[idx, "dest_lon"] = lon
            df.at[idx, "dest_name"] = name
            df.at[idx, "dest_city"] = city

    # Fallback coordinates for any remaining missing coordinates
    df["origin_lat"] = df["origin_lat"].fillna(47.4502)
    df["origin_lon"] = df["origin_lon"].fillna(-122.3088)
    df["dest_lat"] = df["dest_lat"].fillna(37.6213)
    df["dest_lon"] = df["dest_lon"].fillna(-122.3790)

    # Compute distances
    distances = []
    for _, row in df.iterrows():
        try:
            dist = calculate_haversine_distance(row["origin_lat"], row["origin_lon"], row["dest_lat"], row["dest_lon"])
        except Exception:
            dist = 500.0
        distances.append(dist)
    df["distance_miles"] = distances

    df["route"] = df["origin"] + " ➔ " + df["dest"]

    # Normalize carrier codes and assign historical alliance
    from app.utils.alliances import get_carrier_alliance
    carrier_codes = []
    alliances = []
    for _, row in df.iterrows():
        c_code = normalize_carrier_code(row.get("carrier", ""), row.get("flight_number", ""))
        carrier_codes.append(c_code)
        yr = int(row.get("year", 2023))
        a_info = get_carrier_alliance(c_code, yr)
        alliances.append(a_info["alliance_name"] if a_info else "Independent / Unaligned")
    df["carrier_code"] = carrier_codes
    df["alliance"] = alliances

    # Seat position preference
    df["seat_position"] = [classify_seat_position(s) for s in df["seat"]]

    # CO2 footprint
    df["co2_kg"] = [
        calculate_flight_carbon_footprint(r["distance_miles"], r.get("cabin_class", "Economy"), r.get("aircraft_category", "Mainline Narrowbody"))
        for _, r in df.iterrows()
    ]

    return df



def generate_sample_flighty_data() -> pd.DataFrame:
    """
    Generates a realistic 35-flight travel log with frequent flyer patterns
    across Alaska, United, Delta, American, Southwest, and British Airways,
    specifically featuring detailed subfleet variants (e.g. 737-900ER vs 737-800 vs MAX 9).
    """
    sample_records = [
        {"Date": "2023-01-15", "Airline": "Alaska Airlines", "Flight": "AS 12", "From": "SEA", "To": "BOS", "Aircraft": "Boeing 737-900ER", "Seat": "2A", "Class": "First"},
        {"Date": "2023-01-22", "Airline": "Alaska Airlines", "Flight": "AS 25", "From": "BOS", "To": "SEA", "Aircraft": "Boeing 737-900ER", "Seat": "3D", "Class": "First"},
        {"Date": "2023-02-10", "Airline": "United Airlines", "Flight": "UA 450", "From": "SEA", "To": "ORD", "Aircraft": "Boeing 737 MAX 9", "Seat": "7C", "Class": "Economy Plus"},
        {"Date": "2023-02-14", "Airline": "United Airlines", "Flight": "UA 929", "From": "ORD", "To": "LHR", "Aircraft": "Boeing 787-9", "Seat": "11A", "Class": "Polaris Business"},
        {"Date": "2023-02-20", "Airline": "British Airways", "Flight": "BA 49", "From": "LHR", "To": "SEA", "Aircraft": "Airbus A350-1000", "Seat": "15K", "Class": "Club World"},
        {"Date": "2023-03-05", "Airline": "Alaska Airlines", "Flight": "AS 322", "From": "SEA", "To": "SFO", "Aircraft": "Boeing 737-800", "Seat": "6C", "Class": "Premium Class"},
        {"Date": "2023-03-08", "Airline": "Alaska Airlines", "Flight": "AS 311", "From": "SFO", "To": "SEA", "Aircraft": "Boeing 737-900ER", "Seat": "1F", "Class": "First"},
        {"Date": "2023-04-12", "Airline": "Delta Air Lines", "Flight": "DL 1184", "From": "SEA", "To": "ATL", "Aircraft": "Airbus A321neo", "Seat": "10B", "Class": "Comfort+"},
        {"Date": "2023-04-16", "Airline": "Delta Air Lines", "Flight": "DL 892", "From": "ATL", "To": "MIA", "Aircraft": "Boeing 757-200", "Seat": "14D", "Class": "First"},
        {"Date": "2023-04-20", "Airline": "American Airlines", "Flight": "AA 224", "From": "MIA", "To": "DFW", "Aircraft": "Boeing 777-200ER", "Seat": "4A", "Class": "Business"},
        {"Date": "2023-04-20", "Airline": "American Airlines", "Flight": "AA 1520", "From": "DFW", "To": "SEA", "Aircraft": "Boeing 737-800", "Seat": "8E", "Class": "Main Cabin Extra"},
        {"Date": "2023-05-18", "Airline": "Alaska Airlines", "Flight": "AS 490", "From": "SEA", "To": "SAN", "Aircraft": "Boeing 737 MAX 9", "Seat": "6D", "Class": "Premium Class"},
        {"Date": "2023-05-22", "Airline": "Alaska Airlines", "Flight": "AS 495", "From": "SAN", "To": "SEA", "Aircraft": "Boeing 737-800", "Seat": "7A", "Class": "Premium Class"},
        {"Date": "2023-06-10", "Airline": "United Airlines", "Flight": "UA 212", "From": "SEA", "To": "DEN", "Aircraft": "Airbus A320ceo", "Seat": "12F", "Class": "Economy"},
        {"Date": "2023-06-14", "Airline": "United Airlines", "Flight": "UA 560", "From": "DEN", "To": "SEA", "Aircraft": "Boeing 737 MAX 8", "Seat": "9D", "Class": "Economy Plus"},
        {"Date": "2023-07-01", "Airline": "Alaska Airlines", "Flight": "AS 882", "From": "SEA", "To": "HNL", "Aircraft": "Boeing 737-900ER", "Seat": "3A", "Class": "First"},
        {"Date": "2023-07-08", "Airline": "Alaska Airlines", "Flight": "AS 883", "From": "HNL", "To": "SEA", "Aircraft": "Boeing 737-900ER", "Seat": "2F", "Class": "First"},
        {"Date": "2023-08-14", "Airline": "Southwest Airlines", "Flight": "WN 1422", "From": "SEA", "To": "LAS", "Aircraft": "Boeing 737-700", "Seat": "Any", "Class": "Economy"},
        {"Date": "2023-08-17", "Airline": "Southwest Airlines", "Flight": "WN 2108", "From": "LAS", "To": "SEA", "Aircraft": "Boeing 737 MAX 8", "Seat": "Any", "Class": "Economy"},
        {"Date": "2023-09-02", "Airline": "Horizon Air", "Flight": "AS 2012", "From": "SEA", "To": "PDX", "Aircraft": "Embraer E175", "Seat": "4A", "Class": "First"},
        {"Date": "2023-09-04", "Airline": "Horizon Air", "Flight": "AS 2028", "From": "PDX", "To": "SEA", "Aircraft": "Embraer E175", "Seat": "4F", "Class": "First"},
        {"Date": "2023-10-11", "Airline": "Delta Air Lines", "Flight": "DL 480", "From": "SEA", "To": "JFK", "Aircraft": "Airbus A330-900neo", "Seat": "5A", "Class": "Delta One"},
        {"Date": "2023-10-15", "Airline": "Delta Air Lines", "Flight": "DL 485", "From": "JFK", "To": "SEA", "Aircraft": "Boeing 767-300ER", "Seat": "6D", "Class": "Delta One"},
        {"Date": "2023-11-20", "Airline": "Alaska Airlines", "Flight": "AS 70", "From": "SEA", "To": "ANC", "Aircraft": "Boeing 737-900ER", "Seat": "1D", "Class": "First"},
        {"Date": "2023-11-26", "Airline": "Alaska Airlines", "Flight": "AS 77", "From": "ANC", "To": "SEA", "Aircraft": "Boeing 737 MAX 9", "Seat": "2C", "Class": "First"},
        {"Date": "2023-12-22", "Airline": "Alaska Airlines", "Flight": "AS 1084", "From": "SEA", "To": "LAX", "Aircraft": "Boeing 737-900ER", "Seat": "3A", "Class": "First"},
        {"Date": "2023-12-28", "Airline": "Alaska Airlines", "Flight": "AS 1099", "From": "LAX", "To": "SEA", "Aircraft": "Boeing 737-800", "Seat": "7C", "Class": "Premium Class"},
        {"Date": "2024-01-10", "Airline": "United Airlines", "Flight": "UA 1902", "From": "SEA", "To": "IAD", "Aircraft": "Boeing 737 MAX 9", "Seat": "10C", "Class": "Economy Plus"},
        {"Date": "2024-01-14", "Airline": "United Airlines", "Flight": "UA 1905", "From": "IAD", "To": "SEA", "Aircraft": "Boeing 737 MAX 9", "Seat": "11D", "Class": "Economy Plus"},
        {"Date": "2024-02-18", "Airline": "Alaska Airlines", "Flight": "AS 340", "From": "SEA", "To": "PHX", "Aircraft": "Boeing 737-900ER", "Seat": "2D", "Class": "First"},
    ]
    df_raw = pd.DataFrame(sample_records)
    return parse_flighty_csv(df_raw)


def build_flighty_travel_deck(
    df_flights: pd.DataFrame,
    home_airport: str = "SEA",
    map_theme: str = "personal",
    colorway: str = "cobalt"
) -> Any:
    """
    Renders personal travels using AvDB's authentic 1990s in-flight route cartography.
    Aggregates flight segments into unique routes, showing total flight counts as arc weight.
    """
    import pydeck as pdk
    from app.utils.visualizers import MAP_THEMES, ROUTE_COLORWAYS

    if df_flights.empty:
        return pdk.Deck(layers=[])

    # Aggregate route frequencies
    route_agg = df_flights.groupby([
        "origin", "dest", "origin_lat", "origin_lon", "origin_city", "origin_name",
        "dest_lat", "dest_lon", "dest_city", "dest_name"
    ]).size().reset_index(name="flight_count")

    route_agg["route"] = route_agg["origin"] + " ➔ " + route_agg["dest"]
    route_agg["fmt_count"] = route_agg["flight_count"].apply(lambda x: f"{x} flight{'s' if x > 1 else ''}")

    # Palette selection
    palette = ROUTE_COLORWAYS.get(colorway, ROUTE_COLORWAYS["cobalt"])
    route_color = palette["line"]

    # Calculate stroke width based on flight count
    max_count = max(route_agg["flight_count"].max(), 1)
    route_agg["stroke_width"] = 1.8 + (route_agg["flight_count"] / max_count) * 4.5

    # Geodesic route layer
    route_layer = pdk.Layer(
        "GreatCircleLayer",
        data=route_agg,
        id="flighty-routes",
        get_source_position=["origin_lon", "origin_lat"],
        get_target_position=["dest_lon", "dest_lat"],
        get_source_color=route_color,
        get_target_color=route_color,
        get_width="stroke_width",
        width_min_pixels=1.5,
        width_max_pixels=6,
        pickable=True,
        auto_highlight=True,
    )

    # Node points
    all_nodes = []
    seen = set()
    for _, row in df_flights.iterrows():
        o = row["origin"]
        if o not in seen:
            seen.add(o)
            all_nodes.append({
                "code": o,
                "lat": row["origin_lat"],
                "lon": row["origin_lon"],
                "name": row["origin_name"],
                "city": row["origin_city"],
                "is_home": (o == home_airport)
            })
        d = row["dest"]
        if d not in seen:
            seen.add(d)
            all_nodes.append({
                "code": d,
                "lat": row["dest_lat"],
                "lon": row["dest_lon"],
                "name": row["dest_name"],
                "city": row["dest_city"],
                "is_home": (d == home_airport)
            })

    df_nodes = pd.DataFrame(all_nodes)
    df_nodes["radius"] = df_nodes["is_home"].apply(lambda x: 18000 if x else 9000)
    df_nodes["color"] = df_nodes["is_home"].apply(lambda x: [255, 214, 10, 240] if x else [245, 245, 247, 220])

    node_layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_nodes,
        id="flighty-nodes",
        get_position=["lon", "lat"],
        get_radius="radius",
        get_fill_color="color",
        get_line_color=[10, 10, 15, 240],
        line_width_min_pixels=1.5,
        stroked=True,
        filled=True,
        pickable=True,
    )

    # IATA typography text layer
    text_layer = pdk.Layer(
        "TextLayer",
        data=df_nodes,
        id="flighty-text",
        get_position=["lon", "lat"],
        get_text="code",
        get_size=11,
        get_color=[245, 245, 247, 240],
        get_pixel_offset=[10, -8],
        font_family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
        font_weight=700,
        pickable=False
    )

    # Center view
    home_lat, home_lon = 39.5, -98.35
    if home_airport in AIRPORT_COORDINATES:
        home_lat, home_lon, _, _ = AIRPORT_COORDINATES[home_airport]

    view_state = pdk.ViewState(
        latitude=home_lat,
        longitude=home_lon,
        zoom=3.3,
        pitch=0,
        bearing=0
    )

    tooltip = {
        "html": """
            <div style="background-color: #16171B; border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 8px; padding: 10px 14px; font-family: -apple-system, sans-serif; box-shadow: 0 4px 14px rgba(0, 0, 0, 0.5); min-width: 170px;">
                <div style="font-size: 13px; font-weight: 700; color: #F5F5F7; margin-bottom: 4px;">{route}</div>
                <div style="color: #64D2FF; font-size: 11px; font-weight: 600;">{fmt_count}</div>
            </div>
        """,
        "style": {"color": "white"}
    }

    style_url = MAP_THEMES.get(map_theme, MAP_THEMES["personal"])
    from app.config import settings
    api_keys = {"mapbox": settings.mapbox_token} if settings.mapbox_token else None

    return pdk.Deck(
        layers=[route_layer, node_layer, text_layer],
        initial_view_state=view_state,
        map_style=style_url,
        tooltip=tooltip,
        api_keys=api_keys
    )
