"""
Diagnostic script for AvDB data audit and fleet query validation.
"""
from app.utils.bq_client import run_query

def audit_ord_od():
    print("--- 1. Auditing ORD O&D Connecting Markets ---")
    query = """
        SELECT 
            destination as dest,
            SUM(estimated_passengers) as raw_est_pax,
            AVG(avg_fare) as avg_fare
        FROM `db1b-1.DB1B_RAW.v_market_demand_itinerary`
        WHERE origin = 'ORD'
        GROUP BY 1
        ORDER BY raw_est_pax DESC
        LIMIT 20
    """
    df = run_query(query)
    print(df)

def audit_carrier_marketing_vs_operating():
    print("\n--- 2. Checking DB1B Marketing vs Operating Carrier ---")
    query = """
        SELECT column_name, data_type 
        FROM `db1b-1.DB1B_RAW.INFORMATION_SCHEMA.COLUMNS` 
        WHERE table_name = 'OD40_DB1B_RAW'
    """
    df = run_query(query)
    print(df[df["column_name"].str.contains("carrier|Carrier", case=False, na=False)])

def test_fleet_family_filter():
    print("\n--- 3. Testing Fleet Family Filter Query ---")
    from app.utils.queries import get_fleet_kpis, get_fleet_aircraft_breakdown
    res_kpi = get_fleet_kpis("Airbus A320 Family (A319/A320/A321)", 2023)
    print("KPIs for A320:", res_kpi)
    res_df = get_fleet_aircraft_breakdown("Airbus A320 Family (A319/A320/A321)", 2023)
    print("Breakdown for A320 rows:", len(res_df))

if __name__ == "__main__":
    audit_ord_od()
    audit_carrier_marketing_vs_operating()
    test_fleet_family_filter()
