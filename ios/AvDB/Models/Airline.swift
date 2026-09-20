import SwiftUI

public struct Airline: Identifiable, Codable, Hashable, Sendable {
    public var id: String { code }
    public let code: String
    public let name: String
    public let hexColor: String
    public let alliance: String?
    public let primaryHubs: [String]
    public let headquarters: String
    public let isActive: Bool
    public let mergerNote: String?

    public var brandColor: Color {
        Color(hex: hexColor) ?? AvDBTheme.accentBlue
    }

    public init(
        code: String,
        name: String,
        hexColor: String,
        alliance: String? = nil,
        primaryHubs: [String] = [],
        headquarters: String = "",
        isActive: Bool = true,
        mergerNote: String? = nil
    ) {
        self.code = code
        self.name = name
        self.hexColor = hexColor
        self.alliance = alliance
        self.primaryHubs = primaryHubs
        self.headquarters = headquarters
        self.isActive = isActive
        self.mergerNote = mergerNote
    }

    enum CodingKeys: String, CodingKey {
        case code, carrierCode = "carrier_code"
        case name, carrierName = "carrier_name"
        case hexColor, brandColor = "brand_color"
        case alliance
        case primaryHubs, primaryHubsSnake = "primary_hubs"
        case headquarters
        case isActive = "is_active"
        case mergerNote = "merger_note"
    }

    public init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        self.code = (try? container.decode(String.self, forKey: .code)) ??
                    (try? container.decode(String.self, forKey: .carrierCode)) ?? ""
        self.name = (try? container.decode(String.self, forKey: .name)) ??
                    (try? container.decode(String.self, forKey: .carrierName)) ?? ""
        self.hexColor = (try? container.decode(String.self, forKey: .hexColor)) ??
                        (try? container.decode(String.self, forKey: .brandColor)) ?? "#0078D2"
        self.alliance = try? container.decodeIfPresent(String.self, forKey: .alliance)
        self.primaryHubs = (try? container.decode([String].self, forKey: .primaryHubs)) ??
                           (try? container.decode([String].self, forKey: .primaryHubsSnake)) ?? []
        self.headquarters = (try? container.decode(String.self, forKey: .headquarters)) ?? ""
        self.isActive = (try? container.decode(Bool.self, forKey: .isActive)) ?? true
        self.mergerNote = try? container.decodeIfPresent(String.self, forKey: .mergerNote)
    }

    public func encode(to encoder: Encoder) throws {
        var container = encoder.container(keyedBy: CodingKeys.self)
        try container.encode(code, forKey: .code)
        try container.encode(name, forKey: .name)
        try container.encode(hexColor, forKey: .hexColor)
        try container.encodeIfPresent(alliance, forKey: .alliance)
        try container.encode(primaryHubs, forKey: .primaryHubs)
        try container.encode(headquarters, forKey: .headquarters)
        try container.encode(isActive, forKey: .isActive)
        try container.encodeIfPresent(mergerNote, forKey: .mergerNote)
    }
}

public struct AirlineKPIs: Codable, Sendable {
    public let activeRoutes: Int
    public let departures: Int
    public let totalSeats: Int
    public let totalPassengers: Int
    public let loadFactor: Double
    public let asmBillions: Double
    public let rpmBillions: Double
    public let avgOdFare: Double?
    public let yieldPerMile: Double?

    public init(
        activeRoutes: Int,
        departures: Int,
        totalSeats: Int,
        totalPassengers: Int,
        loadFactor: Double,
        asmBillions: Double,
        rpmBillions: Double,
        avgOdFare: Double? = nil,
        yieldPerMile: Double? = nil
    ) {
        self.activeRoutes = activeRoutes
        self.departures = departures
        self.totalSeats = totalSeats
        self.totalPassengers = totalPassengers
        self.loadFactor = loadFactor
        self.asmBillions = asmBillions
        self.rpmBillions = rpmBillions
        self.avgOdFare = avgOdFare
        self.yieldPerMile = yieldPerMile
    }

