-- Mart 2: Airline Network & Yield Performance
-- Destination: reporting.mart_airline_network_performance
-- Partition: flight_date (MONTH)
-- Cluster: unique_carrier, origin, dest

CREATE OR REPLACE TABLE `db1b-1.reporting.mart_airline_network_performance`
PARTITION BY flight_date
CLUSTER BY unique_carrier, origin, dest
AS
WITH base_segments AS (
    SELECT 
        DATE(year, month, 1) AS flight_date,
        year,
        month,
        unique_carrier,
        carrier_name,
        origin,
        dest,
        SUM(departures_performed) AS departures_performed,
        SUM(seats) AS total_seats,
        SUM(passengers) AS operational_passengers,
        AVG(distance) AS distance_miles,
        SUM(seats * distance) AS available_seat_miles,
        SUM(passengers * distance) AS revenue_passenger_miles
    FROM `db1b-1.bts_t100_data.t100_segments`
    WHERE year >= 1990
    GROUP BY 1, 2, 3, 4, 5, 6, 7
),
route_totals AS (
    SELECT 
        year,
        month,
        origin,
        dest,
        SUM(operational_passengers) AS route_total_passengers,
        SUM(total_seats) AS route_total_seats
    FROM base_segments
    GROUP BY 1, 2, 3, 4
),
db1b_yields AS (
    SELECT 
        year,
        month,
        carrier AS unique_carrier,
        origin,
        destination AS dest,
        SUM(estimated_passengers) AS estimated_od_pax,
        AVG(avg_fare) AS avg_fare
    FROM `db1b-1.DB1B_RAW.v_market_demand_itinerary`
    GROUP BY 1, 2, 3, 4, 5
)
SELECT 
    b.flight_date,
    b.year,
    b.month,
    b.unique_carrier,
    b.carrier_name,
    b.origin,
    COALESCE(o_apt.airport_name, b.origin) AS origin_name,
    COALESCE(o_apt.city, '') AS origin_city,
    b.dest,
    COALESCE(d_apt.airport_name, b.dest) AS dest_name,
    COALESCE(d_apt.city, '') AS dest_city,
    b.departures_performed,
    b.total_seats,
    b.operational_passengers,
    b.available_seat_miles,
    b.revenue_passenger_miles,
    ROUND(SAFE_DIVIDE(b.revenue_passenger_miles, b.available_seat_miles) * 100, 1) AS load_factor_pct,
    ROUND(SAFE_DIVIDE(b.operational_passengers, r.route_total_passengers) * 100, 1) AS passenger_market_share_pct,
    ROUND(SAFE_DIVIDE(b.total_seats, r.route_total_seats) * 100, 1) AS seat_capacity_share_pct,
    ROUND(SAFE_DIVIDE(b.available_seat_miles, b.total_seats), 1) AS avg_stage_length_miles,
    ROUND(d.avg_fare, 2) AS avg_od_fare,
    ROUND(SAFE_DIVIDE(d.avg_fare, NULLIF(b.distance_miles, 0)), 4) AS yield_per_mile
FROM base_segments b
LEFT JOIN route_totals r
    ON b.year = r.year 
   AND b.month = r.month 
   AND b.origin = r.origin 
   AND b.dest = r.dest
LEFT JOIN db1b_yields d
    ON b.year = d.year 
   AND b.month = d.month 
   AND b.unique_carrier = d.unique_carrier 
   AND b.origin = d.origin 
   AND b.dest = d.dest
LEFT JOIN `db1b-1.reporting.ref_airports` o_apt 
    ON b.origin = o_apt.airport_code
LEFT JOIN `db1b-1.reporting.ref_airports` d_apt 
    ON b.dest = d_apt.airport_code;
