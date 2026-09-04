import Foundation
import CoreLocation

/// Represents a commercial or metropolitan airport entity
public struct Airport: Identifiable, Codable, Hashable, Sendable {
    public var id: String { airportCode }
    public let airportCode: String
    public let airportName: String
    public let city: String
    public let state: String
    public let country: String
    public let isCommercial: Bool
    public let isMetroCode: Bool
    public let latitude: Double?
    public let longitude: Double?

    public enum CodingKeys: String, CodingKey {
        case airportCode = "airport_code"
        case airportName = "airport_name"
        case city
        case state
        case country
        case isCommercial = "is_commercial"
        case isMetroCode = "is_metro_code"
        case latitude
        case longitude
    }

    public var coordinate: CLLocationCoordinate2D? {
        guard let lat = latitude, let lon = longitude else { return nil }
        return CLLocationCoordinate2D(latitude: lat, longitude: lon)
    }

    public var displayName: String {
        "\(airportCode) - \(city)"
    }
}

/// Metropolitan catchment market data (e.g. WAS, NYC, CHI)
public struct CatchmentInfo: Codable, Hashable, Sendable {
    public let marketCode: String
    public let marketName: String
    public let metroCity: String
    public let memberAirports: [String]
    public let description: String?

    public enum CodingKeys: String, CodingKey {
        case marketCode = "market_code"
        case marketName = "market_name"
        case metroCity = "metro_city"
        case memberAirports = "member_airports"
        case description
    }
}

/// Top-level KPI metrics for an airport
public struct AirportKPIs: Codable, Hashable, Sendable {
    public let airportCode: String
    public let year: int32_or_int
    public let directDestinations: Int
    public let totalDepartures: Int
    public let totalSeats: Int
    public let totalPassengers: Int
    public let loadFactorPct: Double
    public let avgOdFare: Double?
    public let leadingCarrier: String

    public typealias int32_or_int = Int

    public enum CodingKeys: String, CodingKey {
        case airportCode = "airport_code"
        case year
        case directDestinations = "direct_destinations"
        case totalDepartures = "total_departures"
        case totalSeats = "total_seats"
        case totalPassengers = "total_passengers"
        case loadFactorPct = "load_factor_pct"
        case avgOdFare = "avg_od_fare"
        case leadingCarrier = "leading_carrier"
    }

    public static var empty: AirportKPIs {
        AirportKPIs(
            airportCode: "—",
            year: 2023,
            directDestinations: 0,
            totalDepartures: 0,
            totalSeats: 0,
            totalPassengers: 0,
            loadFactorPct: 0.0,
            avgOdFare: nil,
            leadingCarrier: "—"
        )
    }
}

/// Represents an individual outbound route segment
public struct RouteItem: Identifiable, Codable, Hashable, Sendable {
    public var id: String { "\(origin)-\(dest)" }
    public let origin: String
    public let originName: String?
    public let originCity: String?
    public let originLat: Double
    public let originLon: Double
    public let dest: String
    public let destName: String?
    public let destCity: String?
    public let destState: String?
    public let destCountry: String?
    public let destLat: Double
    public let destLon: Double
    public let departuresPerformed: Int
    public let totalSeats: Int
    public let operationalPassengers: Int
    public let loadFactorPct: Double
    public let avgGaugeSeats: Double
    public let distanceMiles: Double
    public let avgOdFare: Double?
    public let operatingCarriers: String?

    public enum CodingKeys: String, CodingKey {
        case origin
        case originName = "origin_name"
        case originCity = "origin_city"
        case originLat = "origin_lat"
        case originLon = "origin_lon"
        case dest
        case destName = "dest_name"
        case destCity = "dest_city"
        case destState = "dest_state"
        case destCountry = "dest_country"
        case destLat = "dest_lat"
        case destLon = "dest_lon"
        case departuresPerformed = "departures_performed"
        case totalSeats = "total_seats"
        case operationalPassengers = "operational_passengers"
        case loadFactorPct = "load_factor_pct"
        case avgGaugeSeats = "avg_gauge_seats"
        case distanceMiles = "distance_miles"
        case avgOdFare = "avg_od_fare"
        case operatingCarriers = "operating_carriers"
    }

    public var originCoordinate: CLLocationCoordinate2D {
        CLLocationCoordinate2D(latitude: originLat, longitude: originLon)
    }

    public var destCoordinate: CLLocationCoordinate2D {
        CLLocationCoordinate2D(latitude: destLat, longitude: destLon)
    }

    public var label: String {
        "\(origin) ➔ \(dest)"
    }
}
