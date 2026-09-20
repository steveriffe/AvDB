import SwiftUI
import Charts

public struct AirlineDetailView: View {
    public let airline: Airline

    @State private var selectedYear: Int = 2024
    @State private var passengerOnly: Bool = true
    @State private var minDepartures: Int = 10

    @State private var kpis: AirlineKPIs?
    @State private var timeline: [AirlineTimelinePoint] = []
    @State private var yieldCurve: [YieldCurvePoint] = []
    @State private var isLoading: Bool = true

    public init(airline: Airline) {
        self.airline = airline
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
                            HStack {
                                Text(airline.name)
                                    .font(.system(size: 18, weight: .bold))
                                    .foregroundColor(AvDBTheme.primaryText)
                                Spacer()
                                if !airline.isActive {
                                    Text("HISTORICAL")
                                        .font(.system(size: 9, weight: .bold))
                                        .padding(.horizontal, 6)
                                        .padding(.vertical, 2)
                                        .background(AvDBTheme.accentAmber.opacity(0.2))
                                        .foregroundColor(AvDBTheme.accentAmber)
                                        .clipShape(Capsule())
                                }
                            }

                            HStack(spacing: 8) {
                                if let alliance = airline.alliance {
                                    Text(alliance)
                                        .font(.system(size: 11, weight: .semibold))
                                        .foregroundColor(AvDBTheme.accentCyan)
                                }
                                if !airline.headquarters.isEmpty {
                                    Text("•")
                                        .foregroundColor(AvDBTheme.tertiaryText)
                                    Text("HQ: \(airline.headquarters)")
                                        .font(.system(size: 11))
                                        .foregroundColor(AvDBTheme.secondaryText)
                                }
                            }
                        }
                    }
                }
                .padding(.horizontal, 16)

                // Merger / Lineage Note
                if let note = airline.mergerNote {
                    HStack(spacing: 8) {
                        Image(systemName: "arrow.triangle.merge")
                            .font(.system(size: 12, weight: .bold))
                            .foregroundColor(AvDBTheme.accentAmber)
                        Text(note)
                            .font(.system(size: 12, weight: .medium))
                            .foregroundColor(AvDBTheme.accentAmber)
                    }
                    .padding(.horizontal, 14)
                    .padding(.vertical, 8)
                    .background(AvDBTheme.accentAmber.opacity(0.1))
                    .clipShape(RoundedRectangle(cornerRadius: 10))
                    .padding(.horizontal, 16)
                }

                // Primary Hubs Bar
                if !airline.primaryHubs.isEmpty {
                    VStack(alignment: .leading, spacing: 8) {
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
                                    .padding(.vertical, 7)
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
                }

                // KPIs
                if let kpi = kpis {
                    VStack(alignment: .leading, spacing: 10) {
                        HStack {
                            Text("System Economics (\(selectedYear))")
                                .font(.system(size: 14, weight: .bold))
                                .foregroundColor(AvDBTheme.primaryText)
                            Spacer()
                            Text("BigQuery Marts")
                                .font(.system(size: 10, weight: .medium))
                                .foregroundColor(AvDBTheme.tertiaryText)
                        }
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
                                subtitle: "\(formatVolume(kpi.totalPassengers)) pax",
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
                                title: "Yield / Mile",
                                value: kpi.yieldPerMile != nil ? String(format: "¢%.1f", kpi.yieldPerMile! * 100) : "—",
                                subtitle: "Per passenger-mile",
                                icon: "chart.line.uptrend.xyaxis",
                                accentColor: AvDBTheme.accentCoral
                            )
                        }
                        .padding(.horizontal, 16)
                    }
                }

                // Capacity (ASM) vs Traffic (RPM) Timeline Swift Chart
                if !timeline.isEmpty {
                    GlassCard(cornerRadius: 16) {
                        VStack(alignment: .leading, spacing: 12) {
                            HStack {
                                VStack(alignment: .leading, spacing: 2) {
                                    Text("Capacity (ASM) vs Traffic (RPM)")
                                        .font(.system(size: 14, weight: .bold))
                                        .foregroundColor(AvDBTheme.primaryText)
                                    Text("Billions of Available vs Revenue Seat Miles (1990–2025)")
                                        .font(.system(size: 11))
                                        .foregroundColor(AvDBTheme.secondaryText)
                                }
                                Spacer()
                            }

                            Chart {
                                ForEach(timeline) { pt in
                                    LineMark(
                                        x: .value("Year", pt.year),
                                        y: .value("ASM", pt.asmBillions),
                                        series: .value("Series", "ASM")
                                    )
                                    .foregroundStyle(AvDBTheme.accentBlue)
                                    .lineStyle(StrokeStyle(lineWidth: 2.5))

                                    LineMark(
                                        x: .value("Year", pt.year),
                                        y: .value("RPM", pt.rpmBillions),
                                        series: .value("Series", "RPM")
                                    )
                                    .foregroundStyle(AvDBTheme.accentGreen)
                                    .lineStyle(StrokeStyle(lineWidth: 2.5))

                                    if pt.year == selectedYear {
                                        RuleMark(x: .value("Selected Year", pt.year))
                                            .foregroundStyle(AvDBTheme.accentCyan.opacity(0.8))
                                            .lineStyle(StrokeStyle(lineWidth: 1.5, dash: [4, 4]))
                                    }
                                }
                            }
                            .chartForegroundStyleScale([
                                "ASM (Capacity)": AvDBTheme.accentBlue,
                                "RPM (Traffic)": AvDBTheme.accentGreen
                            ])
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
                                        if let b = val.as(Double.self) {
                                            Text(String(format: "%.0fB", b))
                                                .font(.system(size: 9, design: .monospaced))
                                                .foregroundStyle(Color.gray)
                                        }
                                    }
                                }
                            }
                            .frame(height: 170)
                        }
                    }
                    .padding(.horizontal, 16)
                }

                // Stage Length vs Fare Yield Curve
                if !yieldCurve.isEmpty {
                    GlassCard(cornerRadius: 16) {
                        VStack(alignment: .leading, spacing: 12) {
                            HStack {
                                VStack(alignment: .leading, spacing: 2) {
                                    Text("Stage Length vs Fare Yield Curve")
                                        .font(.system(size: 14, weight: .bold))
                                        .foregroundColor(AvDBTheme.primaryText)
                                    Text("Short-haul fare premium vs long-haul rate compression")
                                        .font(.system(size: 11))
                                        .foregroundColor(AvDBTheme.secondaryText)
                                }
                                Spacer()
                            }

                            Chart(yieldCurve.prefix(50)) { pt in
                                PointMark(
                                    x: .value("Distance (mi)", pt.stageLengthMiles),
                                    y: .value("Yield (¢/mi)", pt.yieldPerMile * 100.0)
                                )
                                .foregroundStyle(AvDBTheme.accentAmber)
                                .symbolSize(28)
                            }
                            .chartXAxis {
                                AxisMarks { val in
                                    AxisValueLabel {
                                        if let d = val.as(Double.self) {
                                            Text(String(format: "%.0fmi", d))
                                                .font(.system(size: 9, design: .monospaced))
                                                .foregroundStyle(Color.gray)
                                        }
                                    }
                                }
                            }
                            .chartYAxis {
                                AxisMarks(position: .trailing) { val in
                                    AxisValueLabel {
                                        if let y = val.as(Double.self) {
                                            Text(String(format: "¢%.0f", y))
                                                .font(.system(size: 9, design: .monospaced))
                                                .foregroundStyle(Color.gray)
                                        }
                                    }
                                }
                            }
                            .frame(height: 180)
                        }
                    }
                    .padding(.horizontal, 16)
                }
            }
            .padding(.vertical, 12)
        }
        .navigationTitle(airline.code)
        .navigationBarTitleDisplayMode(.inline)
        .avdbCanvas()
        .task {
            await loadData()
        }
    }

    private func loadData() async {
        self.isLoading = true
        async let kpiTask = APIService.shared.getAirlineKPIs(code: airline.code, year: selectedYear)
        async let timelineTask = APIService.shared.getAirlineTimeline(code: airline.code)
        async let yieldTask = APIService.shared.getAirlineYieldCurve(code: airline.code, year: selectedYear)

        self.kpis = await kpiTask
        self.timeline = await timelineTask
        self.yieldCurve = await yieldTask
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
