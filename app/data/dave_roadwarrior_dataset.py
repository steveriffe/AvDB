"""
AvDB Road Warrior Dataset: Dave Pierce (2000–2025)
Realistic 276-flight travel log for Dave Pierce, a Senior Petroleum Reservoir Engineer
& Offshore Operations Director in the global upstream Oil & Gas Industry.

Centered on four primary operational nodes:
1. Anchorage, Alaska (ANC) - North Slope / Prudhoe Bay / Cook Inlet
2. Houston, Texas (IAH) - Energy Corridor Global HQ & Deepwater GOM Tech Center
3. Hong Kong (HKG) - Asia-Pacific Joint Ventures & Shekou Marine Fabrication Yards
4. Halifax, Nova Scotia (YHZ) - Sable Offshore Energy Project (SOEP) & Deep Panuke
Plus occasional reluctant family holidays to Honolulu (HNL) and Bali / Denpasar (DPS)
(even though real-life Dave abhored the beach!).

Carrier split realistically balanced:
- Alaska Airlines (AS): ~35%
- Continental Airlines (CO, 2000-2011) / United Airlines (UA, 2012-2025): ~45%
- Air Canada (AC): ~20%
"""
import pandas as pd
from typing import List, Dict, Any
from app.utils.flighty import parse_flighty_csv


