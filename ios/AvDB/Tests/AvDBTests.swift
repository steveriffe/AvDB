import XCTest
import CoreLocation
@testable import AvDB

final class AvDBTests: XCTestCase {
    func testGeodesicDistanceCalculation() {
        // SEA: 47.4502, -122.3088
        // SFO: 37.6213, -122.3790
        let sea = CLLocationCoordinate2D(latitude: 47.4502, longitude: -122.3088)
        let sfo = CLLocationCoordinate2D(latitude: 37.6213, longitude: -122.3790)

        let distance = GeodesicMath.distanceMiles(from: sea, to: sfo)
        // Expected distance is ~679 miles
        XCTAssertGreaterThan(distance, 650)
        XCTAssertLessThan(distance, 710)
    }

    func testGeodesicWaypointsCount() {
        let sea = CLLocationCoordinate2D(latitude: 47.4502, longitude: -122.3088)
        let jfk = CLLocationCoordinate2D(latitude: 40.6413, longitude: -73.7781)

        let waypoints = GeodesicMath.geodesicWaypoints(from: sea, to: jfk, segments: 16)
        XCTAssertEqual(waypoints.count, 17)
        XCTAssertEqual(waypoints.first?.latitude, sea.latitude)
        XCTAssertEqual(waypoints.last?.latitude, jfk.latitude)
    }

    func testFlightyParser() {
        let sampleCSV = """
        Date,Flight,Airline,From,To,Aircraft,Tail,Seat,Class
        2024-05-12,AS 124,AS,SEA,SFO,Boeing 737-900ER,N413AS,3D,First
        2024-06-01,DL 440,DL,ATL,JFK,Airbus A321neo,N501DN,12A,Main
        """

        let logs = FlightyParser.parseCSVString(sampleCSV)
        XCTAssertEqual(logs.count, 2)
        XCTAssertEqual(logs[0].originIATA, "SEA")
        XCTAssertEqual(logs[0].destIATA, "SFO")
        XCTAssertEqual(logs[0].seatNumber, "3D")
        XCTAssertEqual(logs[1].airlineCode, "DL")
        XCTAssertEqual(logs[1].originIATA, "ATL")
        XCTAssertEqual(logs[1].destIATA, "JFK")
    }

    func testColorHexParsing() {
        let color = Color(hex: "#0A84FF")
        XCTAssertNotNil(color)
    }
}
