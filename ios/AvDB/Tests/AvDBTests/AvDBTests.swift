import XCTest
import CoreLocation
@testable import AvDB

final class AvDBTests: XCTestCase {
    func testGeodesicCoordinatesCalculation() {
        let sea = CLLocationCoordinate2D(latitude: 47.4502, longitude: -122.3088)
        let ord = CLLocationCoordinate2D(latitude: 41.9742, longitude: -87.9073)

        let coords = GeodesicMath.greatCircleCoordinates(from: sea, to: ord, numberOfPoints: 10)
        XCTAssertEqual(coords.count, 10)
        XCTAssertEqual(coords.first?.latitude ?? 0, sea.latitude, accuracy: 0.001)
        XCTAssertEqual(coords.last?.latitude ?? 0, ord.latitude, accuracy: 0.001)

        let dist = GeodesicMath.distanceMiles(from: sea, to: ord)
        XCTAssertGreaterThan(dist, 1600.0)
        XCTAssertLessThan(dist, 1800.0)
    }

    func testFlightyCSVParser() {
        let sampleCSV = """
        Date,Flight,Airline,From,To,Aircraft,Tail,Seat,Distance
        2024-06-15,AS 124,Alaska Airlines,SEA,ORD,Boeing 737-900ER,N413AS,3A,1720
        2024-06-20,UA 412,United Airlines,ORD,BOS,Airbus A321neo,N145UA,12C,867
        """

        let records = FlightyParser.parseCSV(content: sampleCSV)
        XCTAssertEqual(records.count, 2)
        XCTAssertEqual(records[0].origin, "SEA")
        XCTAssertEqual(records[0].destination, "ORD")
        XCTAssertEqual(records[0].distanceMiles, 1720)

        let summary = FlightyParser.computeSummary(from: records)
        XCTAssertEqual(summary.totalFlights, 2)
        XCTAssertEqual(summary.uniqueAirports, 3) // SEA, ORD, BOS
        XCTAssertEqual(summary.totalMiles, 2587)

        let subfleets = FlightyParser.computeSubfleetBreakdown(from: records)
        XCTAssertEqual(subfleets.count, 2)
    }

    func testAirportModelDecoding() throws {
        let json = """
        {
            "airport_code": "SEA",
            "airport_name": "Seattle-Tacoma International",
            "city": "Seattle",
            "state": "WA",
            "country": "US",
            "is_commercial": true,
            "is_metro_code": false,
            "latitude": 47.4502,
            "longitude": -122.3088
        }
        """.data(using: .utf8)!

        let airport = try JSONDecoder().decode(Airport.self, from: json)
        XCTAssertEqual(airport.airportCode, "SEA")
        XCTAssertEqual(airport.city, "Seattle")
        XCTAssertEqual(airport.coordinate?.latitude ?? 0, 47.4502, accuracy: 0.0001)
    }
}
