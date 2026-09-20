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
    public func fetch<T: Decodable>(_ endpoint: String, fallback: () -> T) async -> T {
        let env = AppConfiguration.shared.selectedEnvironment
        if env == .offlineDemo {
            return fallback()
        }

        let fullURL = env.baseURL.appendingPathComponent(endpoint)

        // Check in-memory cache
        if let cached = cache[fullURL.absoluteString],
           Date().timeIntervalSince(cached.timestamp) < ttl,
           let decoded = try? JSONDecoder().decode(T.self, from: cached.data) {
            return decoded
        }

        do {
            let (data, response) = try await session.data(from: fullURL)
            guard let httpResp = response as? HTTPURLResponse, (200...299).contains(httpResp.statusCode) else {
                return fallback()
            }
            cache[fullURL.absoluteString] = (data, Date())
            return try JSONDecoder().decode(T.self, from: data)
        } catch {
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
    public func getAirportKPIs(iata: String) async -> AirportKPIs {
        await fetch("airports/\(iata)/kpis") {
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

    // MARK: - Outbound Routes
    public func getOutboundRoutes(iata: String) async -> [OutboundRoute] {
        await fetch("airports/\(iata)/routes") {
            [
                OutboundRoute(origin: iata, destination: "ORD", carrier: "UA", departures: 1240, seats: 198400, passengers: 168640, loadFactor: 0.85, distanceMiles: 606, avgOdFare: 192.40),
                OutboundRoute(origin: iata, destination: "DFW", carrier: "AA", departures: 1120, seats: 179200, passengers: 154112, loadFactor: 0.86, distanceMiles: 731, avgOdFare: 215.10),
                OutboundRoute(origin: iata, destination: "LAX", carrier: "DL", departures: 980, seats: 186200, passengers: 161994, loadFactor: 0.87, distanceMiles: 1946, avgOdFare: 284.90),
                OutboundRoute(origin: iata, destination: "DEN", carrier: "UA", departures: 890, seats: 151300, passengers: 128605, loadFactor: 0.85, distanceMiles: 1199, avgOdFare: 185.00),
                OutboundRoute(origin: iata, destination: "SEA", carrier: "AS", departures: 760, seats: 121600, passengers: 104576, loadFactor: 0.86, distanceMiles: 2182, avgOdFare: 298.50)
            ]
        }
    }

    // MARK: - Airlines
    public func getAirlines() async -> [Airline] {
        await fetch("airlines") {
            [
                Airline(code: "DL", name: "Delta Air Lines", hexColor: "#E51937", alliance: "SkyTeam", primaryHubs: ["ATL", "DTW", "MSP", "SLC", "SEA", "JFK", "BOS", "LAX"], headquarters: "Atlanta, GA"),
                Airline(code: "UA", name: "United Airlines", hexColor: "#005DAA", alliance: "Star Alliance", primaryHubs: ["ORD", "DEN", "IAH", "EWR", "SFO", "IAD", "LAX"], headquarters: "Chicago, IL"),
                Airline(code: "AA", name: "American Airlines", hexColor: "#0078D2", alliance: "oneworld", primaryHubs: ["DFW", "CLT", "MIA", "ORD", "PHX", "PHL", "LGA", "DCA"], headquarters: "Fort Worth, TX"),
                Airline(code: "AS", name: "Alaska Airlines", hexColor: "#01426A", alliance: "oneworld", primaryHubs: ["SEA", "PDX", "SFO", "LAX", "ANC", "HNL"], headquarters: "Seattle, WA"),
                Airline(code: "WN", name: "Southwest Airlines", hexColor: "#304CB2", alliance: nil, primaryHubs: ["MDW", "DAL", "DEN", "LAS", "BWI", "PHX", "HOU"], headquarters: "Dallas, TX"),
                Airline(code: "B6", name: "JetBlue Airways", hexColor: "#00205B", alliance: nil, primaryHubs: ["JFK", "BOS", "FLL", "MCO"], headquarters: "Long Island City, NY")
            ]
        }
    }

    // MARK: - Airline KPIs
    public func getAirlineKPIs(code: String) async -> AirlineKPIs {
        await fetch("airlines/\(code)/kpis") {
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
                ),
                LoyaltyProgram(
                    carrierCode: "UA",
                    carrierName: "United Airlines",
                    programName: "MileagePlus",
                    activeAlliance: "Star Alliance",
                    tiers: [
                        LoyaltyTier(name: "Premier Silver", eqmRequired: 25000, eqsRequired: 24, upgradeWindowHours: 24, bonusMilesPercent: 40, loungeAccess: false, keyPerks: "Complimentary Economy Plus at check-in, 1 free checked bag"),
                        LoyaltyTier(name: "Premier Gold", eqmRequired: 50000, eqsRequired: 48, upgradeWindowHours: 48, bonusMilesPercent: 60, loungeAccess: true, keyPerks: "Star Alliance Gold, Economy Plus at booking, lounge access on intl"),
                        LoyaltyTier(name: "Premier Platinum", eqmRequired: 75000, eqsRequired: 72, upgradeWindowHours: 72, bonusMilesPercent: 80, loungeAccess: true, keyPerks: "40 PlusPoints for upgrades, 3 free checked bags"),
                        LoyaltyTier(name: "Premier 1K", eqmRequired: 100000, eqsRequired: 96, upgradeWindowHours: 96, bonusMilesPercent: 100, loungeAccess: true, keyPerks: "280 PlusPoints, pre-boarding, dedicated 1K support line")
                    ],
                    partnerships: [
                        LoyaltyPartnership(partnerCarrierCode: "LH", partnerCarrierName: "Lufthansa", relationshipDepth: "Full Alliance / Star Alliance", startYear: 1997, endYear: nil, eliteReciprocal: true, loungeReciprocal: true, historicalNote: "Founding members of the Star Alliance transatlantic joint venture.")
                    ]
                )
            ]
        }
    }
}
