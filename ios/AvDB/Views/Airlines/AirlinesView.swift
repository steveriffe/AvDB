import SwiftUI

public struct AirlinesView: View {
    @State private var airlines: [Airline] = []
    @State private var isLoading: Bool = true

    public init() {}

    public var body: some View {
        NavigationStack {
            ScrollView {
                LazyVStack(spacing: 12) {
                    if isLoading {
                        ProgressView()
                            .tint(AvDBTheme.accentBlue)
                            .padding(.top, 40)
                    } else {
                        ForEach(airlines) { airline in
                            NavigationLink(destination: AirlineDetailView(airline: airline)) {
                                airlineCard(airline)
                            }
                            .buttonStyle(.plain)
                        }
                    }
                }
                .padding(.horizontal, 16)
                .padding(.top, 8)
            }
            .navigationTitle("Airlines Network")
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
                        if let alliance = airline.alliance {
                            Text(alliance)
                                .font(.system(size: 10, weight: .bold))
                                .padding(.horizontal, 7)
                                .padding(.vertical, 3)
                                .background(AvDBTheme.surfaceElevated)
                                .foregroundColor(AvDBTheme.secondaryText)
                                .clipShape(Capsule())
                        }
                    }

                    Text("Hubs: \(airline.primaryHubs.prefix(4).joined(separator: ", "))")
                        .font(.system(size: 12))
                        .foregroundColor(AvDBTheme.secondaryText)
                }

                Image(systemName: "chevron.right")
                    .font(.system(size: 13, weight: .semibold))
                    .foregroundColor(AvDBTheme.tertiaryText)
            }
        }
    }
}

