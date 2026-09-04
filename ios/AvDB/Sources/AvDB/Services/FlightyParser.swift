import Foundation

public struct FlightyParser: Sendable {
    /// Parses Flighty CSV file data into structured FlightyRecord entities
    public static func parseCSV(from url: URL) throws -> [FlightyRecord] {
        let content = try String(contentsOf: url, encoding: .utf8)
        return parseCSV(content: content)
    }

    public static func parseCSV(content: String) -> [FlightyRecord] {
        let lines = content.components(separatedBy: .newlines)
            .map { $0.trimmingCharacters(in: .whitespacesAndNewlines) }
            .filter { !$0.isEmpty }

        guard lines.count > 1 else { return [] }

        // Clean headers: lowercase and remove quotes/spaces
        let headerLine = lines[0]
        let headers = parseCSVLine(headerLine).map { $0.lowercased().replacingOccurrences(of: " ", with: "_") }

        var records: [FlightyRecord] = []

        for i in 1..<lines.count {
            let rowValues = parseCSVLine(lines[i])
            if rowValues.count < headers.count { continue }

            var rowMap: [String: String] = [:]
            for (index, header) in headers.enumerated() {
                if index < rowValues.count {
                    rowMap[header] = rowValues[index]
                }
            }

            let date = rowMap["date"] ?? rowMap["flight_date"] ?? ""
            let flightNum = rowMap["flight"] ?? rowMap["flight_number"] ?? rowMap["flight_num"] ?? ""
            let airline = rowMap["airline"] ?? rowMap["carrier"] ?? "Unknown Airline"
            let origin = rowMap["from"] ?? rowMap["origin"] ?? rowMap["departure"] ?? ""
            let destination = rowMap["to"] ?? rowMap["destination"] ?? rowMap["arrival"] ?? ""
            let aircraft = rowMap["aircraft"] ?? rowMap["aircraft_type"] ?? rowMap["model"] ?? "Unknown Aircraft"
            let tail = rowMap["tail"] ?? rowMap["tail_number"] ?? rowMap["registration"] ?? ""
            let seat = rowMap["seat"] ?? ""
            let distStr = rowMap["distance"] ?? rowMap["distance_miles"] ?? "0"
            let dist = Double(distStr.replacingOccurrences(of: ",", with: "")) ?? 0.0

            if !origin.isEmpty && !destination.isEmpty {
                records.append(
                    FlightyRecord(
                        date: date,
                        flightNumber: flightNum,
                        airline: airline,
                        origin: origin,
                        destination: destination,
                        aircraftType: aircraft,
                        tailNumber: tail,
                        seat: seat,
                        distanceMiles: dist
                    )
                )
            }
        }

        return records
    }

    private static func parseCSVLine(_ line: String) -> [String] {
        var values: [String] = []
        var currentValue = ""
        var insideQuotes = false

        for char in line {
            if char == "\"" {
                insideQuotes.toggle()
            } else if char == "," && !insideQuotes {
                values.append(currentValue.trimmingCharacters(in: .whitespaces))
                currentValue = ""
            } else {
                currentValue.append(char)
            }
        }
        values.append(currentValue.trimmingCharacters(in: .whitespaces))
        return values
    }

    /// Computes summary metrics from flight log records
    public static func computeSummary(from records: [FlightyRecord]) -> FlightySummary {
        guard !records.isEmpty else { return .empty }

        let totalFlights = records.count
        let totalMiles = records.reduce(0.0) { $0 + $1.distanceMiles }

        var airportSet = Set<String>()
        var airlineSet = Set<String>()
        var aircraftCounts: [String: Int] = [:]
        var routeCounts: [String: Int] = [:]

        for r in records {
            airportSet.insert(r.origin)
            airportSet.insert(r.destination)
            if !r.airline.isEmpty { airlineSet.insert(r.airline) }
            aircraftCounts[r.aircraftType, default: 0] += 1
            routeCounts[r.routeKey, default: 0] += 1
        }

        let topAircraft = aircraftCounts.max(by: { $0.value < $1.value })?.key ?? "—"
        let topRoute = routeCounts.max(by: { $0.value < $1.value })?.key ?? "—"

        return FlightySummary(
            totalFlights: totalFlights,
            totalMiles: totalMiles,
            uniqueAirports: airportSet.count,
            uniqueAirlines: airlineSet.count,
            uniqueAircraftTypes: aircraftCounts.count,
            topAircraftType: topAircraft,
            topRoute: topRoute
        )
    }

    /// Groups flights by subfleet / aircraft model
    public static func computeSubfleetBreakdown(from records: [FlightyRecord]) -> [FlightySubfleetGroup] {
        guard !records.isEmpty else { return [] }

        var countMap: [String: Int] = [:]
        var milesMap: [String: Double] = [:]

        for r in records {
            countMap[r.aircraftType, default: 0] += 1
            milesMap[r.aircraftType, default: 0.0] += r.distanceMiles
        }

        let total = Double(records.count)

        return countMap.map { (aircraft, count) in
            FlightySubfleetGroup(
                aircraftType: aircraft,
                flightCount: count,
                totalMiles: milesMap[aircraft] ?? 0.0,
                percentage: (Double(count) / total) * 100.0
            )
        }.sorted { $0.flightCount > $1.flightCount }
    }
}
