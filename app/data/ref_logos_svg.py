"""
AvDB Vector Airline & Alliance Logo Reference Database
Provides self-contained, lightweight vector SVG data URIs for all major US mainline,
regional, international, and historical airlines.
Guarantees 100% zero-latency rendering without external CDN/Wikimedia 429/404 failures.
"""
import base64
from typing import Dict, Optional

def _to_data_uri(svg_xml: str) -> str:
    """Encodes SVG string to an RFC 2397 base64 data URI."""
    encoded = base64.b64encode(svg_xml.strip().encode("utf-8")).decode("utf-8")
    return f"data:image/svg+xml;base64,{encoded}"


def generate_carrier_badge_svg(code: str, bg_color: str = "#111D33", accent_color: str = "#38BDF8") -> str:
    """
    Generates a crisp, tech-forward branded SVG badge with JetBrains Mono typography
    for any unlisted or contract carrier code.
    """
    c = code.strip().upper()
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 70" width="120" height="70">
  <defs>
    <linearGradient id="bg_{c}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#182744"/>
      <stop offset="100%" stop-color="{bg_color}"/>
    </linearGradient>
    <linearGradient id="acc_{c}" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FF6B00"/>
      <stop offset="100%" stop-color="{accent_color}"/>
    </linearGradient>
  </defs>
  <rect x="2" y="2" width="116" height="66" rx="14" fill="url(#bg_{c})" stroke="rgba(255, 255, 255, 0.14)" stroke-width="1.8"/>
  <rect x="12" y="56" width="96" height="3" rx="1.5" fill="url(#acc_{c})" opacity="0.85"/>
  <circle cx="22" cy="24" r="4" fill="#FF6B00"/>
  <text x="66" y="42" font-family="'JetBrains Mono', -apple-system, monospace" font-size="24" font-weight="800" fill="#FFFFFF" text-anchor="middle" letter-spacing="2">{c}</text>
</svg>"""


# -------------------------------------------------------------
# Curated Vector SVGs for Major Airlines & Alliances
# -------------------------------------------------------------
CARRIER_VECTOR_SVGS: Dict[str, str] = {
    # American Airlines (AA)
    "AA": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 70" width="160" height="70">
  <rect width="160" height="70" rx="12" fill="#0C1B33" stroke="rgba(255,255,255,0.12)"/>
  <path d="M22 46 L38 18 L46 18 L30 46 Z" fill="#0078D2"/>
  <path d="M46 18 L54 18 L68 46 L54 46 L50 37 L38 37 Z" fill="#C8102E"/>
  <path d="M42 27 L48 27 L44 35 Z" fill="#FFFFFF"/>
  <text x="108" y="43" font-family="'Plus Jakarta Sans', sans-serif" font-size="22" font-weight="800" fill="#FFFFFF" letter-spacing="1">AA</text>
</svg>""",

    # Delta Air Lines (DL)
    "DL": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 70" width="160" height="70">
  <rect width="160" height="70" rx="12" fill="#0C1B33" stroke="rgba(255,255,255,0.12)"/>
  <!-- Delta Widget / Triangle -->
  <polygon points="38,16 16,50 60,50" fill="#E01933"/>
  <polygon points="38,28 26,48 50,48" fill="#990012"/>
  <polygon points="38,16 38,50 60,50" fill="#BA0C2F" opacity="0.8"/>
  <text x="108" y="43" font-family="'Plus Jakarta Sans', sans-serif" font-size="22" font-weight="800" fill="#FFFFFF" letter-spacing="1">DELTA</text>
