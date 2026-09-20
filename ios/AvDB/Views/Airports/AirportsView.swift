import SwiftUI

public struct AirportsView: View {
    @State private var searchText: String = ""
    @State private var airports: [Airport] = []
    @State private var filterMode: AirportFilterMode = .majorHubs
    @State private var isLoading: Bool = true

    public enum AirportFilterMode: String, CaseIterable, Identifiable {
        case majorHubs = "Primary & Hubs"
        case all = "All Commercial"
        public var id: String { rawValue }
    }

    public init() {}

    private var filteredAirports: [Airport] {
        let baseList: [Airport]
        if !searchText.trimmingCharacters(in: .whitespaces).isEmpty {
            let query = searchText.lowercased().trimmingCharacters(in: .whitespaces)
            return airports.filter {
                $0.iata.lowercased().contains(query) ||
                $0.name.lowercased().contains(query) ||
                $0.city.lowercased().contains(query) ||
                ($0.catchmentMarket?.lowercased().contains(query) ?? false)
            }
        } else {
            switch filterMode {
            case .majorHubs:
                baseList = airports.filter { $0.isMajorHub }
            case .all:
                baseList = airports
            }
            return Array(baseList.prefix(150))
        }
    }

    public var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 12) {
                    Picker("Airport Scope", selection: $filterMode) {
                        ForEach(AirportFilterMode.allCases) { mode in
                            Text(mode.rawValue).tag(mode)
                        }
                    }
                    .pickerStyle(.segmented)
                    .padding(.horizontal, 16)
                    .padding(.top, 4)

                    LazyVStack(spacing: 12) {
                        if isLoading {
                            ProgressView()
                                .tint(AvDBTheme.accentCyan)
                                .padding(.top, 40)
                        } else {
                            ForEach(filteredAirports) { airport in
                                NavigationLink(destination: AirportDetailView(airport: airport)) {
                                    airportRow(airport)
                                }
                                .buttonStyle(.plain)
                            }
                        }
                    }
                    .padding(.horizontal, 16)
                }
                .padding(.top, 4)
            }
            .searchable(text: $searchText, prompt: "Search airport code, city, catchment (e.g. ATL, NYC)...")
            .navigationTitle("Airports Radar")
            .navigationBarTitleDisplayMode(.large)
            .avdbCanvas()
            .task {
                self.airports = await APIService.shared.getAirports()
                self.isLoading = false
            }
        }
    }

    @ViewBuilder
    private func airportRow(_ airport: Airport) -> some View {
        GlassCard(cornerRadius: 14) {
            HStack(spacing: 16) {
                // IATA Badge
                ZStack {
                    RoundedRectangle(cornerRadius: 10, style: .continuous)
                        .fill(airport.isMajorHub ? AvDBTheme.accentBlue.opacity(0.2) : Color.white.opacity(0.06))
                    Text(airport.iata)
                        .font(.system(size: 17, weight: .bold, design: .monospaced))
                        .foregroundColor(airport.isMajorHub ? AvDBTheme.accentCyan : AvDBTheme.primaryText)
                }
                .frame(width: 58, height: 44)

                // Info
                VStack(alignment: .leading, spacing: 3) {
                    HStack {
                        Text(airport.name)
                            .font(.system(size: 15, weight: .semibold))
                            .foregroundColor(AvDBTheme.primaryText)
                            .lineLimit(1)
                        Spacer()
                        if airport.isMajorHub {
                            Text("HUB")
                                .font(.system(size: 9, weight: .bold))
                                .padding(.horizontal, 6)
                                .padding(.vertical, 2)
                                .background(AvDBTheme.accentBlue.opacity(0.3))
                                .foregroundColor(AvDBTheme.accentCyan)
                                .clipShape(Capsule())
                        }
                    }

                    HStack(spacing: 6) {
                        Text("\(airport.city), \(airport.state)")
                            .font(.system(size: 13))
                            .foregroundColor(AvDBTheme.secondaryText)

                        if let catchment = airport.catchmentMarket, catchment != airport.iata {
                            Text("•")
                                .foregroundColor(AvDBTheme.tertiaryText)
                            Text("Catchment \(catchment)")
                                .font(.system(size: 11, weight: .medium))
                                .foregroundColor(AvDBTheme.accentAmber)
                        }
                    }
                }

                Image(systemName: "chevron.right")
                    .font(.system(size: 13, weight: .semibold))
                    .foregroundColor(AvDBTheme.tertiaryText)
            }
        }
    }
}
