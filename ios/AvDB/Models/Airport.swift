import Foundation
import CoreLocation

public struct Airport: Identifiable, Codable, Hashable {
    public var id: String { iata }
    public let iata: String
    public let name: String
    public let city: String
    public let state: String
    public let latitude: Double
    public let longitude: Double
    public let catchmentMarket: String?
    public let isMajorHub: Bool

    public var coordinate: CLLocationCoordinate2D {
        CLLocationCoordinate2D(latitude: latitude, longitude: longitude)
    }

    public var displayName: String {
        "\(iata) - \(name)"
    }

    public init(
        iata: String,
        name: String,
        city: String,
        state: String,
        latitude: Double,
        longitude: Double,
        catchmentMarket: String? = nil,
        isMajorHub: Bool = false
    ) {
        self.iata = iata
        self.name = name
        self.city = city
        self.state = state
        self.latitude = latitude
        self.longitude = longitude
        self.catchmentMarket = catchmentMarket
        self.isMajorHub = isMajorHub
    }
}

public struct AirportKPIs: Codable {
    public let totalDepartures: Int
    public let totalSeats: Int
    public let totalPassengers: Int
    public let loadFactor: Double
    public let nonstopDestinations: Int
    public let avgOdFare: Double?
    public let leadingCarrier: String
    public let leadingCarrierShare: Double

    public init(
        totalDepartures: Int,
        totalSeats: Int,
        totalPassengers: Int,
        loadFactor: Double,
        nonstopDestinations: Int,
        avgOdFare: Double? = nil,
        leadingCarrier: String,
        leadingCarrierShare: Double
    ) {
        self.totalDepartures = totalDepartures
        self.totalSeats = totalSeats
        self.totalPassengers = totalPassengers
        self.loadFactor = loadFactor
        self.nonstopDestinations = nonstopDestinations
        self.avgOdFare = avgOdFare
        self.leadingCarrier = leadingCarrier
        self.leadingCarrierShare = leadingCarrierShare
    }
}

public struct OutboundRoute: Identifiable, Codable, Hashable {
    public var id: String { "\(origin)-\(destination)-\(carrier)" }
    public let origin: String
    public let destination: String
    public let carrier: String
    public let departures: Int
    public let seats: Int
    public let passengers: Int
    public let loadFactor: Double
    public let distanceMiles: Double
    public let avgOdFare: Double?

    public init(
        origin: String,
        destination: String,
        carrier: String,
        departures: Int,
        seats: Int,
        passengers: Int,
        loadFactor: Double,
        distanceMiles: Double,
        avgOdFare: Double? = nil
    ) {
        self.origin = origin
        self.destination = destination
        self.carrier = carrier
        self.departures = departures
        self.seats = seats
        self.passengers = passengers
        self.loadFactor = loadFactor
        self.distanceMiles = distanceMiles
        self.avgOdFare = avgOdFare
    }
}

