import SwiftUI
import CoreLocation

/// Airports Lens: Catchment Indicators, Top KPI Cards, Native Route Map & Outbound Routes
public struct AirportsView: View {
    @StateObject private var settings = AppSettings.shared

    @State private var availableAirports: [Airport] = []
    @State private var selectedAirport: Airport?
    @State private var searchText: String = ""
    @State private var kpis: AirportKPIs = .empty
    @State private var routes: [RouteItem] = []
    @State private var catchment: CatchmentInfo?
    @State private var selectedRoute: RouteItem?
    @State private var isLoading: Bool = false
    @State private var errorMessage: String?

    // Filter controls
    @State private var minDepartures: Int = 10
    @State private var showMapFullScreen: Bool = false

    public init() {}

    private var filteredAirports: [Airport] {
        if searchText.isEmpty {
            return availableAirports
        }
        return availableAirports.filter {
            $0.airportCode.localizedCaseInsensitiveContains(searchText) ||
            $0.city.localizedCaseInsensitiveContains(searchText) ||
            $0.airportName.localizedCaseInsensitiveContains(searchText)
        }
    }

    public var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 20) {
                    // 1. Origin Airport Header & Catchment Badge
                    originSelectorSection

                    if isLoading {
                        ProgressView("Loading Aviation Intelligence...")
                            .padding(.top, 40)
                    } else {
                        // 2. Catchment Market Banner if applicable
                        if let catchment = catchment {
                            catchmentBanner(catchment)
                        }

                        // 3. Top KPI Metric Grid
                        kpiGridSection

                        // 4. Native 120Hz ProMotion Great-Circle Route Map
                        routeMapSection

                        // 5. Outbound Destinations Table
                        destinationsListSection
                    }
                }
                .padding(.horizontal, 16)
                .padding(.bottom, 32)
            }
            .navigationTitle("Airports")
            .navigationBarTitleDisplayMode(.large)
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Picker("Year", selection: $settings.reportingYear) {
                        Text("2024").tag(2024)
                        Text("2023").tag(2023)
                        Text("2022").tag(2022)
                    }
                    .pickerStyle(.menu)
                    .onChange(of: settings.reportingYear) {
                        Task { await loadData() }
                    }
                }
            }
            .task {
                await loadAirportsCatalog()
            }
        }
    }

    // MARK: - Subviews

    private var originSelectorSection: some View {
        GlassCard {
            VStack(alignment: .leading, spacing: 12) {
                Text("ORIGIN AIRPORT")
                    .font(.caption)
                    .fontWeight(.bold)
                    .foregroundStyle(.secondary)

                Menu {
                    ForEach(filteredAirports.prefix(30)) { apt in
                        Button {
                            selectedAirport = apt
                            Task { await loadData() }
                        } label: {
                            HStack {
                                Text("\(apt.airportCode) — \(apt.city)")
                                if apt.airportCode == selectedAirport?.airportCode {
                                    Image(systemName: "checkmark")
                                }
                            }
                        }
                    }
                } label: {
                    HStack {
                        Image(systemName: "airplane.departure")
                            .foregroundStyle(.blue)
                        VStack(alignment: .leading, spacing: 2) {
                            Text(selectedAirport?.airportCode ?? "Select Airport")
                                .font(.title3)
                                .fontWeight(.bold)
                                .foregroundStyle(.primary)
                            Text(selectedAirport?.airportName ?? "Tap to choose origin")
                                .font(.caption)
                                .foregroundStyle(.secondary)
                                .lineLimit(1)
                        }
                        Spacer()
                        Image(systemName: "chevron.up.chevron.down")
                            .foregroundStyle(.secondary)
                    }
                }
            }
        }
    }

    private func catchmentBanner(_ catchment: CatchmentInfo) -> some View {
        HStack(spacing: 12) {
            Image(systemName: "circle.grid.cross.fill")
                .font(.title2)
                .foregroundStyle(.indigo)
            VStack(alignment: .leading, spacing: 2) {
                Text("Metro Catchment Market: \(catchment.marketName)")
                    .font(.subheadline)
                    .fontWeight(.bold)
                Text("Encompasses: \(catchment.memberAirports.joined(separator: ", "))")
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }
            Spacer()
        }
        .padding(14)
        .background(Color.indigo.opacity(0.12), in: RoundedRectangle(cornerRadius: 14))
    }

    private var kpiGridSection: some View {
        LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 12) {
            KPICardView(
                title: "DESTINATIONS",
                value: "\(kpis.directDestinations)",
                subtitle: "Direct Nonstop",
                iconName: "point.3.connected.trianglepath.dotted",
                accentColor: .blue
            )
            KPICardView(
                title: "LOAD FACTOR",
                value: String(format: "%.1f%%", kpis.loadFactorPct),
                subtitle: "Passenger / Seat Ratio",
                iconName: "percent",
                accentColor: .green
            )
            KPICardView(
                title: "DEPARTURES",
                value: formatCompact(kpis.totalDepartures),
                subtitle: "Performed Flights",
                iconName: "airplane.departure",
                accentColor: .orange
            )
            KPICardView(
                title: "PASSENGERS",
                value: formatCompact(kpis.totalPassengers),
                subtitle: "\(formatCompact(kpis.totalSeats)) Seats",
                iconName: "person.2.fill",
                accentColor: .cyan
            )
            KPICardView(
                title: "AVG FARE",
                value: kpis.avgOdFare != nil ? String(format: "$%.0f", kpis.avgOdFare!) : "—",
                subtitle: "DB1B Sample O&D",
                iconName: "dollarsign.circle.fill",
                accentColor: .purple
            )
            KPICardView(
                title: "LEAD CARRIER",
                value: kpis.leadingCarrier,
                subtitle: "Capacity Market Leader",
                iconName: "crown.fill",
                accentColor: .yellow
            )
        }
    }

    private var routeMapSection: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Text("ROUTE NETWORK MAP")
                    .font(.caption)
                    .fontWeight(.bold)
                    .foregroundStyle(.secondary)
                Spacer()
                Text("\(routes.count) Nonstop Markets")
                    .font(.caption2)
                    .foregroundStyle(.secondary)
            }

            RouteMapView(
                routes: routes,
                originCode: selectedAirport?.airportCode,
                originCoordinate: selectedAirport?.coordinate,
                routeColor: .blue,
                selectedRoute: $selectedRoute
            )
            .frame(height: 300)
            .clipShape(RoundedRectangle(cornerRadius: 18))
            .overlay(
                RoundedRectangle(cornerRadius: 18)
                    .stroke(Color.white.opacity(0.15), lineWidth: 1)
            )
        }
    }

    private var destinationsListSection: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Text("TOP OUTBOUND MARKETS")
                    .font(.caption)
                    .fontWeight(.bold)
                    .foregroundStyle(.secondary)
                Spacer()
            }

            ForEach(routes.prefix(15)) { route in
                Button {
                    withAnimation { selectedRoute = route }
                } label: {
                    GlassCard {
                        HStack {
                            VStack(alignment: .leading, spacing: 4) {
                                HStack(spacing: 6) {
                                    Text(route.dest)
                                        .font(.headline)
                                        .fontWeight(.bold)
                                        .foregroundStyle(.primary)
                                    if let city = route.destCity {
                                        Text("(\(city))")
                                            .font(.caption)
                                            .foregroundStyle(.secondary)
                                    }
                                }
                                HStack(spacing: 8) {
                                    Text("\(Int(route.distanceMiles)) mi")
                                        .font(.caption2)
                                        .foregroundStyle(.secondary)
                                    Text("•")
                                        .foregroundStyle(.secondary)
                                    Text("\(Int(route.avgGaugeSeats)) seats/dep")
                                        .font(.caption2)
                                        .foregroundStyle(.secondary)
                                }
                            }
                            Spacer()
                            VStack(alignment: .trailing, spacing: 4) {
                                Text(formatCompact(route.operationalPassengers) + " pax")
                                    .font(.subheadline)
                                    .fontWeight(.bold)
                                    .foregroundStyle(.primary)
                                Text(String(format: "%.1f%% LF", route.loadFactorPct))
                                    .font(.caption2)
                                    .fontWeight(.semibold)
                                    .foregroundStyle(.green)
                            }
                        }
                    }
                }
                .buttonStyle(.plain)
            }
        }
    }

    // MARK: - Data Loading

    private func loadAirportsCatalog() async {
        isLoading = true
        defer { isLoading = false }
        do {
            let list = try await APIService.shared.fetchAirports(baseURL: settings.activeApiBaseURL)
            availableAirports = list
            if selectedAirport == nil {
                selectedAirport = list.first(where: { $0.airportCode == "SEA" }) ?? list.first
            }
            await loadData()
        } catch {
            errorMessage = error.localizedDescription
        }
    }

    private func loadData() async {
        guard let apt = selectedAirport else { return }
        isLoading = true
        defer { isLoading = false }
        let year = settings.reportingYear
        let baseURL = settings.activeApiBaseURL

        async let kpiTask = APIService.shared.fetchAirportKPIs(code: apt.airportCode, year: year, baseURL: baseURL)
        async let routesTask = APIService.shared.fetchAirportRoutes(code: apt.airportCode, year: year, minDepartures: minDepartures, baseURL: baseURL)
        async let catchmentTask = APIService.shared.fetchCatchment(code: apt.airportCode, baseURL: baseURL)

        do {
            let (kpiRes, routesRes, catchmentRes) = try await (kpiTask, routesTask, catchmentTask)
            self.kpis = kpiRes
            self.routes = routesRes
            self.catchment = catchmentRes
        } catch {
            self.errorMessage = error.localizedDescription
        }
    }

    private func formatCompact(_ number: Int) -> String {
        if number >= 1_000_000 {
            return String(format: "%.1fM", Double(number) / 1_000_000.0)
        } else if number >= 1_000 {
            return String(format: "%.1fK", Double(number) / 1_000.0)
        }
        return "\(number)"
    }
}
