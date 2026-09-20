import Foundation
import CoreLocation

/// Mathematical utilities for spherical great-circle navigation and interpolation.
public enum GeodesicMath {
    private static let earthRadiusMiles: Double = 3958.8
    private static let earthRadiusKm: Double = 6371.0

    /// Calculates Great-Circle distance in statute miles between two coordinate points using Haversine formula.
    public static func distanceMiles(from: CLLocationCoordinate2D, to: CLLocationCoordinate2D) -> Double {
        let lat1 = from.latitude * .pi / 180.0
        let lon1 = from.longitude * .pi / 180.0
        let lat2 = to.latitude * .pi / 180.0
        let lon2 = to.longitude * .pi / 180.0

        let dLat = lat2 - lat1
        let dLon = lon2 - lon1

        let a = sin(dLat / 2.0) * sin(dLat / 2.0) +
                cos(lat1) * cos(lat2) *
                sin(dLon / 2.0) * sin(dLon / 2.0)
        let c = 2.0 * atan2(sqrt(a), sqrt(1.0 - a))
        return earthRadiusMiles * c
    }

    /// Interpolates N waypoints along the Great-Circle geodesic arc between two points.
    public static func geodesicWaypoints(
        from: CLLocationCoordinate2D,
        to: CLLocationCoordinate2D,
        segments: Int = 32
    ) -> [CLLocationCoordinate2D] {
        guard segments > 1 else { return [from, to] }

        let lat1 = from.latitude * .pi / 180.0
        let lon1 = from.longitude * .pi / 180.0
        let lat2 = to.latitude * .pi / 180.0
        let lon2 = to.longitude * .pi / 180.0

        let d = 2.0 * asin(sqrt(
            pow(sin((lat1 - lat2) / 2.0), 2) +
            cos(lat1) * cos(lat2) * pow(sin((lon1 - lon2) / 2.0), 2)
        ))

        if d.isNaN || d == 0 {
            return [from, to]
        }

        var coords: [CLLocationCoordinate2D] = []
        for i in 0...segments {
            let f = Double(i) / Double(segments)
            let a = sin((1.0 - f) * d) / sin(d)
            let b = sin(f * d) / sin(d)

            let x = a * cos(lat1) * cos(lon1) + b * cos(lat2) * cos(lon2)
            let y = a * cos(lat1) * sin(lon1) + b * cos(lat2) * sin(lon2)
            let z = a * sin(lat1) + b * sin(lat2)

            let lat = atan2(z, sqrt(x * x + y * y)) * 180.0 / .pi
            let lon = atan2(y, x) * 180.0 / .pi

            coords.append(CLLocationCoordinate2D(latitude: lat, longitude: lon))
        }
        return coords
    }
}

