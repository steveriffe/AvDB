import SwiftUI

/// Airlines Lens: Carrier Hub Network, Yield Curve Economics & Nationwide System Map
public struct AirlinesView: View {
    @StateObject private var settings = AppSettings.shared

    @State private var selectedCarrier: AirlineCarrier = AirlineCarrier.majorCarriers[0] // AS
    @State private var kpis: AirlineKPIs = .empty
    @State private var network: AirlineNetworkResponse?
    @State private var yieldCurve: [YieldCurvePoint] = []
    @State private var selectedRoute: RouteItem?
    @State private var isLoading: Bool = false
    @State private var errorMessage: String?

    public init() {}

    public var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 20) {
                    // 1. Airline Carrier Picker Bar
                    carrierPickerSection

                    if isLoading {
                        ProgressView("Loading Network Atlas...")
                            .padding(.top, 40)
                    } else {
                        // 2. High Density Performance KPIs
                        kpisSection

                        // 3. Nationwide Route Network Map
                        if let network = network {
                            airlineMapSection(network)
                        }

                        // 4. Primary Hub Operations
                        if let network = network, !network.hubs.isEmpty {
                            hubsSection(network.hubs)
                        }

                        // 5. Stage Length vs Yield Economics
                        if !yieldCurve.isEmpty {
                            yieldCurveSection
                        }
                    }
                }
                .padding(.horizontal, 16)
                .padding(.bottom, 32)
            }
            .navigationTitle("Airlines")
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
                        Task { await loadAirlineData() }
                    }
                }
            }
            .task {
                await loadAirlineData()
            }
        }
    }

    // MARK: - Subviews

    private var carrierPickerSection: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 10) {
                ForEach(AirlineCarrier.majorCarriers) { carrier in
                    let isSelected = carrier.code == selectedCarrier.code
                    Button {
                        selectedCarrier = carrier
                        Task { await loadAirlineData() }
                    } label: {
                        HStack(spacing: 6) {
                            Circle()
                                .fill(Color(hex: carrier.signatureColorHex))
                                .frame(width: 10, height: 10)
                            Text(carrier.code)
                                .fontWeight(.bold)
                            Text(carrier.name.components(separatedBy: " ").first ?? "")
                                .font(.caption)
                        }
                        .padding(.horizontal, 12)
                        .padding(.vertical, 8)
                        .background(
                            isSelected ? Color(hex: carrier.signatureColorHex).opacity(0.2) : Color.clear,
                            in: Capsule()
                        )
                        .overlay(
                            Capsule().stroke(
                                isSelected ? Color(hex: carrier.signatureColorHex) : Color.secondary.opacity(0.3),
                                lineWidth: isSelected ? 2 : 1
                            )
                        )
                    }
                    .buttonStyle(.plain)
                }
            }
            .padding(.vertical, 4)
        }
    }

    private var kpisSection: some View {
        LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 12) {
            KPICardView(
                title: "ACTIVE ROUTES",
                value: "\(kpis.activeRoutes)",
                subtitle: "Nationwide City-Pairs",
                iconName: "point.filled.topleft.down.curvedto.point.bottomright.up",
                accentColor: Color(hex: selectedCarrier.signatureColorHex)
            )
            KPICardView(
                title: "SYSTEM LOAD FACTOR",
                value: String(format: "%.1f%%", kpis.systemLoadFactor),
                subtitle: "RPM / ASM Utilization",
                iconName: "percent",
                accentColor: .green
            )
            KPICardView(
                title: "ASM (CAPACITY)",
                value: formatCompactBillions(kpis.totalAsm),
                subtitle: "Available Seat Miles",
                iconName: "airplane",
                accentColor: .blue
            )
            KPICardView(
                title: "RPM (TRAFFIC)",
                value: formatCompactBillions(kpis.totalRpm),
                subtitle: "Rev Passenger Miles",
                iconName: "person.3.fill",
                accentColor: .indigo
            )
            KPICardView(
                title: "AVG NETWORK FARE",
                value: String(format: "$%.0f", kpis.avgNetworkFare),
                subtitle: "Across All Markets",
                iconName: "dollarsign.circle.fill",
                accentColor: .purple
            )
            KPICardView(
                title: "AVG YIELD / MILE",
                value: String(format: "%.2f¢", kpis.avgYieldPerMile * 100.0),
                subtitle: "Passenger Rev / RPM",
                iconName: "chart.line.uptrend.xyaxis",
                accentColor: .teal
            )
        }
    }

    private func airlineMapSection(_ network: AirlineNetworkResponse) -> some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Text("NATIONWIDE ROUTE NETWORK")
                    .font(.caption)
                    .fontWeight(.bold)
                    .foregroundStyle(.secondary)
                Spacer()
                Text("\(network.routes.count) Active Segments")
                    .font(.caption2)
                    .foregroundStyle(.secondary)
            }

            RouteMapView(
                routes: network.routes,
                originCode: network.hubs.first?.airportCode,
                originCoordinate: nil,
                routeColor: Color(hex: selectedCarrier.signatureColorHex),
                selectedRoute: $selectedRoute
            )
            .frame(height: 320)
            .clipShape(RoundedRectangle(cornerRadius: 18))
            .overlay(
                RoundedRectangle(cornerRadius: 18)
                    .stroke(Color.white.opacity(0.15), lineWidth: 1)
            )
        }
    }

    private func hubsSection(_ hubs: [AirlineHub]) -> some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("PRIMARY HUBS & FOCUS CITIES")
                .font(.caption)
                .fontWeight(.bold)
                .foregroundStyle(.secondary)

            ForEach(hubs.prefix(5)) { hub in
                GlassCard {
                    HStack {
                        VStack(alignment: .leading, spacing: 2) {
                            HStack {
                                Text(hub.airportCode)
                                    .font(.headline)
                                    .fontWeight(.bold)
                                if let name = hub.originName {
                                    Text(name)
                                        .font(.caption)
                                        .foregroundStyle(.secondary)
                                }
                            }
                            Text("\(hub.directDestinations) Direct Destinations")
                                .font(.caption2)
                                .foregroundStyle(.secondary)
                        }
                        Spacer()
                        VStack(alignment: .trailing, spacing: 2) {
                            Text(formatCompact(hub.totalSeats) + " Seats")
                                .font(.subheadline)
                                .fontWeight(.bold)
                            Text(formatCompact(hub.departuresPerformed) + " Deps")
                                .font(.caption2)
                                .foregroundStyle(.secondary)
                        }
                    }
                }
            }
        }
    }

    private var yieldCurveSection: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("STAGE LENGTH VS YIELD PROFILE")
                .font(.caption)
                .fontWeight(.bold)
                .foregroundStyle(.secondary)

            ForEach(yieldCurve.prefix(6)) { pt in
                GlassCard {
                    HStack {
                        VStack(alignment: .leading, spacing: 2) {
                            Text(pt.routeLabel)
                                .font(.subheadline)
                                .fontWeight(.bold)
                            Text("\(Int(pt.stageLengthMiles)) miles")
                                .font(.caption2)
                                .foregroundStyle(.secondary)
                        }
                        Spacer()
                        VStack(alignment: .trailing, spacing: 2) {
                            Text(String(format: "$%.0f Fare", pt.avgOdFare))
                                .font(.subheadline)
                                .fontWeight(.bold)
                            Text(String(format: "%.2f¢ / mi", pt.yieldPerMile * 100))
                                .font(.caption2)
                                .foregroundStyle(.secondary)
                        }
                    }
                }
            }
        }
    }

    // MARK: - Data Loading

    private func loadAirlineData() async {
        isLoading = true
        defer { isLoading = false }
        let year = settings.reportingYear
        let code = selectedCarrier.code
        let baseURL = settings.activeApiBaseURL

        async let kpiTask = APIService.shared.fetchAirlineKPIs(code: code, year: year, baseURL: baseURL)
        async let netTask = APIService.shared.fetchAirlineNetwork(code: code, year: year, minDepartures: 20, baseURL: baseURL)
        async let yldTask = APIService.shared.fetchAirlineYieldCurve(code: code, year: year, baseURL: baseURL)

        do {
            let (kpiRes, netRes, yldRes) = try await (kpiTask, netTask, yldTask)
            self.kpis = kpiRes
            self.network = netRes
            self.yieldCurve = yldRes
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

    private func formatCompactBillions(_ number: Int) -> String {
        if number >= 1_000_000_000 {
            return String(format: "%.1fB", Double(number) / 1_000_000_000.0)
        } else if number >= 1_000_000 {
            return String(format: "%.1fM", Double(number) / 1_000_000.0)
        }
        return "\(number)"
    }
}

// Color Hex Extension
extension Color {
    init(hex: String) {
        let hex = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: hex).scanHexInt64(&int)
        let a, r, g, b: UInt64
        switch hex.count {
        case 3: // RGB (12-bit)
            (a, r, g, b) = (255, (int >> 8) * 17, (int >> 4 & 0xF) * 17, (int & 0xF) * 17)
        case 6: // RGB (24-bit)
            (a, r, g, b) = (255, int >> 16, int >> 8 & 0xFF, int & 0xFF)
        case 8: // ARGB (32-bit)
            (a, r, g, b) = (int >> 24, int >> 16 & 0xFF, int >> 8 & 0xFF, int & 0xFF)
        default:
            (a, r, g, b) = (1, 1, 1, 0)
        }

        self.init(
            .sRGB,
            red: Double(r) / 255,
            green: Double(g) / 255,
            blue: Double(b) / 255,
            opacity: Double(a) / 255
        )
    }
}
