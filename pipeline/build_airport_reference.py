"""
Airport Reference Data Pipeline
Fetches, harmonizes, and validates:
1. Master Physical Airports (OurAirports + BTS DOT TransStats Master Coordinates)
2. City Market / Metropolitan Areas (Multi-Airport Catchments like WAS, NYC, CHI, LON)
3. Historical Airport Aliases & Code Migrations (e.g. TXL->BER, PFN->ECP, SXF->BER)
"""

import urllib.request
import csv
import io
import pandas as pd
from typing import Dict, List, Tuple
import os
import subprocess
from google.cloud import bigquery
from app.config import settings


# 1. Multi-Airport City Market Definitions (Catchment Areas)
CITY_MARKETS = [
    {
        "market_code": "WAS",
        "market_name": "Washington, DC Area",
        "city": "Washington",
        "state": "DC",
        "country": "US",
        "metro_lat": 38.8951,
        "metro_lon": -77.0364,
        "primary_airports": ["DCA", "IAD", "BWI"],
        "description": "Metropolitan area including Reagan National (DCA), Dulles (IAD), and Baltimore/Washington (BWI)"
    },
    {
        "market_code": "NYC",
        "market_name": "New York City Area",
        "city": "New York",
        "state": "NY",
        "country": "US",
        "metro_lat": 40.7128,
        "metro_lon": -74.0060,
        "primary_airports": ["JFK", "LGA", "EWR", "HPN", "ISP", "SWF"],
        "description": "New York Tri-State Area including JFK, LaGuardia, Newark, Westchester, Long Island, and Stewart"
    },
    {
        "market_code": "CHI",
        "market_name": "Chicago Area",
        "city": "Chicago",
        "state": "IL",
        "country": "US",
        "metro_lat": 41.8781,
        "metro_lon": -87.6298,
        "primary_airports": ["ORD", "MDW", "RFD"],
        "description": "Chicago Metropolitan Area including O'Hare (ORD), Midway (MDW), and Rockford (RFD)"
    },
    {
        "market_code": "DFW_METRO",
        "market_name": "Dallas/Fort Worth Metroplex",
        "city": "Dallas",
        "state": "TX",
        "country": "US",
        "metro_lat": 32.7767,
        "metro_lon": -96.7970,
        "primary_airports": ["DFW", "DAL"],
        "description": "Dallas/Fort Worth Metroplex including DFW International and Dallas Love Field (DAL)"
    },
    {
        "market_code": "HOU_METRO",
        "market_name": "Houston Area",
        "city": "Houston",
        "state": "TX",
        "country": "US",
        "metro_lat": 29.7604,
        "metro_lon": -95.3698,
        "primary_airports": ["IAH", "HOU"],
        "description": "Houston Area including George Bush Intercontinental (IAH) and William P. Hobby (HOU)"
    },
    {
        "market_code": "MIA_METRO",
        "market_name": "South Florida Metro Area",
        "city": "Miami",
        "state": "FL",
        "country": "US",
        "metro_lat": 25.7617,
        "metro_lon": -80.1918,
        "primary_airports": ["MIA", "FLL", "PBI"],
        "description": "South Florida Area including Miami (MIA), Fort Lauderdale (FLL), and West Palm Beach (PBI)"
    },
    {
        "market_code": "BAY_AREA",
        "market_name": "San Francisco Bay Area",
        "city": "San Francisco",
        "state": "CA",
        "country": "US",
        "metro_lat": 37.7749,
        "metro_lon": -122.4194,
        "primary_airports": ["SFO", "OAK", "SJC", "STS"],
        "description": "San Francisco Bay Area including SFO, Oakland (OAK), San Jose (SJC), and Santa Rosa (STS)"
    },
    {
        "market_code": "LAX_METRO",
        "market_name": "Los Angeles Basin",
        "city": "Los Angeles",
        "state": "CA",
        "country": "US",
        "metro_lat": 34.0522,
        "metro_lon": -118.2437,
        "primary_airports": ["LAX", "BUR", "LGB", "SNA", "ONT"],
        "description": "Los Angeles Greater Basin including LAX, Burbank (BUR), Long Beach (LGB), John Wayne (SNA), and Ontario (ONT)"
    },
    {
        "market_code": "LON",
        "market_name": "London Metropolitan Area",
        "city": "London",
        "state": "ENG",
        "country": "GB",
        "metro_lat": 51.5074,
        "metro_lon": -0.1278,
        "primary_airports": ["LHR", "LGW", "STN", "LCY", "LTN", "SEN"],
        "description": "London Airport System including Heathrow, Gatwick, Stansted, City, Luton, and Southend"
    },
    {
        "market_code": "TYO",
        "market_name": "Tokyo Metropolitan Area",
        "city": "Tokyo",
        "state": "13",
        "country": "JP",
        "metro_lat": 35.6762,
        "metro_lon": 139.6503,
        "primary_airports": ["HND", "NRT"],
        "description": "Tokyo Metropolitan System including Haneda (HND) and Narita (NRT)"
    }
]

