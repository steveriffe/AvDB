import SwiftUI

/// Fleet / Aircraft Lens: Aircraft Family Utilization, Gauge Trends & Subfleet Economics
public struct FleetView: View {
    @StateObject private var settings = AppSettings.shared

    let aircraftFamilies = [
        "All Mainline & Regional",
        "Airbus A320 Family",
        "Boeing 737 Family",
        "Widebody",
        "Embraer E-Jets",
        "Bombardier CRJ"
    ]

    @State private var selectedFamily: String = "Boeing 737 Family"
    @State private var fleetSummary: FleetSummaryResponse?
    @State private var isLoading: Bool = false
    @State private var errorMessage: String?

    public init() {}

    public var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 20) {
                    // 1. Aircraft Family Picker
                    familyPickerSection

                    if isLoading {
                        ProgressView("Analyzing Fleet Economics...")
                            .padding(.top, 40)
                    } else if let summary = fleetSummary {
                        // 2. High-Density Fleet KPIs
                        kpisSection(summary.kpis)

                        // 3. Subfleet Comparison Breakdown
                        subfleetsSection(summary.subfleets)
                    }
                }
                .padding(.horizontal, 16)
                .padding(.bottom, 32)
            }
            .navigationTitle("Fleet Economics")
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
                        Task { await loadFleetData() }
                    }
                }
            }
            .task {
                await loadFleetData()
            }
        }
    }

    // MARK: - Subviews

    private var familyPickerSection: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 10) {
                ForEach(aircraftFamilies, id: \.self) { fam in
                    let isSelected = fam == selectedFamily
                    Button {
                        selectedFamily = fam
                        Task { await loadFleetData() }
                    } label: {
                        Text(fam)
                            .font(.subheadline)
                            .fontWeight(isSelected ? .bold : .regular)
                            .padding(.horizontal, 14)
                            .padding(.vertical, 8)
                            .background(
                                isSelected ? Color.blue.opacity(0.2) : Color.clear,
                                in: Capsule()
                            )
                            .overlay(
                                Capsule().stroke(
                                    isSelected ? Color.blue : Color.secondary.opacity(0.3),
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

    private func kpisSection(_ kpis: FleetKPIs) -> some View {
        LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 12) {
            KPICardView(
                title: "AVG GAUGE",
                value: String(format: "%.1f", kpis.avgGaugeSeats),
                subtitle: "Seats per Departure",
                iconName: "chair.lounge.fill",
                accentColor: .blue
            )
            KPICardView(
                title: "FLEET LOAD FACTOR",
                value: String(format: "%.1f%%", kpis.fleetLoadFactor),
                subtitle: "Passenger Utilization",
                iconName: "percent",
                accentColor: .green
            )
            KPICardView(
                title: "AVG STAGE LENGTH",
                value: "\(kpis.avgStageLength) mi",
                subtitle: "Flight Segment Distance",
                iconName: "arrow.left.and.right.circle.fill",
                accentColor: .purple
            )
            KPICardView(
                title: "AVG SEGMENT FARE",
                value: String(format: "$%.0f", kpis.avgSegmentFare),
                subtitle: "Sample O&D Fare",
                iconName: "dollarsign.circle.fill",
                accentColor: .orange
            )
            KPICardView(
                title: "OPERATING CARRIERS",
                value: "\(kpis.operatingCarriers)",
                subtitle: "Active Operators",
                iconName: "building.2.crop.circle.fill",
                accentColor: .teal
            )
            KPICardView(
                title: "YIELD / MILE",
                value: String(format: "%.2f¢", kpis.yieldPerMile * 100),
                subtitle: "Per Passenger-Mile",
                iconName: "chart.bar.xaxis",
                accentColor: .indigo
            )
        }
    }

    private func subfleetsSection(_ subfleets: [SubfleetItem]) -> some View {
        VStack(alignment: .leading, spacing: 14) {
            HStack {
                Text("SUBFLEET BREAKDOWN & GAUGE ECONOMICS")
                    .font(.caption)
                    .fontWeight(.bold)
                    .foregroundStyle(.secondary)
                Spacer()
                Text("\(subfleets.count) Models")
                    .font(.caption2)
                    .foregroundStyle(.secondary)
            }

            ForEach(subfleets) { model in
                GlassCard {
                    VStack(alignment: .leading, spacing: 10) {
                        HStack {
                            VStack(alignment: .leading, spacing: 2) {
                                Text(model.aircraftDescription)
                                    .font(.headline)
                                    .fontWeight(.bold)
                                Text(model.aircraftFamily)
                                    .font(.caption)
                                    .foregroundStyle(.secondary)
                            }
                            Spacer()
                            VStack(alignment: .trailing, spacing: 2) {
                                Text(String(format: "%.0f seats", model.avgGaugeSeats))
                                    .font(.subheadline)
                                    .fontWeight(.bold)
                                    .foregroundStyle(.blue)
                                Text(String(format: "%.1f%% LF", model.loadFactorPct))
                                    .font(.caption2)
                                    .fontWeight(.semibold)
                                    .foregroundStyle(.green)
                            }
                        }

                        Divider()

                        HStack(spacing: 12) {
                            metricColumn(label: "DEPARTURES", val: formatCompact(model.departuresPerformed))
                            metricColumn(label: "SEATS", val: formatCompact(model.totalSeats))
                            metricColumn(label: "STAGE", val: "\(model.avgStageLength) mi")
                            metricColumn(label: "YIELD", val: String(format: "%.1f¢/mi", model.yieldPerMile * 100))
                        }
                    }
                }
            }
        }
    }

    private func metricColumn(label: String, val: String) -> some View {
        VStack(alignment: .leading, spacing: 2) {
            Text(label)
                .font(.system(size: 8, weight: .semibold))
                .foregroundStyle(.secondary)
            Text(val)
                .font(.caption)
                .fontWeight(.bold)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
    }

    // MARK: - Data Loading

    private func loadFleetData() async {
        isLoading = true
        defer { isLoading = false }
        let year = settings.reportingYear
        let baseURL = settings.activeApiBaseURL

        do {
            self.fleetSummary = try await APIService.shared.fetchFleetSummary(
                family: selectedFamily,
                year: year,
                baseURL: baseURL
            )
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
