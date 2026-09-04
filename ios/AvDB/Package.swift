// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "AvDB",
    defaultLocalization: "en",
    platforms: [
        .iOS(.v17),
        .macOS(.v14)
    ],
    products: [
        .library(
            name: "AvDB",
            targets: ["AvDB"]
        ),
    ],
    dependencies: [
        // Mapbox Maps SDK is optional; Apple MapKit provides 100% native out-of-the-box 120Hz ProMotion rendering
    ],
    targets: [
        .target(
            name: "AvDB",
            dependencies: [],
            path: "Sources/AvDB"
        ),
        .testTarget(
            name: "AvDBTests",
            dependencies: ["AvDB"],
            path: "Tests/AvDBTests"
        )
    ]
)
