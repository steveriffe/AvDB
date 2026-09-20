import SwiftUI

/// AvDB Design System - Dark Mode First, Obsidian Glass, Jet-Aviation Precision.
public enum AvDBTheme {
    // MARK: - Surfaces
    public static let canvasBackground = Color(red: 0.027, green: 0.059, blue: 0.118) // #070F1E
    public static let surfaceObsidian = Color(red: 0.043, green: 0.098, blue: 0.173)  // #0B192C
    public static let surfaceCard = Color(red: 0.067, green: 0.114, blue: 0.200)      // #111D33
    public static let surfaceElevated = Color(red: 0.094, green: 0.153, blue: 0.259)  // #182742

    // MARK: - Vibrant Accents
    public static let accentCyan = Color(red: 0.000, green: 0.949, blue: 0.996)       // #00F2FE
    public static let accentBlue = Color(red: 0.039, green: 0.518, blue: 1.000)       // #0A84FF
    public static let accentGreen = Color(red: 0.188, green: 0.820, blue: 0.345)      // #30D158
    public static let accentAmber = Color(red: 0.961, green: 0.620, blue: 0.043)      // #F59E0B
    public static let accentCoral = Color(red: 1.000, green: 0.420, blue: 0.420)      // #FF6B6B
    public static let accentPurple = Color(red: 0.749, green: 0.353, blue: 0.949)     // #BF5AF2

    // MARK: - Text Gradients
    public static let primaryText = Color.white
    public static let secondaryText = Color(white: 0.65)
    public static let tertiaryText = Color(white: 0.45)
    public static let borderStroke = Color.white.opacity(0.08)
    public static let borderGlow = accentBlue.opacity(0.25)

    // MARK: - Gradients
    public static let heroGradient = LinearGradient(
        colors: [accentCyan, accentBlue],
        startPoint: .topLeading,
        endPoint: .bottomTrailing
    )

    public static let cardGradient = LinearGradient(
        colors: [Color.white.opacity(0.04), Color.white.opacity(0.01)],
        startPoint: .topLeading,
        endPoint: .bottomTrailing
    )
}

public extension View {
    func avdbCanvas() -> some View {
        self.background(AvDBTheme.canvasBackground.ignoresSafeArea())
    }
}

