import SwiftUI
import MapKit

/// Native 120Hz ProMotion Route Network Map with Great-Circle Geodesic Curves
public struct RouteMapView: View {
    let routes: [RouteItem]
    let originCode: String?
    let originCoordinate: CLLocationCoordinate2D?
    let routeColor: Color
    @Binding var selectedRoute: RouteItem?

    @State private var position: MapCameraPosition = .automatic

    public init(
        routes: [RouteItem],
        originCode: String? = nil,
        originCoordinate: CLLocationCoordinate2D? = nil,
        routeColor: Color = .blue,
        selectedRoute: Binding<RouteItem?> = .constant(nil)
    ) {
        self.routes = routes
        self.originCode = originCode
        self.originCoordinate = originCoordinate
        self.routeColor = routeColor
        self._selectedRoute = selectedRoute
    }

    public var body: some View {
        Map(position: $position, selection: .constant(nil)) {
            // 1. Great-Circle Geodesic Route Polylines
            ForEach(routes) { route in
                let coords = GeodesicMath.greatCircleCoordinates(
                    from: route.originCoordinate,
                    to: route.destCoordinate,
                    numberOfPoints: 24
                )
                let isSelected = selectedRoute?.id == route.id

                MapPolyline(coordinates: coords)
                    .stroke(
                        isSelected ? Color.yellow : routeColor.opacity(0.75),
                        style: StrokeStyle(
                            lineWidth: isSelected ? 3.5 : 1.5,
                            lineCap: .round,
                            lineJoin: .round
                        )
                    )
            }

            // 2. Destination Node Annotations
            ForEach(routes) { route in
                Annotation(route.dest, coordinate: route.destCoordinate) {
                    Button {
                        withAnimation(.spring(response: 0.3, dampingFraction: 0.7)) {
                            selectedRoute = route
                        }
                    } label: {
                        VStack(spacing: 2) {
                            Text(route.dest)
                                .font(.system(size: 9, weight: .bold, design: .monospaced))
                                .padding(.horizontal, 4)
                                .padding(.vertical, 2)
                                .background(.black.opacity(0.75))
                                .foregroundStyle(.white)
                                .clipShape(RoundedRectangle(cornerRadius: 4))

                            Circle()
                                .fill(routeColor)
                                .frame(width: 6, height: 6)
                        }
                    }
                }
            }

            // 3. Origin Hub Concentric Bullseye Marker
            if let origin = originCode, let coord = originCoordinate {
                Annotation("★ \(origin)", coordinate: coord) {
                    ZStack {
                        Circle()
                            .stroke(Color.white, lineWidth: 3)
                            .fill(Color.accentColor)
                            .frame(width: 24, height: 24)
                            .shadow(color: .black.opacity(0.3), radius: 4)

                        Text("★")
                            .font(.system(size: 13, weight: .black))
                            .foregroundStyle(.white)
                    }
                }
            }
        }
        .mapStyle(.standard(elevation: .realistic, pointsOfInterest: .excludingAll))
        .mapControls {
            MapCompass()
            MapScaleView()
            MapPitchToggle()
        }
        .overlay(alignment: .bottom) {
            if let route = selectedRoute {
                RouteDetailCard(route: route) {
                    withAnimation { selectedRoute = nil }
                }
                .padding()
                .transition(.move(edge: .bottom).combined(with: .opacity))
            }
        }
        .onAppear {
            recenterMap()
        }
        .onChange(of: routes) {
            recenterMap()
        }
    }

    private func recenterMap() {
        if let origin = originCoordinate {
            position = .camera(
                MapCamera(
                    centerCoordinate: origin,
                    distance: 3_500_000,
                    heading: 0,
                    pitch: 15
                )
            )
        } else if let first = routes.first {
            position = .camera(
                MapCamera(
                    centerCoordinate: first.originCoordinate,
                    distance: 4_500_000,
                    heading: 0,
                    pitch: 10
                )
            )
        }
    }
}

/// Floating Route Inspection Card
struct RouteDetailCard: View {
    let route: RouteItem
    let onDismiss: () -> Void

    var body: some View {
        GlassCard {
            VStack(alignment: .leading, spacing: 10) {
                HStack {
                    VStack(alignment: .leading, spacing: 2) {
                        Text(route.label)
                            .font(.headline)
                            .fontWeight(.bold)
                        if let city = route.destCity {
                            Text(city)
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }
                    }
                    Spacer()
                    Button(action: onDismiss) {
                        Image(systemName: "xmark.circle.fill")
                            .foregroundStyle(.secondary)
                            .font(.title3)
                    }
                }

                Divider()

                HStack(spacing: 16) {
                    VStack(alignment: .leading) {
                        Text("PASSENGERS")
                            .font(.system(size: 9, weight: .semibold))
                            .foregroundStyle(.secondary)
                        Text(formatNumber(route.operationalPassengers))
                            .font(.subheadline)
                            .fontWeight(.bold)
                    }
                    VStack(alignment: .leading) {
                        Text("LOAD FACTOR")
                            .font(.system(size: 9, weight: .semibold))
                            .foregroundStyle(.secondary)
                        Text(String(format: "%.1f%%", route.loadFactorPct))
                            .font(.subheadline)
                            .fontWeight(.bold)
                            .foregroundStyle(.green)
                    }
                    VStack(alignment: .leading) {
                        Text("AVG FARE")
                            .font(.system(size: 9, weight: .semibold))
                            .foregroundStyle(.secondary)
                        if let fare = route.avgOdFare {
                            Text(String(format: "$%.0f", fare))
                                .font(.subheadline)
                                .fontWeight(.bold)
                        } else {
                            Text("—")
                                .font(.subheadline)
                        }
                    }
                    VStack(alignment: .leading) {
                        Text("STAGE")
                            .font(.system(size: 9, weight: .semibold))
                            .foregroundStyle(.secondary)
                        Text("\(Int(route.distanceMiles)) mi")
                            .font(.subheadline)
                            .fontWeight(.bold)
                    }
                }

                if let carriers = route.operatingCarriers {
                    HStack {
                        Text("Carriers:")
                            .font(.caption2)
                            .foregroundStyle(.secondary)
                        Text(carriers)
                            .font(.caption2)
                            .fontWeight(.medium)
                    }
                }
            }
        }
    }

    private func formatNumber(_ num: Int) -> String {
        let formatter = NumberFormatter()
        formatter.numberStyle = .decimal
        return formatter.string(from: NSNumber(value: num)) ?? "\(num)"
    }
}
