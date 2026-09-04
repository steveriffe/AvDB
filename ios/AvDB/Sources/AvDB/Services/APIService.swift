import Foundation

public enum APIError: LocalizedError, Sendable {
    case invalidURL
    case invalidResponse(statusCode: Int)
    case decodingError(String)
    case networkError(String)

    public var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "The API endpoint URL is invalid."
        case .invalidResponse(let statusCode):
            return "Server responded with status code \(statusCode)."
        case .decodingError(let details):
            return "Failed to parse API response: \(details)"
        case .networkError(let details):
            return "Network connection failed: \(details)"
        }
    }
}

/// Thread-safe Network Data Service for AvDB REST API
public actor APIService {
    public static let shared = APIService()

    private let session: URLSession
    private let decoder: JSONDecoder
    private var cache: [String: (timestamp: Date, data: Data)] = [:]
    private let cacheTTL: TimeInterval = 1800 // 30 minutes in-memory cache

    public init(session: URLSession = .shared) {
        self.session = session
        self.decoder = JSONDecoder()
        // Models have custom CodingKeys or snake_case matches
    }

    // MARK: - Core Generic Request Handler

    private func get<T: Decodable>(path: String, queryParams: [String: String] = [:], baseURL: String) async throws -> T {
        guard var components = URLComponents(string: "\(baseURL)\(path)") else {
            throw APIError.invalidURL
        }

        if !queryParams.isEmpty {
            components.queryItems = queryParams.map { URLQueryItem(name: $0.key, value: $0.value) }
        }

        guard let url = components.url else {
            throw APIError.invalidURL
        }

        let cacheKey = url.absoluteString

        // Check cache
        if let entry = cache[cacheKey], Date().timeIntervalSince(entry.timestamp) < cacheTTL {
            do {
                return try decoder.decode(T.self, from: entry.data)
            } catch {
                cache.removeValue(forKey: cacheKey)
            }
        }

        var request = URLRequest(url: url)
        request.httpMethod = "GET"
        request.timeoutInterval = 15.0
        request.setValue("application/json", forHTTPHeaderField: "Accept")

        do {
            let (data, response) = try await session.data(for: request)

            guard let httpResponse = response as? HTTPURLResponse else {
                throw APIError.invalidResponse(statusCode: -1)
            }

            guard (200...299).contains(httpResponse.statusCode) else {
                throw APIError.invalidResponse(statusCode: httpResponse.statusCode)
            }

            cache[cacheKey] = (Date(), data)

            do {
                return try decoder.decode(T.self, from: data)
            } catch let decodeErr {
                throw APIError.decodingError(decodeErr.localizedDescription)
            }
        } catch let err as APIError {
            throw err
        } catch {
            throw APIError.networkError(error.localizedDescription)
        }
    }

    // MARK: - Airport Endpoints

    public func fetchAirports(baseURL: String) async throws -> [Airport] {
        try await get(path: "/api/airports", baseURL: baseURL)
    }

    public func fetchAirportKPIs(code: String, year: Int, baseURL: String) async throws -> AirportKPIs {
        try await get(
            path: "/api/airports/\(code)/kpis",
            queryParams: ["year": "\(year)"],
            baseURL: baseURL
        )
    }

    public func fetchAirportRoutes(code: String, year: Int, minDepartures: Int = 10, baseURL: String) async throws -> [RouteItem] {
        try await get(
            path: "/api/airports/\(code)/routes",
            queryParams: [
                "year": "\(year)",
                "min_departures": "\(minDepartures)"
            ],
            baseURL: baseURL
        )
    }

    public func fetchCatchment(code: String, baseURL: String) async throws -> CatchmentInfo? {
        do {
            return try await get(path: "/api/airports/\(code)/catchment", baseURL: baseURL)
        } catch {
            return nil
        }
    }

    // MARK: - Airline Endpoints

    public func fetchAirlineKPIs(code: String, year: Int, baseURL: String) async throws -> AirlineKPIs {
        try await get(
            path: "/api/airlines/\(code)/kpis",
            queryParams: ["year": "\(year)"],
            baseURL: baseURL
        )
    }

    public func fetchAirlineNetwork(code: String, year: Int, minDepartures: Int = 20, baseURL: String) async throws -> AirlineNetworkResponse {
        try await get(
            path: "/api/airlines/\(code)/network",
            queryParams: [
                "year": "\(year)",
                "min_departures": "\(minDepartures)"
            ],
            baseURL: baseURL
        )
    }

    public func fetchAirlineYieldCurve(code: String, year: Int, baseURL: String) async throws -> [YieldCurvePoint] {
        try await get(
            path: "/api/airlines/\(code)/yield-curve",
            queryParams: ["year": "\(year)"],
            baseURL: baseURL
        )
    }

    // MARK: - Fleet Endpoints

    public func fetchFleetSummary(family: String, year: Int, baseURL: String) async throws -> FleetSummaryResponse {
        try await get(
            path: "/api/fleet/summary",
            queryParams: [
                "family": family,
                "year": "\(year)"
            ],
            baseURL: baseURL
        )
    }

    public func clearCache() {
        cache.removeAll()
    }
}
