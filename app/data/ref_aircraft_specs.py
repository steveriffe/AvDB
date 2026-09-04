"""
AvDB Aircraft Reference Specifications & Technical Specs
Provides engineering specs, seating gauges, ranges, and operator mapping.
"""
from typing import Dict, Any, Optional

AIRCRAFT_SPECS: Dict[str, Dict[str, Any]] = {
    "Boeing 737-800": {
        "family": "Boeing 737 Family",
        "category": "Mainline Narrowbody",
        "seats_typical": "162 - 175 seats (2-class)",
        "range_miles": 2935,
        "wingspan_ft": 117.4,
        "length_ft": 129.5,
        "cruise_speed": "Mach 0.785 (514 mph)",
        "engines": "CFM International CFM56-7B",
        "first_flight": 1997,
        "key_operators": ["WN", "AA", "UA", "DL", "AS"],
        "summary": "Workhorse of global commercial aviation. High-density narrowbody optimized for medium-haul transcontinental networks."
    },
    "Boeing 737-900ER": {
        "family": "Boeing 737 Family",
        "category": "Mainline Narrowbody",
        "seats_typical": "178 - 189 seats (2-class)",
        "range_miles": 2950,
        "wingspan_ft": 117.4,
        "length_ft": 138.2,
        "cruise_speed": "Mach 0.785 (514 mph)",
        "engines": "CFM International CFM56-7BE",
        "first_flight": 2006,
        "key_operators": ["UA", "DL", "AS"],
        "summary": "High-capacity stretched NextGen variant with auxiliary fuel tanks, ideal for transcontinental trunk routes."
    },
    "Boeing 737 MAX 8": {
        "family": "Boeing 737 Family",
        "category": "Mainline Narrowbody",
        "seats_typical": "166 - 178 seats (2-class)",
        "range_miles": 3550,
        "wingspan_ft": 117.8,
        "length_ft": 129.7,
        "cruise_speed": "Mach 0.79 (521 mph)",
        "engines": "CFM LEAP-1B",
        "first_flight": 2016,
        "key_operators": ["WN", "AA", "UA"],
        "summary": "Next-generation CFM LEAP-1B powered narrowbody delivering 14% fuel reduction and extended transpacific/transatlantic range."
    },
    "Boeing 737 MAX 9": {
        "family": "Boeing 737 Family",
        "category": "Mainline Narrowbody",
        "seats_typical": "178 - 193 seats (2-class)",
        "range_miles": 3300,
        "wingspan_ft": 117.8,
        "length_ft": 138.3,
        "cruise_speed": "Mach 0.79 (521 mph)",
        "engines": "CFM LEAP-1B",
        "first_flight": 2017,
        "key_operators": ["UA", "AS"],
        "summary": "Extended-fuselage MAX variant serving high-demand West Coast transcon and Hawaii corridors."
    },
    "Airbus A320neo": {
        "family": "Airbus A320 Family",
        "category": "Mainline Narrowbody",
        "seats_typical": "150 - 180 seats (2-class)",
        "range_miles": 3500,
        "wingspan_ft": 117.4,
        "length_ft": 123.3,
        "cruise_speed": "Mach 0.78 (511 mph)",
        "engines": "CFM LEAP-1A / Pratt & Whitney PW1100G",
        "first_flight": 2014,
        "key_operators": ["F9", "NK", "B6", "UA"],
        "summary": "New Engine Option update to the iconic A320 with large Sharklets, offering superior cabin width and fuel efficiency."
    },
    "Airbus A321neo": {
        "family": "Airbus A320 Family",
        "category": "Mainline Narrowbody",
        "seats_typical": "180 - 200 seats (2-class)",
        "range_miles": 4000,
        "wingspan_ft": 117.4,
        "length_ft": 146.0,
        "cruise_speed": "Mach 0.78 (511 mph)",
        "engines": "CFM LEAP-1A / Pratt & Whitney PW1100G",
        "first_flight": 2016,
        "key_operators": ["AA", "DL", "UA", "B6", "HA", "F9"],
        "summary": "Premier long-haul capable narrowbody with Airbus Cabin Flex (ACF), dominating middle-of-the-market gauge."
    },
    "Boeing 787-9": {
        "family": "Boeing Widebody",
        "category": "Widebody",
        "seats_typical": "257 - 296 seats (3-class)",
        "range_miles": 7565,
        "wingspan_ft": 197.3,
        "length_ft": 206.1,
        "cruise_speed": "Mach 0.85 (561 mph)",
        "engines": "GEnx-1B / Rolls-Royce Trent 1000",
        "first_flight": 2013,
        "key_operators": ["UA", "AA", "HA"],
        "summary": "Composite carbon-fiber widebody offering 6,000-ft lower cabin altitude, higher humidity, and ultra-long range point-to-point capabilities."
    },
    "Boeing 777-200ER": {
        "family": "Boeing Widebody",
        "category": "Widebody",
        "seats_typical": "273 - 312 seats (3-class)",
        "range_miles": 7065,
        "wingspan_ft": 199.9,
        "length_ft": 209.1,
        "cruise_speed": "Mach 0.84 (554 mph)",
        "engines": "GE90-94B / Pratt & Whitney PW4090 / Rolls-Royce Trent 895",
        "first_flight": 1996,
        "key_operators": ["UA", "AA", "DL"],
        "summary": "Heavy twin-aisle cornerstone of transoceanic routes, capable of massive cargo payloads alongside international premium cabins."
    },
    "Boeing 767-300ER": {
        "family": "Boeing Widebody",
        "category": "Widebody",
        "seats_typical": "208 - 226 seats (3-class)",
        "range_miles": 5980,
        "wingspan_ft": 156.1,
        "length_ft": 180.3,
        "cruise_speed": "Mach 0.80 (530 mph)",
        "engines": "GE CF6-80C2 / Pratt & Whitney PW4060",
        "first_flight": 1986,
        "key_operators": ["DL", "UA"],
        "summary": "Historic 7-abreast (2-3-2) passenger favorite for secondary transatlantic routes and transcontinental premium flights."
    },
    "Airbus A350-900": {
        "family": "Airbus Widebody",
        "category": "Widebody",
        "seats_typical": "300 - 350 seats (3-class)",
        "range_miles": 8100,
        "wingspan_ft": 212.4,
        "length_ft": 219.2,
        "cruise_speed": "Mach 0.85 (561 mph)",
        "engines": "Rolls-Royce Trent XWB-84",
        "first_flight": 2013,
        "key_operators": ["DL"],
        "summary": "Flagship composite widebody featuring sculpted winglets, whisper-quiet cabin acoustics, and premier transpacific endurance."
    },
    "Embraer E175": {
        "family": "Embraer E-Jets",
        "category": "Regional Jet",
        "seats_typical": "76 seats (12 First / 64 Economy)",
        "range_miles": 2200,
        "wingspan_ft": 85.3,
        "length_ft": 103.9,
        "cruise_speed": "Mach 0.78 (511 mph)",
        "engines": "GE CF34-8E",
        "first_flight": 2003,
        "key_operators": ["OO", "QX", "MQ", "YX", "DL", "UA", "AA", "AS"],
        "summary": "The backbone of US scope-clause regional flying. Features full 2x2 economy seating with no middle seats and genuine first class."
    },
    "Bombardier CRJ-900": {
        "family": "Bombardier CRJ Series",
        "category": "Regional Jet",
        "seats_typical": "76 seats (9 First / 67 Economy)",
        "range_miles": 1550,
        "wingspan_ft": 81.6,
        "length_ft": 118.9,
        "cruise_speed": "Mach 0.80 (528 mph)",
        "engines": "GE CF34-8C5",
        "first_flight": 2001,
        "key_operators": ["9E", "OO", "DL", "AA"],
        "summary": "High-efficiency regional twin-jet engineered from the Challenger bizjet lineage, widely operated across Delta Connection and American Eagle."
    }
}


