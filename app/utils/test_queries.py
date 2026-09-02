"""
Test script for validating BigQuery query functions.
"""
import app.utils.queries as q

def test_all():
    print("Testing get_airport_routes_dataset...")
    df_routes = q.get_airport_routes_dataset("ORD", 2023, True, 10)
    print(f"✅ get_airport_routes_dataset successful! Rows: {len(df_routes)}")
    print(df_routes[["dest", "dest_city", "departures_performed", "operational_passengers"]].head())

    print("\nTesting get_airport_carrier_breakdown...")
    df_carriers = q.get_airport_carrier_breakdown("ORD", 2023, True, 10)
    print(f"✅ get_airport_carrier_breakdown successful! Rows: {len(df_carriers)}")

    print("\nTesting get_airport_fleet_mix...")
    df_fleet = q.get_airport_fleet_mix("ORD", 2023, True, 10)
    print(f"✅ get_airport_fleet_mix successful! Rows: {len(df_fleet)}")

if __name__ == "__main__":
    test_all()
