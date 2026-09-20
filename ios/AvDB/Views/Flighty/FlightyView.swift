import SwiftUI
import UniformTypeIdentifiers

public struct FlightyView: View {
    @State private var flights: [FlightLog] = []
    @State private var showFileImporter: Bool = false
    @State private var importErrorMessage: String?
    @State private var isShowingError: Bool = false

    public init() {}

    private var totalAirportsVisited: Int {
        let origins = Set(flights.map { $0.originIATA })
        let dests = Set(flights.map { $0.destIATA })
        return origins.union(dests).count
    }

    private var topAirlines: [String] {
        let counts = flights.reduce(into: [String: Int]()) { dict, f in
            let code = f.airlineCode.isEmpty ? "Unknown" : f.airlineCode
            dict[code, default: 0] += 1
        }
        return counts.sorted { $0.value > $1.value }.prefix(3).map { "\($0.key) (\($0.value))" }
    }

    public var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 20) {
                    // Flighty Passport Header Card
                    GlassCard(cornerRadius: 18) {
                        VStack(spacing: 16) {
                            HStack {
                                VStack(alignment: .leading, spacing: 4) {
                                    Label("Flight Passport", systemImage: "airplane.circle.fill")
                                        .font(.system(size: 14, weight: .bold))
                                        .foregroundColor(AvDBTheme.accentCyan)
                                    Text("Flighty Log Vault")
                                        .font(.system(size: 22, weight: .bold))
                                        .foregroundColor(AvDBTheme.primaryText)
                                }
                                Spacer()

                                Button {
                                    showFileImporter = true
                                } label: {
                                    HStack(spacing: 6) {
                                        Image(systemName: "square.and.arrow.down.fill")
                                        Text("Import CSV")
                                    }
                                    .font(.system(size: 13, weight: .bold))
                                    .padding(.horizontal, 14)
                                    .padding(.vertical, 8)
                                    .background(AvDBTheme.accentBlue)
                                    .foregroundColor(.white)
                                    .clipShape(Capsule())
                                }
                            }

                            if flights.isEmpty {
                                VStack(spacing: 8) {
                                    Image(systemName: "doc.badge.plus")
                                        .font(.system(size: 32))
                                        .foregroundColor(AvDBTheme.secondaryText)
                                    Text("No Flighty Log Imported Yet")
                                        .font(.system(size: 14, weight: .semibold))
                                        .foregroundColor(AvDBTheme.secondaryText)
                                    Text("Export your flight history from Flighty (Settings > Export Data) and tap 'Import CSV' to unlock your personal flight analytics.")
                                        .font(.system(size: 12))
                                        .foregroundColor(AvDBTheme.tertiaryText)
                                        .multilineTextAlignment(.center)
                                        .padding(.horizontal, 20)
                                }
                                .padding(.vertical, 16)
                            } else {
                                // Passport Summary Metrics
                                LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible()), GridItem(.flexible())], spacing: 12) {
                                    VStack(spacing: 4) {
                                        Text("\(flights.count)")
                                            .font(.system(size: 20, weight: .bold, design: .rounded))
                                            .foregroundColor(AvDBTheme.accentCyan)
                                        Text("Flights")
                                            .font(.system(size: 10, weight: .semibold))
                                            .foregroundColor(AvDBTheme.secondaryText)
                                            .textCase(.uppercase)
                                    }
                                    VStack(spacing: 4) {
                                        Text("\(totalAirportsVisited)")
                                            .font(.system(size: 20, weight: .bold, design: .rounded))
                                            .foregroundColor(AvDBTheme.accentGreen)
                                        Text("Airports")
                                            .font(.system(size: 10, weight: .semibold))
                                            .foregroundColor(AvDBTheme.secondaryText)
                                            .textCase(.uppercase)
                                    }
                                    VStack(spacing: 4) {
                                        Text("\(topAirlines.first?.components(separatedBy: " ").first ?? "—")")
                                            .font(.system(size: 20, weight: .bold, design: .monospaced))
                                            .foregroundColor(AvDBTheme.accentAmber)
                                        Text("Top Carrier")
                                            .font(.system(size: 10, weight: .semibold))
                                            .foregroundColor(AvDBTheme.secondaryText)
                                            .textCase(.uppercase)
                                    }
                                }
                                .padding(.top, 4)
                            }
                        }
                    }
                    .padding(.horizontal, 16)

                    // Recent Flight Log List
                    if !flights.isEmpty {
                        VStack(alignment: .leading, spacing: 12) {
                            HStack {
                                Text("Recorded Flights (\(flights.count))")
                                    .font(.system(size: 14, weight: .bold))
                                    .foregroundColor(AvDBTheme.primaryText)
                                Spacer()
                                Button("Clear") {
                                    flights.removeAll()
                                }
                                .font(.system(size: 12, weight: .semibold))
                                .foregroundColor(AvDBTheme.accentCoral)
                            }
                            .padding(.horizontal, 16)

                            VStack(spacing: 8) {
                                ForEach(flights.prefix(50)) { f in
                                    GlassCard(cornerRadius: 12) {
                                        HStack {
                                            VStack(alignment: .leading, spacing: 2) {
                                                HStack(spacing: 6) {
                                                    Text(f.originIATA)
                                                        .font(.system(size: 14, weight: .bold, design: .monospaced))
                                                        .foregroundColor(AvDBTheme.accentCyan)
                                                    Image(systemName: "arrow.right")
                                                        .font(.system(size: 10, weight: .bold))
                                                        .foregroundColor(AvDBTheme.tertiaryText)
                                                    Text(f.destIATA)
                                                        .font(.system(size: 14, weight: .bold, design: .monospaced))
                                                        .foregroundColor(AvDBTheme.primaryText)

                                                    if !f.flightNumber.isEmpty {
                                                        Text(f.flightNumber)
                                                            .font(.system(size: 11, weight: .medium, design: .monospaced))
                                                            .foregroundColor(AvDBTheme.secondaryText)
                                                    }
                                                }

                                                HStack(spacing: 6) {
                                                    Text(f.date)
                                                        .font(.system(size: 11))
                                                        .foregroundColor(AvDBTheme.secondaryText)
                                                    if let aircraft = f.aircraftType, !aircraft.isEmpty {
                                                        Text("•")
                                                            .foregroundColor(AvDBTheme.tertiaryText)
                                                        Text(aircraft)
                                                            .font(.system(size: 11))
                                                            .foregroundColor(AvDBTheme.tertiaryText)
                                                    }
                                                }
                                            }

                                            Spacer()

                                            if let seat = f.seatNumber, !seat.isEmpty {
                                                Text(seat)
                                                    .font(.system(size: 12, weight: .semibold, design: .monospaced))
                                                    .padding(.horizontal, 6)
                                                    .padding(.vertical, 3)
                                                    .background(AvDBTheme.surfaceElevated)
                                                    .foregroundColor(AvDBTheme.accentAmber)
                                                    .clipShape(RoundedRectangle(cornerRadius: 4))
                                            }
                                        }
                                    }
                                }
                            }
                            .padding(.horizontal, 16)
                        }
                    }
                }
                .padding(.vertical, 16)
            }
            .navigationTitle("Flighty Vault")
            .navigationBarTitleDisplayMode(.large)
            .avdbCanvas()
            .fileImporter(
                isPresented: $showFileImporter,
                allowedContentTypes: [.commaSeparatedText, .plainText],
                allowsMultipleSelection: false
            ) { result in
                switch result {
                case .success(let urls):
                    guard let fileURL = urls.first else { return }
                    do {
                        let parsed = try FlightyParser.parseCSV(from: fileURL)
                        self.flights = parsed
                    } catch {
                        self.importErrorMessage = error.localizedDescription
                        self.isShowingError = true
                    }
                case .failure(let err):
                    self.importErrorMessage = err.localizedDescription
                    self.isShowingError = true
                }
            }
            .alert("Import Error", isPresented: $isShowingError) {
                Button("OK", role: .cancel) {}
            } message: {
                Text(importErrorMessage ?? "Failed to read CSV file.")
            }
        }
    }
}

