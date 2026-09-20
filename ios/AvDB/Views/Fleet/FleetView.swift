import SwiftUI

public struct FleetView: View {
    @State private var fleetFamilies: [FleetFamily] = []
    @State private var isLoading: Bool = true

    public init() {}

    public var body: some View {
        NavigationStack {
            ScrollView {
                LazyVStack(spacing: 16) {
                    if isLoading {
                        ProgressView()
                            .tint(AvDBTheme.accentCyan)
                            .padding(.top, 40)
                    } else {
                        ForEach(fleetFamilies) { family in
                            familyCard(family)
                        }
                    }
                }
                .padding(.horizontal, 16)
                .padding(.top, 8)
            }
            .navigationTitle("Fleet & Gauge")
            .navigationBarTitleDisplayMode(.large)
            .avdbCanvas()
            .task {
                self.fleetFamilies = await APIService.shared.getFleetFamilies()
                self.isLoading = false
            }
        }
    }

    @ViewBuilder
    private func familyCard(_ family: FleetFamily) -> some View {
        GlassCard(cornerRadius: 16) {
            VStack(alignment: .leading, spacing: 14) {
                HStack(alignment: .top) {
                    VStack(alignment: .leading, spacing: 3) {
                        Text(family.familyName)
                            .font(.system(size: 17, weight: .bold))
                            .foregroundColor(AvDBTheme.primaryText)

                        Text(family.manufacturer)
                            .font(.system(size: 13))
                            .foregroundColor(AvDBTheme.secondaryText)
                    }

                    Spacer()

                    // Gauge badge
                    VStack(alignment: .trailing, spacing: 2) {
                        Text("\(family.avgGauge, specifier: "%.0f") seats")
                            .font(.system(size: 14, weight: .bold, design: .rounded))
                            .foregroundColor(AvDBTheme.accentCyan)
                        Text("avg gauge")
                            .font(.system(size: 10))
                            .foregroundColor(AvDBTheme.tertiaryText)
                    }
                }

                // Operators
                HStack(spacing: 6) {
                    Text("Operators:")
                        .font(.system(size: 11, weight: .medium))
                        .foregroundColor(AvDBTheme.tertiaryText)
                    ForEach(family.dominantOperators, id: \.self) { op in
                        Text(op)
                            .font(.system(size: 10, weight: .bold, design: .monospaced))
                            .padding(.horizontal, 6)
                            .padding(.vertical, 2)
                            .background(AvDBTheme.surfaceElevated)
                            .foregroundColor(AvDBTheme.accentBlue)
                            .clipShape(RoundedRectangle(cornerRadius: 4))
                    }
                }

                // Subfleet breakdown
                if !family.subfleets.isEmpty {
                    VStack(spacing: 8) {
                        ForEach(family.subfleets) { sub in
                            HStack(spacing: 12) {
                                VStack(alignment: .leading, spacing: 2) {
                                    Text(sub.aircraftType)
                                        .font(.system(size: 13, weight: .semibold))
                                        .foregroundColor(AvDBTheme.primaryText)
                                    Text(sub.engineType)
                                        .font(.system(size: 11))
                                        .foregroundColor(AvDBTheme.secondaryText)
                                        .lineLimit(1)
                                }

                                Spacer()

                                VStack(alignment: .trailing, spacing: 2) {
                                    Text("\(sub.typicalSeats) seats")
                                        .font(.system(size: 12, weight: .medium, design: .rounded))
                                        .foregroundColor(AvDBTheme.accentAmber)
                                    Text("\(sub.departures.formatted()) dep")
                                        .font(.system(size: 10))
                                        .foregroundColor(AvDBTheme.tertiaryText)
                                }
                            }
                            .padding(.vertical, 4)
                            if sub.id != family.subfleets.last?.id {
                                Divider().background(AvDBTheme.borderStroke)
                            }
                        }
                    }
                    .padding(10)
                    .background(Color.white.opacity(0.02))
                    .clipShape(RoundedRectangle(cornerRadius: 10))
                }
            }
        }
    }
}

