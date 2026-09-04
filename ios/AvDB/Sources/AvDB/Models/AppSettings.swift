import Foundation
import SwiftUI

public enum MapThemeStyle: String, CaseIterable, Identifiable, Sendable {
    case inFlightPaper = "Classic In-Flight Paper"
    case midnightNavy = "Midnight Navy"
    case minimalSlate = "Minimal Slate"
    case standardApple = "Standard Apple Map"
    case mapboxPersonal = "Mapbox Personal"
    case mapboxLove = "Mapbox Love"
    case mapboxMono = "Mapbox Mono"

    public var id: String { rawValue }

    public var icon: String {
        switch self {
        case .inFlightPaper: return "newspaper"
        case .midnightNavy: return "moon.stars"
        case .minimalSlate: return "square.2.layers.3d"
        case .standardApple: return "map"
        case .mapboxPersonal: return "person.crop.circle"
        case .mapboxLove: return "heart.fill"
        case .mapboxMono: return "circle.lefthalf.filled"
        }
    }
}

public enum APIEnvironment: String, CaseIterable, Identifiable, Sendable {
    case productionCloudRun = "Cloud Run (api.avdb.riffe.co.uk)"
    case localSimulator = "Localhost (127.0.0.1:8000)"
    case localLan = "Local Network (Custom IP)"

    public var id: String { rawValue }

    public var defaultURL: String {
        switch self {
        case .productionCloudRun:
            return "https://api.avdb.riffe.co.uk"
        case .localSimulator:
            return "http://127.0.0.1:8000"
        case .localLan:
            return "http://192.168.1.100:8000"
        }
    }
}

@MainActor
public final class AppSettings: ObservableObject {
    public static let shared = AppSettings()

    @AppStorage("apiEnvironment") public var environment: APIEnvironment = .productionCloudRun
    @AppStorage("customApiBaseUrl") public var customApiBaseUrl: String = "https://api.avdb.riffe.co.uk"
    @AppStorage("reportingYear") public var reportingYear: Int = 2023
    @AppStorage("selectedMapTheme") public var mapTheme: MapThemeStyle = .midnightNavy

    // Mapbox custom tokens and style URLs
    @AppStorage("mapboxToken") public var mapboxToken: String = ""
    @AppStorage("mapboxStylePersonal") public var mapboxStylePersonal: String = ""
    @AppStorage("mapboxStyleLove") public var mapboxStyleLove: String = ""
    @AppStorage("mapboxStyleMono") public var mapboxStyleMono: String = ""

    // Auth tokens
    @AppStorage("authToken") public var authToken: String = ""

    public var activeApiBaseURL: String {
        switch environment {
        case .productionCloudRun:
            return "https://api.avdb.riffe.co.uk"
        case .localSimulator:
            return "http://127.0.0.1:8000"
        case .localLan:
            return customApiBaseUrl.isEmpty ? "http://192.168.1.100:8000" : customApiBaseUrl
        }
    }
}
