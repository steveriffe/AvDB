import Foundation
import CoreLocation

public struct CoordinatePoint: Codable, Hashable {
    public let latitude: Double
    public let longitude: Double

    public var clCoordinate: CLLocationCoordinate2D {
        CLLocationCoordinate2D(latitude: latitude, longitude: longitude)
    }

    public init(latitude: Double, longitude: Double) {
        self.latitude = latitude
        self.longitude = longitude
    }
}

public struct GeodesicRoute: Identifiable, Hashable {
    public var id: String { "\(originIATA)-\(destIATA)-\(carrier)" }
    public let originIATA: String
    public let destIATA: String
    public let carrier: String
    public let originCoord: CoordinatePoint
    public let destCoord: CoordinatePoint
    public let passengerVolume: Int
    public let avgFare: Double?

    public init(
        originIATA: String,
        destIATA: String,
        carrier: String,
        originCoord: CoordinatePoint,
        destCoord: CoordinatePoint,
        passengerVolume: Int,
        avgFare: Double? = nil
    ) {
        self.originIATA = originIATA
        self.destIATA = destIATA
        self.carrier = carrier
        self.originCoord = originCoord
        self.destCoord = destCoord
        self.passengerVolume = passengerVolume
        self.avgFare = avgFare
    }
}
