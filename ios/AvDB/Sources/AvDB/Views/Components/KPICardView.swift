import SwiftUI

/// Elegant Apple Design Language KPI Metric Card
public struct KPICardView: View {
    let title: String
    let value: String
    let subtitle: String?
    let iconName: String
    let accentColor: Color

    public init(
        title: String,
        value: String,
        subtitle: String? = nil,
        iconName: String,
        accentColor: Color = .blue
    ) {
        self.title = title
        self.value = value
        self.subtitle = subtitle
        self.iconName = iconName
        self.accentColor = accentColor
    }

    public var body: some View {
        GlassCard {
            VStack(alignment: .leading, spacing: 6) {
                HStack {
                    Image(systemName: iconName)
                        .font(.system(size: 14, weight: .semibold))
                        .foregroundStyle(accentColor)
                    Text(title)
                        .font(.caption)
                        .fontWeight(.medium)
                        .foregroundStyle(.secondary)
                    Spacer()
                }

                Text(value)
                    .font(.system(size: 22, weight: .bold, design: .rounded))
                    .foregroundStyle(.primary)
                    .minimumScaleFactor(0.7)
                    .lineLimit(1)

                if let subtitle = subtitle {
                    Text(subtitle)
                        .font(.caption2)
                        .foregroundStyle(.secondary)
                        .lineLimit(1)
                }
            }
        }
    }
}