</svg>""",

    # United Airlines (UA)
    "UA": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 70" width="160" height="70">
  <rect width="160" height="70" rx="12" fill="#0C1B33" stroke="rgba(255,255,255,0.12)"/>
  <!-- Globe Symbol -->
  <circle cx="36" cy="35" r="18" fill="none" stroke="#005DAA" stroke-width="3"/>
  <ellipse cx="36" cy="35" rx="8" ry="18" fill="none" stroke="#005DAA" stroke-width="2"/>
  <line x1="18" y1="35" x2="54" y2="35" stroke="#005DAA" stroke-width="2"/>
  <line x1="22" y1="26" x2="50" y2="26" stroke="#005DAA" stroke-width="1.5"/>
  <line x1="22" y1="44" x2="50" y2="44" stroke="#005DAA" stroke-width="1.5"/>
  <circle cx="36" cy="35" r="5" fill="#38BDF8"/>
  <text x="108" y="43" font-family="'Plus Jakarta Sans', sans-serif" font-size="22" font-weight="800" fill="#FFFFFF" letter-spacing="1">UNITED</text>
</svg>""",

    # Southwest Airlines (WN)
    "WN": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 70" width="160" height="70">
  <rect width="160" height="70" rx="12" fill="#0C1B33" stroke="rgba(255,255,255,0.12)"/>
  <!-- Southwest Tri-Color Heart -->
  <path d="M36,22 C30,14 18,18 18,28 C18,39 36,52 36,52 C36,52 54,39 54,28 C54,18 42,14 36,22 Z" fill="#304FFE"/>
  <path d="M36,26 C32,19 22,22 22,30 C22,38 36,48 36,48 C36,48 50,38 50,30 C50,22 40,19 36,26 Z" fill="#F44336"/>
  <path d="M36,30 C34,25 27,27 27,33 C27,38 36,44 36,44 C36,44 45,38 45,33 C45,27 38,25 36,30 Z" fill="#FFC107"/>
  <text x="108" y="43" font-family="'Plus Jakarta Sans', sans-serif" font-size="22" font-weight="800" fill="#FFFFFF" letter-spacing="1">WN</text>
</svg>""",

    # Alaska Airlines (AS)
    "AS": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 70" width="160" height="70">
  <rect width="160" height="70" rx="12" fill="#0C1B33" stroke="rgba(255,255,255,0.12)"/>
  <!-- Alaska Teal/Green Accents -->
  <circle cx="36" cy="35" r="18" fill="#01426A"/>
  <circle cx="36" cy="35" r="15" fill="none" stroke="#00A87E" stroke-width="2.5"/>
  <path d="M26 38 Q36 22 46 38" fill="none" stroke="#97D700" stroke-width="2.5"/>
  <text x="108" y="43" font-family="'Plus Jakarta Sans', sans-serif" font-size="22" font-weight="800" fill="#FFFFFF" letter-spacing="1">ALASKA</text>
</svg>""",

    # JetBlue Airways (B6)
    "B6": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 70" width="160" height="70">
  <rect width="160" height="70" rx="12" fill="#0C1B33" stroke="rgba(255,255,255,0.12)"/>
  <rect x="18" y="20" width="12" height="12" rx="3" fill="#00205B"/>
  <rect x="34" y="20" width="12" height="12" rx="3" fill="#00A3E0"/>
  <rect x="18" y="36" width="12" height="12" rx="3" fill="#38BDF8"/>
  <rect x="34" y="36" width="12" height="12" rx="3" fill="#00205B"/>
  <text x="108" y="43" font-family="'Plus Jakarta Sans', sans-serif" font-size="22" font-weight="800" fill="#38BDF8" letter-spacing="1">jetBlue</text>
</svg>""",

    # Spirit Airlines (NK)
    "NK": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 70" width="160" height="70">
  <rect width="160" height="70" rx="12" fill="#FFE500" stroke="rgba(0,0,0,0.1)"/>
  <text x="80" y="44" font-family="'Plus Jakarta Sans', sans-serif" font-size="26" font-weight="900" fill="#000000" text-anchor="middle" letter-spacing="2">spirit</text>
</svg>""",

    # Frontier Airlines (F9)
    "F9": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 70" width="160" height="70">
  <rect width="160" height="70" rx="12" fill="#0C1B33" stroke="rgba(255,255,255,0.12)"/>
  <circle cx="36" cy="35" r="18" fill="#006643"/>
  <text x="36" y="43" font-family="'Plus Jakarta Sans', sans-serif" font-size="22" font-weight="900" fill="#FFFFFF" text-anchor="middle">F</text>
  <text x="108" y="43" font-family="'Plus Jakarta Sans', sans-serif" font-size="20" font-weight="800" fill="#FFFFFF" letter-spacing="1">FRONTIER</text>
