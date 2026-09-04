import SwiftUI

/// Root Tab Navigation Controller for AvDB iOS App
public struct MainTabView: View {
    @State private var selectedTab: Int = 0

    public init() {}

    public var body: some View {
        TabView(selection: $selectedTab) {
            AirportsView()
                .tabItem {
                    Label("Airports", systemImage: "airplane.departure")
                }
                .tag(0)

            AirlinesView()
                .tabItem {
                    Label("Airlines", systemImage: "building.2")
                }
                .tag(1)

            FleetView()
                .tabItem {
                    Label("Fleet", systemImage: "airplane")
                }
                .tag(2)

            FlightyView()
                .tabItem {
                    Label("Flighty", systemImage: "ticket.fill")
                }
                .tag(3)

            SettingsView()
                .tabItem {
                    Label("Settings", systemImage: "gearshape.fill")
                }
                .tag(4)
        }
        .tint(.blue)
    }
}
