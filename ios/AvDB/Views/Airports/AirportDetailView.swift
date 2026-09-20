import SwiftUI

public struct AirportDetailView: View {
    public let airport: Airport
    @State private var kpis: AirportKPIs?
    @State private var routes: [OutboundRoute] = []
    @State private var mapRoutes: [GeodesicRoute] = []
    @State private var isLoading: Bool = true

    public init(airport: Airport) {
        self.airport = airport
    }

    public var body: some View {
        ScrollView {
            VStack(spacing: 20) {
                // Interactive Map Section
                VStack(alignment: .leading, spacing: 10) {
                    HStack {
                        Label("Great-Circle Route Network", systemImage: "globe.americas.fill")
                            .font(.system(size: 14, weight: .bold))
                            .foregroundColor(AvDBTheme.accentCyan)
                        Spacer()
                        Text("\(routes.count) Nonstop Arcs")
                            .font(.system(size: 12, weight: .medium))
                            .foregroundColor(AvDBTheme.secondaryText)
                    }
                    .padding(.horizontal, 16)

                    GreatCircleMapView(routes: mapRoutes, focusAirport: airport)
                        .frame(height: 260)
                        .clipShape(RoundedRectangle(cornerRadius: 18, style: .continuous))
                        .overlay(
                            RoundedRectangle(cornerRadius: 18, style: .continuous)
                                .stroke(AvDBTheme.borderStroke, lineWidth: 1)
                        )
                        .padding(.horizontal, 16)
                }

                // High Density KPI Grid
                if let kpi = kpis {
                    VStack(alignment: .leading, spacing: 12) {
                        Text("Operational Metrics")
                            .font(.system(size: 14, weight: .bold))
                            .foregroundColor(AvDBTheme.primaryText)
                            .padding(.horizontal, 16)

                        LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 12) {
                            KPICardView(
                                title: "Passengers",
                                value: "\(Double(kpi.totalPassengers) / 1_000_000.0, specifier: "%.1f")M",
                                subtitle: "\(kpi.totalDepartures.formatted()) departures",
                                icon: "person.2.fill",
                                accentColor: AvDBTheme.accentCyan
                            )
                            KPICardView(
                                title: "Load Factor",
                                value: "\(kpi.loadFactor * 100, specifier: "%.1f")%",
                                subtitle: "\(kpi.totalSeats.formatted()) seats",
                                icon: "gauge.with.needle.fill",
                                accentColor: AvDBTheme.accentGreen
                            )
                            KPICardView(
                                title: "Avg O&D Fare",
                                value: kpi.avgOdFare != nil ? "$\(kpi.avgOdFare!, specifier: "%.0f")" : "—",
                                subtitle: "BTS DB1B Survey",
                                icon: "dollarsign.circle.fill",
                                accentColor: AvDBTheme.accentAmber
                            )
                            KPICardView(
                                title: "Lead Carrier",
                                value: kpi.leadingCarrier,
                                subtitle: "\(kpi.leadingCarrierShare * 100, specifier: "%.1f")% seat share",
                                icon: "airplane.circle.fill",
                                accentColor: AvDBTheme.accentBlue
                            )
                        }
                        .padding(.horizontal, 16)
                    }
                }

                // Outbound Routes Section
                VStack(alignment: .leading, spacing: 12) {
                    Text("Top Outbound Markets")
                        .font(.system(size: 14, weight: .bold))
                        .foregroundColor(AvDBTheme.primaryText)
                        .padding(.horizontal, 16)

                    VStack(spacing: 8) {
                        ForEach(routes) { r in
                            GlassCard(cornerRadius: 12) {
                                HStack(spacing: 12) {
                                    VStack(alignment: .leading, spacing: 2) {
                                        HStack(spacing: 6) {
                                            Text(r.origin)
                                                .font(.system(size: 14, weight: .bold, design: .monospaced))
                                                .foregroundColor(AvDBTheme.accentCyan)
                                            Image(systemName: "arrow.right")
                                                .font(.system(size: 10, weight: .bold))
                                                .foregroundColor(AvDBTheme.tertiaryText)
                                            Text(r.destination)
                                                .font(.system(size: 14, weight: .bold, design: .monospaced))
                                                .foregroundColor(AvDBTheme.primaryText)

                                            Text(r.carrier)
                                                .font(.system(size: 10, weight: .bold))
                                                .padding(.horizontal, 5)
                                                .padding(.vertical, 2)
                                                .background(AvDBTheme.surfaceElevated)
                                                .foregroundColor(AvDBTheme.accentBlue)
                                                .clipShape(RoundedRectangle(cornerRadius: 4))
                                        }

                                        Text("\(r.distanceMiles, specifier: "%.0f") mi • \(r.departures.formatted()) departures")
                                            .font(.system(size: 12))
                                            .foregroundColor(AvDBTheme.secondaryText)
                                    }

                                    Spacer()

                                    VStack(alignment: .trailing, spacing: 2) {
                                        if let fare = r.avgOdFare {
                                            Text("$\(fare, specifier: "%.0f")")
                                                .font(.system(size: 14, weight: .bold, design: .rounded))
                                                .foregroundColor(AvDBTheme.accentAmber)
                                        }
                                        Text("\(r.loadFactor * 100, specifier: "%.0f")% LF")
                                            .font(.system(size: 11, weight: .semibold))
                                            .foregroundColor(AvDBTheme.accentGreen)
                                    }
                                }
                            }
                        }
                    }
                    .padding(.horizontal, 16)
                }
            }
            .padding(.vertical, 16)
        }
        .navigationTitle(airport.iata)
        .navigationBarTitleDisplayMode(.inline)
        .avdbCanvas()
        .task {
            async let kpiTask = APIService.shared.getAirportKPIs(iata: airport.iata)
            async let routeTask = APIService.shared.getOutboundRoutes(iata: airport.iata)

            self.kpis = await kpiTask
            self.routes = await routeTask

            // Build map routes with coordinates
            let allAirports = await APIService.shared.getAirports()
            let airportMap = Dictionary(uniqueKeysWithValues: allAirports.map { ($0.iata, $0) })

            var builtMapRoutes: [GeodesicRoute] = []
            for r in self.routes {
                if let destAirport = airportMap[r.destination] {
                    builtMapRoutes.append(GeodesicRoute(
                        originIATA: airport.iata,
                        destIATA: destAirport.iata,
                        carrier: r.carrier,
                        originCoord: CoordinatePoint(latitude: airport.latitude, longitude: airport.longitude),
                        destCoord: CoordinatePoint(latitude: destAirport.latitude, longitude: destAirport.longitude),
                        passengerVolume: r.passengers,
                        avgFare: r.avgOdFare
                    ))
                }
            }
            self.mapRoutes = builtMapRoutes
            self.isLoading = false
        }
    }
}

