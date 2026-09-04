import Foundation
import CoreLocation

/// Model representing an individual flight logged in Flighty
public struct FlightyRecord: Identifiable, Hashable, Sendable {
    public let id: UUID
    public let date: String
    public let flightNumber: String
    public let airline: String
    public let origin: String
    public let destination: String
    public let aircraftType: String
    public let tailNumber: String
    public let seat: String
    public let distanceMiles: Double
    public let durationMinutes: Int?

    public init(
        id: UUID = UUID(),
        date: String,
        flightNumber: String,
        airline: String,
        origin: String,
        destination: String,
        aircraftType: String,
        tailNumber: String = "",
        seat: String = "",
        distanceMiles: Double = 0.0,
        durationMinutes: Int? = nil
    ) {
        self.id = id
        self.date = date
        self.flightNumber = flightNumber
        self.airline = airline
        self.origin = origin.uppercased()
        self.destination = destination.uppercased()
        self.aircraftType = aircraftType
        self.tailNumber = tailNumber
        self.seat = seat
        self.distanceMiles = distanceMiles
        self.durationMinutes = durationMinutes
    }

    public var routeKey: String {
        "\(origin)-\(destination)"
    }
}

/// Aggregated Flighty user statistics
public struct FlightySummary: Sendable {
    public let totalFlights: Int
    public let totalMiles: Double
    public let uniqueAirports: Int
    public let uniqueAirlines: Int
    public let uniqueAircraftTypes: Int
    public let topAircraftType: String
    public let topRoute: String

    public static var empty: FlightySummary {
        FlightySummary(
            totalFlights: 0,
            totalMiles: 0,
            uniqueAirports: 0,
            uniqueAirlines: 0,
            uniqueAircraftTypes: 0,
            topAircraftType: "—",
            topRoute: "—"
        )
    }
}

/// Subfleet grouping for Flighty flights
public struct FlightySubfleetGroup: Identifiable, Hashable, Sendable {
    public var id: String { aircraftType }
    public let aircraftType: String
    public let flightCount: Int
    public let totalMiles: Double
    public let percentage: Double
}
