import SwiftUI
import Charts

public struct AirportDetailView: View {
    public let airport: Airport

    @State private var selectedYear: Int = 2024
    @State private var passengerOnly: Bool = true
    @State private var minDepartures: Int = 10

    @State private var kpis: AirportKPIs?
    @State private var routes: [OutboundRoute] = []
    @State private var timeline: [AirportTimelinePoint] = []
    @State private var carrierShares: [AirportCarrierShare] = []
    @State private var mapRoutes: [GeodesicRoute] = []
    @State private var isLoading: Bool = true
    @State private var selectedRoute: OutboundRoute?

    public init(airport: Airport) {
        self.airport = airport
    }

    public var body: some View {
        ScrollView {
            VStack(spacing: 16) {
                // Interactive Filter Bar
                FilterBarView(
                    selectedYear: $selectedYear,
                    passengerOnly: $passengerOnly,
                    minDepartures: $minDepartures,
                    onFilterChanged: {
                        Task { await loadData() }
                    }
                )
                .padding(.horizontal, 16)

                // Interactive Route Map
                VStack(alignment: .leading, spacing: 8) {
                    HStack {
                        Label("Route Network Atlas (\(selectedYear))", systemImage: "globe.americas.fill")
                            .font(.system(size: 14, weight: .bold))
                            .foregroundColor(AvDBTheme.accentCyan)
                        Spacer()
                        Text("\(mapRoutes.count) Direct Arcs")
                            .font(.system(size: 12, weight: .medium, design: .monospaced))
                            .foregroundColor(AvDBTheme.secondaryText)
                    }
                    .padding(.horizontal, 16)

                    GreatCircleMapView(routes: mapRoutes, focusAirport: airport)
                        .frame(height: 250)
                        .clipShape(RoundedRectangle(cornerRadius: 18, style: .continuous))
                        .overlay(
                            RoundedRectangle(cornerRadius: 18, style: .continuous)
                                .stroke(AvDBTheme.borderStroke, lineWidth: 1)
                        )
                        .padding(.horizontal, 16)
                }

                // High Density KPI Grid
                if let kpi = kpis {
                    VStack(alignment: .leading, spacing: 10) {
                        HStack {
                            Text("Operational Performance")
                                .font(.system(size: 14, weight: .bold))
                                .foregroundColor(AvDBTheme.primaryText)
                            Spacer()
                            Text("BTS BTS-T100 / DB1B")
                                .font(.system(size: 10, weight: .medium))
                                .foregroundColor(AvDBTheme.tertiaryText)
                        }
                        .padding(.horizontal, 16)

                        LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 12) {
                            KPICardView(
                                title: "Passengers",
                                value: formatVolume(kpi.totalPassengers),
                                subtitle: "\(kpi.totalDepartures.formatted()) departures",
                                icon: "person.2.fill",
                                accentColor: AvDBTheme.accentCyan
                            )
                            KPICardView(
                                title: "Load Factor",
                                value: String(format: "%.1f%%", kpi.loadFactor * 100),
                                subtitle: "\(formatVolume(kpi.totalSeats)) seats",
                                icon: "gauge.with.needle.fill",
                                accentColor: AvDBTheme.accentGreen
                            )
                            KPICardView(
                                title: "Direct Markets",
                                value: "\(kpi.nonstopDestinations)",
                                subtitle: "Nonstop destinations",
                                icon: "arrow.triangle.swap",
                                accentColor: AvDBTheme.accentBlue
                            )
                            KPICardView(
                                title: "Avg O&D Fare",
                                value: kpi.avgOdFare != nil ? String(format: "$%.0f", kpi.avgOdFare!) : "—",
                                subtitle: "DB1B 10% Ticket Survey",
                                icon: "dollarsign.circle.fill",
                                accentColor: AvDBTheme.accentAmber
                            )
                        }
                        .padding(.horizontal, 16)
                    }
                }

                // Longitudinal Passenger Growth Chart (1990 - 2025)
                if !timeline.isEmpty {
                    GlassCard(cornerRadius: 16) {
                        VStack(alignment: .leading, spacing: 12) {
                            HStack {
                                VStack(alignment: .leading, spacing: 2) {
                                    Text("Passenger Volume History")
                                        .font(.system(size: 14, weight: .bold))
                                        .foregroundColor(AvDBTheme.primaryText)
                                    Text("1990 — 2025 Annual Longitudinal Traffic")
                                        .font(.system(size: 11))
                                        .foregroundColor(AvDBTheme.secondaryText)
                                }
                                Spacer()
                                if let peak = timeline.max(by: { $0.totalPassengers < $1.totalPassengers }) {
                                    Text("Peak: \(peak.year)")
                                        .font(.system(size: 11, weight: .bold, design: .monospaced))
                                        .padding(.horizontal, 7)
                                        .padding(.vertical, 3)
                                        .background(AvDBTheme.accentCyan.opacity(0.15))
                                        .foregroundColor(AvDBTheme.accentCyan)
                                        .clipShape(Capsule())
                                }
                            }

                            Chart(timeline) { pt in
                                BarMark(
                                    x: .value("Year", pt.year),
                                    y: .value("Passengers", Double(pt.totalPassengers) / 1_000_000.0)
                                )
                                .foregroundStyle(
                                    pt.year == selectedYear ?
                                    LinearGradient(colors: [AvDBTheme.accentCyan, AvDBTheme.accentBlue], startPoint: .top, endPoint: .bottom) :
                                    LinearGradient(colors: [Color.white.opacity(0.35), Color.white.opacity(0.15)], startPoint: .top, endPoint: .bottom)
                                )
                                .cornerRadius(3)
                            }
                            .chartXAxis {
                                AxisMarks(values: [1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025]) { val in
                                    AxisValueLabel()
                                        .font(.system(size: 9, design: .monospaced))
                                        .foregroundStyle(Color.gray)
                                }
                            }
                            .chartYAxis {
                                AxisMarks(position: .trailing) { val in
                                    AxisValueLabel {
                                        if let p = val.as(Double.self) {
                                            Text(String(format: "%.0fM", p))
                                                .font(.system(size: 9, design: .monospaced))
                                                .foregroundStyle(Color.gray)
                                        }
                                    }
                                }
                            }
                            .frame(height: 160)
                        }
                    }
                    .padding(.horizontal, 16)
                }

                // Carrier Seat Share Breakdown
                if !carrierShares.isEmpty {
                    GlassCard(cornerRadius: 16) {
                        VStack(alignment: .leading, spacing: 12) {
                            HStack {
                                Text("Carrier Market Seat Share (\(selectedYear))")
                                    .font(.system(size: 14, weight: .bold))
                                    .foregroundColor(AvDBTheme.primaryText)
                                Spacer()
                                Text("Departing Capacity")
                                    .font(.system(size: 11))
                                    .foregroundColor(AvDBTheme.tertiaryText)
                            }

                            Chart(carrierShares.prefix(6)) { cs in
                                BarMark(
                                    x: .value("Share", cs.seatSharePct ?? 0.0),
                                    y: .value("Carrier", cs.uniqueCarrier)
                                )
                                .foregroundStyle(AvDBTheme.accentBlue)
                                .annotation(position: .trailing) {
                                    Text(String(format: "%.1f%%", cs.seatSharePct ?? 0.0))
                                        .font(.system(size: 10, weight: .bold, design: .monospaced))
                                        .foregroundColor(AvDBTheme.accentCyan)
                                        .padding(.leading, 4)
                                }
                                .cornerRadius(4)
                            }
                            .chartXAxis(.hidden)
                            .chartYAxis {
                                AxisMarks { val in
                                    AxisValueLabel()
                                        .font(.system(size: 11, weight: .bold, design: .monospaced))
                                        .foregroundStyle(Color.white)
                                }
                            }
                            .frame(height: CGFloat(min(carrierShares.count, 6) * 32))
                        }
                    }
                    .padding(.horizontal, 16)
                }

                // Outbound Routes Section
                VStack(alignment: .leading, spacing: 12) {
                    HStack {
                        Text("Top Nonstop Destinations (\(selectedYear))")
                            .font(.system(size: 14, weight: .bold))
                            .foregroundColor(AvDBTheme.primaryText)
                        Spacer()
                        Text("\(routes.count) routes")
                            .font(.system(size: 12))
                            .foregroundColor(AvDBTheme.secondaryText)
                    }
                    .padding(.horizontal, 16)

                    VStack(spacing: 8) {
                        ForEach(routes.prefix(30)) { r in
                            GlassCard(cornerRadius: 12) {
                                HStack(spacing: 12) {
                                    VStack(alignment: .leading, spacing: 3) {
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

                                        Text(String(format: "%.0f mi • %d dep • %d pax", r.distanceMiles, r.departures, r.passengers))
                                            .font(.system(size: 11))
                                            .foregroundColor(AvDBTheme.secondaryText)
                                    }

                                    Spacer()

                                    VStack(alignment: .trailing, spacing: 2) {
                                        if let fare = r.avgOdFare {
                                            Text(String(format: "$%.0f", fare))
                                                .font(.system(size: 14, weight: .bold, design: .rounded))
                                                .foregroundColor(AvDBTheme.accentAmber)
                                        }
                                        Text(String(format: "%.0f%% LF", r.loadFactor * 100))
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
            .padding(.vertical, 12)
        }
        .navigationTitle(airport.iata)
        .navigationBarTitleDisplayMode(.inline)
        .avdbCanvas()
        .task {
            await loadData()
        }
    }

    private func loadData() async {
        self.isLoading = true
        async let kpiTask = APIService.shared.getAirportKPIs(
            iata: airport.iata,
            year: selectedYear,
            passengerOnly: passengerOnly,
            minDepartures: minDepartures
        )
        async let routeTask = APIService.shared.getOutboundRoutes(
            iata: airport.iata,
            year: selectedYear,
            passengerOnly: passengerOnly,
            minDepartures: minDepartures
        )
        async let timelineTask = APIService.shared.getAirportTimeline(
            iata: airport.iata,
            passengerOnly: passengerOnly,
            minDepartures: minDepartures
        )
        async let carrierTask = APIService.shared.getAirportCarriers(
            iata: airport.iata,
            year: selectedYear,
            passengerOnly: passengerOnly
        )

        self.kpis = await kpiTask
        self.routes = (await routeTask).filter { $0.destination != $0.origin }
        self.timeline = await timelineTask
        self.carrierShares = await carrierTask

        // Build geodesic map routes directly from OutboundRoute GPS coordinates
        var builtMapRoutes: [GeodesicRoute] = []
        for r in self.routes {
            let oLat = r.originLat ?? airport.latitude
            let oLon = r.originLon ?? airport.longitude
            if let dLat = r.destLat, let dLon = r.destLon {
                builtMapRoutes.append(GeodesicRoute(
                    originIATA: r.origin,
                    destIATA: r.destination,
                    carrier: r.carrier,
                    originCoord: CoordinatePoint(latitude: oLat, longitude: oLon),
                    destCoord: CoordinatePoint(latitude: dLat, longitude: dLon),
                    passengerVolume: r.passengers,
                    avgFare: r.avgOdFare
                ))
            }
        }
        self.mapRoutes = builtMapRoutes
        self.isLoading = false
    }

    private func formatVolume(_ n: Int) -> String {
        if n >= 1_000_000 {
            return String(format: "%.1fM", Double(n) / 1_000_000.0)
        } else if n >= 1_000 {
            return String(format: "%.0fK", Double(n) / 1_000.0)
        }
        return "\(n)"
    }
}
