import Foundation

/// Fast native parser for Flighty CSV export logs.
public enum FlightyParser {
    public static func parseCSV(from url: URL) throws -> [FlightLog] {
        let isSecurityScoped = url.startAccessingSecurityScopedResource()
        defer {
            if isSecurityScoped {
                url.stopAccessingSecurityScopedResource()
            }
        }

        let content = try String(contentsOf: url, encoding: .utf8)
        return parseCSVString(content)
    }

    public static func parseCSVString(_ content: String) -> [FlightLog] {
        var lines = content.components(separatedBy: .newlines)
        guard !lines.isEmpty else { return [] }

        let headerLine = lines.removeFirst()
        let headers = parseLine(headerLine).map { $0.trimmingCharacters(in: .whitespacesAndNewlines).lowercased() }

        // Find column indices
        let dateIdx = headers.firstIndex(where: { $0.contains("date") })
        let flightNumIdx = headers.firstIndex(where: { $0.contains("flight") && ($0.contains("num") || $0.contains("code")) })
        let airlineIdx = headers.firstIndex(where: { $0.contains("airline") || $0.contains("carrier") })
        let originIdx = headers.firstIndex(where: { $0.contains("from") || $0.contains("origin") || $0.contains("dep") })
        let destIdx = headers.firstIndex(where: { $0.contains("to") || $0.contains("dest") || $0.contains("arr") })
        let aircraftIdx = headers.firstIndex(where: { $0.contains("aircraft") || $0.contains("model") || $0.contains("plane") })
        let tailIdx = headers.firstIndex(where: { $0.contains("tail") || $0.contains("reg") })
        let seatIdx = headers.firstIndex(where: { $0.contains("seat") && !$0.contains("class") })
        let classIdx = headers.firstIndex(where: { $0.contains("class") || $0.contains("cabin") })

        var logs: [FlightLog] = []

        for line in lines {
            let trimmed = line.trimmingCharacters(in: .whitespacesAndNewlines)
            guard !trimmed.isEmpty else { continue }

            let fields = parseLine(trimmed)

            guard let orig = originIdx.flatMap({ fields[safe: $0] })?.trimmingCharacters(in: .whitespaces),
                  let dst = destIdx.flatMap({ fields[safe: $0] })?.trimmingCharacters(in: .whitespaces),
                  orig.count == 3, dst.count == 3 else {
                continue
            }

            let date = dateIdx.flatMap({ fields[safe: $0] }) ?? "Unknown"
            let flightNum = flightNumIdx.flatMap({ fields[safe: $0] }) ?? ""
            let airline = airlineIdx.flatMap({ fields[safe: $0] }) ?? ""
            let aircraft = aircraftIdx.flatMap({ fields[safe: $0] })
            let tail = tailIdx.flatMap({ fields[safe: $0] })
            let seat = seatIdx.flatMap({ fields[safe: $0] })
            let cabinClass = classIdx.flatMap({ fields[safe: $0] })

            logs.append(FlightLog(
                date: date,
                flightNumber: flightNum,
                airlineCode: airline,
                originIATA: orig.uppercased(),
                destIATA: dst.uppercased(),
                aircraftType: aircraft,
                tailNumber: tail,
                seatNumber: seat,
                seatClass: cabinClass
            ))
        }
        return logs
    }

    private static func parseLine(_ line: String) -> [String] {
        var results: [String] = []
        var current = ""
        var inQuotes = false

        for char in line {
            if char == "\"" {
                inQuotes.toggle()
            } else if char == "," && !inQuotes {
                results.append(current.trimmingCharacters(in: CharacterSet(charactersIn: "\"")))
                current = ""
            } else {
                current.append(char)
            }
        }
        results.append(current.trimmingCharacters(in: CharacterSet(charactersIn: "\"")))
        return results
    }
}

private extension Array {
    subscript(safe index: Index) -> Element? {
        indices.contains(index) ? self[index] : nil
    }
}

