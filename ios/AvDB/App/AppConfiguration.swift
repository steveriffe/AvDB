import Foundation

/// Central configuration for AvDB iOS client.
/// Manages backend API endpoints, authentication, caching policies, and developer metadata.
@MainActor
public final class AppConfiguration: ObservableObject {
    public static let shared = AppConfiguration()

    // MARK: - App Identity
    public let appName = "AvDB"
    public let appVersion = "1.0.0"
    public let bundleID = "steveriffe.AvDB"
    public let teamID = "JRM56GZN5H"
    public let developer = "Steve Riffe"

    // MARK: - Endpoints
    public enum Environment: String, CaseIterable, Identifiable, Sendable {
        case cloudRun = "Cloud Run (Production)"
        case localHost = "Localhost (Development)"
        case offlineDemo = "Offline Demo Mode"

        public var id: String { rawValue }

        public var baseURL: URL {
            switch self {
            case .cloudRun:
                return URL(string: "https://avdb-api-448864711884.us-west1.run.app/api")!
            case .localHost:
                return URL(string: "http://localhost:8000/api")!
            case .offlineDemo:
                return URL(string: "https://demo.avdb.local")!
            }
        }
    }

    nonisolated public static var currentEnvironment: Environment {
        let savedEnv = UserDefaults.standard.string(forKey: "avdb_environment")
        return Environment(rawValue: savedEnv ?? "") ?? .cloudRun
    }

    @Published public var selectedEnvironment: Environment {
        didSet {
            UserDefaults.standard.set(selectedEnvironment.rawValue, forKey: "avdb_environment")
        }
    }

    @Published public var enableHaptics: Bool {
        didSet {
            UserDefaults.standard.set(enableHaptics, forKey: "avdb_enable_haptics")
        }
    }

    @Published public var cacheTTLSeconds: TimeInterval = 3600

    private init() {
        let savedEnv = UserDefaults.standard.string(forKey: "avdb_environment")
        self.selectedEnvironment = Environment(rawValue: savedEnv ?? "") ?? .cloudRun
        self.enableHaptics = UserDefaults.standard.object(forKey: "avdb_enable_haptics") as? Bool ?? true
    }
}

