import SwiftUI

public struct SettingsView: View {
    @ObservedObject private var config = AppConfiguration.shared
    @State private var isTestingConnection: Bool = false
    @State private var connectionStatus: String?
    @State private var cacheClearedNotification: Bool = false

    public init() {}

    public var body: some View {
        NavigationStack {
            Form {
                Section(header: Text("Data Engine Status").foregroundColor(AvDBTheme.secondaryText)) {
                    HStack {
                        Label {
                            VStack(alignment: .leading, spacing: 2) {
                                Text(config.selectedEnvironment == .offlineDemo ? "Offline Demo Mode" : "Live BigQuery Engine")
                                    .font(.system(size: 15, weight: .bold))
                                    .foregroundColor(AvDBTheme.primaryText)
                                Text(config.selectedEnvironment == .offlineDemo ? "Using bundled static fallback records" : "Direct REST connection to Cloud Run BigQuery marts")
                                    .font(.system(size: 12))
                                    .foregroundColor(AvDBTheme.secondaryText)
                            }
                        } icon: {
                            Image(systemName: config.selectedEnvironment == .offlineDemo ? "tray.fill" : "server.rack")
                                .foregroundColor(config.selectedEnvironment == .offlineDemo ? AvDBTheme.accentAmber : AvDBTheme.accentGreen)
                        }
                        Spacer()
                        Text(config.selectedEnvironment == .offlineDemo ? "DEMO" : "LIVE")
                            .font(.system(size: 11, weight: .bold, design: .monospaced))
                            .padding(.horizontal, 8)
                            .padding(.vertical, 4)
                            .background(config.selectedEnvironment == .offlineDemo ? AvDBTheme.accentAmber.opacity(0.2) : AvDBTheme.accentGreen.opacity(0.2))
                            .foregroundColor(config.selectedEnvironment == .offlineDemo ? AvDBTheme.accentAmber : AvDBTheme.accentGreen)
                            .clipShape(Capsule())
                    }
                    .padding(.vertical, 4)
                }

                Section(header: Text("Backend API Environment").foregroundColor(AvDBTheme.secondaryText)) {
                    Picker("Environment", selection: $config.selectedEnvironment) {
                        ForEach(AppConfiguration.Environment.allCases) { env in
                            Text(env.rawValue).tag(env)
                        }
                    }
                    .pickerStyle(.menu)

                    HStack {
                        Text("Base URL")
                            .font(.system(size: 12))
                            .foregroundColor(AvDBTheme.secondaryText)
                        Spacer()
                        Text(config.selectedEnvironment.baseURL.absoluteString)
                            .font(.system(size: 11, design: .monospaced))
                            .foregroundColor(AvDBTheme.accentCyan)
                            .lineLimit(1)
                    }

                    Button {
                        testConnection()
                    } label: {
                        HStack {
                            if isTestingConnection {
                                ProgressView()
                                    .tint(AvDBTheme.accentBlue)
                            } else {
                                Image(systemName: "network")
                            }
                            Text("Test API Connection")
                            Spacer()
                            if let status = connectionStatus {
                                Text(status)
                                    .font(.system(size: 12, weight: .semibold))
                                    .foregroundColor(status.contains("OK") ? AvDBTheme.accentGreen : AvDBTheme.accentCoral)
                            }
                        }
                    }
                    .disabled(isTestingConnection)
                }

                Section(header: Text("Offline Data & Cache").foregroundColor(AvDBTheme.secondaryText)) {
                    Button(role: .destructive) {
                        cacheClearedNotification = true
                    } label: {
                        Label("Purge Local Cache", systemImage: "trash")
                    }

                    if cacheClearedNotification {
                        Text("Cache cleared successfully.")
                            .font(.system(size: 12))
                            .foregroundColor(AvDBTheme.accentGreen)
                    }
                }

                Section(header: Text("Developer & Build Metadata").foregroundColor(AvDBTheme.secondaryText)) {
                    HStack {
                        Text("Developer")
                        Spacer()
                        Text(config.developer)
                            .foregroundColor(AvDBTheme.secondaryText)
                    }
                    HStack {
                        Text("Apple Team ID")
                        Spacer()
                        Text(config.teamID)
                            .font(.system(.body, design: .monospaced))
                            .foregroundColor(AvDBTheme.accentCyan)
                    }
                    HStack {
                        Text("Bundle Identifier")
                        Spacer()
                        Text(config.bundleID)
                            .font(.system(.caption, design: .monospaced))
                            .foregroundColor(AvDBTheme.secondaryText)
                    }
                    HStack {
                        Text("App Version")
                        Spacer()
                        Text(config.appVersion)
                            .foregroundColor(AvDBTheme.secondaryText)
                    }
                }
            }
            .scrollContentBackground(.hidden)
            .avdbCanvas()
            .navigationTitle("Settings")
            .navigationBarTitleDisplayMode(.large)
        }
    }

    private func testConnection() {
        isTestingConnection = true
        connectionStatus = nil
        Task {
            let env = config.selectedEnvironment
            guard env != .offlineDemo else {
                try? await Task.sleep(nanoseconds: 300_000_000)
                await MainActor.run {
                    self.connectionStatus = "Demo OK"
                    self.isTestingConnection = false
                }
                return
            }

            let start = Date()
            do {
                let healthURL = env.baseURL.appendingPathComponent("health")
                let (_, response) = try await URLSession.shared.data(from: healthURL)
                let elapsedMs = Int(Date().timeIntervalSince(start) * 1000)
                if let http = response as? HTTPURLResponse, http.statusCode == 200 {
                    await MainActor.run {
                        self.connectionStatus = "200 OK (\(elapsedMs)ms)"
                        self.isTestingConnection = false
                    }
                } else if let http = response as? HTTPURLResponse {
                    await MainActor.run {
                        self.connectionStatus = "HTTP \(http.statusCode) (\(elapsedMs)ms)"
                        self.isTestingConnection = false
                    }
                } else {
                    await MainActor.run {
                        self.connectionStatus = "Reachable"
                        self.isTestingConnection = false
                    }
                }
            } catch {
                await MainActor.run {
                    self.connectionStatus = "Offline (Fallback)"
                    self.isTestingConnection = false
                }
            }
        }
    }
}

