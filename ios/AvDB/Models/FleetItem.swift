import Foundation

public struct FleetFamily: Identifiable, Codable, Hashable {
    public var id: String { familyName }
    public let familyName: String
    public let manufacturer: String
    public let totalDepartures: Int
    public let totalSeats: Int
    public let avgGauge: Double
    public let dominantOperators: [String]
    public let subfleets: [Subfleet]

    public init(
        familyName: String,
        manufacturer: String,
        totalDepartures: Int,
        totalSeats: Int,
        avgGauge: Double,
        dominantOperators: [String],
        subfleets: [Subfleet] = []
    ) {
        self.familyName = familyName
        self.manufacturer = manufacturer
        self.totalDepartures = totalDepartures
        self.totalSeats = totalSeats
        self.avgGauge = avgGauge
        self.dominantOperators = dominantOperators
        self.subfleets = subfleets
    }
}

public struct Subfleet: Identifiable, Codable, Hashable {
    public var id: String { aircraftType }
    public let aircraftType: String
    public let typicalSeats: Int
    public let engineType: String
    public let departures: Int
    public let seats: Int
    public let avgStageLength: Double

    public init(
        aircraftType: String,
        typicalSeats: Int,
        engineType: String,
        departures: Int,
        seats: Int,
        avgStageLength: Double
    ) {
        self.aircraftType = aircraftType
        self.typicalSeats = typicalSeats
        self.engineType = engineType
        self.departures = departures
        self.seats = seats
        self.avgStageLength = avgStageLength
    }
}
