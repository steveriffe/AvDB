import Foundation
import CoreLocation

public struct Airport: Identifiable, Codable, Hashable, Sendable {
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

    enum CodingKeys: String, CodingKey {
        case iata, airportCode = "airport_code"
        case name, airportName = "airport_name"
        case city
        case state
        case latitude
        case longitude
        case catchmentMarket = "catchment_market"
        case isMajorHub = "is_commercial"
    }

    public init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        self.iata = (try? container.decode(String.self, forKey: .iata)) ??
                    (try? container.decode(String.self, forKey: .airportCode)) ?? ""
        self.name = (try? container.decode(String.self, forKey: .name)) ??
                    (try? container.decode(String.self, forKey: .airportName)) ?? ""
        self.city = (try? container.decode(String.self, forKey: .city)) ?? ""
        self.state = (try? container.decode(String.self, forKey: .state)) ?? ""
        self.latitude = (try? container.decode(Double.self, forKey: .latitude)) ?? 0.0
        self.longitude = (try? container.decode(Double.self, forKey: .longitude)) ?? 0.0
        self.catchmentMarket = try? container.decodeIfPresent(String.self, forKey: .catchmentMarket)
        self.isMajorHub = (try? container.decode(Bool.self, forKey: .isMajorHub)) ?? true
    }

    public func encode(to encoder: Encoder) throws {
        var container = encoder.container(keyedBy: CodingKeys.self)
        try container.encode(iata, forKey: .iata)
        try container.encode(name, forKey: .name)
        try container.encode(city, forKey: .city)
        try container.encode(state, forKey: .state)
        try container.encode(latitude, forKey: .latitude)
        try container.encode(longitude, forKey: .longitude)
        try container.encodeIfPresent(catchmentMarket, forKey: .catchmentMarket)
        try container.encode(isMajorHub, forKey: .isMajorHub)
    }
}

public struct AirportKPIs: Codable, Sendable {
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
        leadingCarrierShare: Double = 0.5
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

    enum CodingKeys: String, CodingKey {
        case totalDepartures, totalDeparturesSnake = "total_departures"
        case totalSeats, totalSeatsSnake = "total_seats"
        case totalPassengers, totalPassengersSnake = "total_passengers"
        case loadFactor, loadFactorPct = "load_factor_pct"
        case nonstopDestinations, directDestinations = "direct_destinations"
        case avgOdFare, avgOdFareSnake = "avg_od_fare"
        case leadingCarrier, leadingCarrierSnake = "leading_carrier"
        case leadingCarrierShare, leadingCarrierShareSnake = "leading_carrier_share"
    }

    public init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        self.totalDepartures = (try? container.decode(Int.self, forKey: .totalDepartures)) ??
                               (try? container.decode(Int.self, forKey: .totalDeparturesSnake)) ?? 0
        self.totalSeats = (try? container.decode(Int.self, forKey: .totalSeats)) ??
                          (try? container.decode(Int.self, forKey: .totalSeatsSnake)) ?? 0
        self.totalPassengers = (try? container.decode(Int.self, forKey: .totalPassengers)) ??
                               (try? container.decode(Int.self, forKey: .totalPassengersSnake)) ?? 0
        
        let lf = (try? container.decode(Double.self, forKey: .loadFactor)) ??
                 (try? container.decode(Double.self, forKey: .loadFactorPct)) ?? 85.0
        self.loadFactor = lf > 1.0 ? (lf / 100.0) : lf

        self.nonstopDestinations = (try? container.decode(Int.self, forKey: .nonstopDestinations)) ??
                                   (try? container.decode(Int.self, forKey: .directDestinations)) ?? 0
        self.avgOdFare = (try? container.decodeIfPresent(Double.self, forKey: .avgOdFare)) ??
                         (try? container.decodeIfPresent(Double.self, forKey: .avgOdFareSnake))
        self.leadingCarrier = (try? container.decode(String.self, forKey: .leadingCarrier)) ??
                              (try? container.decode(String.self, forKey: .leadingCarrierSnake)) ?? "—"
        let share = (try? container.decode(Double.self, forKey: .leadingCarrierShare)) ??
                    (try? container.decode(Double.self, forKey: .leadingCarrierShareSnake)) ?? 0.45
        self.leadingCarrierShare = share > 1.0 ? (share / 100.0) : share
    }

    public func encode(to encoder: Encoder) throws {
        var container = encoder.container(keyedBy: CodingKeys.self)
        try container.encode(totalDepartures, forKey: .totalDepartures)
        try container.encode(totalSeats, forKey: .totalSeats)
        try container.encode(totalPassengers, forKey: .totalPassengers)
        try container.encode(loadFactor, forKey: .loadFactor)
        try container.encode(nonstopDestinations, forKey: .nonstopDestinations)
        try container.encodeIfPresent(avgOdFare, forKey: .avgOdFare)
        try container.encode(leadingCarrier, forKey: .leadingCarrier)
        try container.encode(leadingCarrierShare, forKey: .leadingCarrierShare)
    }
}

public struct OutboundRoute: Identifiable, Codable, Hashable, Sendable {
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
    public let originLat: Double?
    public let originLon: Double?
    public let destLat: Double?
    public let destLon: Double?

    public init(
        origin: String,
        destination: String,
        carrier: String,
        departures: Int,
        seats: Int,
        passengers: Int,
        loadFactor: Double,
        distanceMiles: Double,
        avgOdFare: Double? = nil,
        originLat: Double? = nil,
        originLon: Double? = nil,
        destLat: Double? = nil,
        destLon: Double? = nil
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
        self.originLat = originLat
        self.originLon = originLon
        self.destLat = destLat
        self.destLon = destLon
    }

