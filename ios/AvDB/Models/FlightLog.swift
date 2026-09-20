import Foundation

public struct FlightLog: Identifiable, Codable, Hashable, Sendable {
    public var id: String { flightIdentifier }
    public let flightIdentifier: String
    public let date: String
    public let flightNumber: String
    public let airlineCode: String
    public let originIATA: String
    public let destIATA: String
    public let aircraftType: String?
    public let tailNumber: String?
    public let seatNumber: String?
    public let seatClass: String?
    public let distanceMiles: Double?

    public init(
        flightIdentifier: String = UUID().uuidString,
        date: String,
        flightNumber: String,
        airlineCode: String,
        originIATA: String,
        destIATA: String,
        aircraftType: String? = nil,
        tailNumber: String? = nil,
        seatNumber: String? = nil,
        seatClass: String? = nil,
        distanceMiles: Double? = nil
    ) {
        self.flightIdentifier = flightIdentifier
        self.date = date
        self.flightNumber = flightNumber
        self.airlineCode = airlineCode
        self.originIATA = originIATA
        self.destIATA = destIATA
        self.aircraftType = aircraftType
        self.tailNumber = tailNumber
        self.seatNumber = seatNumber
        self.seatClass = seatClass
        self.distanceMiles = distanceMiles
    }
}

