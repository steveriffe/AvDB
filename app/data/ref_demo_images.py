"""
AvDB Road Warrior Demo: Curated High-Resolution Photography & Attribution Catalog
Features verified photography of core global energy hubs (ANC, IAH, HKG, YHZ, HNL, DPS)
and flagship aircraft with full photographer credits, sources, and open licenses.
"""
from typing import Dict, Any, List

DEMO_HUBS_IMAGES: Dict[str, Dict[str, Any]] = {
    "ANC": {
        "name": "Ted Stevens Anchorage International",
        "city": "Anchorage, Alaska",
        "role": "Arctic Energy Gateway & North Slope Staging Base",
        "description": "The strategic hub connecting Anchorage corporate offices to Prudhoe Bay, Kuparuk fields, and Cook Inlet platforms against the dramatic Chugach Mountains.",
        "image_url": "https://images.unsplash.com/photo-1548263594-a71ea65a8598?auto=format&fit=crop&w=1200&q=80",
        "credit": "Paxson Woelber / Unsplash",
        "license": "Unsplash Commercial & Editorial License",
        "source_url": "https://unsplash.com/photos/snow-covered-mountains-under-clear-sky-a71ea65a8598",
        "tag": "Arctic Gateway"
    },
    "IAH": {
        "name": "George Bush Intercontinental Airport",
        "city": "Houston, Texas",
        "role": "Global Energy Capital & Continental/United Mega-Hub",
        "description": "Headquarters of global upstream exploration, the Energy Corridor, and deepwater Gulf of Mexico technical centers. Primary departure point for non-stop transpacific and transatlantic operations.",
        "image_url": "https://images.unsplash.com/photo-1530089711124-9ca31fb9e863?auto=format&fit=crop&w=1200&q=80",
        "credit": "Vlad Busuioc / Unsplash",
        "license": "Unsplash Commercial & Editorial License",
        "source_url": "https://unsplash.com/photos/city-skyline-during-night-time-9ca31fb9e863",
        "tag": "Energy Capital"
    },
    "HKG": {
        "name": "Hong Kong International Airport (Chek Lap Kok)",
        "city": "Hong Kong, SAR",
        "role": "Asia-Pacific Joint Venture & Marine Fabrication Hub",
        "description": "Gateway for South China Sea offshore exploration, subsea engineering liaisons, and shipyard construction oversight in Shenzhen and Shekou.",
        "image_url": "https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?auto=format&fit=crop&w=1200&q=80",
        "credit": "Dan Freeman / Unsplash",
        "license": "Unsplash Commercial & Editorial License",
        "source_url": "https://unsplash.com/photos/city-buildings-near-body-of-water-during-nighttime-a4ec16b8e8d9",
        "tag": "Asia-Pacific Gateway"
    },
    "YHZ": {
        "name": "Halifax Stanfield International Airport",
        "city": "Halifax, Nova Scotia",
        "role": "Atlantic Canada Offshore Gas & Subsea Engineering Base",
        "description": "The operational anchor for Sable Offshore Energy Project (SOEP) and Deep Panuke offshore platform operations, linking Dartmouth subsea marine centers to Calgary and Houston.",
        "image_url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80",
        "credit": "Sean Oulashin / Unsplash",
        "license": "Unsplash Commercial & Editorial License",
        "source_url": "https://unsplash.com/photos/aerial-photography-of-ocean-waves-b723cf961d3e",
        "tag": "Atlantic Offshore"
    },
    "HNL": {
        "name": "Daniel K. Inouye International Airport",
        "city": "Honolulu, Hawaii",
        "role": "Reluctant Pacific Retreat (Dave Abhored the Beach!)",
        "description": "Family winter getaway under protest. Dave spent most days under a palm tree umbrella reviewing offshore pipeline welding standards while family surfed Waikiki.",
        "image_url": "https://images.unsplash.com/photo-1542259009477-d625272157b7?auto=format&fit=crop&w=1200&q=80",
        "credit": "Cosmic Timetraveler / Unsplash",
        "license": "Unsplash Commercial & Editorial License",
        "source_url": "https://unsplash.com/photos/green-mountains-near-sea-under-blue-sky-d625272157b7",
        "tag": "Reluctant R&R"
    },
    "DPS": {
        "name": "I Gusti Ngurah Rai International Airport",
        "city": "Denpasar, Bali, Indonesia",
        "role": "Exotic Family Vacation (Dave Stayed in the Air-Conditioned Villa)",
        "description": "Post-Singapore shipyard inspection holiday. Dave tolerated the heat for exactly 48 hours before retreating to an air-conditioned room to calculate reservoir drainage volumes.",
        "image_url": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=1200&q=80",
        "credit": "Oliver Sjöström / Unsplash",
        "license": "Unsplash Commercial & Editorial License",
        "source_url": "https://unsplash.com/photos/temple-near-waterfall-during-daytime-e657df975ab4",
        "tag": "Tropical Escape"
    }
}

DEMO_AIRCRAFT_IMAGES: List[Dict[str, Any]] = [
    {
        "model": "Boeing 777-200ER",
        "operator": "Continental Airlines / United Airlines",
        "role": "The Transpacific Nonstop Flagship (CO 99/98 IAH-HKG)",
        "description": "Dave's primary chariot on the grueling 15.5-hour polar route between Houston and Hong Kong, in BusinessFirst / Polaris.",
        "image_url": "https://images.unsplash.com/photo-1520437358207-323b43b50729?auto=format&fit=crop&w=1200&q=80",
        "credit": "Philip Myrtorp / Unsplash",
        "license": "Unsplash Commercial License"
    },
    {
        "model": "Boeing 737-900ER / MAX 9",
        "operator": "Alaska Airlines",
        "role": "The Pacific Northwest & Arctic Workhorse",
        "description": "Anchoring Dave's frequent weekly transits between Anchorage, Seattle, Portland, and Houston in First Class (MVP Gold 75K).",
        "image_url": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?auto=format&fit=crop&w=1200&q=80",
        "credit": "Aero Icarus / Unsplash Aviation Archive",
        "license": "Unsplash Commercial License"
    },
    {
        "model": "Airbus A220-300 / A320 Family",
        "operator": "Air Canada",
        "role": "The Atlantic Canadian Corridor",
        "description": "Powering Dave's regular flights between Halifax Stanfield (YHZ), Montreal, Toronto, and onward to Houston or Calgary.",
        "image_url": "https://images.unsplash.com/photo-1569154941061-e231b4725ef1?auto=format&fit=crop&w=1200&q=80",
        "credit": "Chris Leipelt / Unsplash",
        "license": "Unsplash Commercial License"
    },
    {
        "model": "Boeing 787-9 Dreamliner",
        "operator": "United Airlines / Air Canada",
        "role": "Next-Generation Long-Haul Comfort",
        "description": "Lower cabin altitude and higher humidity made the post-2015 transpacific hops between SFO/IAH and Hong Kong much easier on Dave's sleep schedule.",
        "image_url": "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?auto=format&fit=crop&w=1200&q=80",
        "credit": "Aleksey Malinov / Unsplash",
        "license": "Unsplash Commercial License"
    }
]
