import SwiftUI
import UniformTypeIdentifiers

/// Personal Flighty Log Lens: Native File Picker (.fileImporter), Subfleet Breakdown & Personal Route Map
public struct FlightyView: View {
    @State private var records: [FlightyRecord] = []
    @State private var summary: FlightySummary = .empty
    @State private var subfleets: [FlightySubfleetGroup] = []
    @State private var personalRoutes: [RouteItem] = []
    @State private var selectedRoute: RouteItem?

    @State private var isShowingFileImporter: Bool = false
    @State private var selectedTab: Int = 0 // 0: Subfleets, 1: Route Map, 2: Flight Log
    @State private var statusMessage: String?
    @State private var isLoading: Bool = false

    public init() {}

    public var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 20) {
                    // 1. Flighty Import Header Card
                    importHeaderCard

                    if !records.isEmpty {
                        // 2. Personal Lifetime Flight Metrics
                        kpiGridSection

                        // 3. Tab Segment Control
                        Picker("View Mode", selection: $selectedTab) {
                            Text("Subfleets").tag(0)
                            Text("Personal Map").tag(1)
                            Text("Log (\(records.count))").tag(2)
                        }
                        .pickerStyle(.segmented)

                        // 4. Tab Content
                        if selectedTab == 0 {
                            subfleetBreakdownSection
                        } else if selectedTab == 1 {
                            personalMapSection
                        } else {
                            flightLogHistorySection
                        }
                    } else {
                        emptyStateCard
                    }
                }
                .padding(.horizontal, 16)
                .padding(.bottom, 32)
            }
            .navigationTitle("Flighty Passport")
            .navigationBarTitleDisplayMode(.large)
            .fileImporter(
                isPresented: $isShowingFileImporter,
                allowedContentTypes: [.commaSeparatedText, .plainText],
                allowsMultipleSelection: false
            ) { result in
                handleFileSelection(result)
            }
        }
    }

    // MARK: - Subviews

    private var importHeaderCard: some View {
        GlassCard {
            HStack(spacing: 14) {
                Image(systemName: "airplane.circle.fill")
                    .font(.system(size: 38))
                    .foregroundStyle(.blue)

                VStack(alignment: .leading, spacing: 2) {
                    Text("Flighty Log Integration")
                        .font(.headline)
                        .fontWeight(.bold)
                    Text(records.isEmpty ? "Import your Flighty CSV export" : "\(records.count) flights loaded")
                        .font(.caption)
                        .foregroundStyle(.secondary)
                }

                Spacer()

                Button {
                    isShowingFileImporter = true
                } label: {
                    Label("Import", systemName: "square.and.arrow.down")
                        .font(.subheadline)
                        .fontWeight(.semibold)
                }
                .buttonStyle(.borderedProminent)
            }
        }
    }

    private var emptyStateCard: some View {
        GlassCard {
            VStack(spacing: 16) {
                Image(systemName: "doc.text.magnifyingglass")
                    .font(.system(size: 48))
                    .foregroundStyle(.secondary)

                VStack(spacing: 4) {
                    Text("No Flights Imported Yet")
                        .font(.headline)
                        .fontWeight(.bold)
                    Text("Export your flight history from Flighty (Settings ➔ Export Flights ➔ CSV) and tap Import above.")
                        .font(.caption)
                        .foregroundStyle(.secondary)
                        .multilineTextAlignment(.center)
                }

                Button("Load Demo Flight Log (18 Flights)") {
                    loadDemoFlightData()
                }
                .font(.footnote)
                .foregroundStyle(.blue)
            }
            .padding(.vertical, 24)
            .frame(maxWidth: .infinity)
        }
    }

    private var kpiGridSection: some View {
        LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 12) {
            KPICardView(
                title: "TOTAL FLIGHTS",
                value: "\(summary.totalFlights)",
                subtitle: "Logged Itineraries",
                iconName: "ticket.fill",
                accentColor: .blue
            )
            KPICardView(
                title: "TOTAL MILES",
                value: formatCompact(Int(summary.totalMiles)),
                subtitle: "Air Statute Miles",
                iconName: "globe.americas.fill",
                accentColor: .purple
            )
            KPICardView(
                title: "AIRPORTS",
                value: "\(summary.uniqueAirports)",
                subtitle: "Visited Terminals",
                iconName: "building.2.fill",
                accentColor: .cyan
            )
            KPICardView(
                title: "TOP AIRCRAFT",
                value: summary.topAircraftType,
                subtitle: "Most Frequent Gauge",
                iconName: "airplane",
                accentColor: .orange
            )
        }
    }

    private var subfleetBreakdownSection: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("AIRCRAFT & SUBFLEET ALLOCATION")
                .font(.caption)
                .fontWeight(.bold)
                .foregroundStyle(.secondary)

            ForEach(subfleets) { group in
                GlassCard {
                    VStack(alignment: .leading, spacing: 8) {
                        HStack {
                            Text(group.aircraftType)
                                .font(.subheadline)
                                .fontWeight(.bold)
                            Spacer()
                            Text("\(group.flightCount) flights")
                                .font(.subheadline)
                                .fontWeight(.semibold)
                                .foregroundStyle(.blue)
                        }

                        // Progress Bar
                        GeometryReader { geo in
                            ZStack(alignment: .leading) {
                                Capsule()
                                    .fill(Color.secondary.opacity(0.2))
                                    .frame(height: 6)

                                Capsule()
                                    .fill(Color.blue)
                                    .frame(width: max(geo.size.width * CGFloat(group.percentage / 100.0), 4), height: 6)
                            }
                        }
                        .frame(height: 6)

                        HStack {
                            Text(String(format: "%.1f%% of your flights", group.percentage))
                                .font(.caption2)
                                .foregroundStyle(.secondary)
                            Spacer()
                            Text("\(Int(group.totalMiles)) miles")
                                .font(.caption2)
                                .foregroundStyle(.secondary)
                        }
                    }
                }
            }
        }
    }

    private var personalMapSection: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Text("PERSONAL ROUTE MAP")
                    .font(.caption)
                    .fontWeight(.bold)
                    .foregroundStyle(.secondary)
                Spacer()
                Text("\(personalRoutes.count) Unique Routes")
                    .font(.caption2)
                    .foregroundStyle(.secondary)
            }

            RouteMapView(
                routes: personalRoutes,
                routeColor: .cyan,
                selectedRoute: $selectedRoute
            )
            .frame(height: 340)
            .clipShape(RoundedRectangle(cornerRadius: 18))
            .overlay(
                RoundedRectangle(cornerRadius: 18)
                    .stroke(Color.white.opacity(0.15), lineWidth: 1)
            )
        }
    }

    private var flightLogHistorySection: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text("FLIGHT LOG HISTORY")
                .font(.caption)
                .fontWeight(.bold)
                .foregroundStyle(.secondary)

            ForEach(records) { r in
                GlassCard {
                    HStack {
                        VStack(alignment: .leading, spacing: 2) {
                            HStack(spacing: 8) {
                                Text("\(r.origin) ➔ \(r.destination)")
                                    .font(.headline)
                                    .fontWeight(.bold)
                                Text(r.flightNumber)
                                    .font(.caption)
                                    .padding(.horizontal, 6)
                                    .padding(.vertical, 2)
                                    .background(Color.blue.opacity(0.15))
                                    .clipShape(RoundedRectangle(cornerRadius: 4))
                            }
                            Text("\(r.airline) • \(r.aircraftType)")
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }
                        Spacer()
                        VStack(alignment: .trailing, spacing: 2) {
                            Text(r.date)
                                .font(.caption)
                                .fontWeight(.semibold)
                            if !r.seat.isEmpty {
                                Text("Seat \(r.seat)")
                                    .font(.caption2)
                                    .foregroundStyle(.secondary)
                            }
                        }
                    }
                }
            }
        }
    }

    // MARK: - Handlers

    private func handleFileSelection(_ result: Result<[URL], Error>) {
        switch result {
        case .success(let urls):
            guard let url = urls.first else { return }
            guard url.startAccessingSecurityScopedResource() else {
                statusMessage = "Permission denied accessing CSV file."
                return
            }
            defer { url.stopAccessingSecurityScopedResource() }

            do {
                let parsed = try FlightyParser.parseCSV(from: url)
                processRecords(parsed)
            } catch {
                statusMessage = "CSV parse error: \(error.localizedDescription)"
            }
        case .failure(let err):
            statusMessage = err.localizedDescription
        }
    }

    private func processRecords(_ parsed: [FlightyRecord]) {
        self.records = parsed
        self.summary = FlightyParser.computeSummary(from: parsed)
        self.subfleets = FlightyParser.computeSubfleetBreakdown(from: parsed)

        // Build route items with approximate coordinates for personal map
        var routesList: [RouteItem] = []
        let airportCoords: [String: (lat: Double, lon: Double)] = [
            "SEA": (47.4502, -122.3088),
            "ORD": (41.9742, -87.9073),
            "SFO": (37.6213, -122.3790),
            "LAX": (33.9416, -118.4085),
            "JFK": (40.6413, -73.7781),
            "BOS": (42.3656, -71.0096),
            "DFW": (32.8998, -97.0403),
            "ATL": (33.6407, -84.4277),
            "DEN": (39.8561, -104.6737),
            "LHR": (51.4700, -0.4543),
            "CDG": (49.0097, 2.5479),
            "HND": (35.5494, 139.7798)
        ]

        var seenKeys = Set<String>()
        for r in parsed {
            if seenKeys.contains(r.routeKey) { continue }
            seenKeys.insert(r.routeKey)

            let o = airportCoords[r.origin] ?? (37.0, -95.0)
            let d = airportCoords[r.destination] ?? (38.0, -96.0)

            routesList.append(
                RouteItem(
                    origin: r.origin,
                    originName: nil,
                    originCity: r.origin,
                    originLat: o.lat,
                    originLon: o.lon,
                    dest: r.destination,
                    destName: nil,
                    destCity: r.destination,
                    destState: nil,
                    destCountry: nil,
                    destLat: d.lat,
                    destLon: d.lon,
                    departuresPerformed: 1,
                    totalSeats: 160,
                    operationalPassengers: 140,
                    loadFactorPct: 87.5,
                    avgGaugeSeats: 160.0,
                    distanceMiles: r.distanceMiles > 0 ? r.distanceMiles : 1200.0,
                    avgOdFare: nil,
                    operatingCarriers: r.airline
                )
            )
        }
        self.personalRoutes = routesList
    }

    private func loadDemoFlightData() {
        let sample = [
            FlightyRecord(date: "2024-06-15", flightNumber: "AS 124", airline: "Alaska Airlines", origin: "SEA", destination: "ORD", aircraftType: "Boeing 737-900ER", seat: "3A", distanceMiles: 1720),
            FlightyRecord(date: "2024-06-20", flightNumber: "UA 412", airline: "United Airlines", origin: "ORD", destination: "BOS", aircraftType: "Airbus A321neo", seat: "12C", distanceMiles: 867),
            FlightyRecord(date: "2024-07-02", flightNumber: "DL 89", airline: "Delta Air Lines", origin: "BOS", destination: "ATL", aircraftType: "Airbus A321-200", seat: "2D", distanceMiles: 946),
            FlightyRecord(date: "2024-07-08", flightNumber: "DL 1184", airline: "Delta Air Lines", origin: "ATL", destination: "SEA", aircraftType: "Boeing 737-900ER", seat: "10B", distanceMiles: 2182),
            FlightyRecord(date: "2024-08-11", flightNumber: "AS 340", airline: "Alaska Airlines", origin: "SEA", destination: "SFO", aircraftType: "Boeing 737 MAX 8", seat: "1F", distanceMiles: 679),
            FlightyRecord(date: "2024-08-14", flightNumber: "UA 2201", airline: "United Airlines", origin: "SFO", destination: "DEN", aircraftType: "Boeing 777-200", seat: "7L", distanceMiles: 967),
            FlightyRecord(date: "2024-08-18", flightNumber: "UA 384", airline: "United Airlines", origin: "DEN", destination: "SEA", aircraftType: "Boeing 737-800", seat: "21F", distanceMiles: 1024),
        ]
        processRecords(sample)
    }

    private func formatCompact(_ number: Int) -> String {
        let formatter = NumberFormatter()
        formatter.numberStyle = .decimal
        return formatter.string(from: NSNumber(value: number)) ?? "\(number)"
    }
}
