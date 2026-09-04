// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "AvDBCore",
    defaultLocalization: "en",
    platforms: [
        .iOS(.v17),
        .macOS(.v14)
    ],
    products: [
        .library(
            name: "AvDBCore",
            targets: ["AvDBCore"]
        ),
    ],
    dependencies: [
        // Mapbox Maps SDK is optional; Apple MapKit provides 100% native out-of-the-box 120Hz ProMotion rendering
    ],
    targets: [
        .target(
            name: "AvDBCore",
            dependencies: [],
            path: "Sources/AvDB"
        ),
        .testTarget(
            name: "AvDBTests",
            dependencies: ["AvDBCore"],
            path: "Tests/AvDBTests"
        )
    ]
)