def get_aircraft_spec(description: str) -> Optional[Dict[str, Any]]:
    """Returns technical specs matching aircraft description."""
    d = description.strip()
    # Check exact match
    if d in AIRCRAFT_SPECS:
        return AIRCRAFT_SPECS[d]
    # Check partial match
    for name, spec in AIRCRAFT_SPECS.items():
        if name in d or d in name:
            return spec
    # Keyword fallback
    if "737-800" in d:
        return AIRCRAFT_SPECS["Boeing 737-800"]
    if "737-900" in d or "739" in d:
        return AIRCRAFT_SPECS["Boeing 737-900ER"]
    if "MAX 8" in d or "MAX8" in d:
        return AIRCRAFT_SPECS["Boeing 737 MAX 8"]
    if "MAX 9" in d or "MAX9" in d:
        return AIRCRAFT_SPECS["Boeing 737 MAX 9"]
    if "A321" in d:
        return AIRCRAFT_SPECS["Airbus A321neo"]
    if "A320" in d:
        return AIRCRAFT_SPECS["Airbus A320neo"]
    if "787" in d:
        return AIRCRAFT_SPECS["Boeing 787-9"]
    if "777" in d:
        return AIRCRAFT_SPECS["Boeing 777-200ER"]
    if "767" in d:
        return AIRCRAFT_SPECS["Boeing 767-300ER"]
    if "A350" in d:
        return AIRCRAFT_SPECS["Airbus A350-900"]
    if "E175" in d or "E-175" in d:
        return AIRCRAFT_SPECS["Embraer E175"]
    if "CRJ-900" in d or "CRJ9" in d:
        return AIRCRAFT_SPECS["Bombardier CRJ-900"]
    return None
