import Foundation
import CoreLocation

/// Spherical Geodesic Mathematics for Great-Circle Flight Path Rendering
public struct GeodesicMath: Sendable {
    private static let earthRadiusMiles = 3958.8

    /// Generates intermediate geodesic coordinates along a great-circle arc between two coordinates.
    /// Produces the smooth curved routes characteristic of in-flight route atlases.
    public static func greatCircleCoordinates(
        from origin: CLLocationCoordinate2D,
        to destination: CLLocationCoordinate2D,
        numberOfPoints: Int = 32
    ) -> [CLLocationCoordinate2D] {
        let lat1 = origin.latitude * .pi / 180.0
        let lon1 = origin.longitude * .pi / 180.0
        let lat2 = destination.latitude * .pi / 180.0
        let lon2 = destination.longitude * .pi / 180.0

        // Spherical angular distance (d) using Haversine
        let dLat = lat2 - lat1
        let dLon = lon2 - lon1
        let a = sin(dLat / 2.0) * sin(dLat / 2.0) +
                cos(lat1) * cos(lat2) * sin(dLon / 2.0) * sin(dLon / 2.0)
        let d = 2.0 * atan2(sqrt(a), sqrt(1.0 - a))

        if d < 0.0001 {
            return [origin, destination]
        }

        var points: [CLLocationCoordinate2D] = []
        points.reserveCapacity(numberOfPoints)

        for i in 0..<numberOfPoints {
            let f = Double(i) / Double(numberOfPoints - 1)
            let A = sin((1.0 - f) * d) / sin(d)
            let B = sin(f * d) / sin(d)

            let x = A * cos(lat1) * cos(lon1) + B * cos(lat2) * cos(lon2)
            let y = A * cos(lat1) * sin(lon1) + B * cos(lat2) * sin(lon2)
            let z = A * sin(lat1) + B * sin(lat2)

            let newLat = atan2(z, sqrt(x * x + y * y)) * 180.0 / .pi
            let newLon = atan2(y, x) * 180.0 / .pi

            points.append(CLLocationCoordinate2D(latitude: newLat, longitude: newLon))
        }

        return points
    }

    /// Computes great-circle distance in statute miles
    public static func distanceMiles(
        from origin: CLLocationCoordinate2D,
        to destination: CLLocationCoordinate2D
    ) -> Double {
        let lat1 = origin.latitude * .pi / 180.0
        let lon1 = origin.longitude * .pi / 180.0
        let lat2 = destination.latitude * .pi / 180.0
        let lon2 = destination.longitude * .pi / 180.0

        let dLat = lat2 - lat1
        let dLon = lon2 - lon1
        let a = sin(dLat / 2.0) * sin(dLat / 2.0) +
                cos(lat1) * cos(lat2) * sin(dLon / 2.0) * sin(dLon / 2.0)
        let c = 2.0 * atan2(sqrt(a), sqrt(1.0 - a))
        return earthRadiusMiles * c
    }
}
