import Foundation

/// Top-level utilization and economics for an aircraft family
public struct FleetKPIs: Codable, Hashable, Sendable {
    public let familyFilter: String
    public let year: Int
    public let uniqueModels: Int
    public let operatingCarriers: Int
    public let totalDepartures: Int
    public let totalSeats: Int
    public let totalPassengers: Int
    public let avgGaugeSeats: Double
    public let fleetLoadFactor: Double
    public let avgStageLength: Int
    public let avgSegmentFare: Double
    public let yieldPerMile: Double

    public enum CodingKeys: String, CodingKey {
        case familyFilter = "family_filter"
        case year
        case uniqueModels = "unique_models"
        case operatingCarriers = "operating_carriers"
        case totalDepartures = "total_departures"
        case totalSeats = "total_seats"
        case totalPassengers = "total_passengers"
        case avgGaugeSeats = "avg_gauge_seats"
        case fleetLoadFactor = "fleet_load_factor"
        case avgStageLength = "avg_stage_length"
        case avgSegmentFare = "avg_segment_fare"
        case yieldPerMile = "yield_per_mile"
    }

    public static var empty: FleetKPIs {
        FleetKPIs(
            familyFilter: "All",
            year: 2023,
            uniqueModels: 0,
            operatingCarriers: 0,
            totalDepartures: 0,
            totalSeats: 0,
            totalPassengers: 0,
            avgGaugeSeats: 0.0,
            fleetLoadFactor: 0.0,
            avgStageLength: 0,
            avgSegmentFare: 0.0,
            yieldPerMile: 0.0
        )
    }
}

/// Subfleet model detail (e.g. 737-900ER vs 737-800, A321neo vs A320-200)
public struct SubfleetItem: Identifiable, Codable, Hashable, Sendable {
    public var id: String { "\(aircraftFamily)-\(aircraftDescription)" }
    public let aircraftFamily: String
    public let aircraftDescription: String
    public let departuresPerformed: Int
    public let totalSeats: Int
    public let operationalPassengers: Int
    public let avgGaugeSeats: Double
    public let loadFactorPct: Double
    public let avgStageLength: Int
    public let avgSegmentFare: Double
    public let yieldPerMile: Double

    public enum CodingKeys: String, CodingKey {
        case aircraftFamily = "aircraft_family"
        case aircraftDescription = "aircraft_description"
        case departuresPerformed = "departures_performed"
        case totalSeats = "total_seats"
        case operationalPassengers = "operational_passengers"
        case avgGaugeSeats = "avg_gauge_seats"
        case loadFactorPct = "load_factor_pct"
        case avgStageLength = "avg_stage_length"
        case avgSegmentFare = "avg_segment_fare"
        case yieldPerMile = "yield_per_mile"
    }
}

/// Full fleet summary response
public struct FleetSummaryResponse: Codable, Hashable, Sendable {
    public let familyFilter: String
    public let year: Int
    public let kpis: FleetKPIs
    public let subfleets: [SubfleetItem]

    public enum CodingKeys: String, CodingKey {
        case familyFilter = "family_filter"
        case year
        case kpis
        case subfleets
    }
}