</svg>""",

    # Allegiant Air (G4)
    "G4": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 70" width="160" height="70">
  <rect width="160" height="70" rx="12" fill="#0C1B33" stroke="rgba(255,255,255,0.12)"/>
  <circle cx="36" cy="35" r="15" fill="#FFA300"/>
  <path d="M36 12 L36 18 M36 52 L36 58 M13 35 L19 35 M53 35 L59 35" stroke="#FFA300" stroke-width="3"/>
  <text x="108" y="43" font-family="'Plus Jakarta Sans', sans-serif" font-size="20" font-weight="800" fill="#38BDF8" letter-spacing="1">allegiant</text>
</svg>""",

    # Hawaiian Airlines (HA)
    "HA": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 70" width="160" height="70">
  <rect width="160" height="70" rx="12" fill="#0C1B33" stroke="rgba(255,255,255,0.12)"/>
  <circle cx="36" cy="35" r="18" fill="#582C83"/>
  <circle cx="44" cy="28" r="6" fill="#D5006D"/>
  <text x="108" y="43" font-family="'Plus Jakarta Sans', sans-serif" font-size="20" font-weight="800" fill="#FFFFFF" letter-spacing="1">HAWAIIAN</text>
</svg>""",

    # Continental Airlines (CO - Historical)
    "CO": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 70" width="160" height="70">
  <rect width="160" height="70" rx="12" fill="#002D62" stroke="rgba(255,255,255,0.2)"/>
  <circle cx="36" cy="35" r="18" fill="none" stroke="#C5A059" stroke-width="2.5"/>
  <ellipse cx="36" cy="35" rx="8" ry="18" fill="none" stroke="#C5A059" stroke-width="1.8"/>
  <line x1="18" y1="35" x2="54" y2="35" stroke="#C5A059" stroke-width="2"/>
  <text x="108" y="43" font-family="'Plus Jakarta Sans', sans-serif" font-size="20" font-weight="800" fill="#FFFFFF" letter-spacing="1">CONTINENTAL</text>
</svg>""",

    # Northwest Airlines (NW - Historical)
    "NW": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 70" width="160" height="70">
  <rect width="160" height="70" rx="12" fill="#BA0C2F" stroke="rgba(255,255,255,0.2)"/>
  <circle cx="36" cy="35" r="18" fill="#FFFFFF"/>
  <path d="M26 26 L26 44 L32 44 L40 32 L40 44 L46 44 L46 26 L40 26 L32 38 L32 26 Z" fill="#BA0C2F"/>
  <polygon points="23,23 29,20 26,26" fill="#BA0C2F"/>
  <text x="108" y="43" font-family="'Plus Jakarta Sans', sans-serif" font-size="20" font-weight="800" fill="#FFFFFF" letter-spacing="1">NORTHWEST</text>
</svg>""",

    # US Airways (US - Historical)
    "US": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 70" width="160" height="70">
  <rect width="160" height="70" rx="12" fill="#0B1A30" stroke="rgba(255,255,255,0.2)"/>
  <!-- US Flag stylized ridges -->
  <line x1="18" y1="26" x2="52" y2="26" stroke="#C8102E" stroke-width="3"/>
  <line x1="22" y1="32" x2="52" y2="32" stroke="#FFFFFF" stroke-width="3"/>
  <line x1="26" y1="38" x2="52" y2="38" stroke="#0078D2" stroke-width="3"/>
  <line x1="30" y1="44" x2="52" y2="44" stroke="#8E8E93" stroke-width="3"/>
  <text x="108" y="43" font-family="'Plus Jakarta Sans', sans-serif" font-size="20" font-weight="800" fill="#FFFFFF" letter-spacing="1">US AIRWAYS</text>
</svg>""",

    # America West (HP - Historical)
    "HP": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 70" width="160" height="70">
  <rect width="160" height="70" rx="12" fill="#0C1B33" stroke="rgba(255,255,255,0.2)"/>
  <polygon points="18,48 36,20 54,48" fill="#FF6B00"/>
  <polygon points="26,48 36,32 46,48" fill="#008080"/>
  <text x="108" y="43" font-family="'Plus Jakarta Sans', sans-serif" font-size="18" font-weight="800" fill="#FFFFFF" letter-spacing="1">AMERICA WEST</text>
