import SwiftUI

public struct Airline: Identifiable, Codable, Hashable {
    public var id: String { code }
    public let code: String
    public let name: String
    public let hexColor: String
    public let alliance: String?
    public let primaryHubs: [String]
    public let headquarters: String

    public var brandColor: Color {
        Color(hex: hexColor) ?? AvDBTheme.accentBlue
    }

    public init(
        code: String,
        name: String,
        hexColor: String,
        alliance: String? = nil,
        primaryHubs: [String] = [],
        headquarters: String = ""
    ) {
        self.code = code
        self.name = name
        self.hexColor = hexColor
        self.alliance = alliance
        self.primaryHubs = primaryHubs
        self.headquarters = headquarters
    }
}

public struct AirlineKPIs: Codable {
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

