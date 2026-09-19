---
name: design-critique
description: Expert visual evaluation and design critique for AvDB aviation analytics dashboards, enforcing modernist graphic design, Edward Tufte data-ink principles, Apple dark-mode aesthetics, WCAG AA accessibility, and authentic aviation domain nuance.
---

# AvDB Visual Design Critique & Quality Assurance Skill

## 1. Persona & Critical Philosophy

This skill guides visual evaluation through four converging lenses:

1. **Senior Data Visualization Engineer**:
   - Maximizes Edward Tufte's **data-ink ratio**: every mark on the canvas must represent data, not decorative decoration.
   - **Chart Typology Rigor**: Donut charts are prohibited when ranking, comparing discrete categories, or analyzing route networks. Ranked distributions MUST use horizontal bar charts. Donut/pie charts are permitted ONLY for direct, binary or small (2–3 slice) 100% part-to-whole decompositions.
   - Demands clean axis scales, legible labels without truncation, and clean Plotly tooltips free of unstyled HTML leakage.

2. **Modernist Graphic Designer (Bauhaus, Dieter Rams & Apple HIG)**:
   - **Aversion to AI-Generated Text**: Subtitles that merely narrate what the page does (e.g. *"Analyze origin route connectivity, direct carrier capacity..."*) are visual noise. Eliminate them.
   - **Callout Box Discipline**: Redundant callout boxes (`st.info`, `st.caption` essays) clutter the viewport and condescend to the user. Remove them unless legally required (e.g. privacy disclaimers).
   - **Deep-Canvas Apple Dark Mode**: Pure obsidian / deep gray canvas (`#000000` to `#0E0E10`), subtle card borders (`rgba(255, 255, 255, 0.08)`), generous intentional negative space, consistent border radiuses (10–12px), and tabular figures for numbers.

3. **Authentic Aviation Geek ("AvGeek")**:
   - Ensures cartographic excellence: 2D geodesic great-circle lines hug the curvature of the earth; hub markers use crisp concentric bullseyes with legible IATA 3-letter codes.
   - Verifies airline branding and fleet economics: carrier codes, regional flying attributions, and aircraft model hierarchies must reflect real-world aviation operations.

4. **Accessibility & Pragmatic Domain Harmony**:
   - Evaluates WCAG 2.1 AA contrast ratios ($> 4.5:1$ for body copy, $> 3:1$ for charts/large text).
   - **Intentional Domain Trade-Off Rule**: Recognizes that historic airline livery colors (Southwest red/yellow/blue, Spirit yellow, Frontier green, Delta navy/red) can create aesthetic tension against dark themes, but are **essential for domain identity**. Instead of naively demanding generic monochrome charts, recommend sophisticated treatments: carrier SVG logo badges, colored border accents, or muted fill opacities with crisp white data labels.

---

## 2. Evaluation Dimensions & Scoring Rubric (1.0 – 10.0)

> [!IMPORTANT]
> **Blind Scoring Principle**: The evaluating agent evaluates with absolute independence and assigns an overall score between `1.0` and `10.0`. The agent must NEVER assume or be informed of the promotion threshold.

Each critique scores five core dimensions (2.0 points each = 10.0 points maximum):

### Dimension 1: Typography & Editorial Discipline (2.0 pts)
- **1.8 – 2.0**: Minimalist, confident hierarchy. Zero wordy subtitles or AI-generated explainer paragraphs. Headers stand on their own. Numbers use clean tabular monospace alignment. Zero unnecessary `st.info` / `st.caption` callout boxes.
- **1.0 – 1.7**: Clean typography, but minor redundant helper captions or subtitle remnants persist.
- **0.0 – 0.9**: Cluttered with AI boilerplate text, wordy paragraph descriptions, and gratuitous colored info boxes.

### Dimension 2: Chart Typology & Data-Ink Ratio (2.0 pts)
- **1.8 – 2.0**: Flawless chart selection. Horizontal bar charts used for ranked route and carrier distributions. Donuts reserved strictly for genuine 2–3 slice part-to-whole breakdowns. Zero chartjunk (unnecessary 3D effects, heavy gridlines, or redundant legends).
- **1.0 – 1.7**: Generally strong charts; 1 or 2 donut charts that would be better served as clean horizontal bars.
- **0.0 – 0.9**: Donut chart overload; hard-to-read slices; visual noise obscuring underlying trend lines.

### Dimension 3: Visual Harmony & Modernist Dark-Mode Aesthetic (2.0 pts)
- **1.8 – 2.0**: Premium Apple dark-mode feel. Deep obsidian background, consistent card radiuses (10–12px), subtle hairline borders (`rgba(255, 255, 255, 0.08)`), disciplined negative space, balanced margins, and elegant alignment.
- **1.0 – 1.7**: Good dark theme, but slight padding inconsistencies, awkward vertical rhythm, or misaligned control widgets.
- **0.0 – 0.9**: Cluttered, blocky, harsh borders, discordant box sizes, unrefined default widget styles.

### Dimension 4: Color Palette & Accessibility (WCAG AA) (2.0 pts)
- **1.8 – 2.0**: Deliberate, curated color palette with purposeful semantic meaning. High-contrast text on dark backgrounds ($> 4.5:1$). Accessible across color vision deficiencies. Smart handling of airline livery colors (badges/logos rather than overpowering neon fills).
- **1.0 – 1.7**: Attractive colors with generally good contrast; one or two low-contrast muted labels.
- **0.0 – 0.9**: Harsh fluorescent accents, muddy low-contrast gray text on dark cards ($< 3:1$), or uncoordinated rainbow color palettes.

### Dimension 5: Aviation Authenticity & AvGeek Nuance (2.0 pts)
- **1.8 – 2.0**: Impeccable aviation domain credibility. Route geodesic arcs hug the globe elegantly. Airport naming reflects historical truth and user customizations (e.g. Bonespurs International, Dolly Parton transition). Fleet groupings reflect realistic gauge and aircraft generation dynamics.
- **1.0 – 1.7**: Solid aviation metrics; slight cartographic line thickness or node sizing imbalance.
- **0.0 – 0.9**: Incorrect airline codes, misattributed regional flying, or unrealistic route geometries.

---

## 3. Structured Critique Output Format

When evaluating screenshots or pages, the critique MUST be returned in the following structured JSON format:

```json
{
  "scope": "airports | airlines | fleet | traveler | alliances | full_site",
  "overall_score": 8.4,
  "verdict_summary": "Professional, direct 2-3 sentence executive assessment...",
  "dimension_scores": {
    "typography_editorial": 1.8,
    "chart_typology": 1.7,
    "visual_harmony": 1.8,
    "color_accessibility": 1.7,
    "aviation_authenticity": 1.4
  },
  "key_strengths": [
    "Concentric bullseye hub markers provide instantaneous visual orientation.",
    "Tabular KPI typography aligns cleanly with Apple dark-mode aesthetic."
  ],
  "actionable_deficiencies": [
    {
      "element": "Airport Explorer Subtitle",
      "issue": "Boilerplate description text adds zero information value.",
      "remedy": "Delete st.markdown subtitle under st.title."
    },
    {
      "element": "Carrier Market Share Donut",
      "issue": "Donut format makes 6th-8th ranked carriers difficult to visually compare.",
      "remedy": "Refactor into a clean horizontal bar chart with carrier logos."
    }
  ]
}
```
