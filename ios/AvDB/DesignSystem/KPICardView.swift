import SwiftUI

/// Metric card display for aviation metrics (Load factor, seats/departure, fare, ASM, RPM).
public struct KPICardView: View {
    public let title: String
    public let value: String
    public let subtitle: String?
    public let icon: String
    public let accentColor: Color

    public init(
        title: String,
        value: String,
        subtitle: String? = nil,
        icon: String = "chart.bar.fill",
        accentColor: Color = AvDBTheme.accentBlue
    ) {
        self.title = title
        self.value = value
        self.subtitle = subtitle
        self.icon = icon
        self.accentColor = accentColor
    }

    public var body: some View {
        GlassCard(cornerRadius: 14) {
            VStack(alignment: .leading, spacing: 8) {
                HStack {
                    Image(systemName: icon)
                        .font(.system(size: 14, weight: .semibold))
                        .foregroundColor(accentColor)
                    Spacer()
                }

                Text(value)
                    .font(.system(size: 22, weight: .bold, design: .rounded))
                    .foregroundColor(AvDBTheme.primaryText)
                    .lineLimit(1)
                    .minimumScaleFactor(0.8)

                VStack(alignment: .leading, spacing: 2) {
                    Text(title)
                        .font(.system(size: 11, weight: .medium))
                        .foregroundColor(AvDBTheme.secondaryText)
                        .textCase(.uppercase)

                    if let subtitle = subtitle {
                        Text(subtitle)
                            .font(.system(size: 10, weight: .regular))
                            .foregroundColor(AvDBTheme.tertiaryText)
                    }
                }
            }
        }
    }
}

