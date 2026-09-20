import SwiftUI

public struct AirlineDetailView: View {
    public let airline: Airline
    @State private var kpis: AirlineKPIs?
    @State private var isLoading: Bool = true

    public init(airline: Airline) {
        self.airline = airline
    }

    public var body: some View {
        ScrollView {
            VStack(spacing: 20) {
                // Header Banner
                GlassCard(cornerRadius: 16) {
                    HStack(spacing: 16) {
                        Circle()
                            .fill(airline.brandColor)
                            .frame(width: 48, height: 48)
                            .overlay(
                                Text(airline.code)
                                    .font(.system(size: 16, weight: .bold, design: .monospaced))
                                    .foregroundColor(.white)
                            )

                        VStack(alignment: .leading, spacing: 4) {
                            Text(airline.name)
                                .font(.system(size: 18, weight: .bold))
                                .foregroundColor(AvDBTheme.primaryText)

                            HStack(spacing: 8) {
                                if let alliance = airline.alliance {
                                    Text(alliance)
                                        .font(.system(size: 11, weight: .semibold))
                                        .foregroundColor(AvDBTheme.accentCyan)
                                }
                                Text("HQ: \(airline.headquarters)")
                                    .font(.system(size: 11))
                                    .foregroundColor(AvDBTheme.secondaryText)
                            }
                        }
                        Spacer()
                    }
                }
                .padding(.horizontal, 16)

                // Primary Hubs Bar
                VStack(alignment: .leading, spacing: 10) {
                    Text("Primary Network Hubs")
                        .font(.system(size: 14, weight: .bold))
                        .foregroundColor(AvDBTheme.primaryText)
                        .padding(.horizontal, 16)

                    ScrollView(.horizontal, showsIndicators: false) {
                        HStack(spacing: 8) {
                            ForEach(airline.primaryHubs, id: \.self) { hub in
                                HStack(spacing: 6) {
                                    Image(systemName: "airplane.circle.fill")
                                        .font(.system(size: 12))
                                        .foregroundColor(airline.brandColor)
                                    Text(hub)
                                        .font(.system(size: 13, weight: .bold, design: .monospaced))
                                        .foregroundColor(AvDBTheme.primaryText)
                                }
                                .padding(.horizontal, 12)
                                .padding(.vertical, 8)
                                .background(AvDBTheme.surfaceCard)
                                .clipShape(Capsule())
                                .overlay(
                                    Capsule().stroke(AvDBTheme.borderStroke, lineWidth: 1)
                                )
                            }
                        }
                        .padding(.horizontal, 16)
                    }
                }

                // KPIs
                if let kpi = kpis {
                    VStack(alignment: .leading, spacing: 12) {
                        Text("System Economics & Scale")
                            .font(.system(size: 14, weight: .bold))
                            .foregroundColor(AvDBTheme.primaryText)
                            .padding(.horizontal, 16)

                        LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 12) {
                            KPICardView(
                                title: "Active Routes",
                                value: "\(kpi.activeRoutes)",
                                subtitle: "\(kpi.departures.formatted()) departures",
                                icon: "arrow.triangle.swap",
                                accentColor: AvDBTheme.accentCyan
                            )
                            KPICardView(
                                title: "Load Factor",
                                value: String(format: "%.1f%%", kpi.loadFactor * 100),
                                subtitle: "\(String(format: "%.1f", Double(kpi.totalPassengers) / 1_000_000.0))M passengers",
                                icon: "gauge.with.needle.fill",
                                accentColor: AvDBTheme.accentGreen
                            )
                            KPICardView(
                                title: "Avg Network Fare",
                                value: kpi.avgOdFare != nil ? String(format: "$%.0f", kpi.avgOdFare!) : "—",
                                subtitle: "DB1B Survey",
                                icon: "dollarsign.circle.fill",
                                accentColor: AvDBTheme.accentAmber
                            )
                            KPICardView(
                                title: "Yield / RPM",
                                value: kpi.yieldPerMile != nil ? String(format: "¢%.1f", kpi.yieldPerMile! * 100) : "—",
                                subtitle: "Per passenger-mile",
                                icon: "chart.line.uptrend.xyaxis",
                                accentColor: AvDBTheme.accentCoral
                            )
                        }
                        .padding(.horizontal, 16)

                        // Capacity & Traffic
                        GlassCard(cornerRadius: 14) {
                            VStack(spacing: 12) {
                                HStack {
                                    Text("Capacity (ASM) vs Traffic (RPM)")
                                        .font(.system(size: 13, weight: .semibold))
                                        .foregroundColor(AvDBTheme.secondaryText)
                                    Spacer()
                                }
                                HStack(spacing: 20) {
                                    VStack(alignment: .leading) {
                                        Text("\(String(format: "%.1f", kpi.asmBillions))B")
                                            .font(.system(size: 18, weight: .bold, design: .rounded))
                                            .foregroundColor(AvDBTheme.accentBlue)
                                        Text("Available Seat Miles")
                                            .font(.system(size: 11))
                                            .foregroundColor(AvDBTheme.tertiaryText)
                                    }
                                    Spacer()
                                    VStack(alignment: .trailing) {
                                        Text("\(String(format: "%.1f", kpi.rpmBillions))B")
                                            .font(.system(size: 18, weight: .bold, design: .rounded))
                                            .foregroundColor(AvDBTheme.accentGreen)
                                        Text("Revenue Pax Miles")
                                            .font(.system(size: 11))
                                            .foregroundColor(AvDBTheme.tertiaryText)
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
        .navigationTitle(airline.code)
        .navigationBarTitleDisplayMode(.inline)
        .avdbCanvas()
        .task {
            self.kpis = await APIService.shared.getAirlineKPIs(code: airline.code)
            self.isLoading = false
        }
    }
}

