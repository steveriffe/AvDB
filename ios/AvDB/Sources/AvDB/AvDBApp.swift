import SwiftUI

@main
public struct AvDBApp: App {
    public init() {}

    public var body: some Scene {
        WindowGroup {
            MainTabView()
                .preferredColorScheme(.dark) // Default to sleek midnight theme matching AvDB web
        }
    }
}