    enum CodingKeys: String, CodingKey {
        case activeRoutes, activeRoutesSnake = "active_routes"
        case departures, totalDepartures = "total_departures"
        case totalSeats, totalSeatsSnake = "total_seats"
        case totalPassengers, totalPassengersSnake = "total_passengers"
        case loadFactor, systemLoadFactor = "system_load_factor"
        case asmBillions, totalAsm = "total_asm"
        case rpmBillions, totalRpm = "total_rpm"
        case avgOdFare, avgNetworkFare = "avg_network_fare"
        case yieldPerMile, avgYieldPerMile = "avg_yield_per_mile"
    }

    public init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        self.activeRoutes = (try? container.decode(Int.self, forKey: .activeRoutes)) ??
                            (try? container.decode(Int.self, forKey: .activeRoutesSnake)) ?? 0
        self.departures = (try? container.decode(Int.self, forKey: .departures)) ??
                          (try? container.decode(Int.self, forKey: .totalDepartures)) ?? 0
        self.totalSeats = (try? container.decode(Int.self, forKey: .totalSeats)) ??
                          (try? container.decode(Int.self, forKey: .totalSeatsSnake)) ?? 0
        self.totalPassengers = (try? container.decode(Int.self, forKey: .totalPassengers)) ??
                               (try? container.decode(Int.self, forKey: .totalPassengersSnake)) ?? 0

        let lf = (try? container.decode(Double.self, forKey: .loadFactor)) ??
                 (try? container.decode(Double.self, forKey: .systemLoadFactor)) ?? 85.0
        self.loadFactor = lf > 1.0 ? (lf / 100.0) : lf

        if let rawAsm = try? container.decode(Double.self, forKey: .totalAsm) {
            self.asmBillions = rawAsm > 1_000_000 ? (rawAsm / 1_000_000_000.0) : rawAsm
        } else if let asmB = try? container.decode(Double.self, forKey: .asmBillions) {
            self.asmBillions = asmB
        } else {
            self.asmBillions = 25.0
        }

        if let rawRpm = try? container.decode(Double.self, forKey: .totalRpm) {
            self.rpmBillions = rawRpm > 1_000_000 ? (rawRpm / 1_000_000_000.0) : rawRpm
        } else if let rpmB = try? container.decode(Double.self, forKey: .rpmBillions) {
            self.rpmBillions = rpmB
        } else {
            self.rpmBillions = 21.0
        }

        self.avgOdFare = (try? container.decodeIfPresent(Double.self, forKey: .avgOdFare)) ??
                         (try? container.decodeIfPresent(Double.self, forKey: .avgNetworkFare))
        self.yieldPerMile = (try? container.decodeIfPresent(Double.self, forKey: .yieldPerMile)) ??
                            (try? container.decodeIfPresent(Double.self, forKey: .avgYieldPerMile))
    }

    public func encode(to encoder: Encoder) throws {
        var container = encoder.container(keyedBy: CodingKeys.self)
        try container.encode(activeRoutes, forKey: .activeRoutes)
        try container.encode(departures, forKey: .departures)
        try container.encode(totalSeats, forKey: .totalSeats)
        try container.encode(totalPassengers, forKey: .totalPassengers)
        try container.encode(loadFactor, forKey: .loadFactor)
        try container.encode(asmBillions, forKey: .asmBillions)
        try container.encode(rpmBillions, forKey: .rpmBillions)
        try container.encodeIfPresent(avgOdFare, forKey: .avgOdFare)
        try container.encodeIfPresent(yieldPerMile, forKey: .yieldPerMile)
    }
}

public struct AirlineTimelinePoint: Identifiable, Codable, Hashable, Sendable {
    public var id: Int { year }
    public let year: Int
    public let asmBillions: Double
    public let rpmBillions: Double
    public let systemLoadFactor: Double
    public let totalPassengers: Int
    public let totalDepartures: Int
    public let avgNetworkFare: Double?
    public let avgYieldPerMile: Double?

    public init(
        year: Int,
        asmBillions: Double,
        rpmBillions: Double,
        systemLoadFactor: Double,
        totalPassengers: Int,
        totalDepartures: Int,
        avgNetworkFare: Double? = nil,
        avgYieldPerMile: Double? = nil
    ) {
        self.year = year
        self.asmBillions = asmBillions
        self.rpmBillions = rpmBillions
        self.systemLoadFactor = systemLoadFactor
        self.totalPassengers = totalPassengers
        self.totalDepartures = totalDepartures
        self.avgNetworkFare = avgNetworkFare
        self.avgYieldPerMile = avgYieldPerMile
    }

