# AvDB Native iOS Application (SwiftUI & MapKit)

Welcome to the native Apple iOS implementation of **AvDB** — the aviation analytics platform designed specifically for iPhone with Apple Human Interface Guidelines (HIG), SwiftUI, and 120Hz ProMotion great-circle geodesic route mapping.

---

## 📱 Architectural Blueprint

```text
ios/
├── README.md                           # This setup and pairing guide
└── AvDB/
    ├── Package.swift                   # Swift Package manifest (iOS 17+)
    ├── Sources/
    │   └── AvDB/
    │       ├── AvDBApp.swift           # @main application entry point
    │       ├── Models/
    │       │   ├── AirportModels.swift # Airport catalog, KPIs, catchment, routes
    │       │   ├── AirlineModels.swift # Airline KPIs, primary hubs, yield curve
    │       │   ├── FleetModels.swift   # Fleet utilization, subfleet economics
    │       │   ├── FlightyModels.swift # Flighty passport records, subfleets
    │       │   └── AppSettings.swift   # User preferences, environment, Mapbox styles
    │       ├── Services/
    │       │   ├── APIService.swift    # Swift async/await actor client + caching
    │       │   ├── GeodesicMath.swift  # Haversine spherical great-circle interpolation
    │       │   └── FlightyParser.swift # Native CSV parser for Flighty export logs
    │       └── Views/
    │           ├── MainTabView.swift   # 5-tab native navigation controller
    │           ├── AirportsView.swift  # Catchment badges, KPI cards, route map
    │           ├── AirlinesView.swift  # Carrier selector, network map, hubs, yield curve
    │           ├── FleetView.swift     # Family picker, subfleet gauge economics
    │           ├── FlightyView.swift   # .fileImporter picker, subfleet stats, personal map
    │           ├── SettingsView.swift  # Backend switcher, Mapbox styles, cache controls
    │           └── Components/
    │               ├── RouteMapView.swift # Native MapKit 120Hz geodesic map
    │               ├── GlassCard.swift    # Liquid Glass / ultraThinMaterial container
    │               └── KPICardView.swift  # High-density rounded metric cards
    └── Tests/
        └── AvDBTests/
            └── AvDBTests.swift         # Unit tests for geodesic math, parser, models
```

---

## 🚀 Core Features

1. **Airports Explorer (`AirportsView.swift`)**:
   - Fast search across all commercial airports and metropolitan markets.
   - Catchment market indicators (e.g. WAS, NYC, CHI).
   - High-density KPI cards: Direct Nonstop Destinations, Load Factor, Departures, Seats, Passenger Volume, Average O&D Fare, and Leading Carrier.
   - 120Hz ProMotion Great-Circle Route Map with interactive route selection.
   - Outbound market table with stage lengths, seats per departure, and passenger volumes.

2. **Airlines Explorer (`AirlinesView.swift`)**:
   - Airline selector supporting all major carriers (AS, UA, DL, AA, WN, B6, NK, F9, G4) styled with signature airline brand palettes.
   - Network KPIs: Active Routes, System Load Factor, Capacity (ASM), Traffic (RPM), Network Average Fare, and Yield per Passenger-Mile.
   - Nationwide Route Network Map with primary hub concentric bullseye markers.
   - Hub and focus city operational rankings.
   - Stage length vs. Yield curve analysis.

3. **Fleet & Aircraft Lens (`FleetView.swift`)**:
   - Aircraft family allocation picker: All Mainline & Regional, Airbus A320 Family, Boeing 737 Family, Widebody, Embraer E-Jets, Bombardier CRJ.
   - Utilization metrics: Average Gauge (seats/departure), Fleet Load Factor, Average Stage Length, and Yield.
   - Subfleet economics breakdown (e.g., comparing Boeing 737-900ER vs. 737-800 vs. 737 MAX 8; Airbus A321neo vs. A320-200; Embraer E175 vs. CRJ-900).

4. **Flighty Passport Integration (`FlightyView.swift`)**:
   - Native iOS file picker using `.fileImporter` supporting Flighty CSV exports.
   - Personal lifetime flight statistics: Total Flights, Total Miles Flown, Visited Airports, Flown Airlines, and Top Aircraft Model.
   - Subfleet allocation analysis displaying your personal distribution across aircraft types.
   - Personal Flight Map rendering great-circle arcs between all your flown routes.
   - One-tap demo data loader for instant previewing without an export file.

