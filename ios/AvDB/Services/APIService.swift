import Foundation

/// Thread-safe actor responsible for communicating with AvDB FastAPI backend and providing intelligent offline fallback.
public actor APIService {
    public static let shared = APIService()

    private let session: URLSession
    private var cache: [String: (data: Data, timestamp: Date)] = [:]
    private let ttl: TimeInterval = 3600 // 1 hour cache

    private init() {
        let config = URLSessionConfiguration.default
        config.timeoutIntervalForRequest = 15
        config.waitsForConnectivity = true
        self.session = URLSession(configuration: config)
    }

    // MARK: - Generic Fetch with Cache & Mock Fallback
    public func fetch<T: Decodable & Sendable>(
        _ endpoint: String,
        queryItems: [URLQueryItem] = [],
        fallback: @Sendable () -> T
    ) async -> T {
        let env = AppConfiguration.currentEnvironment
        if env == .offlineDemo {
            return fallback()
        }

        var url = env.baseURL
        for comp in endpoint.split(separator: "/") {
            url.appendPathComponent(String(comp))
        }

        var components = URLComponents(url: url, resolvingAgainstBaseURL: true)
        if !queryItems.isEmpty {
            components?.queryItems = queryItems
        }

        guard let requestURL = components?.url else {
            return fallback()
        }

        // Check in-memory cache
        if let cached = cache[requestURL.absoluteString],
           Date().timeIntervalSince(cached.timestamp) < ttl,
           let decoded = try? JSONDecoder().decode(T.self, from: cached.data) {
            return decoded
        }

        do {
            let (data, response) = try await session.data(from: requestURL)
            guard let httpResp = response as? HTTPURLResponse, (200...299).contains(httpResp.statusCode) else {
                return fallback()
            }
            let decoded = try JSONDecoder().decode(T.self, from: data)
            cache[requestURL.absoluteString] = (data, Date())
            return decoded
        } catch {
            print("AvDB API fetch fallback for \(requestURL.absoluteString): \(error.localizedDescription)")
            return fallback()
        }
    }

    // MARK: - Curated Airports
    public func getAirports() async -> [Airport] {
        await fetch("airports") {
            [
                Airport(iata: "ATL", name: "Hartsfield-Jackson Atlanta Intl", city: "Atlanta", state: "GA", latitude: 33.6407, longitude: -84.4277, catchmentMarket: "ATL", isMajorHub: true),
                Airport(iata: "ORD", name: "O'Hare International", city: "Chicago", state: "IL", latitude: 41.9742, longitude: -87.9073, catchmentMarket: "CHI", isMajorHub: true),
                Airport(iata: "DFW", name: "Dallas/Fort Worth Intl", city: "Dallas", state: "TX", latitude: 32.8998, longitude: -97.0403, catchmentMarket: "DFW", isMajorHub: true),
                Airport(iata: "DEN", name: "Denver International", city: "Denver", state: "CO", latitude: 39.8561, longitude: -104.6737, catchmentMarket: "DEN", isMajorHub: true),
                Airport(iata: "LAX", name: "Los Angeles International", city: "Los Angeles", state: "CA", latitude: 33.9416, longitude: -118.4085, catchmentMarket: "LAX", isMajorHub: true),
                Airport(iata: "SEA", name: "Seattle-Tacoma International", city: "Seattle", state: "WA", latitude: 47.4502, longitude: -122.3088, catchmentMarket: "SEA", isMajorHub: true),
                Airport(iata: "SFO", name: "San Francisco International", city: "San Francisco", state: "CA", latitude: 37.6213, longitude: -122.3790, catchmentMarket: "SFO", isMajorHub: true),
                Airport(iata: "JFK", name: "John F. Kennedy International", city: "New York", state: "NY", latitude: 40.6413, longitude: -73.7781, catchmentMarket: "NYC", isMajorHub: true),
                Airport(iata: "EWR", name: "Newark Liberty International", city: "Newark", state: "NJ", latitude: 40.6895, longitude: -74.1745, catchmentMarket: "NYC", isMajorHub: true),
                Airport(iata: "LGA", name: "LaGuardia Airport", city: "New York", state: "NY", latitude: 40.7769, longitude: -73.8740, catchmentMarket: "NYC", isMajorHub: true),
                Airport(iata: "BOS", name: "Boston Logan International", city: "Boston", state: "MA", latitude: 42.3656, longitude: -71.0096, catchmentMarket: "BOS", isMajorHub: true),
                Airport(iata: "CLT", name: "Charlotte Douglas International", city: "Charlotte", state: "NC", latitude: 35.2144, longitude: -80.9473, catchmentMarket: "CLT", isMajorHub: true),
                Airport(iata: "MIA", name: "Miami International", city: "Miami", state: "FL", latitude: 25.7959, longitude: -80.2870, catchmentMarket: "MIA", isMajorHub: true),
                Airport(iata: "PHX", name: "Phoenix Sky Harbor", city: "Phoenix", state: "AZ", latitude: 33.4373, longitude: -112.0078, catchmentMarket: "PHX", isMajorHub: true),
                Airport(iata: "MSP", name: "Minneapolis-St. Paul Intl", city: "Minneapolis", state: "MN", latitude: 44.8848, longitude: -93.2223, catchmentMarket: "MSP", isMajorHub: true),
                Airport(iata: "DTW", name: "Detroit Metropolitan", city: "Detroit", state: "MI", latitude: 42.2162, longitude: -83.3554, catchmentMarket: "DTW", isMajorHub: true),
                Airport(iata: "SLC", name: "Salt Lake City International", city: "Salt Lake City", state: "UT", latitude: 40.7899, longitude: -111.9791, catchmentMarket: "SLC", isMajorHub: true),
                Airport(iata: "IAH", name: "George Bush Intercontinental", city: "Houston", state: "TX", latitude: 29.9902, longitude: -95.3368, catchmentMarket: "HOU", isMajorHub: true),
                Airport(iata: "IAD", name: "Washington Dulles International", city: "Dulles", state: "VA", latitude: 38.9531, longitude: -77.4565, catchmentMarket: "WAS", isMajorHub: true),
                Airport(iata: "DCA", name: "Ronald Reagan Washington Natl", city: "Arlington", state: "VA", latitude: 38.8512, longitude: -77.0402, catchmentMarket: "WAS", isMajorHub: true),
                Airport(iata: "PDX", name: "Portland International", city: "Portland", state: "OR", latitude: 45.5898, longitude: -122.5951, catchmentMarket: "PDX", isMajorHub: false),
                Airport(iata: "SAN", name: "San Diego International", city: "San Diego", state: "CA", latitude: 32.7338, longitude: -117.1933, catchmentMarket: "SAN", isMajorHub: false),
                Airport(iata: "HNL", name: "Daniel K. Inouye Intl", city: "Honolulu", state: "HI", latitude: 21.3187, longitude: -157.9224, catchmentMarket: "HNL", isMajorHub: true),
                Airport(iata: "ANC", name: "Ted Stevens Anchorage Intl", city: "Anchorage", state: "AK", latitude: 61.1743, longitude: -149.9962, catchmentMarket: "ANC", isMajorHub: true)
            ]
        }
    }

    // MARK: - Airport KPIs
    public func getAirportKPIs(
        iata: String,
        year: Int = 2024,
        passengerOnly: Bool = true,
        minDepartures: Int = 10
    ) async -> AirportKPIs {
        let qItems = [
            URLQueryItem(name: "year", value: String(year)),
            URLQueryItem(name: "passenger_only", value: String(passengerOnly)),
            URLQueryItem(name: "min_departures", value: String(minDepartures))
        ]
        return await fetch("airports/\(iata)/kpis", queryItems: qItems) {
            AirportKPIs(
                totalDepartures: 28410,
                totalSeats: 4890200,
                totalPassengers: 4120300,
                loadFactor: 0.842,
                nonstopDestinations: 148,
                avgOdFare: 218.50,
                leadingCarrier: "DL",
                leadingCarrierShare: 0.542
            )
        }
    }

    // MARK: - Airport Longitudinal Timeline
    public func getAirportTimeline(
        iata: String,
        passengerOnly: Bool = true,
        minDepartures: Int = 10
    ) async -> [AirportTimelinePoint] {
        let qItems = [
            URLQueryItem(name: "passenger_only", value: String(passengerOnly)),
            URLQueryItem(name: "min_departures", value: String(minDepartures))
        ]
        return await fetch("airports/\(iata)/timeline", queryItems: qItems) {
            var mock: [AirportTimelinePoint] = []
            for yr in 2000...2024 {
                let factor = 1.0 + Double(yr - 2000) * 0.03
                let pax = Int(Double(32_000_000) * factor * (yr == 2020 ? 0.45 : (yr == 2021 ? 0.75 : 1.0)))
                let deps = Int(Double(pax) / 142.0)
                let seats = Int(Double(pax) / 0.84)
                mock.append(AirportTimelinePoint(
                    year: yr,
                    totalPassengers: pax,
                    totalDepartures: deps,
                    totalSeats: seats,
                    loadFactorPct: 84.2,
                    directDestinations: 125,
                    avgOdFare: 185.0 + Double(yr - 2000) * 2.8
                ))
            }
            return mock
        }
    }

    // MARK: - Airport Carrier Market Share
    public func getAirportCarriers(
        iata: String,
        year: Int = 2024,
        passengerOnly: Bool = true
    ) async -> [AirportCarrierShare] {
        let qItems = [
            URLQueryItem(name: "year", value: String(year)),
            URLQueryItem(name: "passenger_only", value: String(passengerOnly))
        ]
        return await fetch("airports/\(iata)/carriers", queryItems: qItems) {
            [
                AirportCarrierShare(uniqueCarrier: "DL", carrierName: "Delta Air Lines", departuresPerformed: 45000, totalSeats: 7500000, operationalPassengers: 6400000, loadFactorPct: 85.3, seatSharePct: 48.5, avgFare: 224.0),
                AirportCarrierShare(uniqueCarrier: "UA", carrierName: "United Airlines", departuresPerformed: 22000, totalSeats: 3600000, operationalPassengers: 3050000, loadFactorPct: 84.7, seatSharePct: 23.3, avgFare: 218.0),
                AirportCarrierShare(uniqueCarrier: "AA", carrierName: "American Airlines", departuresPerformed: 15000, totalSeats: 2400000, operationalPassengers: 2020000, loadFactorPct: 84.2, seatSharePct: 15.5, avgFare: 235.0),
                AirportCarrierShare(uniqueCarrier: "WN", carrierName: "Southwest Airlines", departuresPerformed: 12000, totalSeats: 1900000, operationalPassengers: 1610000, loadFactorPct: 84.7, seatSharePct: 12.3, avgFare: 195.0),
            ]
        }
    }

    // MARK: - Outbound Routes
    public func getOutboundRoutes(
        iata: String,
        year: Int = 2024,
        passengerOnly: Bool = true,
        minDepartures: Int = 10
    ) async -> [OutboundRoute] {
        let qItems = [
            URLQueryItem(name: "year", value: String(year)),
            URLQueryItem(name: "passenger_only", value: String(passengerOnly)),
            URLQueryItem(name: "min_departures", value: String(minDepartures))
        ]
        return await fetch("airports/\(iata)/routes", queryItems: qItems) {
            APIService.generateFallbackRoutes(for: iata)
        }
    }

    public static func generateFallbackRoutes(for origin: String) -> [OutboundRoute] {
        struct DestMeta {
            let code: String
            let lat: Double
            let lon: Double
            let carrier: String
            let baseFare: Double
        }

        let hubs: [DestMeta] = [
            DestMeta(code: "LGA", lat: 40.7769, lon: -73.8740, carrier: "DL", baseFare: 215.0),
            DestMeta(code: "LAX", lat: 33.9416, lon: -118.4085, carrier: "UA", baseFare: 285.0),
            DestMeta(code: "DFW", lat: 32.8998, lon: -97.0403, carrier: "AA", baseFare: 210.0),
            DestMeta(code: "DEN", lat: 39.8561, lon: -104.6737, carrier: "UA", baseFare: 185.0),
            DestMeta(code: "SFO", lat: 37.6213, lon: -122.3790, carrier: "UA", baseFare: 295.0),
            DestMeta(code: "SEA", lat: 47.4502, lon: -122.3088, carrier: "AS", baseFare: 298.0),
            DestMeta(code: "ATL", lat: 33.6407, lon: -84.4277, carrier: "DL", baseFare: 195.0),
            DestMeta(code: "ORD", lat: 41.9742, lon: -87.9073, carrier: "UA", baseFare: 220.0),
            DestMeta(code: "BOS", lat: 42.3656, lon: -71.0096, carrier: "B6", baseFare: 225.0),
            DestMeta(code: "MIA", lat: 25.7959, lon: -80.2870, carrier: "AA", baseFare: 245.0),
            DestMeta(code: "PHX", lat: 33.4373, lon: -112.0078, carrier: "AA", baseFare: 215.0),
            DestMeta(code: "MCO", lat: 28.4312, lon: -81.3081, carrier: "WN", baseFare: 175.0),
            DestMeta(code: "LAS", lat: 36.0840, lon: -115.1537, carrier: "WN", baseFare: 190.0),
            DestMeta(code: "MSP", lat: 44.8848, lon: -93.2223, carrier: "DL", baseFare: 165.0),
            DestMeta(code: "DTW", lat: 42.2162, lon: -83.3554, carrier: "DL", baseFare: 170.0),
            DestMeta(code: "CLT", lat: 35.2144, lon: -80.9473, carrier: "AA", baseFare: 198.0),
            DestMeta(code: "SAN", lat: 32.7338, lon: -117.1933, carrier: "AS", baseFare: 260.0),
            DestMeta(code: "HNL", lat: 21.3187, lon: -157.9224, carrier: "UA", baseFare: 420.0)
        ]

        let originCoord = hubs.first(where: { $0.code == origin }) ?? DestMeta(code: origin, lat: 41.9742, lon: -87.9073, carrier: "UA", baseFare: 200.0)

        var results: [OutboundRoute] = []
        for dest in hubs {
            guard dest.code != origin else { continue } // Strictly prevent circular origin-origin routes

            let dLat = dest.lat - originCoord.lat
            let dLon = dest.lon - originCoord.lon
            let approxMiles = max(120.0, sqrt(dLat * dLat + dLon * dLon) * 60.0)
            let departures = Int.random(in: 600...2400)
            let seats = departures * 160
            let loadFactor = Double.random(in: 0.82...0.89)
            let pax = Int(Double(seats) * loadFactor)

            results.append(OutboundRoute(
                origin: origin,
                destination: dest.code,
                carrier: dest.carrier,
                departures: departures,
                seats: seats,
                passengers: pax,
                loadFactor: loadFactor,
                distanceMiles: round(approxMiles),
                avgOdFare: dest.baseFare,
                originLat: originCoord.lat,
                originLon: originCoord.lon,
                destLat: dest.lat,
                destLon: dest.lon
            ))
        }
        return results.sorted(by: { $0.passengers > $1.passengers })
    }

    // MARK: - Airlines
    public func getAirlines() async -> [Airline] {
        await fetch("airlines") {
            [
                Airline(code: "AS", name: "Alaska Airlines", hexColor: "#01426A", alliance: "oneworld", primaryHubs: ["SEA", "PDX", "ANC", "SFO", "LAX", "HNL"], headquarters: "Seattle, WA"),
                Airline(code: "DL", name: "Delta Air Lines", hexColor: "#E51937", alliance: "SkyTeam", primaryHubs: ["ATL", "DTW", "MSP", "SLC", "SEA", "JFK", "BOS", "LAX"], headquarters: "Atlanta, GA"),
                Airline(code: "UA", name: "United Airlines", hexColor: "#005DAA", alliance: "Star Alliance", primaryHubs: ["ORD", "DEN", "IAH", "EWR", "SFO", "IAD", "LAX"], headquarters: "Chicago, IL"),
                Airline(code: "AA", name: "American Airlines", hexColor: "#0078D2", alliance: "oneworld", primaryHubs: ["DFW", "CLT", "MIA", "ORD", "PHX", "PHL", "LGA", "DCA"], headquarters: "Fort Worth, TX"),
                Airline(code: "WN", name: "Southwest Airlines", hexColor: "#304CB2", alliance: nil, primaryHubs: ["MDW", "DAL", "DEN", "LAS", "BWI", "PHX", "HOU"], headquarters: "Dallas, TX"),
                Airline(code: "B6", name: "JetBlue Airways", hexColor: "#00205B", alliance: nil, primaryHubs: ["JFK", "BOS", "FLL", "MCO"], headquarters: "Long Island City, NY"),
                Airline(code: "NK", name: "Spirit Airlines", hexColor: "#F3C300", alliance: nil, primaryHubs: ["FLL", "MCO", "DTW", "LAS", "DFW"], headquarters: "Dania Beach, FL"),
                Airline(code: "F9", name: "Frontier Airlines", hexColor: "#006643", alliance: nil, primaryHubs: ["DEN", "MCO", "LAS", "PHX", "ATL"], headquarters: "Denver, CO"),
                Airline(code: "G4", name: "Allegiant Air", hexColor: "#00529B", alliance: nil, primaryHubs: ["SFB", "PIE", "PGD", "LAS", "AZA"], headquarters: "Las Vegas, NV"),
                Airline(code: "HA", name: "Hawaiian Airlines", hexColor: "#5D2A68", alliance: "oneworld", primaryHubs: ["HNL", "OGG"], headquarters: "Honolulu, HI", isActive: true, mergerNote: "Acquired by Alaska Airlines in 2024"),
                Airline(code: "CO", name: "Continental Airlines", hexColor: "#0A3161", alliance: "Star Alliance", primaryHubs: ["IAH", "EWR", "CLE"], headquarters: "Houston, TX", isActive: false, mergerNote: "Merged with United Airlines in 2010"),
                Airline(code: "NW", name: "Northwest Airlines", hexColor: "#C00000", alliance: "SkyTeam", primaryHubs: ["MSP", "DTW", "MEM"], headquarters: "Eagan, MN", isActive: false, mergerNote: "Merged with Delta Air Lines in 2008"),
                Airline(code: "US", name: "US Airways", hexColor: "#1E2A38", alliance: "Star Alliance", primaryHubs: ["CLT", "PHL", "PHX"], headquarters: "Tempe, AZ", isActive: false, mergerNote: "Merged with American Airlines in 2013"),
                Airline(code: "HP", name: "America West Airlines", hexColor: "#2E7D32", alliance: nil, primaryHubs: ["PHX", "LAS"], headquarters: "Tempe, AZ", isActive: false, mergerNote: "Merged with US Airways in 2005 / American 2013"),
                Airline(code: "TW", name: "Trans World Airlines (TWA)", hexColor: "#B30838", alliance: nil, primaryHubs: ["STL", "JFK"], headquarters: "St. Louis, MO", isActive: false, mergerNote: "Acquired by American Airlines in 2001"),
                Airline(code: "VX", name: "Virgin America", hexColor: "#D81B60", alliance: nil, primaryHubs: ["SFO", "LAX"], headquarters: "Burlingame, CA", isActive: false, mergerNote: "Acquired by Alaska Airlines in 2016")
            ]
        }
    }

    // MARK: - Airline KPIs
    public func getAirlineKPIs(code: String, year: Int = 2024) async -> AirlineKPIs {
        let qItems = [URLQueryItem(name: "year", value: String(year))]
        return await fetch("airlines/\(code)/kpis", queryItems: qItems) {
            AirlineKPIs(
                activeRoutes: 842,
                departures: 87400,
                totalSeats: 14200000,
                totalPassengers: 12070000,
                loadFactor: 0.850,
                asmBillions: 18.4,
                rpmBillions: 15.6,
                avgOdFare: 242.80,
                yieldPerMile: 0.184
            )
        }
    }

    // MARK: - Airline Timeline
    public func getAirlineTimeline(code: String) async -> [AirlineTimelinePoint] {
        await fetch("airlines/\(code)/timeline") {
            var mock: [AirlineTimelinePoint] = []
            for yr in 2000...2024 {
                let factor = 1.0 + Double(yr - 2000) * 0.04
                let asm = (yr == 2020 ? 12.0 : (yr == 2021 ? 18.0 : 25.0 * factor))
                let rpm = asm * 0.84
                mock.append(AirlineTimelinePoint(
                    year: yr,
                    asmBillions: asm,
                    rpmBillions: rpm,
                    systemLoadFactor: 84.5,
                    totalPassengers: Int(rpm * 1_000_000_000 / 1100),
                    totalDepartures: Int(asm * 1_000_000_000 / 160_000),
                    avgNetworkFare: 195.0 + Double(yr - 2000) * 2.2,
                    avgYieldPerMile: 0.175 + Double(yr - 2000) * 0.001
                ))
            }
            return mock
        }
    }

    // MARK: - Airline Yield Curve
    public func getAirlineYieldCurve(code: String, year: Int = 2024) async -> [YieldCurvePoint] {
        let qItems = [URLQueryItem(name: "year", value: String(year))]
        return await fetch("airlines/\(code)/yield-curve", queryItems: qItems) {
            [
                YieldCurvePoint(origin: "SEA", dest: "PDX", routeLabel: "SEA-PDX", stageLengthMiles: 129, avgOdFare: 115, yieldPerMile: 0.8915, operationalPassengers: 450000, loadFactorPct: 82.4),
                YieldCurvePoint(origin: "SEA", dest: "SFO", routeLabel: "SEA-SFO", stageLengthMiles: 679, avgOdFare: 168, yieldPerMile: 0.2474, operationalPassengers: 580000, loadFactorPct: 85.1),
                YieldCurvePoint(origin: "ORD", dest: "LGA", routeLabel: "ORD-LGA", stageLengthMiles: 733, avgOdFare: 215, yieldPerMile: 0.2933, operationalPassengers: 720000, loadFactorPct: 86.3),
                YieldCurvePoint(origin: "ORD", dest: "LAX", routeLabel: "ORD-LAX", stageLengthMiles: 1745, avgOdFare: 285, yieldPerMile: 0.1633, operationalPassengers: 810000, loadFactorPct: 87.4),
                YieldCurvePoint(origin: "SFO", dest: "JFK", routeLabel: "SFO-JFK", stageLengthMiles: 2586, avgOdFare: 345, yieldPerMile: 0.1334, operationalPassengers: 690000, loadFactorPct: 88.0)
            ]
        }
    }

    // MARK: - Fleet Families
    public func getFleetFamilies() async -> [FleetFamily] {
        await fetch("fleet") {
            [
                FleetFamily(
                    familyName: "Airbus A320 Family",
                    manufacturer: "Airbus",
                    totalDepartures: 342000,
                    totalSeats: 58140000,
                    avgGauge: 170.0,
                    dominantOperators: ["AA", "DL", "UA", "B6", "NK", "F9"],
                    subfleets: [
                        Subfleet(aircraftType: "A321neo", typicalSeats: 200, engineType: "PW1100G / CFM LEAP-1A", departures: 98000, seats: 19600000, avgStageLength: 1280),
                        Subfleet(aircraftType: "A320neo", typicalSeats: 165, engineType: "CFM LEAP-1A / PW1100G", departures: 120000, seats: 19800000, avgStageLength: 950),
                        Subfleet(aircraftType: "A319ceo", typicalSeats: 128, engineType: "CFM56-5B", departures: 75000, seats: 9600000, avgStageLength: 820)
                    ]
                ),
                FleetFamily(
                    familyName: "Boeing 737 Family",
                    manufacturer: "Boeing",
                    totalDepartures: 412000,
                    totalSeats: 67980000,
                    avgGauge: 165.0,
                    dominantOperators: ["WN", "UA", "AA", "AS"],
                    subfleets: [
                        Subfleet(aircraftType: "737 MAX 9", typicalSeats: 178, engineType: "CFM LEAP-1B", departures: 64000, seats: 11392000, avgStageLength: 1420),
                        Subfleet(aircraftType: "737 MAX 8", typicalSeats: 175, engineType: "CFM LEAP-1B", departures: 158000, seats: 27650000, avgStageLength: 1150),
                        Subfleet(aircraftType: "737-800", typicalSeats: 160, engineType: "CFM56-7B", departures: 190000, seats: 30400000, avgStageLength: 980)
                    ]
                ),
                FleetFamily(
                    familyName: "McDonnell Douglas DC-9 / MD-80 Family",
                    manufacturer: "McDonnell Douglas",
                    totalDepartures: 18200,
                    totalSeats: 2639000,
                    avgGauge: 145.0,
                    dominantOperators: ["DL", "AA", "NW", "CO", "OZ", "RC"],
                    subfleets: [
                        Subfleet(aircraftType: "MD-88 / MD-90", typicalSeats: 149, engineType: "JT8D-219 / V2500", departures: 11200, seats: 1668800, avgStageLength: 720),
                        Subfleet(aircraftType: "DC-9-30/50", typicalSeats: 115, engineType: "Pratt & Whitney JT8D", departures: 7000, seats: 805000, avgStageLength: 540)
                    ]
                ),
                FleetFamily(
                    familyName: "Boeing 787 Dreamliner",
                    manufacturer: "Boeing",
                    totalDepartures: 42000,
                    totalSeats: 11760000,
                    avgGauge: 280.0,
                    dominantOperators: ["UA", "AA"],
                    subfleets: [
                        Subfleet(aircraftType: "787-9", typicalSeats: 285, engineType: "GEnx-1B / Trent 1000", departures: 28000, seats: 7980000, avgStageLength: 3950),
                        Subfleet(aircraftType: "787-8", typicalSeats: 242, engineType: "GEnx-1B", departures: 14000, seats: 3388000, avgStageLength: 3400)
                    ]
                )
            ]
        }
    }

    // MARK: - Loyalty Programs
    public func getLoyaltyPrograms() async -> [LoyaltyProgram] {
        await fetch("loyalty") {
            [
                LoyaltyProgram(
                    carrierCode: "AS",
                    carrierName: "Alaska Airlines",
                    programName: "Mileage Plan",
                    activeAlliance: "oneworld",
                    tiers: [
                        LoyaltyTier(name: "MVP", eqmRequired: 20000, eqsRequired: 30, upgradeWindowHours: 48, bonusMilesPercent: 50, loungeAccess: false, keyPerks: "First class upgrades at 48h, 2 free checked bags"),
                        LoyaltyTier(name: "MVP Gold", eqmRequired: 40000, eqsRequired: 60, upgradeWindowHours: 72, bonusMilesPercent: 100, loungeAccess: false, keyPerks: "First class upgrades at 72h, companion upgrades"),
                        LoyaltyTier(name: "MVP Gold 75K", eqmRequired: 75000, eqsRequired: 90, upgradeWindowHours: 120, bonusMilesPercent: 125, loungeAccess: true, keyPerks: "50,000 bonus miles, 4 day lounge passes"),
                        LoyaltyTier(name: "MVP Gold 100K", eqmRequired: 100000, eqsRequired: 140, upgradeWindowHours: 120, bonusMilesPercent: 150, loungeAccess: true, keyPerks: "Top upgrade priority, international upgrade certificates")
                    ],
                    partnerships: [
                        LoyaltyPartnership(partnerCarrierCode: "CO", partnerCarrierName: "Continental Airlines", relationshipDepth: "Bilateral Reciprocal Earn/Burn", startYear: 1996, endYear: 2009, eliteReciprocal: true, loungeReciprocal: true, historicalNote: "Extensive reciprocal partnership prior to Continental's merger with United."),
                        LoyaltyPartnership(partnerCarrierCode: "NW", partnerCarrierName: "Northwest Airlines", relationshipDepth: "Bilateral Reciprocal Earn/Burn", startYear: 1997, endYear: 2008, eliteReciprocal: true, loungeReciprocal: true, historicalNote: "Shared Seattle and West Coast feed; ended after Delta acquired Northwest."),
                        LoyaltyPartnership(partnerCarrierCode: "DL", partnerCarrierName: "Delta Air Lines", relationshipDepth: "Codeshare & Reciprocal", startYear: 2004, endYear: 2017, eliteReciprocal: true, loungeReciprocal: true, historicalNote: "Longterm codeshare that disintegrated into the bitter 'Battle for Seattle' hub rivalry."),
                        LoyaltyPartnership(partnerCarrierCode: "BA", partnerCarrierName: "British Airways", relationshipDepth: "Full Alliance / oneworld", startYear: 2021, endYear: nil, eliteReciprocal: true, loungeReciprocal: true, historicalNote: "oneworld alliance member with seamless tier reciprocity.")
                    ]
                )
            ]
        }
    }
}
