import SwiftUI

public struct FilterBarView: View {
    @Binding public var selectedYear: Int
    @Binding public var passengerOnly: Bool
    @Binding public var minDepartures: Int

    public var onFilterChanged: () -> Void

    public init(
        selectedYear: Binding<Int>,
        passengerOnly: Binding<Bool>,
        minDepartures: Binding<Int>,
        onFilterChanged: @escaping () -> Void = {}
    ) {
        self._selectedYear = selectedYear
        self._passengerOnly = passengerOnly
        self._minDepartures = minDepartures
        self.onFilterChanged = onFilterChanged
    }

    public var body: some View {
        GlassCard(cornerRadius: 14) {
            VStack(spacing: 10) {
                // Top row: Year & Service Type
                HStack(spacing: 12) {
                    // Year Menu
                    Menu {
                        ForEach((1990...2025).reversed(), id: \.self) { yr in
                            Button {
                                selectedYear = yr
                                onFilterChanged()
                            } label: {
                                if yr == selectedYear {
                                    Label("\(yr)", systemImage: "checkmark")
                                } else {
                                    Text("\(yr)")
                                }
                            }
                        }
                    } label: {
                        HStack(spacing: 6) {
                            Image(systemName: "calendar")
                                .font(.system(size: 13, weight: .bold))
                                .foregroundColor(AvDBTheme.accentCyan)
                            Text("\(selectedYear)")
                                .font(.system(size: 14, weight: .bold, design: .rounded))
                                .foregroundColor(AvDBTheme.primaryText)
                            Image(systemName: "chevron.up.chevron.down")
                                .font(.system(size: 10, weight: .semibold))
                                .foregroundColor(AvDBTheme.tertiaryText)
                        }
                        .padding(.horizontal, 10)
                        .padding(.vertical, 6)
                        .background(Color.white.opacity(0.06))
                        .clipShape(Capsule())
                    }

                    // Pax / All toggle
                    Button {
                        passengerOnly.toggle()
                        onFilterChanged()
                    } label: {
                        HStack(spacing: 5) {
                            Image(systemName: passengerOnly ? "person.2.fill" : "shippingbox.fill")
                                .font(.system(size: 11, weight: .bold))
                            Text(passengerOnly ? "Passenger" : "All Ops")
                                .font(.system(size: 12, weight: .semibold))
                        }
                        .padding(.horizontal, 10)
                        .padding(.vertical, 6)
                        .background(passengerOnly ? AvDBTheme.accentBlue.opacity(0.2) : Color.white.opacity(0.06))
                        .foregroundColor(passengerOnly ? AvDBTheme.accentCyan : AvDBTheme.secondaryText)
                        .clipShape(Capsule())
                    }

                    Spacer()

                    // Frequency Filter Menu
                    Menu {
                        Button("≥ 10 flights (Standard)") {
                            minDepartures = 10
                            onFilterChanged()
                        }
                        Button("≥ 50 flights (Weekly+)") {
                            minDepartures = 50
                            onFilterChanged()
                        }
                        Button("≥ 365 flights (Daily)") {
                            minDepartures = 365
                            onFilterChanged()
                        }
                        Button("≥ 1 flight (All/Charters)") {
                            minDepartures = 1
                            onFilterChanged()
                        }
                    } label: {
                        HStack(spacing: 4) {
                            Image(systemName: "slider.horizontal.3")
                                .font(.system(size: 11))
                            Text(freqTitle)
                                .font(.system(size: 12, weight: .medium))
                        }
                        .padding(.horizontal, 8)
                        .padding(.vertical, 6)
                        .foregroundColor(AvDBTheme.secondaryText)
                    }
                }

                // Quick scrubbing year bar
                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: 6) {
                        ForEach([2024, 2023, 2021, 2019, 2015, 2010, 2000, 1995], id: \.self) { yr in
                            Button {
                                selectedYear = yr
                                onFilterChanged()
                            } label: {
                                Text("\(yr)")
                                    .font(.system(size: 11, weight: selectedYear == yr ? .bold : .medium, design: .monospaced))
                                    .padding(.horizontal, 8)
                                    .padding(.vertical, 3)
                                    .background(selectedYear == yr ? AvDBTheme.accentCyan.opacity(0.25) : Color.white.opacity(0.04))
                                    .foregroundColor(selectedYear == yr ? AvDBTheme.accentCyan : AvDBTheme.tertiaryText)
                                    .clipShape(Capsule())
                            }
                            .buttonStyle(.plain)
                        }
                    }
                }
            }
            .padding(.vertical, 2)
        }
    }

    private var freqTitle: String {
        switch minDepartures {
        case 50: return "≥50 flt"
        case 365: return "Daily"
        case 1: return "All"
        default: return "≥10 flt"
        }
    }
}