5. **Settings & Cartography Engine (`SettingsView.swift`)**:
   - Live backend switcher: Google Cloud Run (`api.avdb.riffe.co.uk`), Local Simulator (`127.0.0.1:8000`), or Local Network LAN IP.
   - Cartography style selector: Classic In-Flight Paper (1990s vintage), Midnight Navy, Minimal Slate, Standard Apple Map, or custom Mapbox Studio styles (Personal, Love, Mono).
   - Mapbox Access Token and custom style URL fields.
   - In-memory route and query cache clearing.

---

## 🛠️ Opening and Running in Xcode

### Method 1: Open Swift Package Directly
1. Open the project in Xcode:
   ```bash
   open ios/AvDB/Package.swift
   ```
2. In Xcode, select an iOS Simulator (e.g., iPhone 16 Pro) or your connected physical iPhone in the scheme selector.
3. Press **Cmd + R** to build and run.

### Method 2: Create an iOS App Xcode Project (Recommended for Physical Device Signing)
1. Open Xcode and select **File ➔ New ➔ Project ➔ iOS ➔ App**.
2. Product Name: `AvDB`
   - Interface: `SwiftUI`
   - Language: `Swift`
3. Add the package via **File ➔ Add Package Dependencies... ➔ Add Local...** and choose `ios/AvDB` (Module: `AvDBCore`), or drag `ios/AvDB/Sources/AvDB` into your target.
4. In the target's **Signing & Capabilities** tab:
   - Check **Automatically manage signing**.
   - Team: Select your **Personal Team** (free Apple ID account, no \$99 developer subscription required for development on your own iPhone).
   - Bundle Identifier: `com.yourname.avdb`
5. Connect your iPhone via USB or Wi-Fi, select it from the device target menu, and click **Run (Cmd + R)**.
   > **Note for Physical Devices**: On your iPhone, go to **Settings ➔ General ➔ VPN & Device Management**, tap your Apple ID under Developer App, and tap **Trust**. Enable Developer Mode under **Settings ➔ Privacy & Security ➔ Developer Mode** if prompted.

### 🚨 Troubleshooting: "Multiple commands produce ... AvDB.swiftmodule"
If Xcode reports:
```text
Multiple commands produce '.../Build/Products/Debug-iphoneos/AvDB.swiftmodule/Project/arm64-apple-ios.swiftsourceinfo'
Multiple commands produce '.../Build/Products/Debug-iphoneos/AvDB.swiftmodule/arm64-apple-ios.swiftmodule'
```
**Why this happens**:
Both your Xcode App target (`AvDB`) and the Swift Package were attempting to compile modules with the identical name `AvDB`, causing the build system to collide on output file paths.

**How to resolve**:
1. We have renamed the Swift package product/target to **`AvDBCore`**, eliminating module name collisions.
2. In Terminal, wipe the cached conflicted build artifacts:
   ```bash
   rm -rf ~/Library/Developer/Xcode/DerivedData/AvDB-*
   ```
3. In Xcode:
   - Choose **Product ➔ Clean Build Folder** (`Shift + Cmd + K`).
   - If using `import AvDB`, update to `import AvDBCore`.
   - Press **Cmd + R** to build and run on your iPhone 16 Pro Max (iOS 18 / iOS 27 Beta).

---

## 🔗 Pairing with the Backend API

The app connects to the AvDB REST API via `APIService.swift`.

### 1. Connecting to Production Cloud Run (Default)
Out of the box, the app defaults to:
```text
https://api.avdb.riffe.co.uk
```
No local server is needed; requests query pre-aggregated BigQuery marts hosted in GCP.

### 2. Testing against Local FastAPI Backend
To develop or debug locally:
1. Start the FastAPI server on your Mac:
   ```bash
   ./.venv/bin/uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
   ```
2. Verify it is running by opening:
   - API Root: `http://localhost:8000`
   - Interactive Swagger Docs: `http://localhost:8000/docs`
3. Configure the iOS App:
   - **In iOS Simulator**: Open **Settings** tab in the app, set Environment to `Localhost (127.0.0.1:8000)`.
   - **On Physical iPhone**: Ensure your iPhone and Mac are on the same Wi-Fi network. In the app's **Settings** tab, select `Local Network (Custom IP)` and enter your Mac's LAN IP (e.g. `http://192.168.1.145:8000`).
   - Tap **Test API Connection** to verify sub-50ms latency.

---

## ✈️ Flighty Export CSV Instructions

To view your personal flight network:
1. Open the **Flighty** app on your iPhone.
2. Tap your profile icon in the top right.
3. Tap **Settings (gear icon)** ➔ **Export Flights** ➔ **Export CSV**.
4. Save the file to **Files** (iCloud Drive or On My iPhone).
5. In AvDB, open the **Flighty** tab, tap **Import**, and select your exported CSV.
6. Your personal flight map, subfleet allocation, and flight history will immediately generate.