# 2. Historical Airport Code Changes & Relocations
HISTORICAL_ALIASES = [
    {
        "historical_code": "TXL",
        "airport_name": "Berlin Tegel Airport",
        "city": "Berlin",
        "country": "DE",
        "status": "Closed",
        "replacement_code": "BER",
        "effective_year": 2020,
        "notes": "Closed in Nov 2020; all operations consolidated to Berlin Brandenburg (BER)"
    },
    {
        "historical_code": "SXF",
        "airport_name": "Berlin Schönefeld Airport",
        "city": "Berlin",
        "country": "DE",
        "status": "Renamed/Integrated",
        "replacement_code": "BER",
        "effective_year": 2020,
        "notes": "Integrated into Berlin Brandenburg (BER) as Terminal 5"
    },
    {
        "historical_code": "PFN",
        "airport_name": "Panama City-Bay County Airport",
        "city": "Panama City",
        "country": "US",
        "status": "Closed",
        "replacement_code": "ECP",
        "effective_year": 2010,
        "notes": "Closed in 2010; replaced by Northwest Florida Beaches International Airport (ECP)"
    },
    {
        "historical_code": "HKG_OLD",
        "airport_name": "Kai Tak Airport",
        "city": "Hong Kong",
        "country": "HK",
        "status": "Closed",
        "replacement_code": "HKG",
        "effective_year": 1998,
        "notes": "Closed in July 1998; replaced by Chek Lap Kok International (HKG)"
    },
    {
        "historical_code": "ISL",
        "airport_name": "Istanbul Atatürk Airport",
        "city": "Istanbul",
        "country": "TR",
        "status": "Cargo/VIP Only",
        "replacement_code": "IST",
        "effective_year": 2019,
        "notes": "Commercial passenger operations transferred to new Istanbul Airport (IST) in April 2019"
    },
    {
        "historical_code": "FYV",
        "airport_name": "Drake Field",
        "city": "Fayetteville",
        "country": "US",
        "status": "General Aviation Only",
        "replacement_code": "XNA",
        "effective_year": 1998,
        "notes": "Commercial passenger service shifted to Northwest Arkansas National Airport (XNA) in 1998"
    }
]


def download_ourairports() -> pd.DataFrame:
    """Download and parse latest OurAirports global database."""
    url = "https://davidmegginson.github.io/ourairports-data/airports.csv"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (AvDB Pipeline)"})
    with urllib.request.urlopen(req) as resp:
        content = resp.read()
    df = pd.read_csv(io.BytesIO(content), low_memory=False)
    return df