    enum CodingKeys: String, CodingKey {
        case origin
        case destination, dest
        case carrier, operatingCarriers = "operating_carriers"
        case departures, departuresPerformed = "departures_performed"
        case seats, totalSeats = "total_seats"
        case passengers, operationalPassengers = "operational_passengers"
        case loadFactor, loadFactorPct = "load_factor_pct"
        case distanceMiles, distanceMilesSnake = "distance_miles"
        case avgOdFare, avgOdFareSnake = "avg_od_fare"
        case originLat = "origin_lat"
        case originLon = "origin_lon"
        case destLat = "dest_lat"
        case destLon = "dest_lon"
    }

    public init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        self.origin = (try? container.decode(String.self, forKey: .origin)) ?? ""
        self.destination = (try? container.decode(String.self, forKey: .destination)) ??
                           (try? container.decode(String.self, forKey: .dest)) ?? ""
        self.carrier = (try? container.decode(String.self, forKey: .carrier)) ??
                       (try? container.decode(String.self, forKey: .operatingCarriers)) ?? "—"
        self.departures = (try? container.decode(Int.self, forKey: .departures)) ??
                          (try? container.decode(Int.self, forKey: .departuresPerformed)) ?? 0
        self.seats = (try? container.decode(Int.self, forKey: .seats)) ??
                     (try? container.decode(Int.self, forKey: .totalSeats)) ?? 0
        self.passengers = (try? container.decode(Int.self, forKey: .passengers)) ??
                          (try? container.decode(Int.self, forKey: .operationalPassengers)) ?? 0

        let lf = (try? container.decode(Double.self, forKey: .loadFactor)) ??
                 (try? container.decode(Double.self, forKey: .loadFactorPct)) ?? 85.0
        self.loadFactor = lf > 1.0 ? (lf / 100.0) : lf

        self.distanceMiles = (try? container.decode(Double.self, forKey: .distanceMiles)) ??
                             (try? container.decode(Double.self, forKey: .distanceMilesSnake)) ?? 500.0
        self.avgOdFare = (try? container.decodeIfPresent(Double.self, forKey: .avgOdFare)) ??
                         (try? container.decodeIfPresent(Double.self, forKey: .avgOdFareSnake))
        self.originLat = try? container.decodeIfPresent(Double.self, forKey: .originLat)
        self.originLon = try? container.decodeIfPresent(Double.self, forKey: .originLon)
        self.destLat = try? container.decodeIfPresent(Double.self, forKey: .destLat)
        self.destLon = try? container.decodeIfPresent(Double.self, forKey: .destLon)
    }

    public func encode(to encoder: Encoder) throws {
        var container = encoder.container(keyedBy: CodingKeys.self)
        try container.encode(origin, forKey: .origin)
        try container.encode(destination, forKey: .destination)
        try container.encode(carrier, forKey: .carrier)
        try container.encode(departures, forKey: .departures)
        try container.encode(seats, forKey: .seats)
        try container.encode(passengers, forKey: .passengers)
        try container.encode(loadFactor, forKey: .loadFactor)
        try container.encode(distanceMiles, forKey: .distanceMiles)
        try container.encodeIfPresent(avgOdFare, forKey: .avgOdFare)
    }
}

public struct AirportTimelinePoint: Identifiable, Codable, Hashable, Sendable {
    public var id: Int { year }
    public let year: Int
    public let totalPassengers: Int
    public let totalDepartures: Int
    public let totalSeats: Int
    public let loadFactorPct: Double
    public let directDestinations: Int
    public let avgOdFare: Double?

    public init(
        year: Int,
        totalPassengers: Int,
        totalDepartures: Int,
        totalSeats: Int,
        loadFactorPct: Double,
        directDestinations: Int,
        avgOdFare: Double? = nil
    ) {
        self.year = year
        self.totalPassengers = totalPassengers
        self.totalDepartures = totalDepartures
        self.totalSeats = totalSeats
        self.loadFactorPct = loadFactorPct
        self.directDestinations = directDestinations
        self.avgOdFare = avgOdFare
    }

    enum CodingKeys: String, CodingKey {
        case year
        case totalPassengers = "total_passengers"
        case totalDepartures = "total_departures"
        case totalSeats = "total_seats"
        case loadFactorPct = "load_factor_pct"
        case directDestinations = "direct_destinations"
        case avgOdFare = "avg_od_fare"
    }
}

public struct AirportCarrierShare: Identifiable, Codable, Hashable, Sendable {
    public var id: String { uniqueCarrier }
    public let uniqueCarrier: String
    public let carrierName: String?
    public let departuresPerformed: Int
    public let totalSeats: Int
    public let operationalPassengers: Int
    public let loadFactorPct: Double
    public let seatSharePct: Double?
    public let avgFare: Double?

    public init(
        uniqueCarrier: String,
        carrierName: String? = nil,
        departuresPerformed: Int,
        totalSeats: Int,
        operationalPassengers: Int,
        loadFactorPct: Double,
        seatSharePct: Double? = nil,
        avgFare: Double? = nil
    ) {
        self.uniqueCarrier = uniqueCarrier
        self.carrierName = carrierName
        self.departuresPerformed = departuresPerformed
        self.totalSeats = totalSeats
        self.operationalPassengers = operationalPassengers
        self.loadFactorPct = loadFactorPct
        self.seatSharePct = seatSharePct
        self.avgFare = avgFare
    }

    enum CodingKeys: String, CodingKey {
        case uniqueCarrier = "unique_carrier"
        case carrierName = "carrier_name"
        case departuresPerformed = "departures_performed"
        case totalSeats = "total_seats"
        case operationalPassengers = "operational_passengers"
        case loadFactorPct = "load_factor_pct"
        case seatSharePct = "seat_share_pct"
        case avgFare = "avg_fare"
    }
}