    enum CodingKeys: String, CodingKey {
        case year
        case totalAsm = "total_asm"
        case totalRpm = "total_rpm"
        case systemLoadFactor = "system_load_factor"
        case totalPassengers = "total_passengers"
        case totalDepartures = "total_departures"
        case avgNetworkFare = "avg_network_fare"
        case avgYieldPerMile = "avg_yield_per_mile"
    }

    public init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        self.year = try container.decode(Int.self, forKey: .year)

        let rawAsm = (try? container.decode(Double.self, forKey: .totalAsm)) ?? 0.0
        self.asmBillions = rawAsm > 1_000_000 ? (rawAsm / 1_000_000_000.0) : rawAsm

        let rawRpm = (try? container.decode(Double.self, forKey: .totalRpm)) ?? 0.0
        self.rpmBillions = rawRpm > 1_000_000 ? (rawRpm / 1_000_000_000.0) : rawRpm

        self.systemLoadFactor = (try? container.decode(Double.self, forKey: .systemLoadFactor)) ?? 85.0
        self.totalPassengers = (try? container.decode(Int.self, forKey: .totalPassengers)) ?? 0
        self.totalDepartures = (try? container.decode(Int.self, forKey: .totalDepartures)) ?? 0
        self.avgNetworkFare = try? container.decodeIfPresent(Double.self, forKey: .avgNetworkFare)
        self.avgYieldPerMile = try? container.decodeIfPresent(Double.self, forKey: .avgYieldPerMile)
    }

    public func encode(to encoder: Encoder) throws {
        var container = encoder.container(keyedBy: CodingKeys.self)
        try container.encode(year, forKey: .year)
        try container.encode(asmBillions, forKey: .totalAsm)
        try container.encode(rpmBillions, forKey: .totalRpm)
        try container.encode(systemLoadFactor, forKey: .systemLoadFactor)
        try container.encode(totalPassengers, forKey: .totalPassengers)
        try container.encode(totalDepartures, forKey: .totalDepartures)
        try container.encodeIfPresent(avgNetworkFare, forKey: .avgNetworkFare)
        try container.encodeIfPresent(avgYieldPerMile, forKey: .avgYieldPerMile)
    }
}

public struct YieldCurvePoint: Identifiable, Codable, Hashable, Sendable {
    public var id: String { "\(origin)-\(dest)" }
    public let origin: String
    public let dest: String
    public let routeLabel: String
    public let stageLengthMiles: Double
    public let avgOdFare: Double
    public let yieldPerMile: Double
    public let operationalPassengers: Int
    public let loadFactorPct: Double

    public init(
        origin: String,
        dest: String,
        routeLabel: String,
        stageLengthMiles: Double,
        avgOdFare: Double,
        yieldPerMile: Double,
        operationalPassengers: Int,
        loadFactorPct: Double
    ) {
        self.origin = origin
        self.dest = dest
        self.routeLabel = routeLabel
        self.stageLengthMiles = stageLengthMiles
        self.avgOdFare = avgOdFare
        self.yieldPerMile = yieldPerMile
        self.operationalPassengers = operationalPassengers
        self.loadFactorPct = loadFactorPct
    }

    enum CodingKeys: String, CodingKey {
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

public extension Color {
    init?(hex: String) {
        var hexSanitized = hex.trimmingCharacters(in: .whitespacesAndNewlines)
        hexSanitized = hexSanitized.replacingOccurrences(of: "#", with: "")

        var rgb: UInt64 = 0
        guard Scanner(string: hexSanitized).scanHexInt64(&rgb) else { return nil }

        let r = Double((rgb & 0xFF0000) >> 16) / 255.0
        let g = Double((rgb & 0x00FF00) >> 8) / 255.0
        let b = Double(rgb & 0x0000FF) / 255.0
        self.init(red: r, green: g, blue: b)
    }
}