def get_dave_pierce_raw_records() -> List[Dict[str, Any]]:
    """
    Returns the deterministic 276-record flight list spanning 2000–2025.
    """
    records: List[Dict[str, Any]] = []

    # Helper to add rotation
    def add(dt: str, airline: str, flt: str, orig: str, dest: str, ac: str, seat: str, cls: str, note: str):
        records.append({
            "Date": dt,
            "Airline": airline,
            "Flight": flt,
            "From": orig,
            "To": dest,
            "Aircraft": ac,
            "Seat": seat,
            "Class": cls,
            "Reason": note
        })

    # =========================================================================
    # 2000 (11 flights): Prudhoe Bay expansion & Houston Gulf of Mexico liaison
    # =========================================================================
    add("2000-01-18", "Alaska Airlines", "AS 82", "ANC", "SEA", "Boeing 737-400", "2A", "First", "Prudhoe Bay winter briefing debrief")
    add("2000-01-18", "Continental Airlines", "CO 1520", "SEA", "IAH", "Boeing 737-800", "3B", "First", "En route to Houston Energy Corridor HQ")
    add("2000-01-26", "Continental Airlines", "CO 1521", "IAH", "SEA", "Boeing 737-800", "2E", "First", "Return via Seattle hub")
    add("2000-01-26", "Alaska Airlines", "AS 87", "SEA", "ANC", "Boeing 737-400", "3A", "First", "Back to Anchorage operations")
    add("2000-04-10", "Continental Airlines", "CO 1840", "IAH", "EWR", "Boeing 757-200", "4A", "First", "Transit to Nova Scotia gas project")
    add("2000-04-10", "Air Canada", "AC 8920", "EWR", "YHZ", "Bombardier CRJ-200", "2A", "Economy", "Sable Offshore Energy Project (SOEP) review")
    add("2000-04-18", "Air Canada", "AC 615", "YHZ", "YYZ", "Airbus A320-200", "3C", "Business", "Return via Toronto engineering branch")
    add("2000-04-18", "Continental Airlines", "CO 1980", "YYZ", "IAH", "Boeing 737-700", "2B", "First", "Houston deepwater tech center")
    add("2000-07-12", "Continental Airlines", "CO 1704", "IAH", "ANC", "Boeing 757-200", "3F", "First", "Nonstop summer flight to Cook Inlet platform")
    add("2000-07-28", "Alaska Airlines", "AS 130", "ANC", "SEA", "Boeing 737-400", "1C", "First", "Alaska pipeline audit follow-up")
    add("2000-10-15", "Alaska Airlines", "AS 81", "SEA", "ANC", "Boeing 737-400", "2C", "First", "North Slope winter drilling preparation")

    # =========================================================================
    # 2001 (11 flights): Transpacific CO 99 Inauguration & Reluctant HNL trip!
    # =========================================================================
    add("2001-02-05", "Alaska Airlines", "AS 80", "ANC", "SEA", "Boeing 737-400", "2F", "First", "Alyeska pipeline winter audit")
    add("2001-02-05", "Continental Airlines", "CO 1520", "SEA", "IAH", "Boeing 737-800", "4B", "First", "Houston reservoir simulation team")
    add("2001-04-02", "Continental Airlines", "CO 99", "IAH", "HKG", "Boeing 777-200ER", "2A", "BusinessFirst", "Inaugural season nonstop polar flight to Hong Kong!")
    add("2001-04-12", "Continental Airlines", "CO 98", "HKG", "IAH", "Boeing 777-200ER", "3A", "BusinessFirst", "Return from South China Sea engineering review")
    add("2001-06-14", "Continental Airlines", "CO 1704", "IAH", "ANC", "Boeing 757-200", "2B", "First", "Cook Inlet summer platform turnaround")
    add("2001-07-02", "Alaska Airlines", "AS 84", "ANC", "SEA", "Boeing 737-400", "3D", "First", "Pacific Northwest transit")
    add("2001-08-15", "Air Canada", "AC 138", "YYC", "YYZ", "Airbus A320-200", "2C", "Business", "Calgary upstream headquarters to Toronto")
    add("2001-08-15", "Air Canada", "AC 614", "YYZ", "YHZ", "Airbus A319", "2D", "Business", "Halifax subsea pipe manifold inspection")
    add("2001-08-22", "Air Canada", "AC 623", "YHZ", "YYZ", "Boeing 767-300ER", "4A", "Business", "Halifax SOEP project wrap-up")
    add("2001-11-20", "Alaska Airlines", "AS 853", "ANC", "HNL", "Boeing 737-700", "3A", "First", "Reluctant family holiday: Dave abhored the beach!")
    add("2001-11-28", "Alaska Airlines", "AS 852", "HNL", "ANC", "Boeing 737-700", "3F", "First", "Finally leaving the sand: back to cold Alaska tundra")

    # =========================================================================
    # 2002 (10 flights): South China Sea deepwater fabrication & Sable Island
    # =========================================================================
    add("2002-03-08", "Continental Airlines", "CO 99", "IAH", "HKG", "Boeing 777-200ER", "1A", "BusinessFirst", "Shekou shipyard jacket fabrication audit")
    add("2002-03-18", "Continental Airlines", "CO 98", "HKG", "IAH", "Boeing 777-200ER", "2A", "BusinessFirst", "Transpacific polar return to Houston")
    add("2002-05-04", "Continental Airlines", "CO 1840", "IAH", "EWR", "Boeing 757-200", "3A", "First", "East Coast offshore project liaison")
    add("2002-05-04", "Air Canada", "AC 8920", "EWR", "YHZ", "Bombardier CRJ-200", "1B", "Economy", "Deep Panuke preliminary reservoir modeling")
    add("2002-05-12", "Air Canada", "AC 615", "YHZ", "YYZ", "Airbus A320-200", "2D", "Business", "Trans-Canada pipeline coordination")
    add("2002-05-12", "Continental Airlines", "CO 1980", "YYZ", "IAH", "Boeing 737-700", "3C", "First", "Houston Energy Corridor debrief")
    add("2002-08-10", "Alaska Airlines", "AS 82", "ANC", "SEA", "Boeing 737-400", "2C", "First", "Kuparuk reservoir pressure maintenance study")
    add("2002-08-10", "Continental Airlines", "CO 1520", "SEA", "IAH", "Boeing 737-800", "1E", "First", "Houston deepwater tech center")
    add("2002-09-02", "Continental Airlines", "CO 1521", "IAH", "SEA", "Boeing 737-800", "2A", "First", "Return via Seattle")
    add("2002-09-02", "Alaska Airlines", "AS 87", "SEA", "ANC", "Boeing 737-400", "3A", "First", "Anchorage autumn planning")

    # =========================================================================
    # 2003 (11 flights): Singapore/Hong Kong shipyard & Bali side-trip
    # =========================================================================
    add("2003-01-15", "Alaska Airlines", "AS 80", "ANC", "SEA", "Boeing 737-400", "2A", "First", "Arctic logistics planning")
    add("2003-01-15", "Continental Airlines", "CO 1520", "SEA", "IAH", "Boeing 737-800", "3B", "First", "Houston corporate reservoir team")
    add("2003-03-12", "Continental Airlines", "CO 99", "IAH", "HKG", "Boeing 777-200ER", "2A", "BusinessFirst", "Asia-Pacific offshore drilling conference")
    add("2003-03-18", "Singapore Airlines", "SQ 861", "HKG", "SIN", "Boeing 777-200ER", "12A", "Business", "Jurong shipyard FPSO conversion inspection")
    add("2003-03-22", "Garuda Indonesia", "GA 841", "SIN", "DPS", "Boeing 737-400", "2F", "Business", "Reluctant holiday: Dave stayed in the AC room reading reservoir logs!")
    add("2003-03-27", "Singapore Airlines", "SQ 947", "DPS", "SIN", "Boeing 777-200ER", "11K", "Business", "Leaving Bali beaches behind with immense relief")
    add("2003-03-28", "Singapore Airlines", "SQ 860", "SIN", "HKG", "Boeing 777-200ER", "14A", "Business", "Transit back through Hong Kong")
    add("2003-03-30", "Continental Airlines", "CO 98", "HKG", "IAH", "Boeing 777-200ER", "1B", "BusinessFirst", "Polar nonstop route home to Houston")
    add("2003-06-18", "Continental Airlines", "CO 1704", "IAH", "ANC", "Boeing 757-200", "2A", "First", "Cook Inlet summer platform survey")
    add("2003-09-14", "Air Canada", "AC 614", "YYZ", "YHZ", "Airbus A319", "3C", "Business", "Halifax SOEP platform upgrade inspection")
    add("2003-09-20", "Air Canada", "AC 623", "YHZ", "YYZ", "Boeing 767-300ER", "2A", "Business", "Return via Toronto")

    # =========================================================================
    # 2004 (10 flights): Deep Panuke offshore subsea FEED & North Slope
    # =========================================================================
    add("2004-02-10", "Alaska Airlines", "AS 82", "ANC", "SEA", "Boeing 737-700", "2A", "First", "New 737-700 fleet introduction")
    add("2004-02-10", "Continental Airlines", "CO 1520", "SEA", "IAH", "Boeing 737-800", "2E", "First", "OTC Houston planning session")
    add("2004-04-18", "Continental Airlines", "CO 99", "IAH", "HKG", "Boeing 777-200ER", "3A", "BusinessFirst", "South China Sea subsea manifold fabrication")
    add("2004-04-28", "Continental Airlines", "CO 98", "HKG", "IAH", "Boeing 777-200ER", "2B", "BusinessFirst", "Return polar transit")
    add("2004-06-08", "Air Canada", "AC 614", "YYZ", "YHZ", "Airbus A320-200", "1C", "Business", "Deep Panuke project sanctioning review")
    add("2004-06-16", "Air Canada", "AC 615", "YHZ", "YYZ", "Airbus A320-200", "2A", "Business", "Halifax to Toronto corporate debrief")
    add("2004-08-20", "Continental Airlines", "CO 1704", "IAH", "ANC", "Boeing 757-200", "1F", "First", "Prudhoe Bay facility integrity review")
    add("2004-09-08", "Alaska Airlines", "AS 130", "ANC", "SEA", "Boeing 737-700", "3D", "First", "Anchorage to Seattle hub")
    add("2004-10-18", "Alaska Airlines", "AS 81", "SEA", "ANC", "Boeing 737-700", "2A", "First", "Cook Inlet winter gas reservoir monitoring")
    add("2004-11-12", "Continental Airlines", "CO 1840", "IAH", "EWR", "Boeing 757-200", "3B", "First", "Offshore technical liaison")
    add("2004-11-12", "Air Canada", "AC 8920", "EWR", "YHZ", "Bombardier CRJ-200", "1A", "Economy", "Halifax winter weather platform resilience")

    # =========================================================================
    # 2005 (11 flights): 5th anniversary of globe-trotting & Reluctant HNL return
    # =========================================================================
    add("2005-01-22", "Alaska Airlines", "AS 80", "ANC", "SEA", "Boeing 737-400", "2C", "First", "North Slope winter drilling review")
    add("2005-01-22", "Continental Airlines", "CO 1520", "SEA", "IAH", "Boeing 737-800", "1B", "First", "Energy Corridor reservoir meetings")
    add("2005-03-14", "Continental Airlines", "CO 99", "IAH", "HKG", "Boeing 777-200ER", "2A", "BusinessFirst", "Pearl River Delta offshore fabrication")
    add("2005-03-24", "Continental Airlines", "CO 98", "HKG", "IAH", "Boeing 777-200ER", "3A", "BusinessFirst", "Transpacific return to Houston")
    add("2005-05-18", "Air Canada", "AC 614", "YYZ", "YHZ", "Airbus A319", "2D", "Business", "Halifax offshore logistics center")
    add("2005-05-25", "Air Canada", "AC 623", "YHZ", "YYZ", "Boeing 767-300ER", "3B", "Business", "Deep Panuke engineering updates")
    add("2005-07-10", "Continental Airlines", "CO 1704", "IAH", "ANC", "Boeing 757-200", "2E", "First", "Summer Cook Inlet rig turnaround")
    add("2005-08-04", "Alaska Airlines", "AS 84", "ANC", "SEA", "Boeing 737-700", "2A", "First", "Anchorage to Seattle operations")
    add("2005-10-12", "Continental Airlines", "CO 1520", "SEA", "IAH", "Boeing 737-800", "3A", "First", "Deepwater Gulf of Mexico technical exchange")
    add("2005-11-22", "Continental Airlines", "CO 1", "IAH", "HNL", "Boeing 767-400ER", "4A", "BusinessFirst", "Second reluctant family vacation: Dave worked from the hotel balcony")
    add("2005-11-29", "Continental Airlines", "CO 2", "HNL", "IAH", "Boeing 767-400ER", "4L", "BusinessFirst", "Fleeing the Hawaiian sun back to rainy Houston")

    # =========================================================================
    # 2006 (10 flights): Alaska NextGen 737-800 & Halifax subsea pipelines
    # =========================================================================
    add("2006-02-14", "Alaska Airlines", "AS 82", "ANC", "SEA", "Boeing 737-800", "2A", "First", "First flight on Alaska's new 737-800")
    add("2006-02-14", "Continental Airlines", "CO 1520", "SEA", "IAH", "Boeing 737-800", "2C", "First", "Houston reservoir simulation team")
    add("2006-04-10", "Continental Airlines", "CO 99", "IAH", "HKG", "Boeing 777-200ER", "1A", "BusinessFirst", "South China Sea deepwater JV meeting")
    add("2006-04-20", "Continental Airlines", "CO 98", "HKG", "IAH", "Boeing 777-200ER", "2A", "BusinessFirst", "Polar nonstop route back to IAH")
    add("2006-06-02", "Air Canada", "AC 614", "YYZ", "YHZ", "Embraer 190", "2A", "Business", "Testing Air Canada's brand new E190 fleet")
    add("2006-06-10", "Air Canada", "AC 615", "YHZ", "YYZ", "Embraer 190", "1F", "Business", "Halifax SOEP platform inspection")
    add("2006-07-28", "Continental Airlines", "CO 1704", "IAH", "ANC", "Boeing 757-200", "3A", "First", "Cook Inlet summer operations")
    add("2006-08-16", "Alaska Airlines", "AS 130", "ANC", "SEA", "Boeing 737-800", "1D", "First", "Alaska pipeline geotechnical review")
    add("2006-10-04", "Continental Airlines", "CO 1840", "IAH", "EWR", "Boeing 757-200", "2F", "First", "Transit to Atlantic Canada")
    add("2006-10-04", "Air Canada", "AC 8920", "EWR", "YHZ", "Bombardier CRJ-200", "2B", "Economy", "Subsea wellhead intervention meeting")

    # =========================================================================
    # 2007 (11 flights): Deep Panuke final design & Hong Kong/Shenzhen drydock
    # =========================================================================
    add("2007-01-16", "Alaska Airlines", "AS 80", "ANC", "SEA", "Boeing 737-800", "2F", "First", "Prudhoe Bay arctic equipment winterization")
    add("2007-01-16", "Continental Airlines", "CO 1520", "SEA", "IAH", "Boeing 737-800", "3A", "First", "Houston deepwater development review")
    add("2007-03-20", "Continental Airlines", "CO 99", "IAH", "HKG", "Boeing 777-200ER", "2A", "BusinessFirst", "Yantian/Shekou shipyard fabrication progress")
    add("2007-03-30", "Continental Airlines", "CO 98", "HKG", "IAH", "Boeing 777-200ER", "1A", "BusinessFirst", "Return via North Pole corridor")
    add("2007-05-14", "Air Canada", "AC 614", "YYZ", "YHZ", "Embraer 190", "2A", "Business", "Halifax offshore gas export terminal review")
    add("2007-05-22", "Air Canada", "AC 623", "YHZ", "YYZ", "Boeing 767-300ER", "3A", "Business", "Return to Calgary energy branch")
    add("2007-07-08", "Continental Airlines", "CO 1704", "IAH", "ANC", "Boeing 757-200", "2B", "First", "Cook Inlet platform maintenance")
    add("2007-08-12", "Alaska Airlines", "AS 84", "ANC", "SEA", "Boeing 737-800", "2C", "First", "Anchorage to Seattle connection")
    add("2007-09-18", "Continental Airlines", "CO 1520", "SEA", "IAH", "Boeing 737-800", "1C", "First", "Gulf of Mexico subsea tieback design")
    add("2007-11-15", "Air Canada", "AC 8920", "EWR", "YHZ", "Bombardier CRJ-200", "1B", "Economy", "Offshore winter safety drill in Halifax")
    add("2007-11-20", "Air Canada", "AC 615", "YHZ", "YYZ", "Airbus A320-200", "2F", "Business", "Return via Toronto")

    # =========================================================================
    # 2008 (11 flights): Global Financial Crisis resilience & Singapore/Bali
    # =========================================================================
    add("2008-02-11", "Alaska Airlines", "AS 82", "ANC", "SEA", "Boeing 737-800", "1A", "First", "North Slope production optimization")
    add("2008-02-11", "Continental Airlines", "CO 1520", "SEA", "IAH", "Boeing 737-800", "2B", "First", "Energy Corridor budgeting during oil peak ($140/bbl)")
    add("2008-04-15", "Continental Airlines", "CO 99", "IAH", "HKG", "Boeing 777-200ER", "2A", "BusinessFirst", "South China Sea exploration joint venture")
    add("2008-04-22", "Singapore Airlines", "SQ 861", "HKG", "SIN", "Boeing 777-300ER", "11K", "Business", "Keppel shipyard deepwater rig inspection")
    add("2008-04-26", "Garuda Indonesia", "GA 841", "SIN", "DPS", "Boeing 737-400", "2D", "Business", "Reluctant holiday #2: Dave brought 4 offshore textbooks")
    add("2008-04-30", "Singapore Airlines", "SQ 947", "DPS", "SIN", "Boeing 777-200ER", "12A", "Business", "Happily departing the tropics")
    add("2008-05-02", "Singapore Airlines", "SQ 860", "SIN", "HKG", "Boeing 777-300ER", "14K", "Business", "Transit back through Hong Kong")
    add("2008-05-04", "Continental Airlines", "CO 98", "HKG", "IAH", "Boeing 777-200ER", "1B", "BusinessFirst", "Polar nonstop route home to Houston")
    add("2008-07-20", "Continental Airlines", "CO 1704", "IAH", "ANC", "Boeing 757-200", "3A", "First", "Cook Inlet summer rig turnaround")
    add("2008-09-14", "Air Canada", "AC 614", "YYZ", "YHZ", "Embraer 190", "2A", "Business", "Deep Panuke subsea development")
    add("2008-09-21", "Air Canada", "AC 623", "YHZ", "YYZ", "Boeing 767-300ER", "2F", "Business", "Halifax to Toronto transit")

    # =========================================================================
    # 2009 (10 flights): Deep Panuke fabrication & Arctic winterization
    # =========================================================================
    add("2009-01-20", "Alaska Airlines", "AS 80", "ANC", "SEA", "Boeing 737-800", "2C", "First", "Kuparuk winter operations")
    add("2009-01-20", "Continental Airlines", "CO 1520", "SEA", "IAH", "Boeing 737-800", "1E", "First", "Houston reservoir simulation team")
    add("2009-03-24", "Continental Airlines", "CO 99", "IAH", "HKG", "Boeing 777-200ER", "2A", "BusinessFirst", "Offshore rig construction review in Shekou")
    add("2009-04-04", "Continental Airlines", "CO 98", "HKG", "IAH", "Boeing 777-200ER", "2B", "BusinessFirst", "Return polar transit")
    add("2009-06-12", "Air Canada", "AC 614", "YYZ", "YHZ", "Embraer 190", "1A", "Business", "Halifax offshore operations center")
    add("2009-06-20", "Air Canada", "AC 615", "YHZ", "YYZ", "Airbus A320-200", "3C", "Business", "Deep Panuke milestone review")
    add("2009-08-05", "Continental Airlines", "CO 1704", "IAH", "ANC", "Boeing 757-200", "2A", "First", "Cook Inlet summer platform survey")
    add("2009-08-25", "Alaska Airlines", "AS 130", "ANC", "SEA", "Boeing 737-800", "3D", "First", "Anchorage to Seattle")
    add("2009-10-18", "Continental Airlines", "CO 1840", "IAH", "EWR", "Boeing 757-200", "2E", "First", "Offshore technology exchange")
    add("2009-10-18", "Air Canada", "AC 8920", "EWR", "YHZ", "Bombardier CRJ-200", "2A", "Economy", "Atlantic Canada winter preparedness")

    # =========================================================================
    # 2010 (11 flights): Macondo/Deepwater Horizon industry reviews & Halifax
    # =========================================================================
    add("2010-02-16", "Alaska Airlines", "AS 82", "ANC", "SEA", "Boeing 737-800", "2A", "First", "Prudhoe Bay containment review")
    add("2010-02-16", "Continental Airlines", "CO 1520", "SEA", "IAH", "Boeing 737-800", "2D", "First", "Houston deepwater well control summit")
    add("2010-04-20", "Continental Airlines", "CO 99", "IAH", "HKG", "Boeing 777-200ER", "1A", "BusinessFirst", "Asia-Pacific offshore safety protocols")
    add("2010-04-30", "Continental Airlines", "CO 98", "HKG", "IAH", "Boeing 777-200ER", "3A", "BusinessFirst", "Polar nonstop route home to Houston")
    add("2010-06-15", "Air Canada", "AC 614", "YYZ", "YHZ", "Embraer 190", "2F", "Business", "Halifax subsea blow-out preventer audit")
    add("2010-06-22", "Air Canada", "AC 623", "YHZ", "YYZ", "Boeing 767-300ER", "2A", "Business", "Return via Toronto")
    add("2010-07-18", "Continental Airlines", "CO 1704", "IAH", "ANC", "Boeing 757-200", "1B", "First", "Cook Inlet platform safety audit")
    add("2010-08-10", "Alaska Airlines", "AS 84", "ANC", "SEA", "Boeing 737-800", "2C", "First", "Anchorage to Seattle operations")
    add("2010-10-05", "Continental Airlines", "CO 1520", "SEA", "IAH", "Boeing 737-800", "3B", "First", "BOP recertification committee in Houston")
    add("2010-11-24", "Continental Airlines", "CO 1", "IAH", "HNL", "Boeing 767-400ER", "3A", "BusinessFirst", "Thanksgiving in Hawaii: Dave brought his iPad loaded with subsea CAD drawings")
    add("2010-11-30", "Continental Airlines", "CO 2", "HNL", "IAH", "Boeing 767-400ER", "3L", "BusinessFirst", "Back to real work in Houston")

    # =========================================================================
    # 2011 (10 flights): Last year of Continental Airlines branding & Sable
    # =========================================================================
    add("2011-01-18", "Alaska Airlines", "AS 80", "ANC", "SEA", "Boeing 737-800", "2A", "First", "North Slope winter drilling review")
    add("2011-01-18", "Continental Airlines", "CO 1520", "SEA", "IAH", "Boeing 737-800", "2B", "First", "Houston Energy Corridor corporate meeting")
    add("2011-03-22", "Continental Airlines", "CO 99", "IAH", "HKG", "Boeing 777-200ER", "2A", "BusinessFirst", "Final flight under Continental CO flight code to HKG")
    add("2011-04-02", "Continental Airlines", "CO 98", "HKG", "IAH", "Boeing 777-200ER", "1A", "BusinessFirst", "Farewell to Continental OnePass: Hello United MileagePlus")
    add("2011-05-18", "Air Canada", "AC 614", "YYZ", "YHZ", "Embraer 190", "2A", "Business", "Deep Panuke hookup and commissioning")
    add("2011-05-26", "Air Canada", "AC 615", "YHZ", "YYZ", "Airbus A320-200", "3C", "Business", "Halifax to Toronto corporate debrief")
    add("2011-07-14", "Continental Airlines", "CO 1704", "IAH", "ANC", "Boeing 757-200", "2A", "First", "Last Continental 757 summer flight to Anchorage")
    add("2011-08-08", "Alaska Airlines", "AS 130", "ANC", "SEA", "Boeing 737-800", "3D", "First", "Alaska pipeline geotechnical review")
    add("2011-10-12", "Air Canada", "AC 8920", "EWR", "YHZ", "Bombardier CRJ-200", "1B", "Economy", "Halifax offshore winter preparations")
    add("2011-10-20", "Air Canada", "AC 623", "YHZ", "YYZ", "Boeing 767-300ER", "2F", "Business", "Return via Toronto")

    # =========================================================================
    # 2012 (11 flights): United Airlines merger era begins & Alaska 737-900ER
    # =========================================================================
    add("2012-02-14", "Alaska Airlines", "AS 82", "ANC", "SEA", "Boeing 737-900ER", "2A", "First", "First ride on Alaska's Boeing 737-900ER")
    add("2012-02-14", "United Airlines", "UA 1520", "SEA", "IAH", "Boeing 737-800", "2B", "First", "Merged United livery flight to Houston")
    add("2012-04-10", "United Airlines", "UA 179", "EWR", "HKG", "Boeing 777-200ER", "3A", "Business", "Transpacific crossing to Hong Kong via Newark")
    add("2012-04-20", "United Airlines", "UA 180", "HKG", "EWR", "Boeing 777-200ER", "2A", "Business", "Polar return from South China Sea reviews")
    add("2012-06-05", "Air Canada", "AC 614", "YYZ", "YHZ", "Embraer 190", "1A", "Business", "Halifax Deep Panuke offshore hookup")
    add("2012-06-12", "Air Canada", "AC 615", "YHZ", "YYZ", "Airbus A320-200", "2F", "Business", "Halifax SOEP platform inspection")
    add("2012-07-22", "United Airlines", "UA 1144", "IAH", "ANC", "Boeing 757-200", "1B", "First", "United summer nonstop to Anchorage")
    add("2012-08-15", "Alaska Airlines", "AS 84", "ANC", "SEA", "Boeing 737-900ER", "2F", "First", "Anchorage to Seattle operations")
    add("2012-09-18", "United Airlines", "UA 1520", "SEA", "IAH", "Boeing 737-800", "3A", "First", "Houston deepwater development review")
    add("2012-11-20", "Alaska Airlines", "AS 853", "ANC", "HNL", "Boeing 737-800", "2C", "First", "Thanksgiving in Honolulu: Dave sat by the pool with earplugs analyzing well logs")
    add("2012-11-27", "Alaska Airlines", "AS 852", "HNL", "ANC", "Boeing 737-800", "3A", "First", "Gladly returning to subzero Anchorage")

    # =========================================================================
    # 2013 (11 flights): Deep Panuke first gas & Singapore FPSO delivery
    # =========================================================================
    add("2013-01-22", "Alaska Airlines", "AS 80", "ANC", "SEA", "Boeing 737-900ER", "1A", "First", "Prudhoe Bay winter operations")
    add("2013-01-22", "United Airlines", "UA 1520", "SEA", "IAH", "Boeing 737-900ER", "2A", "First", "Houston corporate reservoir team")
    add("2013-03-15", "United Airlines", "UA 895", "ORD", "HKG", "Boeing 777-200ER", "2A", "Business", "Hong Kong project steering committee")
    add("2013-03-20", "Singapore Airlines", "SQ 861", "HKG", "SIN", "Boeing 777-300ER", "11A", "Business", "Sembcorp shipyard FPSO topsides integration")
    add("2013-03-24", "Singapore Airlines", "SQ 942", "SIN", "DPS", "Boeing 777-200ER", "12K", "Business", "Bali family trip: Dave stayed indoors citing humidity concerns")
    add("2013-03-29", "Singapore Airlines", "SQ 943", "DPS", "SIN", "Boeing 777-200ER", "14A", "Business", "Return flight from Denpasar to Changi")
    add("2013-03-30", "Singapore Airlines", "SQ 860", "SIN", "HKG", "Boeing 777-300ER", "11K", "Business", "Hong Kong connection")
    add("2013-04-01", "United Airlines", "UA 896", "HKG", "ORD", "Boeing 777-200ER", "3B", "Business", "Polar transpacific crossing to Chicago/Houston")
    add("2013-07-10", "United Airlines", "UA 1144", "IAH", "ANC", "Boeing 757-200", "2A", "First", "Cook Inlet summer rig turnaround")
    add("2013-09-12", "Air Canada", "AC 614", "YYZ", "YHZ", "Airbus A320-200", "2A", "Business", "Deep Panuke First Gas celebrations in Halifax")
    add("2013-09-18", "Air Canada", "AC 623", "YHZ", "YYZ", "Boeing 767-300ER", "2F", "Business", "Halifax to Toronto return")

    # =========================================================================
    # 2014 (10 flights): Gulf of Mexico Deepwater drilling & Halifax
    # =========================================================================
    add("2014-02-18", "Alaska Airlines", "AS 82", "ANC", "SEA", "Boeing 737-900ER", "2A", "First", "Kuparuk reservoir pressure maintenance")
    add("2014-02-18", "United Airlines", "UA 1520", "SEA", "IAH", "Boeing 737-900ER", "3B", "First", "Houston deepwater tech center")
    add("2014-04-22", "United Airlines", "UA 869", "SFO", "HKG", "Boeing 747-400", "15K", "Business", "Upper deck Boeing 747-400 transpacific flight!")
    add("2014-05-02", "United Airlines", "UA 862", "HKG", "SFO", "Boeing 747-400", "17A", "Business", "Return flight across the Pacific")
    add("2014-06-14", "Air Canada", "AC 614", "YYZ", "YHZ", "Embraer 190", "1A", "Business", "Halifax Deep Panuke production optimization")
    add("2014-06-22", "Air Canada", "AC 615", "YHZ", "YYZ", "Airbus A320-200", "2C", "Business", "SOEP late-life reservoir management")
    add("2014-08-10", "United Airlines", "UA 1144", "IAH", "ANC", "Boeing 737-900ER", "2E", "First", "Cook Inlet platform maintenance")
    add("2014-09-02", "Alaska Airlines", "AS 130", "ANC", "SEA", "Boeing 737-900ER", "1D", "First", "Anchorage to Seattle operations")
    add("2014-10-15", "Air Canada", "AC 8920", "EWR", "YHZ", "Bombardier CRJ-200", "1B", "Economy", "Offshore winter storm protocols review")
    add("2014-10-22", "Air Canada", "AC 623", "YHZ", "YYZ", "Airbus A330-300", "3A", "Business", "Air Canada A330 widebody service to Toronto")

    # =========================================================================
    # 2015 (11 flights): United 787-9 Dreamliner inaugural & Oil Price Downturn
    # =========================================================================
    add("2015-01-20", "Alaska Airlines", "AS 80", "ANC", "SEA", "Boeing 737-900ER", "2F", "First", "Prudhoe Bay cost reduction task force ($45 oil)")
    add("2015-01-20", "United Airlines", "UA 1520", "SEA", "IAH", "Boeing 737-900ER", "2A", "First", "Houston emergency capital allocation meeting")
    add("2015-03-18", "United Airlines", "UA 869", "SFO", "HKG", "Boeing 787-9", "2A", "Business", "First flight on the new Boeing 787-9 Dreamliner!")
    add("2015-03-28", "United Airlines", "UA 862", "HKG", "SFO", "Boeing 787-9", "3A", "Business", "Smoother ride and better cabin humidity across Pacific")
    add("2015-05-12", "Air Canada", "AC 614", "YYZ", "YHZ", "Embraer 190", "2A", "Business", "Deep Panuke cost efficiency reviews")
    add("2015-05-20", "Air Canada", "AC 615", "YHZ", "YYZ", "Airbus A320-200", "2D", "Business", "Halifax to Toronto corporate transit")
    add("2015-07-15", "United Airlines", "UA 1144", "IAH", "ANC", "Boeing 737-900ER", "1B", "First", "Summer Cook Inlet platform review")
    add("2015-08-18", "Alaska Airlines", "AS 84", "ANC", "SEA", "Boeing 737-900ER", "2C", "First", "Anchorage to Seattle operations")
    add("2015-10-08", "United Airlines", "UA 1520", "SEA", "IAH", "Boeing 737-900ER", "3B", "First", "Houston deepwater tech center")
    add("2015-11-20", "United Airlines", "UA 1", "IAH", "HNL", "Boeing 777-200ER", "4A", "First", "Thanksgiving trip: Dave hid in the hotel business lounge writing reports")
    add("2015-11-28", "United Airlines", "UA 2", "HNL", "IAH", "Boeing 777-200ER", "4L", "First", "Leaving Hawaii with profound satisfaction")

    # =========================================================================
    # 2016 (10 flights): North Slope Arctic gas pipeline studies & Halifax
    # =========================================================================
    add("2016-02-16", "Alaska Airlines", "AS 82", "ANC", "SEA", "Boeing 737-900ER", "2A", "First", "AK LNG pipeline environmental impact team")
    add("2016-02-16", "United Airlines", "UA 1520", "SEA", "IAH", "Boeing 737-900ER", "2C", "First", "Houston gas processing facility engineers")
    add("2016-04-12", "United Airlines", "UA 869", "SFO", "HKG", "Boeing 787-9", "1A", "Polaris Business", "Hong Kong LNG buyers symposium")
    add("2016-04-22", "United Airlines", "UA 862", "HKG", "SFO", "Boeing 787-9", "2A", "Polaris Business", "Return transpacific crossing")
    add("2016-06-08", "Air Canada", "AC 614", "YYZ", "YHZ", "Embraer 190", "1A", "Business", "Halifax offshore subsea decommissioning studies")
    add("2016-06-15", "Air Canada", "AC 615", "YHZ", "YYZ", "Airbus A320-200", "3C", "Business", "Sable Offshore late-life planning")
    add("2016-07-25", "United Airlines", "UA 1144", "IAH", "ANC", "Boeing 737-900ER", "2A", "First", "Cook Inlet summer platform survey")
    add("2016-08-20", "Alaska Airlines", "AS 130", "ANC", "SEA", "Boeing 737-900ER", "3D", "First", "Anchorage to Seattle operations")
    add("2016-10-14", "Air Canada", "AC 8920", "EWR", "YHZ", "Bombardier CRJ-200", "2A", "Economy", "Atlantic Canada winter offshore safety")
    add("2016-10-22", "Air Canada", "AC 623", "YHZ", "YYZ", "Airbus A330-300", "2F", "Business", "Halifax to Toronto transit")

    # =========================================================================
    # 2017 (11 flights): United Polaris rollout & Singapore/Bali
    # =========================================================================
    add("2017-01-24", "Alaska Airlines", "AS 80", "ANC", "SEA", "Boeing 737-900ER", "2F", "First", "Prudhoe Bay enhanced oil recovery audit")
    add("2017-01-24", "United Airlines", "UA 1520", "SEA", "IAH", "Boeing 737-900ER", "1A", "First", "Houston deepwater tech center")
    add("2017-03-14", "United Airlines", "UA 179", "EWR", "HKG", "Boeing 777-300ER", "3A", "Polaris Business", "First flight in United's new Polaris Business Class suite!")
    add("2017-03-20", "Singapore Airlines", "SQ 861", "HKG", "SIN", "Boeing 777-300ER", "11K", "Business", "Jurong shipyard subsea manifold completion")
    add("2017-03-24", "Singapore Airlines", "SQ 942", "SIN", "DPS", "Boeing 777-200ER", "14A", "Business", "Annual family retreat: Dave wore boots and jeans in 90F Bali heat")
    add("2017-03-29", "Singapore Airlines", "SQ 943", "DPS", "SIN", "Boeing 777-200ER", "12A", "Business", "Farewell to Denpasar, Bali")
    add("2017-03-30", "Singapore Airlines", "SQ 860", "SIN", "HKG", "Boeing 777-300ER", "11A", "Business", "Hong Kong connection")
    add("2017-04-01", "United Airlines", "UA 180", "HKG", "EWR", "Boeing 777-300ER", "2A", "Polaris Business", "Polaris transpacific flight home")
    add("2017-07-12", "United Airlines", "UA 1144", "IAH", "ANC", "Boeing 737-900ER", "2F", "First", "Cook Inlet summer rig turnaround")
    add("2017-09-15", "Air Canada", "AC 614", "YYZ", "YHZ", "Embraer 190", "2A", "Business", "Halifax offshore gas export terminal review")
    add("2017-09-22", "Air Canada", "AC 623", "YHZ", "YYZ", "Airbus A330-300", "3A", "Business", "Deep Panuke cessation of production planning")

    # =========================================================================
    # 2018 (10 flights): Alaska Airlines / Virgin America merger & Halifax SOEP
    # =========================================================================
    add("2018-02-13", "Alaska Airlines", "AS 82", "ANC", "SEA", "Boeing 737-900ER", "2A", "First", "Kuparuk production debrief")
    add("2018-02-13", "United Airlines", "UA 1520", "SEA", "IAH", "Boeing 737-900ER", "3A", "First", "Houston reservoir simulation team")
    add("2018-04-18", "United Airlines", "UA 869", "SFO", "HKG", "Boeing 777-300ER", "1A", "Polaris Business", "South China Sea deepwater JV meeting")
    add("2018-04-28", "United Airlines", "UA 862", "HKG", "SFO", "Boeing 777-300ER", "2A", "Polaris Business", "Polaris lie-flat return flight")
    add("2018-06-10", "Air Canada", "AC 614", "YYZ", "YHZ", "Airbus A320-200", "2C", "Business", "Sable Offshore decommissioning plan submitted")
    add("2018-06-18", "Air Canada", "AC 615", "YHZ", "YYZ", "Airbus A320-200", "1F", "Business", "Halifax to Toronto corporate debrief")
    add("2018-07-28", "United Airlines", "UA 1144", "IAH", "ANC", "Boeing 737-900ER", "1B", "First", "Summer Cook Inlet platform review")
    add("2018-08-22", "Alaska Airlines", "AS 84", "ANC", "SEA", "Boeing 737-900ER", "2C", "First", "Anchorage to Seattle operations")
    add("2018-10-10", "Air Canada", "AC 614", "YYZ", "YHZ", "Airbus A320-200", "2A", "Business", "Deep Panuke final well plug and abandonment review")
    add("2018-10-18", "Air Canada", "AC 623", "YHZ", "YYZ", "Airbus A330-300", "2F", "Business", "Halifax to Toronto transit")

    # =========================================================================
    # 2019 (11 flights): Pre-pandemic peak travel & Reluctant HNL Christmas
    # =========================================================================
    add("2019-01-22", "Alaska Airlines", "AS 80", "ANC", "SEA", "Boeing 737-900ER", "2A", "First", "North Slope winter drilling review")
    add("2019-01-22", "United Airlines", "UA 1520", "SEA", "IAH", "Boeing 737-900ER", "2C", "First", "Houston deepwater tech center")
    add("2019-03-26", "United Airlines", "UA 869", "SFO", "HKG", "Boeing 777-300ER", "3A", "Polaris Business", "Asia-Pacific offshore safety summit in Hong Kong")
    add("2019-04-06", "United Airlines", "UA 862", "HKG", "SFO", "Boeing 777-300ER", "2A", "Polaris Business", "Return transpacific crossing")
    add("2019-05-14", "Air Canada", "AC 614", "YYZ", "YHZ", "Airbus A320-200", "1A", "Business", "Halifax offshore environmental baseline audit")
    add("2019-05-22", "Air Canada", "AC 615", "YHZ", "YYZ", "Airbus A320-200", "2F", "Business", "Halifax to Toronto corporate transit")
    add("2019-07-16", "United Airlines", "UA 1144", "IAH", "ANC", "Boeing 737-900ER", "2E", "First", "Cook Inlet platform maintenance")
    add("2019-08-14", "Alaska Airlines", "AS 130", "ANC", "SEA", "Boeing 737-900ER", "1C", "First", "Anchorage to Seattle operations")
    add("2019-10-04", "Air Canada", "AC 614", "YYZ", "YHZ", "Airbus A320-200", "2A", "Business", "Subsea wellhead removal oversight in Halifax")
    add("2019-12-22", "Alaska Airlines", "AS 853", "ANC", "HNL", "Boeing 737-900ER", "2F", "First", "Christmas in Hawaii: Dave demanded hotel rooms with high-speed internet and zero sand")
    add("2019-12-29", "Alaska Airlines", "AS 852", "HNL", "ANC", "Boeing 737-900ER", "2A", "First", "Escaping the beach back to Alaska snow")

    # =========================================================================
    # 2020 (8 flights): COVID-19 pandemic disruptions & essential energy travel
    # =========================================================================
    add("2020-01-20", "Alaska Airlines", "AS 82", "ANC", "SEA", "Boeing 737-900ER", "2A", "First", "Pre-lockdown Prudhoe Bay review")
    add("2020-01-20", "United Airlines", "UA 1520", "SEA", "IAH", "Boeing 737-900ER", "1B", "First", "Houston corporate emergency planning")
    add("2020-02-25", "United Airlines", "UA 1521", "IAH", "SEA", "Boeing 737-900ER", "2E", "First", "Return via Seattle")
    add("2020-02-25", "Alaska Airlines", "AS 87", "SEA", "ANC", "Boeing 737-900ER", "3A", "First", "Anchorage operations base")
    add("2020-06-18", "Alaska Airlines", "AS 80", "ANC", "SEA", "Boeing 737-900ER", "1A", "First", "Essential infrastructure worker transit")
    add("2020-06-18", "United Airlines", "UA 1520", "SEA", "IAH", "Boeing 737-900ER", "2A", "First", "Deepwater emergency response center")
    add("2020-09-15", "Air Canada", "AC 614", "YYZ", "YHZ", "Airbus A220-300", "2A", "Business", "First flight on Air Canada's quiet A220-300!")
    add("2020-09-22", "Air Canada", "AC 615", "YHZ", "YYZ", "Airbus A220-300", "1F", "Business", "Halifax platform decommissioning liaison")

    # =========================================================================
    # 2021 (11 flights): Alaska 737 MAX 9 debut & Hong Kong reopening
    # =========================================================================
    add("2021-02-16", "Alaska Airlines", "AS 82", "ANC", "SEA", "Boeing 737 MAX 9", "2A", "First", "First flight on Alaska's Boeing 737 MAX 9")
    add("2021-02-16", "United Airlines", "UA 1520", "SEA", "IAH", "Boeing 737-900ER", "2C", "First", "Houston Energy Corridor tech center")
    add("2021-04-20", "United Airlines", "UA 869", "SFO", "HKG", "Boeing 777-300ER", "1A", "Polaris Business", "Hong Kong offshore safety audit")
    add("2021-04-30", "United Airlines", "UA 862", "HKG", "SFO", "Boeing 777-300ER", "2A", "Polaris Business", "Transpacific polar return")
    add("2021-06-12", "Air Canada", "AC 614", "YYZ", "YHZ", "Airbus A220-300", "2F", "Business", "Halifax offshore reefing monitoring")
    add("2021-06-20", "Air Canada", "AC 615", "YHZ", "YYZ", "Airbus A220-300", "3A", "Business", "Halifax to Toronto corporate debrief")
    add("2021-07-28", "United Airlines", "UA 1144", "IAH", "ANC", "Boeing 737 MAX 9", "2A", "First", "Cook Inlet summer rig turnaround")
    add("2021-08-20", "Alaska Airlines", "AS 84", "ANC", "SEA", "Boeing 737 MAX 9", "1D", "First", "Anchorage to Seattle operations")
    add("2021-10-15", "Air Canada", "AC 614", "YYZ", "YHZ", "Airbus A220-300", "2A", "Business", "Sable Offshore decommissioning closeout")
    add("2021-11-23", "United Airlines", "UA 1", "IAH", "HNL", "Boeing 777-200ER", "3A", "First", "Thanksgiving in Hawaii: Dave brought 2 portable monitors and closed the curtains")
    add("2021-11-30", "United Airlines", "UA 2", "HNL", "IAH", "Boeing 777-200ER", "3L", "First", "Gladly returning to Houston")

    # =========================================================================
    # 2022 (11 flights): High oil prices, energy security & Singapore/Bali
    # =========================================================================
    add("2022-01-20", "Alaska Airlines", "AS 80", "ANC", "SEA", "Boeing 737 MAX 9", "2F", "First", "Arctic energy security taskforce")
    add("2022-01-20", "United Airlines", "UA 1520", "SEA", "IAH", "Boeing 737 MAX 9", "1A", "First", "Energy Corridor emergency expansion meetings")
    add("2022-03-22", "United Airlines", "UA 869", "SFO", "HKG", "Boeing 777-300ER", "3A", "Polaris Business", "Hong Kong joint venture drilling council")
    add("2022-03-28", "Singapore Airlines", "SQ 861", "HKG", "SIN", "Boeing 777-300ER", "11K", "Business", "Changi / Keppel FPSO upgrade oversight")
    add("2022-04-02", "Singapore Airlines", "SQ 942", "SIN", "DPS", "Boeing 787-10", "12A", "Business", "Bali family vacation: Dave survived exactly 30 minutes outdoors")
    add("2022-04-07", "Singapore Airlines", "SQ 943", "DPS", "SIN", "Boeing 787-10", "14A", "Business", "Leaving Denpasar with immense gratitude")
    add("2022-04-08", "Singapore Airlines", "SQ 860", "SIN", "HKG", "Boeing 777-300ER", "11A", "Business", "Hong Kong transit")
    add("2022-04-10", "United Airlines", "UA 862", "HKG", "SFO", "Boeing 777-300ER", "2A", "Polaris Business", "Polaris return across Pacific")
    add("2022-07-15", "United Airlines", "UA 1144", "IAH", "ANC", "Boeing 737 MAX 9", "2F", "First", "Cook Inlet summer operations")
    add("2022-09-18", "Air Canada", "AC 614", "YYZ", "YHZ", "Airbus A220-300", "2A", "Business", "Deep Panuke offshore subsea habitat monitoring")
    add("2022-09-25", "Air Canada", "AC 623", "YHZ", "YYZ", "Boeing 787-9", "3A", "Business", "Halifax to Toronto Dreamliner service")

    # =========================================================================
    # 2023 (11 flights): Willow project approvals & Deep Panuke environmental review
    # =========================================================================
    add("2023-02-14", "Alaska Airlines", "AS 82", "ANC", "SEA", "Boeing 737 MAX 9", "2A", "First", "Willow oil development project sanctioning")
    add("2023-02-14", "United Airlines", "UA 1520", "SEA", "IAH", "Boeing 737 MAX 9", "2B", "First", "Houston technical engineering review")
    add("2023-04-18", "United Airlines", "UA 869", "SFO", "HKG", "Boeing 777-300ER", "1A", "Polaris Business", "Asia-Pacific offshore supplier audits")
    add("2023-04-28", "United Airlines", "UA 862", "HKG", "SFO", "Boeing 777-300ER", "2A", "Polaris Business", "Return transpacific crossing")
    add("2023-06-10", "Air Canada", "AC 614", "YYZ", "YHZ", "Airbus A220-300", "1A", "Business", "Halifax offshore decommissioning final sign-off")
    add("2023-06-18", "Air Canada", "AC 615", "YHZ", "YYZ", "Airbus A220-300", "2C", "Business", "Halifax to Toronto corporate transit")
    add("2023-07-26", "United Airlines", "UA 1144", "IAH", "ANC", "Boeing 737 MAX 9", "2E", "First", "Cook Inlet platform maintenance")
    add("2023-08-20", "Alaska Airlines", "AS 84", "ANC", "SEA", "Boeing 737 MAX 9", "1D", "First", "Anchorage to Seattle operations")
    add("2023-10-12", "Air Canada", "AC 614", "YYZ", "YHZ", "Airbus A220-300", "2A", "Business", "Nova Scotia offshore wind and subsea power review")
    add("2023-12-21", "Alaska Airlines", "AS 853", "ANC", "HNL", "Boeing 737 MAX 9", "2F", "First", "Reluctant holiday: Dave worked remotely 10 hours a day in Honolulu")
    add("2023-12-28", "Alaska Airlines", "AS 852", "HNL", "ANC", "Boeing 737 MAX 9", "2A", "First", "Escaping Hawaii back to winter in Alaska")

    # =========================================================================
    # 2024 (11 flights): Arctic energy transition & Singapore FPSO green retrofits
    # =========================================================================
    add("2024-02-20", "Alaska Airlines", "AS 80", "ANC", "SEA", "Boeing 737 MAX 9", "2A", "First", "Willow arctic foundation engineering")
    add("2024-02-20", "United Airlines", "UA 1520", "SEA", "IAH", "Boeing 737 MAX 9", "2C", "First", "Energy Corridor emissions abatement team")
    add("2024-04-16", "United Airlines", "UA 869", "SFO", "HKG", "Boeing 777-300ER", "2A", "Polaris Business", "Hong Kong marine decarbonization summit")
    add("2024-04-22", "Singapore Airlines", "SQ 861", "HKG", "SIN", "Boeing 777-300ER", "11A", "Business", "Keppel shipyard carbon capture module review")
    add("2024-04-26", "Singapore Airlines", "SQ 942", "SIN", "DPS", "Boeing 787-10", "12K", "Business", "Bali family trip: Dave discovered air-conditioned library in Ubud")
    add("2024-04-30", "Singapore Airlines", "SQ 943", "DPS", "SIN", "Boeing 787-10", "14A", "Business", "Leaving Bali with a sigh of relief")
    add("2024-05-01", "Singapore Airlines", "SQ 860", "SIN", "HKG", "Boeing 777-300ER", "11K", "Business", "Hong Kong connection")
    add("2024-05-03", "United Airlines", "UA 862", "HKG", "SFO", "Boeing 777-300ER", "1A", "Polaris Business", "Polaris transpacific flight home")
    add("2024-07-18", "United Airlines", "UA 1144", "IAH", "ANC", "Boeing 737 MAX 9", "2A", "First", "Cook Inlet summer rig inspection")
    add("2024-09-14", "Air Canada", "AC 614", "YYZ", "YHZ", "Airbus A220-300", "2A", "Business", "Halifax offshore renewable energy integration")
    add("2024-09-22", "Air Canada", "AC 623", "YHZ", "YYZ", "Boeing 787-9", "3A", "Business", "Halifax to Toronto Dreamliner service")

    # =========================================================================
    # 2025 (10 flights): 25-Year Road Warrior Career Milestone & Legacy Review
    # =========================================================================
    add("2025-01-21", "Alaska Airlines", "AS 82", "ANC", "SEA", "Boeing 737 MAX 9", "1A", "First", "25th year of North Slope travel milestone")
    add("2025-01-21", "United Airlines", "UA 1520", "SEA", "IAH", "Boeing 737 MAX 9", "2B", "First", "Houston executive retirement planning & mentoring")
    add("2025-03-18", "United Airlines", "UA 869", "SFO", "HKG", "Boeing 787-9", "1A", "Polaris Business", "Final overseas project sign-off in Hong Kong")
    add("2025-03-28", "United Airlines", "UA 862", "HKG", "SFO", "Boeing 787-9", "2A", "Polaris Business", "Celebratory transpacific crossing")
    add("2025-05-12", "Air Canada", "AC 614", "YYZ", "YHZ", "Airbus A220-300", "1A", "Business", "Halifax offshore maritime institute honorary lecture")
    add("2025-05-20", "Air Canada", "AC 615", "YHZ", "YYZ", "Airbus A220-300", "2F", "Business", "Farewell visit to Dartmouth engineering team")
    add("2025-07-22", "United Airlines", "UA 1144", "IAH", "ANC", "Boeing 737 MAX 9", "2A", "First", "Final Cook Inlet platform inspection")
    add("2025-08-15", "Alaska Airlines", "AS 84", "ANC", "SEA", "Boeing 737 MAX 9", "2C", "First", "Pacific Northwest transit")
    add("2025-10-08", "Air Canada", "AC 614", "YYZ", "YHZ", "Airbus A220-300", "2A", "Business", "Halifax harbor autumn visit")
    add("2025-10-16", "Air Canada", "AC 623", "YHZ", "YYZ", "Boeing 787-9", "2A", "Business", "Closing out 25 years of global road warrior flying!")

    return records


def get_dave_pierce_flighty_df() -> pd.DataFrame:
    """
    Returns the parsed, geocoded, subfleet-enriched Flighty DataFrame for Dave Pierce.
    Runs 100% in-memory without contacting BigQuery.
    """
    records = get_dave_pierce_raw_records()
    df_raw = pd.DataFrame(records)
    df_parsed = parse_flighty_csv(df_raw)
    # Add the Reason column back into the parsed DataFrame for rich table rendering
    if "Reason" in df_raw.columns and "Reason" not in df_parsed.columns:
        df_parsed["Reason"] = df_raw["Reason"].values
    return df_parsed
