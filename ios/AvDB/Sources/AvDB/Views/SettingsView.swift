import SwiftUI

/// Settings Lens: API Backend Config, Mapbox Token & Style Selector, Auth Tokens
public struct SettingsView: View {
    @StateObject private var settings = AppSettings.shared

    @State private var connectionStatus: String?
    @State private var isTestingConnection: Bool = false
    @State private var showAuthToken: Bool = false
    @State private var cacheClearedNotification: Bool = false

    public init() {}

    public var body: some View {
        NavigationStack {
            Form {
                // MARK: - API Backend & Cloud Run Configuration
                Section {
                    Picker("Environment", selection: $settings.environment) {
                        ForEach(APIEnvironment.allCases) { env in
                            Text(env.rawValue).tag(env)
                        }
                    }

                    if settings.environment == .localLan {
                        HStack {
                            Text("Base URL")
                                .font(.subheadline)
                            Spacer()
                            TextField("http://192.168.1.X:8000", text: $settings.customApiBaseUrl)
                                .multilineTextAlignment(.trailing)
                                .textInputAutocapitalization(.never)
                                .autocorrectionDisabled()
                                .font(.subheadline)
                        }
                    }

                    HStack {
                        Text("Active Endpoint")
                            .font(.caption)
                            .foregroundStyle(.secondary)
                        Spacer()
                        Text(settings.activeApiBaseURL)
                            .font(.caption)
                            .foregroundStyle(.blue)
                            .lineLimit(1)
                    }

                    Button {
                        Task { await testAPIConnection() }
                    } label: {
                        HStack {
                            if isTestingConnection {
                                ProgressView()
                                    .scaleEffect(0.8)
                            } else {
                                Image(systemName: "antenna.radiowaves.left.and.right")
                            }
                            Text("Test API Connection")
                            Spacer()
                            if let status = connectionStatus {
                                Text(status)
                                    .font(.caption)
                                    .foregroundStyle(status.contains("Online") ? .green : .red)
                            }
                        }
                    }
                    .disabled(isTestingConnection)
                } header: {
                    Label("API Server & Cloud Run", systemName: "server.rack")
                } footer: {
                    Text("Default endpoint runs on Google Cloud Run (api.avdb.riffe.co.uk) with sub-second BigQuery analytical marts.")
                }

                // MARK: - Mapbox Configuration & Cartography Styles
                Section {
                    HStack {
                        Text("Access Token")
                            .font(.subheadline)
                        Spacer()
                        SecureField("pk.eyJ1...", text: $settings.mapboxToken)
                            .multilineTextAlignment(.trailing)
                            .textInputAutocapitalization(.never)
                            .autocorrectionDisabled()
                    }

                    Picker("Cartography Style", selection: $settings.mapTheme) {
                        ForEach(MapThemeStyle.allCases) { style in
                            Label(style.rawValue, systemImage: style.icon).tag(style)
                        }
                    }

                    // Mapbox custom style URLs matching AvDB config
                    DisclosureGroup("Custom Mapbox Style URLs") {
                        VStack(alignment: .leading, spacing: 10) {
                            styleField(title: "Personal Style", text: $settings.mapboxStylePersonal, placeholder: "mapbox://styles/...")
                            styleField(title: "Love Style", text: $settings.mapboxStyleLove, placeholder: "mapbox://styles/...")
                            styleField(title: "Mono Style", text: $settings.mapboxStyleMono, placeholder: "mapbox://styles/...")
                        }
                        .padding(.vertical, 4)
                    }
                } header: {
                    Label("Cartography & Mapbox", systemName: "map.fill")
                } footer: {
                    Text("Select between authentic 1990s in-flight paper, modern midnight navy, or your custom Mapbox Studio styles (Personal, Love, Mono).")
                }

                // MARK: - Authentication & Security Tokens
                Section {
                    HStack {
                        Text("Auth Token")
                            .font(.subheadline)
                        Spacer()
                        if showAuthToken {
                            TextField("Bearer Token", text: $settings.authToken)
                                .multilineTextAlignment(.trailing)
                                .textInputAutocapitalization(.never)
                                .autocorrectionDisabled()
                        } else {
                            SecureField("Bearer Token", text: $settings.authToken)
                                .multilineTextAlignment(.trailing)
                                .textInputAutocapitalization(.never)
                                .autocorrectionDisabled()
                        }
                        Button {
                            showAuthToken.toggle()
                        } label: {
                            Image(systemName: showAuthToken ? "eye.slash" : "eye")
                                .foregroundStyle(.secondary)
                        }
                        .buttonStyle(.plain)
                    }
                } header: {
                    Label("Security & Access Tokens", systemName: "lock.shield")
                }

                // MARK: - Cache & Storage Management
                Section {
                    Button(role: .destructive) {
                        Task {
                            await APIService.shared.clearCache()
                            withAnimation {
                                cacheClearedNotification = true
                            }
                            try? await Task.sleep(nanoseconds: 2_000_000_000)
                            withAnimation {
                                cacheClearedNotification = false
                            }
                        }
                    } label: {
                        HStack {
                            Image(systemName: "trash")
                            Text("Clear Query & Route Cache")
                            Spacer()
                            if cacheClearedNotification {
                                Text("Cleared!")
                                    .font(.caption)
                                    .foregroundStyle(.green)
                            }
                        }
                    }
                } header: {
                    Label("Data Cache", systemName: "internaldrive")
                }

                // MARK: - About AvDB
                Section {
                    HStack {
                        Text("Version")
                        Spacer()
                        Text("1.0.0 (Build 2026.1)")
                            .foregroundStyle(.secondary)
                    }
                    HStack {
                        Text("Data Warehouse")
                        Spacer()
                        Text("Google Cloud BigQuery (db1b-1)")
                            .foregroundStyle(.secondary)
                    }
                    HStack {
                        Text("Datasets")
                        Spacer()
                        Text("BTS T-100 & DB1B Survey")
                            .foregroundStyle(.secondary)
                    }
                } header: {
                    Label("About AvDB", systemName: "info.circle")
                }
            }
            .navigationTitle("Settings")
            .navigationBarTitleDisplayMode(.large)
        }
    }

    private func styleField(title: String, text: Binding<String>, placeholder: String) -> some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(title)
                .font(.caption2)
                .foregroundStyle(.secondary)
            TextField(placeholder, text: text)
                .font(.caption)
                .textInputAutocapitalization(.never)
                .autocorrectionDisabled()
                .padding(8)
                .background(Color.secondary.opacity(0.1), in: RoundedRectangle(cornerRadius: 8))
        }
    }

    private func testAPIConnection() async {
        isTestingConnection = true
        connectionStatus = nil
        defer { isTestingConnection = false }

        do {
            let airports = try await APIService.shared.fetchAirports(baseURL: settings.activeApiBaseURL)
            connectionStatus = "Online (\(airports.count) apts)"
        } catch {
            connectionStatus = "Failed: \(error.localizedDescription)"
        }
    }
}
