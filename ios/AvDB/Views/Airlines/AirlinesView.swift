import SwiftUI

public struct AirlinesView: View {
    @State private var airlines: [Airline] = []
    @State private var searchText: String = ""
    @State private var filterMode: FilterMode = .all
    @State private var isLoading: Bool = true

    public enum FilterMode: String, CaseIterable, Identifiable {
        case all = "All"
        case active = "Active"
        case historical = "Historical"
        public var id: String { rawValue }
    }

    public init() {}

    private var filteredAirlines: [Airline] {
        var list = airlines
        switch filterMode {
        case .active:
            list = list.filter { $0.isActive }
        case .historical:
            list = list.filter { !$0.isActive }
        case .all:
            break
        }

        if searchText.trimmingCharacters(in: .whitespaces).isEmpty {
            return list
        }
        let q = searchText.lowercased().trimmingCharacters(in: .whitespaces)
        return list.filter {
            $0.code.lowercased().contains(q) ||
            $0.name.lowercased().contains(q) ||
            $0.primaryHubs.contains { $0.lowercased().contains(q) } ||
            ($0.alliance?.lowercased().contains(q) ?? false)
        }
    }

    public var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 12) {
                    // Filter Mode Picker
                    Picker("Carrier Status", selection: $filterMode) {
                        ForEach(FilterMode.allCases) { mode in
                            Text(mode.rawValue).tag(mode)
                        }
                    }
                    .pickerStyle(.segmented)
                    .padding(.horizontal, 16)
                    .padding(.top, 4)

                    LazyVStack(spacing: 12) {
                        if isLoading {
                            ProgressView()
                                .tint(AvDBTheme.accentBlue)
                                .padding(.top, 40)
                        } else {
                            ForEach(filteredAirlines) { airline in
                                NavigationLink(destination: AirlineDetailView(airline: airline)) {
                                    airlineCard(airline)
                                }
                                .buttonStyle(.plain)
                            }
                        }
                    }
                    .padding(.horizontal, 16)
                }
                .padding(.top, 4)
            }
            .searchable(text: $searchText, prompt: "Search carrier name, code, or hub...")
            .navigationTitle("Airlines Radar")
            .navigationBarTitleDisplayMode(.large)
            .avdbCanvas()
            .task {
                self.airlines = await APIService.shared.getAirlines()
                self.isLoading = false
            }
        }
    }

    @ViewBuilder
    private func airlineCard(_ airline: Airline) -> some View {
        GlassCard(cornerRadius: 14) {
            HStack(spacing: 16) {
                // Livery Code Badge
                ZStack {
                    RoundedRectangle(cornerRadius: 10, style: .continuous)
                        .fill(airline.brandColor.opacity(0.2))
                    Text(airline.code)
                        .font(.system(size: 18, weight: .bold, design: .monospaced))
                        .foregroundColor(airline.brandColor)
                }
                .frame(width: 58, height: 44)

                VStack(alignment: .leading, spacing: 3) {
                    HStack {
                        Text(airline.name)
                            .font(.system(size: 15, weight: .semibold))
                            .foregroundColor(AvDBTheme.primaryText)
                        Spacer()
                        if !airline.isActive {
                            Text("HISTORICAL")
                                .font(.system(size: 8, weight: .bold))
                                .padding(.horizontal, 6)
                                .padding(.vertical, 2)
                                .background(AvDBTheme.accentAmber.opacity(0.2))
                                .foregroundColor(AvDBTheme.accentAmber)
                                .clipShape(Capsule())
                        } else if let alliance = airline.alliance {
                            Text(alliance)
                                .font(.system(size: 9, weight: .bold))
                                .padding(.horizontal, 6)
                                .padding(.vertical, 2)
                                .background(AvDBTheme.surfaceElevated)
                                .foregroundColor(AvDBTheme.secondaryText)
                                .clipShape(Capsule())
                        }
                    }

                    if let note = airline.mergerNote {
                        Text(note)
                            .font(.system(size: 11))
                            .foregroundColor(AvDBTheme.accentAmber)
                            .lineLimit(1)
                    } else if !airline.primaryHubs.isEmpty {
                        Text("Hubs: \(airline.primaryHubs.prefix(4).joined(separator: ", "))")
                            .font(.system(size: 12))
                            .foregroundColor(AvDBTheme.secondaryText)
                    }
                }

                Image(systemName: "chevron.right")
                    .font(.system(size: 13, weight: .semibold))
                    .foregroundColor(AvDBTheme.tertiaryText)
            }
        }
    }
}
