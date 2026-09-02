"""
Test script for validating BigQuery query functions.
"""
import app.utils.queries as q

def test_all():
    print("Testing get_airport_routes_dataset...")
    df_routes = q.get_airport_routes_dataset("ORD", 2023, True, 10)
    print(f"✅ get_airport_routes_dataset successful! Rows: {len(df_routes)}")

    print("\nTesting get_fleet_kpis...")
    kpis = q.get_fleet_kpis("All Mainline & Regional", 2023)
    print(f"✅ get_fleet_kpis successful! Result: {kpis}")

    print("\nTesting get_airline_hub_expansion_proposals for AS...")
    proposals = q.get_airline_hub_expansion_proposals("AS", 2023)
    print(f"✅ get_airline_hub_expansion_proposals successful! Hubs found: {list(proposals.keys())}")

if __name__ == "__main__":
    test_all()
