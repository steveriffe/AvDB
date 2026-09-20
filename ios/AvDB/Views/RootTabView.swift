import SwiftUI

public struct RootTabView: View {
    @State private var selectedTab: Int = 0
    @State private var showSettings: Bool = false

    public init() {}

    public var body: some View {
        TabView(selection: $selectedTab) {
            AirportsView()
                .tabItem {
                    Label("Airports", systemImage: "airplane.circle")
                }
                .tag(0)

            AirlinesView()
                .tabItem {
                    Label("Airlines", systemImage: "point.3.filled.connected.trianglepath.dotted")
                }
                .tag(1)

            FleetView()
                .tabItem {
                    Label("Fleet", systemImage: "airplane")
                }
                .tag(2)

            LoyaltyPartnershipsView()
                .tabItem {
                    Label("Loyalty", systemImage: "creditcard.fill")
                }
                .tag(3)

            FlightyView()
                .tabItem {
                    Label("Flighty Log", systemImage: "book.closed.fill")
                }
                .tag(4)
        }
        .tint(AvDBTheme.accentCyan)
        .toolbar {
            ToolbarItem(placement: .navigationBarTrailing) {
                Button {
                    showSettings = true
                } label: {
                    Image(systemName: "gearshape.fill")
                        .foregroundColor(AvDBTheme.secondaryText)
                }
            }
        }
        .sheet(isPresented: $showSettings) {
            SettingsView()
        }
    }
}

