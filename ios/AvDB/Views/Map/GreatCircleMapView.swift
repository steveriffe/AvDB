import SwiftUI
import MapKit

/// High-performance Great-Circle geodesic route visualizer built with MapKit.
public struct GreatCircleMapView: UIViewRepresentable {
    public let routes: [GeodesicRoute]
    public let focusAirport: Airport?

    public init(routes: [GeodesicRoute], focusAirport: Airport? = nil) {
        self.routes = routes
        self.focusAirport = focusAirport
    }

    public func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }

    public func makeUIView(context: Context) -> MKMapView {
        let mapView = MKMapView()
        mapView.delegate = context.coordinator
        mapView.isPitchEnabled = true
        mapView.isRotateEnabled = true
        mapView.showsCompass = true
        mapView.showsScale = true
        mapView.overrideUserInterfaceStyle = .dark

        // Dark map configuration
        if #available(iOS 16.0, *) {
            let config = MKStandardMapConfiguration(elevationStyle: .realistic, emphasisStyle: .muted)
            mapView.preferredConfiguration = config
        }

        updateOverlays(for: mapView)
        return mapView
    }

    public func updateUIView(_ uiView: MKMapView, context: Context) {
        updateOverlays(for: uiView)
    }

    private func updateOverlays(for mapView: MKMapView) {
        mapView.removeOverlays(mapView.overlays)
        mapView.removeAnnotations(mapView.annotations)

        var allCoordinates: [CLLocationCoordinate2D] = []

        // Add Great-Circle arcs
        for route in routes {
            let start = route.originCoord.clCoordinate
            let end = route.destCoord.clCoordinate

            var coords = [start, end]
            let geodesicPolyline = MKGeodesicPolyline(coordinates: &coords, count: 2)
            mapView.addOverlay(geodesicPolyline, level: .aboveLabels)

            allCoordinates.append(start)
            allCoordinates.append(end)

            // Add Pin for destination
            let destPin = MKPointAnnotation()
            destPin.coordinate = end
            destPin.title = route.destIATA
            destPin.subtitle = "\(route.passengerVolume.formatted()) pax • $\(String(format: "%.0f", route.avgFare ?? 0))"
            mapView.addAnnotation(destPin)
        }

        // Add Hub pin
        if let focus = focusAirport {
            let hubPin = MKPointAnnotation()
            hubPin.coordinate = focus.coordinate
            hubPin.title = "\(focus.iata) [HUB]"
            hubPin.subtitle = focus.name
            mapView.addAnnotation(hubPin)
            allCoordinates.append(focus.coordinate)
        }

        // Fit map camera smoothly
        if !allCoordinates.isEmpty {
            let minLat = allCoordinates.map { $0.latitude }.min() ?? 30.0
            let maxLat = allCoordinates.map { $0.latitude }.max() ?? 50.0
            let minLon = allCoordinates.map { $0.longitude }.min() ?? -125.0
            let maxLon = allCoordinates.map { $0.longitude }.max() ?? -70.0

            let center = CLLocationCoordinate2D(latitude: (minLat + maxLat) / 2.0, longitude: (minLon + maxLon) / 2.0)
            let span = MKCoordinateSpan(latitudeDelta: max(abs(maxLat - minLat) * 1.35, 4.0), longitudeDelta: max(abs(maxLon - minLon) * 1.35, 4.0))
            let region = MKCoordinateRegion(center: center, span: span)
            mapView.setRegion(region, animated: true)
        }
    }

    public class Coordinator: NSObject, MKMapViewDelegate {
        var parent: GreatCircleMapView

        init(_ parent: GreatCircleMapView) {
            self.parent = parent
        }

        public func mapView(_ mapView: MKMapView, rendererFor overlay: MKOverlay) -> MKOverlayRenderer {
            if let polyline = overlay as? MKPolyline {
                let renderer = MKPolylineRenderer(polyline: polyline)
                renderer.strokeColor = UIColor(red: 0.0, green: 0.95, blue: 1.0, alpha: 0.75) // Electric Cyan
                renderer.lineWidth = 2.5
                renderer.lineCap = .round
                return renderer
            }
            return MKOverlayRenderer(overlay: overlay)
        }

        public func mapView(_ mapView: MKMapView, viewFor annotation: MKAnnotation) -> MKAnnotationView? {
            let identifier = "AirportPin"
            var view = mapView.dequeueReusableAnnotationView(withIdentifier: identifier) as? MKMarkerAnnotationView
            if view == nil {
                view = MKMarkerAnnotationView(annotation: annotation, reuseIdentifier: identifier)
                view?.canShowCallout = true
            } else {
                view?.annotation = annotation
            }

            if let title = annotation.title ?? "", title.contains("[HUB]") {
                view?.markerTintColor = UIColor(red: 0.04, green: 0.52, blue: 1.0, alpha: 1.0) // Royal Blue
                view?.glyphImage = UIImage(systemName: "airplane.circle.fill")
                view?.displayPriority = .required
            } else {
                view?.markerTintColor = UIColor(red: 0.96, green: 0.62, blue: 0.04, alpha: 1.0) // Amber
                view?.glyphImage = UIImage(systemName: "airplane.departure")
                view?.displayPriority = .defaultHigh
            }

            return view
        }
    }
}