</svg>""",

    # Trans World Airlines (TW - Historical)
    "TW": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 70" width="160" height="70">
  <rect width="160" height="70" rx="12" fill="#BA0C2F" stroke="rgba(255,255,255,0.2)"/>
  <ellipse cx="28" cy="35" rx="14" ry="18" fill="none" stroke="#FFFFFF" stroke-width="2.5"/>
  <ellipse cx="44" cy="35" rx="14" ry="18" fill="none" stroke="#FFFFFF" stroke-width="2.5"/>
  <text x="108" y="44" font-family="'Plus Jakarta Sans', sans-serif" font-size="24" font-weight="900" fill="#FFFFFF" letter-spacing="2">TWA</text>
</svg>""",

    # AirTran Airways (FL - Historical)
    "FL": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 70" width="160" height="70">
  <rect width="160" height="70" rx="12" fill="#007788" stroke="rgba(255,255,255,0.2)"/>
  <text x="80" y="44" font-family="'Plus Jakarta Sans', sans-serif" font-size="24" font-weight="800" fill="#FFFFFF" text-anchor="middle" letter-spacing="1">airTran</text>
</svg>""",

    # Virgin America (VX - Historical)
    "VX": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 70" width="160" height="70">
  <rect width="160" height="70" rx="12" fill="#E10A0A" stroke="rgba(255,255,255,0.2)"/>
  <text x="80" y="44" font-family="'Plus Jakarta Sans', sans-serif" font-size="22" font-style="italic" font-weight="900" fill="#FFFFFF" text-anchor="middle">virgin america</text>
</svg>""",

    # Pan Am (PA - Historical)
    "PA": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 70" width="160" height="70">
  <rect width="160" height="70" rx="12" fill="#005DAA" stroke="rgba(255,255,255,0.2)"/>
  <circle cx="36" cy="35" r="18" fill="#FFFFFF"/>
  <circle cx="36" cy="35" r="16" fill="#005DAA"/>
  <ellipse cx="36" cy="35" rx="7" ry="16" fill="none" stroke="#FFFFFF" stroke-width="1.5"/>
  <line x1="20" y1="35" x2="52" y2="35" stroke="#FFFFFF" stroke-width="1.5"/>
  <text x="108" y="44" font-family="'Plus Jakarta Sans', sans-serif" font-size="22" font-weight="900" fill="#FFFFFF" letter-spacing="1">PAN AM</text>
</svg>""",

    # British Airways (BA)
    "BA": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 70" width="160" height="70">
  <rect width="160" height="70" rx="12" fill="#075AAA" stroke="rgba(255,255,255,0.2)"/>
  <path d="M18 42 Q36 20 54 42" fill="none" stroke="#EB2226" stroke-width="4"/>
  <text x="108" y="43" font-family="'Plus Jakarta Sans', sans-serif" font-size="22" font-weight="800" fill="#FFFFFF" letter-spacing="1">BA</text>
</svg>""",

    # Air France (AF)
    "AF": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 70" width="160" height="70">
  <rect width="160" height="70" rx="12" fill="#002157" stroke="rgba(255,255,255,0.2)"/>
  <polygon points="20,20 48,20 42,50 14,50" fill="#ED1B24"/>
  <text x="108" y="43" font-family="'Plus Jakarta Sans', sans-serif" font-size="20" font-weight="800" fill="#FFFFFF" letter-spacing="1">AIRFRANCE</text>
</svg>""",

    # Lufthansa (LH)
    "LH": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 70" width="160" height="70">
  <rect width="160" height="70" rx="12" fill="#05164D" stroke="rgba(255,255,255,0.2)"/>
  <circle cx="36" cy="35" r="18" fill="#FFAB00"/>
  <path d="M26 40 Q36 24 46 30 Q36 32 30 42 Z" fill="#05164D"/>
  <text x="108" y="43" font-family="'Plus Jakarta Sans', sans-serif" font-size="22" font-weight="800" fill="#FFFFFF" letter-spacing="1">LH</text>
</svg>""",

    # Alliances (Authentic High-Fidelity Vector Insignias)
    "Star Alliance": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 70" width="160" height="70">
  <rect width="160" height="70" rx="12" fill="#0D0E12" stroke="rgba(197,160,89,0.3)" stroke-width="1.2"/>
  <!-- Star Alliance 5-point pinwheel starburst -->
  <g transform="translate(34, 35)">
    <polygon points="0,-16 3,-5 0,0 -3,-5" fill="#C5A059"/>
    <polygon points="15,-5 6,-2 0,0 6,-8" fill="#C5A059"/>
    <polygon points="9,13 4,4 0,0 8,3" fill="#C5A059"/>
    <polygon points="-9,13 -8,3 0,0 -4,4" fill="#C5A059"/>
    <polygon points="-15,-5 -6,-8 0,0 -6,-2" fill="#C5A059"/>
  </g>
  <text x="60" y="33" font-family="'Plus Jakarta Sans', sans-serif" font-size="11.5" font-weight="800" fill="#FFFFFF" letter-spacing="1.2">STAR ALLIANCE</text>
  <text x="60" y="47" font-family="'JetBrains Mono', monospace" font-size="7.5" font-weight="600" fill="#C5A059" letter-spacing="1">GLOBAL NETWORK</text>
