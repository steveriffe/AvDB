"""
AvDB Airline Merger & Corporate Lineage Reference Data
Authoritative timeline of major US commercial airline mergers, acquisitions,
and operating certificate consolidations dating back to 1990.
"""
from typing import List, Dict, Any, Optional

AIRLINE_MERGERS: List[Dict[str, Any]] = [
    {
        "merger_id": "CO_UA_2010",
        "predecessor_code": "CO",
        "predecessor_name": "Continental Airlines",
        "predecessor_logo": "https://upload.wikimedia.org/wikipedia/commons/b/b2/Continental_Airlines_Logo_1991.svg",
        "successor_code": "UA",
        "successor_name": "United Airlines",
        "successor_logo": "https://upload.wikimedia.org/wikipedia/commons/e/e0/United_Airlines_Logo.svg",
        "announced_date": "2010-05-03",
        "closing_date": "2010-10-01",
        "soc_date": "2011-11-30",  # Single Operating Certificate
        "final_flight_date": "2012-03-02",  # CO1268 PHX-CLE
        "cutover_year": 2012,
        "hubs_absorbed": ["IAH", "EWR", "CLE", "GUM"],
        "fleet_types_inherited": ["Boeing 737-700/800/900ER", "Boeing 757-200/300", "Boeing 767-200ER/400ER", "Boeing 777-200ER", "Boeing 787-8"],
        "summary": "United and Continental combined in a $3.2B merger of equals to create the world's largest carrier at the time. Adopted the United name and Continental's globe livery and Houston/Newark mega-hubs.",
        "source_url": "https://ir.united.com/news-releases/news-release-details/united-and-continental-announce-merger-equals-create-world-class"
    },
    {
        "merger_id": "NW_DL_2008",
        "predecessor_code": "NW",
        "predecessor_name": "Northwest Airlines",
        "predecessor_logo": "https://upload.wikimedia.org/wikipedia/commons/e/ec/Northwest_Airlines_Logo.svg",
        "successor_code": "DL",
        "successor_name": "Delta Air Lines",
        "successor_logo": "https://upload.wikimedia.org/wikipedia/commons/d/d1/Delta_logo.svg",
        "announced_date": "2008-04-14",
        "closing_date": "2008-10-29",
        "soc_date": "2009-12-31",
        "final_flight_date": "2010-01-31",  # NW2470 LAX-MSP
        "cutover_year": 2010,
        "hubs_absorbed": ["MSP", "DTW", "MEM", "NRT"],
        "fleet_types_inherited": ["Airbus A330-200/300", "Airbus A319/A320", "Boeing 747-400", "Boeing 757-200/300", "McDonnell Douglas DC-9"],
        "summary": "Delta acquired Northwest Airlines in a $2.6B all-stock transaction, pioneering post-deregulation mega-consolidation. Delta gained key upper-Midwest hubs (DTW, MSP) and premier transpacific routes via Tokyo Narita.",
        "source_url": "https://news.delta.com/delta-air-lines-northwest-airlines-combining-create-americas-premier-global-airline"
    },
    {
        "merger_id": "US_AA_2013",
        "predecessor_code": "US",
        "predecessor_name": "US Airways",
        "predecessor_logo": "https://upload.wikimedia.org/wikipedia/commons/2/23/US_Airways_logo.svg",
        "successor_code": "AA",
        "successor_name": "American Airlines",
        "successor_logo": "https://upload.wikimedia.org/wikipedia/commons/0/07/American_Airlines_logo_2013.svg",
        "announced_date": "2013-02-14",
        "closing_date": "2013-12-09",
        "soc_date": "2015-04-08",
        "final_flight_date": "2015-10-16",  # US1931 SFO-PHL
        "cutover_year": 2015,
        "hubs_absorbed": ["CLT", "PHL", "PHX", "DCA"],
        "fleet_types_inherited": ["Airbus A319/A320/A321", "Airbus A330-200/300", "Boeing 757-200", "Embraer E190"],
        "summary": "US Airways merged with AMR Corporation as American exited Chapter 11 bankruptcy. US Airways leadership assumed control of the combined airline, retaining the American Airlines name and adding major East Coast hubs.",
        "source_url": "https://news.aa.com/news/news-details/2013/American-Airlines-And-US-Airways-Complete-Merger-To-Create-The-New-American-Airlines/default.aspx"
    },
    {
        "merger_id": "HP_US_2005",
        "predecessor_code": "HP",
        "predecessor_name": "America West Airlines",
        "predecessor_logo": "https://upload.wikimedia.org/wikipedia/commons/f/f3/America_West_Airlines_logo.svg",
        "successor_code": "US",
        "successor_name": "US Airways",
        "successor_logo": "https://upload.wikimedia.org/wikipedia/commons/2/23/US_Airways_logo.svg",
        "announced_date": "2005-05-19",
        "closing_date": "2005-09-27",
        "soc_date": "2007-09-25",
        "final_flight_date": "2007-10-01",
        "cutover_year": 2007,
        "hubs_absorbed": ["PHX", "LAS"],
        "fleet_types_inherited": ["Airbus A319/A320", "Boeing 737-300", "Boeing 757-200"],
        "summary": "America West merged with bankrupt US Airways in a reverse takeover led by America West CEO Doug Parker. Retained the US Airways brand while incorporating America West's Phoenix and Las Vegas hubs.",
        "source_url": "https://en.wikipedia.org/wiki/America_West_Airlines"
    },
    {
        "merger_id": "QQ_AA_1999",
        "predecessor_code": "QQ",
        "predecessor_name": "Reno Air",
        "predecessor_logo": "https://upload.wikimedia.org/wikipedia/commons/e/e0/Reno_Air_logo.svg",
        "successor_code": "AA",
        "successor_name": "American Airlines",
        "successor_logo": "https://upload.wikimedia.org/wikipedia/commons/0/07/American_Airlines_logo_2013.svg",
        "announced_date": "1998-11-19",
        "closing_date": "1999-02-01",
        "soc_date": "1999-08-31",
        "final_flight_date": "1999-08-30",
        "cutover_year": 1999,
        "hubs_absorbed": ["RNO", "SJC"],
        "fleet_types_inherited": ["McDonnell Douglas MD-82/MD-83", "McDonnell Douglas MD-90"],
        "summary": "American Airlines acquired low-cost regional pioneer Reno Air for $124M to establish a West Coast focus city presence in San Jose (SJC) and Reno (RNO), integrating its MD-80/90 fleet.",
        "source_url": "https://en.wikipedia.org/wiki/Reno_Air"
    },
    {
        "merger_id": "TW_AA_2001",
        "predecessor_code": "TW",
        "predecessor_name": "Trans World Airlines (TWA)",
        "predecessor_logo": "https://upload.wikimedia.org/wikipedia/commons/2/2c/Trans_World_Airlines_Logo.svg",
        "successor_code": "AA",
        "successor_name": "American Airlines",
        "successor_logo": "https://upload.wikimedia.org/wikipedia/commons/0/07/American_Airlines_logo_2013.svg",
        "announced_date": "2001-01-10",
        "closing_date": "2001-04-09",
        "soc_date": "2001-12-01",
        "final_flight_date": "2001-12-01",  # TW220 Kansas City-St. Louis
        "cutover_year": 2001,
        "hubs_absorbed": ["STL", "JFK"],
        "fleet_types_inherited": ["Boeing 717-200", "Boeing 757-200", "Boeing 767-300ER", "McDonnell Douglas MD-82/MD-83"],
        "summary": "American Airlines acquired the assets of storied carrier TWA out of Chapter 11 bankruptcy. Absorbed TWA's St. Louis (STL) central fortress hub and modern Boeing 717 aircraft.",
        "source_url": "https://en.wikipedia.org/wiki/Trans_World_Airlines"
    },
    {
        "merger_id": "FL_WN_2011",
        "predecessor_code": "FL",
        "predecessor_name": "AirTran Airways",
        "predecessor_logo": "https://upload.wikimedia.org/wikipedia/commons/5/52/AirTran_Airways_logo.svg",
        "successor_code": "WN",
        "successor_name": "Southwest Airlines",
        "successor_logo": "https://upload.wikimedia.org/wikipedia/commons/c/c4/Southwest_Airlines_logo_2014.svg",
        "announced_date": "2010-09-27",
        "closing_date": "2011-05-02",
        "soc_date": "2012-03-01",
        "final_flight_date": "2014-12-28",  # FL1 ATL-TPA
        "cutover_year": 2014,
        "hubs_absorbed": ["ATL", "MCO", "BWI", "MDW"],
        "fleet_types_inherited": ["Boeing 717-200 (subleased to Delta)", "Boeing 737-700"],
        "summary": "Southwest Airlines acquired AirTran for $1.4B, gaining immediate critical scale in Atlanta (ATL)—the world's busiest airport—and inaugural international routes into the Caribbean and Mexico.",
        "source_url": "https://www.southwestairlinesinvestorrelations.com/news-and-events/news-releases/2011/05-02-2011"
    },
    {
        "merger_id": "VX_AS_2016",
        "predecessor_code": "VX",
        "predecessor_name": "Virgin America",
        "predecessor_logo": "https://upload.wikimedia.org/wikipedia/commons/5/5a/Virgin_America_Logo.svg",
        "successor_code": "AS",
        "successor_name": "Alaska Airlines",
        "successor_logo": "https://upload.wikimedia.org/wikipedia/commons/1/17/Alaska_Airlines_logo.svg",
        "announced_date": "2016-04-04",
        "closing_date": "2016-12-14",
        "soc_date": "2018-01-11",
        "final_flight_date": "2018-04-24",  # VX1947 SFO-LAX
        "cutover_year": 2018,
        "hubs_absorbed": ["SFO", "LAX"],
        "fleet_types_inherited": ["Airbus A319-100", "Airbus A320-200", "Airbus A321neo"],
        "summary": "Alaska Air Group acquired California boutique carrier Virgin America for $2.6B, solidifying Alaska's position as the dominant West Coast airline and adding prime slots at SFO, LAX, and JFK.",
        "source_url": "https://news.alaskaair.com/news-releases/alaska-air-group-closes-acquisition-of-virgin-america/"
    },
    {
        "merger_id": "YX_F9_2009",
        "predecessor_code": "YX",
        "predecessor_name": "Midwest Airlines (Midwest Express)",
        "predecessor_logo": "https://upload.wikimedia.org/wikipedia/commons/3/30/Midwest_Airlines_logo.svg",
        "successor_code": "F9",
        "successor_name": "Frontier Airlines",
        "successor_logo": "https://upload.wikimedia.org/wikipedia/commons/8/86/Frontier_Airlines_Logo.svg",
        "announced_date": "2009-06-23",
        "closing_date": "2009-07-31",
        "soc_date": "2010-04-13",
        "final_flight_date": "2011-10-31",
        "cutover_year": 2011,
        "hubs_absorbed": ["MKE", "OMA"],
        "fleet_types_inherited": ["Boeing 717-200", "Embraer E170/E190"],
        "summary": "Republic Airways Holdings acquired Midwest Airlines and Frontier Airlines in 2009, combining operations under the Frontier name and transitioning Milwaukee (MKE) from an upscale hub into an LCC focus city.",
        "source_url": "https://en.wikipedia.org/wiki/Midwest_Airlines"
    },
    {
        "merger_id": "HA_AS_2024",
        "predecessor_code": "HA",
        "predecessor_name": "Hawaiian Airlines",
        "predecessor_logo": "https://upload.wikimedia.org/wikipedia/commons/5/52/Hawaiian_Airlines_Logo.svg",
        "successor_code": "AS",
        "successor_name": "Alaska Airlines",
        "successor_logo": "https://upload.wikimedia.org/wikipedia/commons/1/17/Alaska_Airlines_logo.svg",
        "announced_date": "2023-12-03",
        "closing_date": "2024-09-18",
        "soc_date": "Pending",
        "final_flight_date": "Active dual-brand",
        "cutover_year": 2025,
        "hubs_absorbed": ["HNL", "OGG"],
        "fleet_types_inherited": ["Airbus A330-200", "Airbus A321neo", "Boeing 787-9", "Boeing 717-200"],
        "summary": "Alaska Air Group acquired Hawaiian Airlines for $1.9B, preserving both iconic Pacific brand identities under a unified loyalty program, single operating certificate, and joint network hub in Honolulu (HNL).",
        "source_url": "https://news.alaskaair.com/news-releases/alaska-air-group-completes-acquisition-of-hawaiian-airlines/"
    },
    {
        "merger_id": "PA_DL_1991",
        "predecessor_code": "PA",
        "predecessor_name": "Pan American World Airways (Pan Am)",
        "predecessor_logo": "https://upload.wikimedia.org/wikipedia/commons/2/26/Pan_Am_Logo.svg",
        "successor_code": "DL",
        "successor_name": "Delta Air Lines",
        "successor_logo": "https://upload.wikimedia.org/wikipedia/commons/d/d1/Delta_logo.svg",
        "announced_date": "1991-07-27",
        "closing_date": "1991-09-01",
        "soc_date": "1991-11-01",
        "final_flight_date": "1991-12-04",
        "cutover_year": 1991,
        "hubs_absorbed": ["JFK", "FRA"],
        "fleet_types_inherited": ["Airbus A310-200/300", "Boeing 727-200"],
        "summary": "Delta acquired Pan Am's transatlantic route authorities, European hub operations in Frankfurt (FRA), and the Pan Am Shuttle (LGA/BOS/DCA) out of bankruptcy for $416M, transforming Delta into a major global transatlantic player.",
        "source_url": "https://en.wikipedia.org/wiki/Pan_American_World_Airways"
    }
]


def get_all_airline_mergers() -> List[Dict[str, Any]]:
    """Returns all recorded airline mergers in chronological order."""
    return sorted(AIRLINE_MERGERS, key=lambda m: m["announced_date"])

