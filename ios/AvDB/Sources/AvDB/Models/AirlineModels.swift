import Foundation
import CoreLocation

/// Performance KPIs for an airline network
public struct AirlineKPIs: Codable, Hashable, Sendable {
    public let carrierCode: String
    public let year: Int
    public let activeRoutes: Int
    public let totalDepartures: Int
    public let totalSeats: Int
    public let totalPassengers: Int
    public let totalAsm: Int
    public let totalRpm: Int
    public let systemLoadFactor: Double
    public let avgNetworkFare: Double
    public let avgYieldPerMile: Double

    public enum CodingKeys: String, CodingKey {
        case carrierCode = "carrier_code"
        case year
        case activeRoutes = "active_routes"
        case totalDepartures = "total_departures"
        case totalSeats = "total_seats"
        case totalPassengers = "total_passengers"
        case totalAsm = "total_asm"
        case totalRpm = "total_rpm"
        case systemLoadFactor = "system_load_factor"
        case avgNetworkFare = "avg_network_fare"
        case avgYieldPerMile = "avg_yield_per_mile"
    }

    public static var empty: AirlineKPIs {
        AirlineKPIs(
            carrierCode: "—",
            year: 2023,
            activeRoutes: 0,
            totalDepartures: 0,
            totalSeats: 0,
            totalPassengers: 0,
            totalAsm: 0,
            totalRpm: 0,
            systemLoadFactor: 0.0,
            avgNetworkFare: 0.0,
            avgYieldPerMile: 0.0
        )
    }
}

/// Airline Hub operation summary
public struct AirlineHub: Identifiable, Codable, Hashable, Sendable {
    public var id: String { airportCode }
    public let airportCode: String
    public let originName: String?
    public let originCity: String?
    public let departuresPerformed: Int
    public let totalSeats: Int
    public let totalPassengers: Int
    public let directDestinations: Int

    public enum CodingKeys: String, CodingKey {
        case airportCode = "airport_code"
        case originName = "origin_name"
        case originCity = "origin_city"
        case departuresPerformed = "departures_performed"
        case totalSeats = "total_seats"
        case totalPassengers = "total_passengers"
        case directDestinations = "direct_destinations"
    }
}

/// Stage-length vs Yield curve point
public struct YieldCurvePoint: Identifiable, Codable, Hashable, Sendable {
    public var id: String { routeLabel }
    public let origin: String
    public let dest: String
    public let routeLabel: String
    public let stageLengthMiles: Double
    public let avgOdFare: Double
    public let yieldPerMile: Double
    public let operationalPassengers: Int
    public let loadFactorPct: Double

    public enum CodingKeys: String, CodingKey {
        case origin
        case dest
        case routeLabel = "route_label"
        case stageLengthMiles = "stage_length_miles"
        case avgOdFare = "avg_od_fare"
        case yieldPerMile = "yield_per_mile"
        case operationalPassengers = "operational_passengers"
        case loadFactorPct = "load_factor_pct"
    }
}

/// Full nationwide network response
public struct AirlineNetworkResponse: Codable, Hashable, Sendable {
    public let carrierCode: String
    public let carrierName: String
    public let year: Int
    public let hubs: [AirlineHub]
    public let routes: [RouteItem]

    public enum CodingKeys: String, CodingKey {
        case carrierCode = "carrier_code"
        case carrierName = "carrier_name"
        case year
        case hubs
        case routes
    }
}

public struct AirlineCarrier: Identifiable, Hashable, Sendable {
    public var id: String { code }
    public let code: String
    public let name: String
    public let signatureColorHex: String

    public static let majorCarriers: [AirlineCarrier] = [
        AirlineCarrier(code: "AS", name: "Alaska Airlines", signatureColorHex: "#01426A"),
        AirlineCarrier(code: "UA", name: "United Airlines", signatureColorHex: "#005DAA"),
        AirlineCarrier(code: "DL", name: "Delta Air Lines", signatureColorHex: "#E01933"),
        AirlineCarrier(code: "AA", name: "American Airlines", signatureColorHex: "#0078D2"),
        AirlineCarrier(code: "WN", name: "Southwest Airlines", signatureColorHex: "#F9B612"),
        AirlineCarrier(code: "B6", name: "JetBlue Airways", signatureColorHex: "#00205B"),
        AirlineCarrier(code: "NK", name: "Spirit Airlines", signatureColorHex: "#FFE700"),
        AirlineCarrier(code: "F9", name: "Frontier Airlines", signatureColorHex: "#006643"),
        AirlineCarrier(code: "G4", name: "Allegiant Air", signatureColorHex: "#005596")
    ]
}