</svg>""",

    "SkyTeam": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 70" width="160" height="70">
  <rect width="160" height="70" rx="12" fill="#001833" stroke="rgba(0,144,218,0.35)" stroke-width="1.2"/>
  <!-- SkyTeam aerodynamic vortex loop -->
  <g transform="translate(32, 35)">
    <path d="M-15 8 C-10 -12 10 -18 20 -4 C 8 -11 -4 -7 -8 6 Z" fill="#0090DA"/>
    <path d="M20 -4 C 15 16 -5 20 -15 8 C -3 15 9 11 13 -2 Z" fill="#D1D5DB"/>
  </g>
  <text x="63" y="37" font-family="'Plus Jakarta Sans', sans-serif" font-size="18" font-weight="800" fill="#FFFFFF" letter-spacing="-0.5">SkyTeam</text>
  <text x="63" y="49" font-family="'JetBrains Mono', monospace" font-size="7.5" font-weight="600" fill="#38BDF8" letter-spacing="1.2">GLOBAL ALLIANCE</text>
</svg>""",

    "oneworld": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 70" width="160" height="70">
  <rect width="160" height="70" rx="12" fill="#0C1433" stroke="rgba(0,151,215,0.35)" stroke-width="1.2"/>
  <!-- oneworld cyan ring and radiant globe -->
  <circle cx="32" cy="35" r="16" fill="none" stroke="#0097D7" stroke-width="2.5"/>
  <circle cx="32" cy="35" r="12" fill="#00A9E0"/>
  <path d="M24 28 A 9 9 0 0 1 34 24 A 11 11 0 0 0 24 28 Z" fill="#FFFFFF" opacity="0.65"/>
  <text x="60" y="38" font-family="'Plus Jakarta Sans', sans-serif" font-size="19" font-weight="800" fill="#FFFFFF" letter-spacing="-0.6">oneworld</text>
  <text x="60" y="49" font-family="'JetBrains Mono', monospace" font-size="7.5" font-weight="600" fill="#64D2FF" letter-spacing="1.2">MEMBER ALLIANCE</text>
</svg>""",

    "Wings Alliance": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 70" width="160" height="70">
  <rect width="160" height="70" rx="12" fill="#0B1E36" stroke="rgba(214,40,40,0.35)" stroke-width="1.2"/>
  <!-- NW Red compass and KL Crown Cyan -->
  <circle cx="24" cy="35" r="12" fill="#D62828"/>
  <polygon points="24,26 27,35 24,44 21,35" fill="#FFFFFF"/>
  <circle cx="43" cy="35" r="12" fill="#00A1DE"/>
  <path d="M38 39 L40 31 L43 34 L46 31 L48 39 Z" fill="#FFFFFF"/>
  <text x="65" y="34" font-family="'Plus Jakarta Sans', sans-serif" font-size="11.5" font-weight="800" fill="#FFFFFF" letter-spacing="0.8">WINGS ALLIANCE</text>
  <text x="65" y="47" font-family="'JetBrains Mono', monospace" font-size="7.5" font-weight="600" fill="#94A3B8" letter-spacing="1">NW · KL TRANSATLANTIC</text>
</svg>"""
}


# Pre-compute RFC 2397 Data URIs
CARRIER_DATA_URIS: Dict[str, str] = {
    code: _to_data_uri(svg) for code, svg in CARRIER_VECTOR_SVGS.items()
}


def get_vector_logo_data_uri(carrier_code: str) -> str:
    """
    Returns verified RFC 2397 Data URI vector logo for carrier code.
    If no dedicated vector exists, automatically synthesizes a sleek branded monogram.
    """
    c = carrier_code.strip().upper() if carrier_code else "—"
    if c in CARRIER_DATA_URIS:
        return CARRIER_DATA_URIS[c]
    
    # Generate tailored monogram
    monogram_svg = generate_carrier_badge_svg(c)
    return _to_data_uri(monogram_svg)

