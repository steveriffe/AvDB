-- Mart 1: Airport Network & Route Summary
-- Destination: reporting.mart_airport_network_summary
-- Partition: flight_date (MONTH)
-- Cluster: origin, dest, unique_carrier

CREATE OR REPLACE TABLE `db1b-1.reporting.mart_airport_network_summary`
PARTITION BY flight_date
CLUSTER BY origin, dest, unique_carrier
AS
WITH t100_monthly AS (
    SELECT 
        DATE(year, month, 1) AS flight_date,
        year,
        month,
        origin,
        dest,
        unique_carrier,
        carrier_name,
        SUM(departures_performed) AS departures_performed,
        SUM(seats) AS total_seats,
        SUM(passengers) AS operational_passengers,
        AVG(distance) AS distance_miles
    FROM `db1b-1.bts_t100_data.t100_segments`
    WHERE year >= 2018
    GROUP BY 1, 2, 3, 4, 5, 6, 7
),
db1b_monthly AS (
    SELECT 
        year,
        month,
        origin,
        destination AS dest,
        carrier AS unique_carrier,
        SUM(estimated_passengers) AS estimated_od_passengers,
        AVG(avg_fare) AS avg_od_fare
    FROM `db1b-1.DB1B_RAW.v_market_demand_itinerary`
    GROUP BY 1, 2, 3, 4, 5
)
SELECT 
    t.flight_date,
    t.year,
    t.month,
    t.origin,
    COALESCE(o_apt.airport_name, t.origin) AS origin_name,
    COALESCE(o_apt.city, '') AS origin_city,
    COALESCE(o_apt.state_region, '') AS origin_state,
    COALESCE(o_apt.country, 'US') AS origin_country,
    o_apt.latitude AS origin_lat,
    o_apt.longitude AS origin_lon,
    o_apt.is_metro_code AS origin_is_metro,
    t.dest,
    COALESCE(d_apt.airport_name, t.dest) AS dest_name,
    COALESCE(d_apt.city, '') AS dest_city,
    COALESCE(d_apt.state_region, '') AS dest_state,
    COALESCE(d_apt.country, 'US') AS dest_country,
    d_apt.latitude AS dest_lat,
    d_apt.longitude AS dest_lon,
    d_apt.is_metro_code AS dest_is_metro,
    t.unique_carrier,
    t.carrier_name,
    t.departures_performed,
    t.total_seats,
    t.operational_passengers,
    ROUND(SAFE_DIVIDE(t.operational_passengers, t.total_seats) * 100, 1) AS load_factor_pct,
    ROUND(SAFE_DIVIDE(t.total_seats, NULLIF(t.departures_performed, 0)), 1) AS seats_per_departure,
    t.distance_miles,
    ROUND(d.estimated_od_passengers, 0) AS estimated_od_passengers,
    ROUND(d.avg_od_fare, 2) AS avg_od_fare
FROM t100_monthly t
LEFT JOIN db1b_monthly d
    ON t.year = d.year 
   AND t.month = d.month 
   AND t.origin = d.origin 
   AND t.dest = d.dest 
   AND t.unique_carrier = d.unique_carrier
LEFT JOIN `db1b-1.reporting.ref_airports` o_apt 
    ON t.origin = o_apt.airport_code
LEFT JOIN `db1b-1.reporting.ref_airports` d_apt 
    ON t.dest = d_apt.airport_code;
