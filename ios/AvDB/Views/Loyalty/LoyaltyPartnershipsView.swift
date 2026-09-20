import SwiftUI

public struct LoyaltyPartnershipsView: View {
    @State private var programs: [LoyaltyProgram] = []
    @State private var selectedProgram: LoyaltyProgram?
    @State private var isLoading: Bool = true

    public init() {}

    public var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 20) {
                    if isLoading {
                        ProgressView()
                            .tint(AvDBTheme.accentAmber)
                            .padding(.top, 40)
                    } else if let prog = selectedProgram {
                        // Program Selector Horizontal Bar
                        ScrollView(.horizontal, showsIndicators: false) {
                            HStack(spacing: 10) {
                                ForEach(programs) { p in
                                    Button {
                                        self.selectedProgram = p
                                    } label: {
                                        HStack(spacing: 8) {
                                            Text(p.carrierCode)
                                                .font(.system(size: 13, weight: .bold, design: .monospaced))
                                                .foregroundColor(p.id == prog.id ? .white : AvDBTheme.secondaryText)
                                            Text(p.programName)
                                                .font(.system(size: 13, weight: .semibold))
                                                .foregroundColor(p.id == prog.id ? .white : AvDBTheme.primaryText)
                                        }
                                        .padding(.horizontal, 14)
                                        .padding(.vertical, 8)
                                        .background(p.id == prog.id ? AvDBTheme.accentBlue : AvDBTheme.surfaceCard)
                                        .clipShape(Capsule())
                                        .overlay(
                                            Capsule().stroke(p.id == prog.id ? AvDBTheme.accentCyan : AvDBTheme.borderStroke, lineWidth: 1)
                                        )
                                    }
                                }
                            }
                            .padding(.horizontal, 16)
                        }

                        // Program Overview
                        GlassCard(cornerRadius: 16) {
                            VStack(alignment: .leading, spacing: 8) {
                                HStack {
                                    VStack(alignment: .leading, spacing: 2) {
                                        Text(prog.programName)
                                            .font(.system(size: 20, weight: .bold))
                                            .foregroundColor(AvDBTheme.primaryText)
                                        Text(prog.carrierName)
                                            .font(.system(size: 13))
                                            .foregroundColor(AvDBTheme.secondaryText)
                                    }
                                    Spacer()
                                    if let alliance = prog.activeAlliance {
                                        Text(alliance)
                                            .font(.system(size: 11, weight: .bold))
                                            .padding(.horizontal, 8)
                                            .padding(.vertical, 4)
                                            .background(AvDBTheme.surfaceElevated)
                                            .foregroundColor(AvDBTheme.accentCyan)
                                            .clipShape(Capsule())
                                    }
                                }
                            }
                        }
                        .padding(.horizontal, 16)

                        // Status Tiers
                        VStack(alignment: .leading, spacing: 12) {
                            Text("Elite Status Tiers & Upgrade Windows")
                                .font(.system(size: 14, weight: .bold))
                                .foregroundColor(AvDBTheme.primaryText)
                                .padding(.horizontal, 16)

                            VStack(spacing: 10) {
                                ForEach(prog.tiers) { tier in
                                    GlassCard(cornerRadius: 12) {
                                        VStack(alignment: .leading, spacing: 6) {
                                            HStack {
                                                Text(tier.name)
                                                    .font(.system(size: 15, weight: .bold))
                                                    .foregroundColor(AvDBTheme.accentAmber)

                                                Spacer()

                                                Text("\(tier.upgradeWindowHours)h window")
                                                    .font(.system(size: 12, weight: .semibold))
                                                    .foregroundColor(AvDBTheme.accentCyan)
                                            }

                                            HStack(spacing: 12) {
                                                Text("\(tier.eqmRequired.formatted()) EQM")
                                                    .font(.system(size: 12, weight: .medium, design: .monospaced))
                                                    .foregroundColor(AvDBTheme.secondaryText)
                                                Text("•")
                                                    .foregroundColor(AvDBTheme.tertiaryText)
                                                Text("+\(tier.bonusMilesPercent)% bonus")
                                                    .font(.system(size: 12, weight: .medium))
                                                    .foregroundColor(AvDBTheme.accentGreen)

                                                if tier.loungeAccess {
                                                    Text("•")
                                                        .foregroundColor(AvDBTheme.tertiaryText)
                                                    Text("Lounge Access")
                                                        .font(.system(size: 11, weight: .semibold))
                                                        .foregroundColor(AvDBTheme.accentPurple)
                                                }
                                            }

                                            Text(tier.keyPerks)
                                                .font(.system(size: 12))
                                                .foregroundColor(AvDBTheme.tertiaryText)
                                        }
                                    }
                                }
                            }
                            .padding(.horizontal, 16)
                        }

                        // Bilateral Alliances Web
                        if !prog.partnerships.isEmpty {
                            VStack(alignment: .leading, spacing: 12) {
                                Text("Bilateral Partnerships & Historical Webs")
                                    .font(.system(size: 14, weight: .bold))
                                    .foregroundColor(AvDBTheme.primaryText)
                                    .padding(.horizontal, 16)

                                VStack(spacing: 10) {
                                    ForEach(prog.partnerships) { part in
                                        GlassCard(cornerRadius: 12) {
                                            VStack(alignment: .leading, spacing: 6) {
                                                HStack {
                                                    Text(part.partnerCarrierName)
                                                        .font(.system(size: 14, weight: .semibold))
                                                        .foregroundColor(AvDBTheme.primaryText)

                                                    Spacer()

                                                    Text("\(part.startYear) – \(part.endYear != nil ? "\(part.endYear!)" : "Present")")
                                                        .font(.system(size: 11, weight: .medium, design: .monospaced))
                                                        .foregroundColor(part.endYear == nil ? AvDBTheme.accentGreen : AvDBTheme.secondaryText)
                                                }

                                                Text(part.relationshipDepth)
                                                    .font(.system(size: 11, weight: .semibold))
                                                    .foregroundColor(AvDBTheme.accentBlue)

                                                Text(part.historicalNote)
                                                    .font(.system(size: 11))
                                                    .foregroundColor(AvDBTheme.secondaryText)
                                            }
                                        }
                                    }
                                }
                                .padding(.horizontal, 16)
                            }
                        }
                    }
                }
                .padding(.vertical, 16)
            }
            .navigationTitle("Loyalty & Alliances")
            .navigationBarTitleDisplayMode(.large)
            .avdbCanvas()
            .task {
                let loaded = await APIService.shared.getLoyaltyPrograms()
                self.programs = loaded
                self.selectedProgram = loaded.first
                self.isLoading = false
            }
        }
    }
}
