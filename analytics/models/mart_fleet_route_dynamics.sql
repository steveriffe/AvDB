-- Mart 3: Fleet Deployment & Aircraft Routing Economics
-- Destination: reporting.mart_fleet_route_dynamics
-- Partition: flight_date (MONTH)
-- Cluster: aircraft_family, unique_carrier, origin

CREATE OR REPLACE TABLE `db1b-1.reporting.mart_fleet_route_dynamics`
PARTITION BY flight_date
CLUSTER BY aircraft_family, unique_carrier, origin
AS
WITH segment_fleet AS (
    SELECT 
        DATE(s.year, s.month, 1) AS flight_date,
        s.year,
        s.month,
        s.origin,
        s.dest,
        s.unique_carrier,
        s.carrier_name,
        SAFE_CAST(s.aircraft_type AS INT64) AS aircraft_type_code,
        ac.Description AS aircraft_description,
        CASE
            WHEN ac.Description LIKE '%777%' OR ac.Description LIKE '%787%' OR ac.Description LIKE '%A350%' OR ac.Description LIKE '%A330%' OR ac.Description LIKE '%767%' OR ac.Description LIKE '%A380%' THEN 'Widebody'
            WHEN ac.Description LIKE '%737%' OR ac.Description LIKE '%A320%' OR ac.Description LIKE '%A321%' OR ac.Description LIKE '%A319%' OR ac.Description LIKE '%757%' OR ac.Description LIKE '%A220%' THEN 'Mainline Narrowbody'
            WHEN ac.Description LIKE '%CRJ%' OR ac.Description LIKE '%ERJ%' OR ac.Description LIKE '%E170%' OR ac.Description LIKE '%E175%' OR ac.Description LIKE '%E190%' OR ac.Description LIKE '%Embraer%' THEN 'Regional Jet'
            WHEN ac.Description LIKE '%Dash%' OR ac.Description LIKE '%ATR%' OR ac.Description LIKE '%Saab%' OR ac.Description LIKE '%Caravan%' OR ac.Description LIKE '%Beech%' THEN 'Turboprop / Regional Prop'
            ELSE 'Other / Uncategorized'
        END AS aircraft_family,
        SUM(s.departures_performed) AS departures_performed,
        SUM(s.seats) AS total_seats,
        SUM(s.passengers) AS operational_passengers,
        AVG(s.distance) AS distance_miles
    FROM `db1b-1.bts_t100_data.t100_segments` s
    LEFT JOIN `db1b-1.t100_data.L_AIRCRAFT_TYPE` ac
        ON SAFE_CAST(s.aircraft_type AS INT64) = ac.Code
    WHERE s.year >= 1990
    GROUP BY 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
),
db1b_fares AS (
    SELECT 
        year,
        month,
        origin,
        destination AS dest,
        carrier AS unique_carrier,
        AVG(avg_fare) AS avg_fare
    FROM `db1b-1.DB1B_RAW.v_market_demand_itinerary`
    GROUP BY 1, 2, 3, 4, 5
)
SELECT 
    f.flight_date,
    f.year,
    f.month,
    f.unique_carrier,
    f.carrier_name,
    f.origin,
    COALESCE(o_apt.airport_name, f.origin) AS origin_name,
    COALESCE(o_apt.city, '') AS origin_city,
    f.dest,
    COALESCE(d_apt.airport_name, f.dest) AS dest_name,
    COALESCE(d_apt.city, '') AS dest_city,
    f.aircraft_type_code,
    COALESCE(f.aircraft_description, 'Unknown Equipment') AS aircraft_description,
    f.aircraft_family,
    f.departures_performed,
    f.total_seats,
    f.operational_passengers,
    ROUND(SAFE_DIVIDE(f.operational_passengers, f.total_seats) * 100, 1) AS load_factor_pct,
    ROUND(SAFE_DIVIDE(f.total_seats, NULLIF(f.departures_performed, 0)), 1) AS avg_gauge_seats,
    f.distance_miles,
    ROUND(d.avg_fare, 2) AS avg_od_fare,
    ROUND(SAFE_DIVIDE(d.avg_fare, NULLIF(f.distance_miles, 0)), 4) AS yield_per_mile
FROM segment_fleet f
LEFT JOIN db1b_fares d
    ON f.year = d.year 
   AND f.month = d.month 
   AND f.origin = d.origin 
   AND f.dest = d.dest 
   AND f.unique_carrier = d.unique_carrier
LEFT JOIN `db1b-1.reporting.ref_airports` o_apt 
    ON f.origin = o_apt.airport_code
LEFT JOIN `db1b-1.reporting.ref_airports` d_apt 
    ON f.dest = d_apt.airport_code;