def build_master_airport_table(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and standardizes airports for commercial and general aviation.
    Extracts IATA primary key with ICAO and Local Code fallbacks.
    """
    # Clean string columns
    for col in ["iata_code", "ident", "local_code", "name", "municipality", "iso_country", "iso_region"]:
        if col in df_raw.columns:
            df_raw[col] = df_raw[col].fillna("").astype(str).str.strip()

    # Filter to non-empty coordinates
    df_valid = df_raw.dropna(subset=["latitude_deg", "longitude_deg"]).copy()
    
    # Priority for code mapping: iata_code -> ident (if 3-4 chars) -> local_code
    rows = []
    seen_codes = set()

    # Pass 1: Commercial airports with explicit IATA codes
    iata_subset = df_valid[df_valid["iata_code"].str.len() == 3]
    for _, r in iata_subset.iterrows():
        code = r["iata_code"].upper()
        if code and code not in seen_codes:
            seen_codes.add(code)
            rows.append({
                "airport_code": code,
                "iata_code": code,
                "icao_code": r["ident"].upper() if len(r["ident"]) == 4 else "",
                "airport_name": r["name"],
                "airport_type": r["type"],
                "city": r["municipality"],
                "state_region": r["iso_region"].replace("US-", "") if r["iso_region"].startswith("US-") else r["iso_region"],
                "country": r["iso_country"],
                "latitude": float(r["latitude_deg"]),
                "longitude": float(r["longitude_deg"]),
                "elevation_ft": float(r["elevation_ft"]) if pd.notnull(r["elevation_ft"]) and r["elevation_ft"] != "" else None,
                "is_commercial": r["type"] in ["large_airport", "medium_airport"],
                "is_metro_code": False
            })

    # Pass 2: Secondary US & regional airfields by local_code / ident
    non_iata_subset = df_valid[~df_valid["ident"].isin(seen_codes)]
    for _, r in non_iata_subset.iterrows():
        local = r["local_code"].upper() if len(r["local_code"]) in [3, 4] else r["ident"].upper()
        if local and local not in seen_codes and len(local) in [3, 4]:
            seen_codes.add(local)
            rows.append({
                "airport_code": local,
                "iata_code": r["iata_code"].upper() if len(r["iata_code"]) == 3 else "",
                "icao_code": r["ident"].upper() if len(r["ident"]) == 4 else "",
                "airport_name": r["name"],
                "airport_type": r["type"],
                "city": r["municipality"],
                "state_region": r["iso_region"].replace("US-", "") if r["iso_region"].startswith("US-") else r["iso_region"],
                "country": r["iso_country"],
                "latitude": float(r["latitude_deg"]),
                "longitude": float(r["longitude_deg"]),
                "elevation_ft": float(r["elevation_ft"]) if pd.notnull(r["elevation_ft"]) and r["elevation_ft"] != "" else None,
                "is_commercial": r["type"] in ["large_airport", "medium_airport"],
                "is_metro_code": False
            })

    # Pass 3: Add City Market Metro Codes (WAS, NYC, CHI, LON, TYO, etc.)
    for m in CITY_MARKETS:
        code = m["market_code"]
        if code not in seen_codes:
            seen_codes.add(code)
            rows.append({
                "airport_code": code,
                "iata_code": code if len(code) == 3 else "",
                "icao_code": "",
                "airport_name": m["market_name"],
                "airport_type": "city_market_metro",
                "city": m["city"],
                "state_region": m["state"],
                "country": m["country"],
                "latitude": m["metro_lat"],
                "longitude": m["metro_lon"],
                "elevation_ft": None,
                "is_commercial": True,
                "is_metro_code": True
            })

    return pd.DataFrame(rows)


def upload_reference_tables(client: bigquery.Client, dataset_id: str = "reporting"):
    """Builds and loads all reference tables to BigQuery."""
    print("1. Downloading OurAirports global database...")
    df_raw = download_ourairports()
    print(f"Downloaded {len(df_raw)} raw airport entries.")

    print("2. Harmonizing master airport reference table...")
    df_master = build_master_airport_table(df_raw)
    print(f"Generated {len(df_master)} master airports & metro codes.")
    df_master.to_parquet("data/ref_airports.parquet", index=False)

    print("3. Building City Market Catchments table...")
    market_rows = []
    for m in CITY_MARKETS:
        for apt in m["primary_airports"]:
            market_rows.append({
                "market_code": m["market_code"],
                "market_name": m["market_name"],
                "airport_code": apt,
                "metro_city": m["city"],
                "metro_state": m["state"],
                "country": m["country"],
                "description": m["description"]
            })
    df_city_markets = pd.DataFrame(market_rows)
    df_city_markets.to_parquet("data/ref_city_markets.parquet", index=False)

    print("4. Building Historical Airport Aliases table...")
    df_history = pd.DataFrame(HISTORICAL_ALIASES)
    df_history.to_parquet("data/ref_airport_code_history.parquet", index=False)

    # Load via bq load CLI with Parquet format
    tables = [
        ("ref_airports", "data/ref_airports.parquet", "Master Airport Coordinates and Classification"),
        ("ref_city_markets", "data/ref_city_markets.parquet", "Multi-Airport Metropolitan Catchment Mapping"),
        ("ref_airport_code_history", "data/ref_airport_code_history.parquet", "Historical Airport Renaming and Relocation Mapping")
    ]

    project_id = client.project or settings.gcp_project_id or "db1b-1"
    for table_name, parquet_path, desc in tables:
        target_id = f"{project_id}:{dataset_id}.{table_name}"
        print(f"Loading {parquet_path} into `{target_id}`...")
        # Drop existing to ensure fresh schema
        subprocess.run(["bq", "rm", "-f", "-t", target_id], capture_output=True)
        cmd = [
            "bq", "load",
            "--source_format=PARQUET",
            target_id,
            parquet_path
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"✅ Loaded into `{target_id}` ({desc}).")
        else:
            print(f"❌ Error loading `{target_id}`: {res.stderr}")


if __name__ == "__main__":
    bq_client = bigquery.Client(project=settings.gcp_project_id or "db1b-1")
    upload_reference_tables(bq_client, dataset_id="reporting")
