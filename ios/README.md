# AvDB Native iOS Application (SwiftUI & MapKit)

Welcome to the native Apple iOS implementation of **AvDB** — the aviation analytics platform designed specifically for iPhone and iPad with Apple Human Interface Guidelines (HIG), SwiftUI, and 120Hz ProMotion Great-Circle geodesic route mapping.

---

## 📱 Project Specifications & Apple Developer Setup

| Setting | Value |
| :--- | :--- |
| **Project Location** | `ios/AvDB.xcodeproj` |
| **Bundle Identifier** | `uk.co.riffe.AvDB` |
| **Apple Developer Team ID** | `JRM56GZN5H` (Steve Riffe) |
| **Target Deployment** | iOS 17.0+ / iPadOS 17.0+ |
| **Language & Concurrency** | Swift 5.0 / Swift 6 Strict Concurrency |
| **UI Framework** | SwiftUI with `.ultraThinMaterial` Obsidian Glass |
| **Geodesic Engine** | Apple MapKit (`MKGeodesicPolyline`) |
| **Backend Sync** | AvDB FastAPI (`https://avdb.riffe.co.uk/api`) with offline caching |

---

## 🚀 How to Install & Run as a Beta App on Your iPhone

There are two primary ways to run AvDB on your personal iPhone:

### Method A: Direct Install from Xcode (Fastest, Immediate)

1. **Open the Project in Xcode**:
   In your terminal, run:
   ```bash
   open ios/AvDB.xcodeproj
   ```
2. **Connect Your iPhone**:
   - Plug your iPhone into your Mac using a USB-C or Lightning cable (or connect via Wi-Fi once paired).
   - If prompted on your iPhone, tap **Trust This Computer**.
3. **Enable Developer Mode on Your iPhone** (One-time setup on iOS 16/17/18):
   - On your iPhone, open **Settings** > **Privacy & Security**.
   - Scroll down to the bottom and tap **Developer Mode**.
   - Toggle **Developer Mode ON**.
   - Your iPhone will prompt you to restart. Tap **Restart**.
   - After restarting and unlocking, tap **Turn On** and enter your passcode.
4. **Select Your Device & Run**:
   - In the top toolbar of Xcode, click the device selector next to **AvDB** and select **Steve's iPhone**.
   - Press **`Cmd + R`** (or click the **Play** button).
   - Xcode will compile, code-sign with your Developer Team ID (`JRM56GZN5H`), and install AvDB directly onto your home screen!

---

### Method B: TestFlight Distribution (Wireless Beta Sharing)

To distribute AvDB as an official TestFlight beta app that updates automatically over the air:

1. **Verify Bundle ID in App Store Connect**:
   - Go to [developer.apple.com/account/resources/identifiers](https://developer.apple.com/account/resources/identifiers)
   - Ensure an App ID with identifier `uk.co.riffe.AvDB` exists (Xcode will automatically register it if you have automatic signing enabled).
   - Go to [appstoreconnect.apple.com/apps](https://appstoreconnect.apple.com/apps) and click **+ New App**:
     - **Platforms**: iOS
     - **Name**: AvDB Aviation Analytics
     - **Primary Language**: English (US)
     - **Bundle ID**: `uk.co.riffe.AvDB`
     - **SKU**: `avdb-ios-01`
     - **User Access**: Full Access
2. **Create an Archive in Xcode**:
   - In Xcode, select **Any iOS Device (arm64)** as the destination.
   - Go to menu bar: **Product** > **Archive**.
   - When the Organizer window appears with your build, click **Distribute App**.
   - Select **TestFlight & App Store** > **Distribute** > follow the on-screen upload wizard.
3. **Install from TestFlight**:
   - Once uploaded (usually 5–10 minutes for Apple processing), go to **App Store Connect** > **AvDB** > **TestFlight**.
   - Under **Internal Testing**, add yourself (Steve Riffe).
   - You will immediately receive an email / push notification in the **TestFlight app** on your iPhone. Tap **Install**!
   - *Note: Internal testing does NOT require waiting for Apple App Store Review approval.*

---

## 🧭 Core Architectural Pillars

```text
ios/
├── AvDB.xcodeproj/                      # Native Xcode project configured for JRM56GZN5H
├── README.md                            # This guide
└── AvDB/
    ├── App/
    │   ├── AvDBApp.swift                # @main app entry point & dark navigation styling
    │   └── AppConfiguration.swift       # Environment switcher (Cloud Run vs Localhost vs Demo)
    ├── DesignSystem/
    │   ├── Theme.swift                  # Obsidian (#070F1E) glass color scheme & accents
    │   ├── GlassCard.swift              # .ultraThinMaterial frosted container with hairline glow
    │   └── KPICardView.swift            # Aviation KPI cards (SF Symbols, delta badges)
    ├── Models/
    │   ├── Airport.swift                # Airport catalog, catchment codes, and outbound routes
    │   ├── Airline.swift                # Carrier metadata, brand colors, hubs, network stats
    │   ├── Route.swift                  # Geodesic routes with start/destination coordinates
    │   ├── FleetItem.swift              # Aircraft families, subfleets, gauge, and engine specs
    │   ├── LoyaltyProgram.swift         # FFP status tiers, upgrade windows, bilateral alliances
    │   └── FlightLog.swift              # Model for parsed Flighty logs
    ├── Services/
    │   ├── APIService.swift             # Thread-safe actor for FastAPI sync & offline cache
    │   ├── GeodesicMath.swift           # Haversine distance & spherical waypoint interpolation
    │   └── FlightyParser.swift          # Streaming CSV parser for personal Flighty exports
    ├── Views/
    │   ├── RootTabView.swift            # 5-tab floating navigation controller
    │   ├── Map/
    │   │   └── GreatCircleMapView.swift # MapKit MKGeodesicPolyline Great-Circle route renderer
    │   ├── Airports/
    │   │   ├── AirportsView.swift       # Search with instant IATA/City/Catchment filter
    │   │   └── AirportDetailView.swift  # Geodesic map, KPI cards, outbound market tables
    │   ├── Airlines/
    │   │   ├── AirlinesView.swift       # Carrier grid with brand liveries
    │   │   └── AirlineDetailView.swift  # Hub badges, system economics, ASM/RPM cards
    │   ├── Fleet/
    │   │   └── FleetView.swift          # Fleet families & gauge (DC-9, A320, 737, 787)
    │   ├── Loyalty/
    │   │   └── LoyaltyPartnershipsView.swift # Status tiers, upgrade windows, bilateral webs
    │   ├── Flighty/
    │   │   └── FlightyView.swift        # .fileImporter picker & personal flight passport
    │   └── Settings/
    │       └── SettingsView.swift       # Backend switcher, cache purge, developer info
    ├── Assets.xcassets/                 # AppIcon and AccentColor
    └── Tests/
        └── AvDBTests.swift              # Unit tests for geodesic math and Flighty parser
```

---

## 🛠 Local Backend Pairing
By default, the iOS app queries the production Cloud Run backend at `https://avdb.riffe.co.uk/api`.
To test against a local API:
1. Start your local FastAPI backend:
   ```bash
   ./.venv/bin/uvicorn api.main:app --reload --port 8000
   ```
2. In the iOS app, tap the **Settings** gear in the top right.
3. Switch **Environment** to **Localhost (Development)**.
4. Tap **Test API Connection** to verify connectivity.
