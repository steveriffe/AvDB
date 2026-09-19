"""
AvDB Frequent Flyer Program (FFP) Historical Partnerships Reference Database
Comprehensive historical catalog of US airline loyalty programs, status tier hierarchies,
qualification thresholds, elite reciprocity, and bilateral partnership networks from 1980 through 2026.
"""
from typing import Dict, List, Any, Optional

# -----------------------------------------------------------------------------
# 1. Major US Airline Frequent Flyer Programs (1980 - 2026)
# -----------------------------------------------------------------------------
PROGRAMS: Dict[str, Dict[str, Any]] = {
    "AS_MILEAGE_PLAN": {
        "program_id": "AS_MILEAGE_PLAN",
        "program_name": "Mileage Plan",
        "carrier_code": "AS",
        "carrier_name": "Alaska Airlines",
        "founded_year": 1983,
        "dissolved_year": None,
        "is_active": True,
        "successor_program": None,
        "currency_name": "Mileage Plan Miles",
        "currency_type": "Distance-Flown (transitioned to dynamic redemption; joined oneworld 2021)",
        "lineage_summary": (
            "Founded in 1983 as Gold Coast Travel, renamed Mileage Plan in 1987. "
            "Famous for decades as commercial aviation's quintessential 'free agent' program, "
            "maintaining simultaneous reciprocal earn/burn partnerships with American, Continental, "
            "Northwest, Delta, British Airways, Cathay Pacific, and Emirates without joining any global alliance. "
            "Joined oneworld in March 2021 and acquired Hawaiian Airlines' HawaiianMiles in 2024."
        ),
        "status_tiers": [
            {
                "tier_name": "MVP",
                "tier_level": 1,
                "eqm_required": 20000,
                "eqs_required": 30,
                "spend_required": None,
                "upgrade_window": "48 hours prior to departure",
                "bonus_miles_pct": 50,
                "baggage_allowance": "2 complimentary checked bags",
                "lounge_access": "Discounted Alaska Lounge membership; no day passes",
                "priority_services": "Priority check-in, TSA security lane, and preferred Group B boarding",
            },
            {
                "tier_name": "MVP Gold",
                "tier_level": 2,
                "eqm_required": 40000,
                "eqs_required": 60,
                "spend_required": None,
                "upgrade_window": "72 hours prior to departure",
                "bonus_miles_pct": 100,
                "baggage_allowance": "2 complimentary checked bags for member + companion",
                "lounge_access": "Complimentary drink chits; reciprocal oneworld Sapphire lounge access on intl itineraries",
                "priority_services": "First Class check-in, priority security, Group A boarding, fee waivers on changes",
            },
            {
                "tier_name": "MVP Gold 75K",
                "tier_level": 3,
                "eqm_required": 75000,
                "eqs_required": 90,
                "spend_required": None,
                "upgrade_window": "120 hours (5 days) prior to departure",
                "bonus_miles_pct": 125,
                "baggage_allowance": "3 complimentary checked bags for member + companions",
                "lounge_access": "4 complimentary Alaska Lounge day passes annually; oneworld Emerald intl First Class lounges",
                "priority_services": "Highest domestic First upgrade priority, 50,000 bonus miles upon qualification, nominate an MVP companion",
            },
            {
                "tier_name": "MVP Gold 100K",
                "tier_level": 4,
                "eqm_required": 100000,
                "eqs_required": 140,
                "spend_required": None,
                "upgrade_window": "120 hours prior (highest priority over 75K)",
                "bonus_miles_pct": 150,
                "baggage_allowance": "3 complimentary checked bags; international partner priority luggage handling",
                "lounge_access": "Unlimited Alaska Lounge access when traveling on long-haul partner routes + oneworld Emerald",
                "priority_services": "Choice benefit selection (75K miles, Alaska Lounge+ membership discount, or WiFi pass), dedicated elite concierge line",
            },
        ],
    },

    "NW_WORLDPERKS": {
        "program_id": "NW_WORLDPERKS",
        "program_name": "WorldPerks",
        "carrier_code": "NW",
        "carrier_name": "Northwest Airlines",
        "founded_year": 1986,
        "dissolved_year": 2009,
        "is_active": False,
        "successor_program": "Delta SkyMiles",
        "currency_name": "WorldPerks Miles",
        "currency_type": "Distance-Flown (Expiring miles policy softened in 2007)",
        "lineage_summary": (
            "Originating as the Free Flight Plan following the 1986 Republic Airlines merger, "
            "Northwest WorldPerks pioneered global airline alliances through its landmark 1989 KLM joint venture. "
            "Anchor program of the domestic 'Wings Alliance' with Continental from 1998 to 2008, featuring reciprocal "
            "unlimited first-class domestic upgrades. WorldPerks merged into Delta SkyMiles on October 1, 2009."
        ),
        "status_tiers": [
            {
                "tier_name": "Silver Elite",
                "tier_level": 1,
                "eqm_required": 25000,
                "eqs_required": 30,
                "spend_required": "None (Legacy distance era)",
                "upgrade_window": "24 hours prior to departure",
                "bonus_miles_pct": 25,
                "baggage_allowance": "2 complimentary checked bags",
                "lounge_access": "Discounted WorldClub membership",
                "priority_services": "Priority check-in, priority security screening, Zone 2 boarding",
            },
            {
                "tier_name": "Gold Elite",
                "tier_level": 2,
                "eqm_required": 50000,
                "eqs_required": 60,
                "spend_required": "None (Legacy distance era)",
                "upgrade_window": "72 hours prior to departure",
                "bonus_miles_pct": 100,
                "baggage_allowance": "3 complimentary checked bags",
                "lounge_access": "WorldClub / KLM Crown Lounge access on same-day transatlantic itineraries",
                "priority_services": "First Class check-in, priority baggage delivery, SkyTeam Elite Plus reciprocal privileges",
            },
            {
                "tier_name": "Platinum Elite",
                "tier_level": 3,
                "eqm_required": 75000,
                "eqs_required": 90,
                "spend_required": "None (Legacy distance era)",
                "upgrade_window": "120 hours (5 days) prior to departure",
                "bonus_miles_pct": 125,
                "baggage_allowance": "3 complimentary checked bags (70 lbs each)",
                "lounge_access": "Reciprocal Continental Presidents Club & KLM Crown Lounge privileges",
                "priority_services": "Top upgrade priority on NW & Continental, guaranteed Y-class seat reservation 24h prior, dedicated phone line",
            },
        ],
    },

    "CO_ONEPASS": {
        "program_id": "CO_ONEPASS",
        "program_name": "OnePass",
        "carrier_code": "CO",
        "carrier_name": "Continental Airlines",
        "founded_year": 1987,
        "dissolved_year": 2012,
        "is_active": False,
        "successor_program": "United MileagePlus",
        "currency_name": "OnePass Miles",
        "currency_type": "Distance-Flown (Famous for 'Miles that Never Expire' policy instituted in 2004)",
        "lineage_summary": (
            "Created in 1987 by Texas Air Corporation under Frank Lorenzo, OnePass unified the frequent flyer programs "
            "of Continental Airlines and Eastern Air Lines. After Eastern's demise, OnePass gained legendary loyalty under "
            "Gordon Bethune's turnaround, establishing deep bilateral alliances with America West (1994) and Northwest (1998). "
            "Joined SkyTeam in 2004, defected to Star Alliance in 2009, and merged into United MileagePlus in March 2012."
        ),
        "status_tiers": [
            {
                "tier_name": "Silver Elite",
                "tier_level": 1,
                "eqm_required": 25000,
                "eqs_required": 30,
                "spend_required": "None",
                "upgrade_window": "24 hours prior to departure",
                "bonus_miles_pct": 25,
                "baggage_allowance": "2 complimentary checked bags",
                "lounge_access": "Presidents Club discounted rate",
                "priority_services": "EliteAccess check-in, security lane, and priority boarding",
            },
            {
                "tier_name": "Gold Elite",
                "tier_level": 2,
                "eqm_required": 50000,
                "eqs_required": 60,
                "spend_required": "None",
                "upgrade_window": "72 hours prior to departure",
                "bonus_miles_pct": 100,
                "baggage_allowance": "3 complimentary checked bags",
                "lounge_access": "Presidents Club access when departing on same-day international flights",
                "priority_services": "Reciprocal elite upgrades on Northwest & Copa Airlines; priority baggage tags",
            },
            {
                "tier_name": "Platinum Elite",
                "tier_level": 3,
                "eqm_required": 75000,
                "eqs_required": 90,
                "spend_required": "None",
                "upgrade_window": "120 hours (5 days) prior to departure",
                "bonus_miles_pct": 125,
                "baggage_allowance": "3 complimentary checked bags (70 lbs)",
                "lounge_access": "Full reciprocal lounge access across SkyTeam / Star Alliance international networks",
                "priority_services": "Highest complimentary upgrade priority; fee exemptions for ticket redeposits and close-in bookings",
            },
            {
                "tier_name": "PresidentialPlus / Infinite Elite",
                "tier_level": 4,
                "eqm_required": 100000,
                "eqs_required": 120,
                "spend_required": "Co-branded credit card spend tier or invitation",
                "upgrade_window": "120 hours prior (breaker over Platinum)",
                "bonus_miles_pct": 150,
                "baggage_allowance": "3 complimentary checked bags with heavy allowance",
                "lounge_access": "Complimentary full Presidents Club membership included",
                "priority_services": "Top priority waitlist standing, dedicated executive desk, Hertz President's Circle elite status",
            },
        ],
    },

    "HP_FLIGHTFUND": {
        "program_id": "HP_FLIGHTFUND",
        "program_name": "FlightFund",
        "carrier_code": "HP",
        "carrier_name": "America West Airlines",
        "founded_year": 1987,
        "dissolved_year": 2006,
        "is_active": False,
        "successor_program": "US Airways Dividend Miles",
        "currency_name": "FlightFund Miles",
        "currency_type": "Distance-Flown (generous 750-mile minimum segment guarantee)",
        "lineage_summary": (
            "Launched in 1987 to build loyalty around America West's Phoenix (PHX) and Las Vegas (LAS) hubs. "
            "Following Chapter 11 bankruptcy reorganization in 1994, Continental Airlines acquired a 33% stake, "
            "forging a deep 8-year bilateral alliance with shared codeshares, reciprocal OnePass/FlightFund elite perks, "
            "and club reciprocity. When America West acquired US Airways in 2005, FlightFund folded into Dividend Miles."
        ),
        "status_tiers": [
            {
                "tier_name": "Silver Elite",
                "tier_level": 1,
                "eqm_required": 25000,
                "eqs_required": 30,
                "spend_required": "None",
                "upgrade_window": "24 hours prior to departure",
                "bonus_miles_pct": 25,
                "baggage_allowance": "2 complimentary checked bags",
                "lounge_access": "Discounted Phoenix Club America membership",
                "priority_services": "Priority check-in and Zone 1 boarding",
            },
            {
                "tier_name": "Gold Elite",
                "tier_level": 2,
                "eqm_required": 50000,
                "eqs_required": 60,
                "spend_required": "None",
                "upgrade_window": "48 hours prior to departure",
                "bonus_miles_pct": 50,
                "baggage_allowance": "2 complimentary checked bags",
                "lounge_access": "Club America access on international itineraries (Mexico/Canada)",
                "priority_services": "Space-available complimentary first class upgrades, reciprocal perks on Continental",
            },
            {
                "tier_name": "Platinum Elite",
                "tier_level": 3,
                "eqm_required": 75000,
                "eqs_required": 90,
                "spend_required": "None",
                "upgrade_window": "72 hours prior to departure",
                "bonus_miles_pct": 100,
                "baggage_allowance": "3 complimentary checked bags",
                "lounge_access": "Complimentary Club America day passes",
                "priority_services": "Top domestic first upgrade clearance, guaranteed reservations on sold-out flights, fee waivers",
            },
        ],
    },

    "US_DIVIDEND_MILES": {
        "program_id": "US_DIVIDEND_MILES",
        "program_name": "Dividend Miles",
        "carrier_code": "US",
        "carrier_name": "US Airways",
        "founded_year": 1988,
        "dissolved_year": 2015,
        "is_active": False,
        "successor_program": "American Airlines AAdvantage",
        "currency_name": "Dividend Miles",
        "currency_type": "Distance-Flown (Famous for off-peak transatlantic chart bargains and 100% buy-miles promos)",
        "lineage_summary": (
            "Originally USAir Frequent Traveler Program (1983), rebranded as Dividend Miles in 1988. "
            "Held an extensive equity and codeshare partnership with British Airways throughout the 1990s. "
            "Joined Star Alliance in 2004, merged with America West in 2005 (retaining the Dividend Miles brand), "
            "and finally switched to oneworld on March 31, 2014 before merging into American AAdvantage in April 2015."
        ),
        "status_tiers": [
            {
                "tier_name": "Silver Preferred",
                "tier_level": 1,
                "eqm_required": 25000,
                "eqs_required": 30,
                "spend_required": "None",
                "upgrade_window": "48 hours prior to departure",
                "bonus_miles_pct": 25,
                "baggage_allowance": "1 complimentary checked bag",
                "lounge_access": "Discounted US Airways Club membership",
                "priority_services": "Preferred check-in, PreferredAccess security lane, Zone 2 boarding",
            },
            {
                "tier_name": "Gold Preferred",
                "tier_level": 2,
                "eqm_required": 50000,
                "eqs_required": 60,
                "spend_required": "None",
                "upgrade_window": "72 hours prior to departure",
                "bonus_miles_pct": 50,
                "baggage_allowance": "2 complimentary checked bags",
                "lounge_access": "Star Alliance Gold / oneworld Sapphire lounge privileges on international flights",
                "priority_services": "Star Alliance Gold priority baggage, fee exemptions for same-day confirmed travel",
            },
            {
                "tier_name": "Platinum Preferred",
                "tier_level": 3,
                "eqm_required": 75000,
                "eqs_required": 90,
                "spend_required": "None",
                "upgrade_window": "96 hours prior to departure",
                "bonus_miles_pct": 75,
                "baggage_allowance": "3 complimentary checked bags",
                "lounge_access": "Reciprocal partner club access when flying abroad",
                "priority_services": "High-priority domestic First upgrade clearance, complimentary preferred seat selection for party",
            },
            {
                "tier_name": "Chairman's Preferred",
                "tier_level": 4,
                "eqm_required": 100000,
                "eqs_required": 120,
                "spend_required": "None",
                "upgrade_window": "168 hours (7 days) prior to departure",
                "bonus_miles_pct": 100,
                "baggage_allowance": "3 complimentary checked bags (70 lbs each)",
                "lounge_access": "Reciprocal alliance lounge access + 2 complimentary club guest admissions",
                "priority_services": "Systemwide Electronic Upgrade Certificates (transatlantic confirmed), top gate upgrade priority, dedicated Chairman's concierge desk",
            },
        ],
    },

    "TW_AVIATORS": {
        "program_id": "TW_AVIATORS",
        "program_name": "Aviators",
        "carrier_code": "TW",
        "carrier_name": "Trans World Airlines (TWA)",
        "founded_year": 1979,
        "dissolved_year": 2001,
        "is_active": False,
        "successor_program": "American Airlines AAdvantage",
        "currency_name": "Aviators Miles",
        "currency_type": "Distance-Flown (originally Frequent Flight Bonus - FFB)",
        "lineage_summary": (
            "TWA launched its loyalty initiative as the Frequent Flight Bonus (FFB) program in 1979—one of the "
            "earliest programs in commercial aviation history. Rebranded as Aviators in 1997, it was widely praised "
            "for pioneering 'Comfort Class' legroom and generous transatlantic awards. In April 2001, following TWA's "
            "Chapter 11 filing, American Airlines acquired TWA and fully integrated Aviators accounts into AAdvantage."
        ),
        "status_tiers": [
            {
                "tier_name": "Select",
                "tier_level": 1,
                "eqm_required": 20000,
                "eqs_required": 24,
                "spend_required": "None",
                "upgrade_window": "24 hours prior to departure",
                "bonus_miles_pct": 25,
                "baggage_allowance": "2 complimentary checked bags",
                "lounge_access": "Ambassadors Club discount",
                "priority_services": "Priority check-in, priority boarding, space-available Trans World First upgrade standby",
            },
            {
                "tier_name": "Elite",
                "tier_level": 2,
                "eqm_required": 40000,
                "eqs_required": 50,
                "spend_required": "None",
                "upgrade_window": "72 hours prior to departure",
                "bonus_miles_pct": 50,
                "baggage_allowance": "3 complimentary checked bags",
                "lounge_access": "Ambassadors Club access when traveling internationally (e.g. Trans World One to Europe)",
                "priority_services": "Unlimited confirmed domestic First Class upgrades at 72 hours, fee waivers",
            },
            {
                "tier_name": "Elite 1",
                "tier_level": 3,
                "eqm_required": 80000,
                "eqs_required": 100,
                "spend_required": "None",
                "upgrade_window": "120 hours prior to departure",
                "bonus_miles_pct": 100,
                "baggage_allowance": "3 complimentary checked bags with heavy baggage tolerance",
                "lounge_access": "Complimentary Ambassadors Club full membership",
                "priority_services": "Guaranteed seats on sold-out flights, annual transatlantic Trans World One upgrade vouchers, VIP special assistance desk",
            },
        ],
    },

    "DL_SKYMILES": {
        "program_id": "DL_SKYMILES",
        "program_name": "SkyMiles",
        "carrier_code": "DL",
        "carrier_name": "Delta Air Lines",
        "founded_year": 1981,
        "dissolved_year": None,
        "is_active": True,
        "successor_program": None,
        "currency_name": "SkyMiles",
        "currency_type": "Revenue-Spend (transitioned from distance to MQDs / ticket dollars in 2015 and 2024)",
        "lineage_summary": (
            "Founded in 1981 as the Delta Frequent Flyer program, renamed SkyMiles in 1995. "
            "Pioneered non-expiring miles in 2011. Delta absorbed Western Airlines' program in 1987 and Northwest WorldPerks "
            "in 2009 to create the world's largest loyalty program at the time. Lead founding member of SkyTeam in 2000. "
            "Transitioned entirely to pure Medallion Qualification Dollars (MQD) spend tracking in 2024."
        ),
        "status_tiers": [
            {
                "tier_name": "Silver Medallion",
                "tier_level": 1,
                "eqm_required": 25000,
                "eqs_required": 30,
                "spend_required": "$5,000 MQDs (2024 standard)",
                "upgrade_window": "24 hours prior to departure",
                "bonus_miles_pct": 40,
                "baggage_allowance": "1 complimentary checked bag (70 lbs on domestic flights)",
                "lounge_access": "None (Sky Club access restricted to credit card / membership)",
                "priority_services": "Priority check-in, Main Cabin 1 priority boarding, SkyTeam Elite recognition",
            },
            {
                "tier_name": "Gold Medallion",
                "tier_level": 2,
                "eqm_required": 50000,
                "eqs_required": 60,
                "spend_required": "$10,000 MQDs (2024 standard)",
                "upgrade_window": "72 hours prior to departure",
                "bonus_miles_pct": 60,
                "baggage_allowance": "2 complimentary checked bags (70 lbs each)",
                "lounge_access": "SkyTeam Elite Plus international lounge access when flying SkyTeam member carriers abroad",
                "priority_services": "SkyPriority check-in, security, expedited baggage, and complimentary Comfort+ seating at 72 hours",
            },
            {
                "tier_name": "Platinum Medallion",
                "tier_level": 3,
                "eqm_required": 75000,
                "eqs_required": 90,
                "spend_required": "$15,000 MQDs (2024 standard)",
                "upgrade_window": "120 hours prior to departure",
                "bonus_miles_pct": 80,
                "baggage_allowance": "3 complimentary checked bags (70 lbs each)",
                "lounge_access": "Reciprocal SkyTeam Elite Plus lounge access on international routes",
                "priority_services": "Immediate complimentary Comfort+ seat selection upon ticketing, 1 Choice Benefit selection (e.g. Regional Upgrade Certificates), fee exemptions",
            },
            {
                "tier_name": "Diamond Medallion",
                "tier_level": 4,
                "eqm_required": 125000,
                "eqs_required": 140,
                "spend_required": "$28,000 MQDs (2024 standard)",
                "upgrade_window": "120 hours prior (highest First Class clearance tier)",
                "bonus_miles_pct": 120,
                "baggage_allowance": "3 complimentary checked bags (70 lbs each) with SkyPriority yellow tags",
                "lounge_access": "Choice Benefit option for Delta Sky Club Executive Membership or Guest Passes",
                "priority_services": "Global Upgrade Certificates (transoceanic confirmed into Delta One), CLEAR Plus credit, highest boarding priority behind Delta One",
            },
            {
                "tier_name": "Delta 360°",
                "tier_level": 5,
                "eqm_required": None,
                "eqs_required": None,
                "spend_required": "Invitation only (typically $60K+ annual spend on high-yield premium cabins)",
                "upgrade_window": "Top systemwide gate upgrade ranking; proactive flight protection",
                "bonus_miles_pct": 120,
                "baggage_allowance": "3 complimentary checked bags + private apron tarmac transfers in Porsche vehicles",
                "lounge_access": "Executive Sky Club membership + Delta One Lounge access",
                "priority_services": "Direct executive phone concierge, dedicated tarmac monitoring, top IRROPS rerouting protection",
            },
        ],
    },

    "AA_AADVANTAGE": {
        "program_id": "AA_AADVANTAGE",
        "program_name": "AAdvantage",
        "carrier_code": "AA",
        "carrier_name": "American Airlines",
        "founded_year": 1981,
        "dissolved_year": None,
        "is_active": True,
        "successor_program": None,
        "currency_name": "AAdvantage Miles",
        "currency_type": "Loyalty Points (LP) spend/activity model (transitioned in 2022 from EQMs)",
        "lineage_summary": (
            "Launched on May 1, 1981, AAdvantage is recognized as the world's first modern frequent flyer program, "
            "conceived to capitalize on American's SABRE computer reservation system. Absorbed Air California (1987), "
            "Reno Air (1999), TWA Aviators (2001), and US Airways Dividend Miles (2015). Lead founding carrier of oneworld in 1999. "
            "Reinvented elite qualification in 2022 around universal 'Loyalty Points' encompassing card spend and partner shopping."
        ),
        "status_tiers": [
            {
                "tier_name": "AAdvantage Gold",
                "tier_level": 1,
                "eqm_required": 25000,
                "eqs_required": 30,
                "spend_required": "40,000 Loyalty Points (LP)",
                "upgrade_window": "24 hours prior to departure",
                "bonus_miles_pct": 40,
                "baggage_allowance": "1 complimentary checked bag (50 lbs)",
                "lounge_access": "None (Admirals Club requires membership/pass)",
                "priority_services": "Priority check-in, priority security, Group 4 boarding, oneworld Ruby status worldwide",
            },
            {
                "tier_name": "AAdvantage Platinum",
                "tier_level": 2,
                "eqm_required": 50000,
                "eqs_required": 60,
                "spend_required": "75,000 Loyalty Points (LP)",
                "upgrade_window": "48 hours prior to departure",
                "bonus_miles_pct": 60,
                "baggage_allowance": "2 complimentary checked bags (50 lbs each)",
                "lounge_access": "Admirals Club and oneworld Sapphire business lounges when flying on qualifying long-haul international flights",
                "priority_services": "Priority baggage delivery, Group 3 boarding, complimentary Main Cabin Extra seats at booking",
            },
            {
                "tier_name": "AAdvantage Platinum Pro",
                "tier_level": 3,
                "eqm_required": 75000,
                "eqs_required": 90,
                "spend_required": "125,000 Loyalty Points (LP)",
                "upgrade_window": "72 hours prior to departure",
                "bonus_miles_pct": 80,
                "baggage_allowance": "3 complimentary checked bags (70 lbs each)",
                "lounge_access": "oneworld Emerald lounge privileges worldwide (First Class lounges on long-haul routes)",
                "priority_services": "Complimentary upgrades on Alaska Airlines, Group 2 boarding, fee waivers on same-day confirmed flight changes",
            },
            {
                "tier_name": "Executive Platinum",
                "tier_level": 4,
                "eqm_required": 100000,
                "eqs_required": 120,
                "spend_required": "200,000 Loyalty Points (LP)",
                "upgrade_window": "120 hours (5 days) prior to departure",
                "bonus_miles_pct": 120,
                "baggage_allowance": "3 complimentary checked bags (70 lbs each)",
                "lounge_access": "International Flagship Lounge & oneworld Emerald First Class lounges (e.g. BA Concorde/First, Cathay Pier First)",
                "priority_services": "Systemwide Upgrades (SWUs) redeemable from Economy to Business/First transpacific/transatlantic, Group 1 boarding, dedicated EXP desk",
            },
            {
                "tier_name": "ConciergeKey",
                "tier_level": 5,
                "eqm_required": None,
                "eqs_required": None,
                "spend_required": "Invitation-only (estimated $50K–$100K+ annual spend on full-fare premium routes)",
                "upgrade_window": "Highest gate clearance priority; proactive clearing before 120h window",
                "bonus_miles_pct": 120,
                "baggage_allowance": "3 complimentary checked bags with tarmac baggage expediting",
                "lounge_access": "Full Admirals Club & Flagship Lounge access regardless of itinerary; Flagship First Dining access",
                "priority_services": "Private tarmac transfers in Cadillac luxury vehicles, pre-boarding before Group 1, dedicated 24/7 ConciergeKey phone desk",
            },
        ],
    },

    "UA_MILEAGEPLUS": {
        "program_id": "UA_MILEAGEPLUS",
        "program_name": "MileagePlus",
        "carrier_code": "UA",
        "carrier_name": "United Airlines",
        "founded_year": 1981,
        "dissolved_year": None,
        "is_active": True,
        "successor_program": None,
        "currency_name": "MileagePlus Miles",
        "currency_type": "Premier Qualifying Points (PQP) and Premier Qualifying Flights (PQF)",
        "lineage_summary": (
            "Launched on May 6, 1981, one week after American's AAdvantage. "
            "Pioneered global interline loyalty redemption and transatlantic alliances with Lufthansa. "
            "Lead founding member of Star Alliance in 1997. Following United's 2010 merger with Continental Airlines, "
            "the programs combined under the MileagePlus name while retaining Continental's OnePass technology platform. "
            "Shifted to PQP spend-based elite requirements in 2020."
        ),
        "status_tiers": [
            {
                "tier_name": "Premier Silver",
                "tier_level": 1,
                "eqm_required": 25000,
                "eqs_required": 30,
                "spend_required": "4,000 PQP + 12 PQF (or 5,000 PQP)",
                "upgrade_window": "24 hours prior to departure",
                "bonus_miles_pct": 40,
                "baggage_allowance": "1 complimentary checked bag (70 lbs)",
                "lounge_access": "None (United Club requires membership/trip pass)",
                "priority_services": "Premier Access check-in and priority security, Group 2 boarding, complimentary Economy Plus at check-in",
            },
            {
                "tier_name": "Premier Gold",
                "tier_level": 2,
                "eqm_required": 50000,
                "eqs_required": 60,
                "spend_required": "8,000 PQP + 24 PQF (or 10,000 PQP)",
                "upgrade_window": "48 hours prior to departure",
                "bonus_miles_pct": 60,
                "baggage_allowance": "2 complimentary checked bags (70 lbs each)",
                "lounge_access": "Star Alliance Gold lounge privileges worldwide on international itineraries (Lufthansa Senator Lounges, etc.)",
                "priority_services": "Complimentary Economy Plus seat selection at booking for member + 1 companion, Group 1 boarding, Star Gold baggage handling",
            },
            {
                "tier_name": "Premier Platinum",
                "tier_level": 3,
                "eqm_required": 75000,
                "eqs_required": 90,
                "spend_required": "12,000 PQP + 36 PQF (or 15,000 PQP)",
                "upgrade_window": "72 hours prior to departure",
                "bonus_miles_pct": 80,
                "baggage_allowance": "3 complimentary checked bags (70 lbs each)",
                "lounge_access": "Star Alliance Gold reciprocal lounge privileges",
                "priority_services": "40 PlusPoints awarded annually (redeemable for domestic First / transcon premium upgrades), Economy Plus for up to 8 companions",
            },
            {
                "tier_name": "Premier 1K",
                "tier_level": 4,
                "eqm_required": 100000,
                "eqs_required": 120,
                "spend_required": "18,000 PQP + 54 PQF (or 24,000 PQP)",
                "upgrade_window": "96 hours (4 days) prior to departure",
                "bonus_miles_pct": 100,
                "baggage_allowance": "3 complimentary checked bags (70 lbs each)",
                "lounge_access": "Star Alliance Gold privileges + 1K drink vouchers on domestic flights",
                "priority_services": "280 PlusPoints (redeemable for intercontinental United Polaris upgrades), pre-boarding before Group 1, free snack/beverage in Economy",
            },
            {
                "tier_name": "Global Services",
                "tier_level": 5,
                "eqm_required": None,
                "eqs_required": None,
                "spend_required": "Invitation-only (estimated $50,000+ spend on high-yield premium fares)",
                "upgrade_window": "Proactive clearing 120h+ prior to departure; highest upgrade priority in Polaris/First",
                "bonus_miles_pct": 100,
                "baggage_allowance": "3 complimentary checked bags with Mercedes-Benz tarmac transfer assistance",
                "lounge_access": "United Club access regardless of ticket class; United Polaris Lounge on international itineraries",
                "priority_services": "Private check-in lobbies at SFO, ORD, EWR, IAH; dedicated 24/7 Global Services phone line; priority boarding ahead of all passengers",
            },
        ],
    },

    "EA_ONEPASS": {
        "program_id": "EA_ONEPASS",
        "program_name": "Ionosphere Club / OnePass",
        "carrier_code": "EA",
        "carrier_name": "Eastern Air Lines",
        "founded_year": 1981,
        "dissolved_year": 1991,
        "is_active": False,
        "successor_program": "Continental OnePass",
        "currency_name": "OnePass Miles",
        "currency_type": "Distance-Flown (originally Eastern Frequent Traveler Bonus program)",
        "lineage_summary": (
            "Eastern established the Ionosphere Club in the early 1960s as one of the first VIP airport lounge clubs, "
            "and rolled out its Frequent Traveler Bonus program in 1981 to counter AAdvantage. In 1987, following "
            "Eastern's acquisition by Texas Air Corporation, Frank Lorenzo consolidated Eastern's and Continental's "
            "loyalty schemes into 'OnePass'—the world's first multi-airline combined loyalty program. "
            "When Eastern collapsed in January 1991 amid labor strife, Continental preserved all OnePass accounts."
        ),
        "status_tiers": [
            {
                "tier_name": "Bronze OnePass",
                "tier_level": 1,
                "eqm_required": 25000,
                "eqs_required": 30,
                "spend_required": "None",
                "upgrade_window": "Gate standby / 24 hours prior",
                "bonus_miles_pct": 25,
                "baggage_allowance": "2 complimentary checked bags",
                "lounge_access": "Ionosphere Club membership discount",
                "priority_services": "Priority check-in counters and baggage handling",
            },
            {
                "tier_name": "Silver OnePass",
                "tier_level": 2,
                "eqm_required": 50000,
                "eqs_required": 60,
                "spend_required": "None",
                "upgrade_window": "48 hours prior to departure",
                "bonus_miles_pct": 50,
                "baggage_allowance": "3 complimentary checked bags",
                "lounge_access": "Ionosphere Club and Continental Presidents Club reciprocal access",
                "priority_services": "Space-available complimentary first-class upgrades across both Eastern and Continental networks",
            },
            {
                "tier_name": "Gold OnePass",
                "tier_level": 3,
                "eqm_required": 75000,
                "eqs_required": 90,
                "spend_required": "None",
                "upgrade_window": "72 hours prior to departure",
                "bonus_miles_pct": 100,
                "baggage_allowance": "3 complimentary checked bags (heavy baggage allowance)",
                "lounge_access": "Complimentary Ionosphere Club full access",
                "priority_services": "Highest upgrade priority on Eastern Whisperjet A300 and Boeing 757 flights; guaranteed seat on Eastern Shuttle (LGA-BOS-DCA)",
            },
        ],
    },

    "PA_WORLDPASS": {
        "program_id": "PA_WORLDPASS",
        "program_name": "WorldPass",
        "carrier_code": "PA",
        "carrier_name": "Pan American World Airways (Pan Am)",
        "founded_year": 1982,
        "dissolved_year": 1991,
        "is_active": False,
        "successor_program": "Delta SkyMiles",
        "currency_name": "WorldPass Miles",
        "currency_type": "Distance-Flown (famous for 30-day unlimited First Class 'Around the World' awards at 175K miles)",
        "lineage_summary": (
            "Introduced in February 1982, WorldPass was the premier global loyalty program of the jet age, "
            "leveraging Pan Am's iconic intercontinental routes across Europe, Asia, Latin America, and the Middle East. "
            "WorldPass featured legendary redemption awards, including Concorde connections, 30-day global passes, "
            "and penthouse suite stays with InterContinental Hotels. As Pan Am liquidated its route assets, United acquired "
            "its Pacific routes in 1985, American acquired its London Heathrow authority, and Delta purchased its European network "
            "and shuttle in 1991, honoring WorldPass miles in Delta Frequent Flyer."
        ),
        "status_tiers": [
            {
                "tier_name": "WorldPass Preferred",
                "tier_level": 1,
                "eqm_required": 30000,
                "eqs_required": 20,
                "spend_required": "None",
                "upgrade_window": "48 hours prior to departure",
                "bonus_miles_pct": 25,
                "baggage_allowance": "2 complimentary checked bags",
                "lounge_access": "Clipper Club discount",
                "priority_services": "Priority Clipper Class check-in, priority boarding, standby first-class upgrade vouchers",
            },
            {
                "tier_name": "WorldPass Platinum / Clipper Executive",
                "tier_level": 2,
                "eqm_required": 75000,
                "eqs_required": 50,
                "spend_required": "None",
                "upgrade_window": "72 hours prior to departure",
                "bonus_miles_pct": 50,
                "baggage_allowance": "3 complimentary checked bags (70 lbs each)",
                "lounge_access": "Complimentary Clipper Club lounge access worldwide (JFK Worldport, LHR, FRA, NRT)",
                "priority_services": "Confirmed First Class sleeper seat upgrades on Boeing 747 intercontinental routes; personal Clipper concierge at gateway airports",
            },
        ],
    },
}

# Quick carrier-to-program lookup
CARRIER_TO_PROGRAM: Dict[str, str] = {
    prog["carrier_code"]: prog["program_id"]
    for prog in PROGRAMS.values()
}


# -----------------------------------------------------------------------------
# 2. Curated Bilateral Partnerships Web (1980 - 2026)
# -----------------------------------------------------------------------------
BILATERAL_PARTNERSHIPS: List[Dict[str, Any]] = [
    # -------------------------------------------------------------------------
    # The Alaska Airlines "Independent Maverick" Web (1995 - 2020)
    # -------------------------------------------------------------------------
    {
        "partnership_id": "AS_CO_1995_2011",
        "carrier_1": "AS",
        "carrier_2": "CO",
        "carrier_1_name": "Alaska Airlines",
        "carrier_2_name": "Continental Airlines",
        "program_1": "Mileage Plan",
        "program_2": "OnePass",
        "partnership_type": "Codeshare & Reciprocal Earn/Burn",
        "start_year": 1995,
        "end_year": 2011,
        "is_active": False,
        "elite_reciprocity": True,
        "lounge_reciprocity": True,
        "reciprocity_details": "Reciprocal elite qualifying miles, complimentary space-available domestic First Class upgrades, and Board Room / Presidents Club access.",
        "historical_context": (
            "Alaska and Continental established an extraordinarily close bilateral alliance in the 1990s. "
            "Mileage Plan members could earn and redeem miles seamlessly across Continental's Houston (IAH), "
            "Newark (EWR), and Cleveland (CLE) hubs, while Continental flyers gained deep access across the Pacific Northwest and Alaska. "
            "Terminated following Continental's merger into United Airlines."
        ),
        "significance": "Pioneering domestic multi-hub bilateral integration between non-competing networks.",
        "tags": ["Alaska Free Agent", "Reciprocal Upgrades", "West Coast Feed"]
    },
    {
        "partnership_id": "AS_NW_1996_2009",
        "carrier_1": "AS",
        "carrier_2": "NW",
        "carrier_1_name": "Alaska Airlines",
        "carrier_2_name": "Northwest Airlines",
        "program_1": "Mileage Plan",
        "program_2": "WorldPerks",
        "partnership_type": "Codeshare & Reciprocal Earn/Burn",
        "start_year": 1996,
        "end_year": 2009,
        "is_active": False,
        "elite_reciprocity": True,
        "lounge_reciprocity": True,
        "reciprocity_details": "Reciprocal EQM earning, elite upgrades on domestic segments, and Alaska Board Room / Northwest WorldClub access.",
        "historical_context": (
            "Northwest utilized Alaska to feed its Minneapolis (MSP), Detroit (DTW), and Seattle-Tokyo transpacific flights. "
            "Alaska members could redeem WorldPerks awards across Northwest's expansive Asian route network. "
            "Folded into the Delta-Alaska alliance when Delta acquired Northwest in 2008–2009."
        ),
        "significance": "Anchored Alaska's Asian gateway connections via Seattle and Tokyo Narita.",
        "tags": ["Alaska Free Agent", "Pacific Gateway", "Wings Alliance Tie"]
    },
    {
        "partnership_id": "AS_DL_2004_2017",
        "carrier_1": "AS",
        "carrier_2": "DL",
        "carrier_1_name": "Alaska Airlines",
        "carrier_2_name": "Delta Air Lines",
        "program_1": "Mileage Plan",
        "program_2": "SkyMiles",
        "partnership_type": "Codeshare & Reciprocal Earn/Burn",
        "start_year": 2004,
        "end_year": 2017,
        "is_active": False,
        "elite_reciprocity": True,
        "lounge_reciprocity": True,
        "reciprocity_details": "Reciprocal elite upgrades, priority check-in, and Sky Club / Board Room access for elite flyers.",
        "historical_context": (
            "Initially a cozy codeshare where Alaska fed Delta's transpacific expansion from Seattle-Tacoma (SEA). "
            "However, around 2013 Delta decided to build Seattle into a massive global hub of its own, directly duplicating "
            "Alaska's most profitable West Coast routes. Tensions escalated into a full-scale corporate dogfight, resulting in "
            "Delta cutting all reciprocal elite benefits and terminating the partnership on April 30, 2017."
        ),
        "significance": "A friendly feeder partnership that devolved into one of commercial aviation's fiercest hub rivalries.",
        "tags": ["Seattle Hub War", "Alaska Free Agent", "Bitter Divorce"]
    },
    {
        "partnership_id": "AS_AA_1999_ACTIVE",
        "carrier_1": "AS",
        "carrier_2": "AA",
        "carrier_1_name": "Alaska Airlines",
        "carrier_2_name": "American Airlines",
        "program_1": "Mileage Plan",
        "program_2": "AAdvantage",
        "partnership_type": "Full Alliance / Joint Venture",
        "start_year": 1999,
        "end_year": None,
        "is_active": True,
        "elite_reciprocity": True,
        "lounge_reciprocity": True,
        "reciprocity_details": "Full elite reciprocity: complimentary First Class upgrades, priority baggage, oneworld Emerald/Sapphire status recognition, and Admirals Club access.",
        "historical_context": (
            "Started in 1999 as a domestic bilateral codeshare that weathered multiple industry shakeups. "
            "When Delta launched its aggressive Seattle invasion, Alaska and American strengthened their West Coast Alliance in 2020. "
            "This culminated in Alaska Airlines formally joining the oneworld global alliance on March 31, 2021, cementing "
            "complete reciprocal loyalty integration."
        ),
        "significance": "A durable 25+ year alliance that bridged Alaska's independence into formal oneworld membership.",
        "tags": ["oneworld", "West Coast Alliance", "Surviving Partnership"]
    },
    {
        "partnership_id": "AS_BA_2001_ACTIVE",
        "carrier_1": "AS",
        "carrier_2": "BA",
        "carrier_1_name": "Alaska Airlines",
        "carrier_2_name": "British Airways",
        "program_1": "Mileage Plan",
        "program_2": "Executive Club",
        "partnership_type": "Full Alliance / Joint Venture",
        "start_year": 2001,
        "end_year": None,
        "is_active": True,
        "elite_reciprocity": True,
        "lounge_reciprocity": True,
        "reciprocity_details": "Mileage Plan members can redeem on BA Club World and First cabins; oneworld Emerald/Sapphire reciprocal lounge access.",
        "historical_context": (
            "Alaska's longest-standing transatlantic partnership, allowing West Coast members to reach London Heathrow and Europe. "
            "Persisted continuously throughout Alaska's independent years and deepened further with oneworld entry."
        ),
        "significance": "The primary European gateway partnership for Alaska Mileage Plan members for over two decades.",
        "tags": ["Transatlantic", "oneworld", "Legacy Bilateral"]
    },
    {
        "partnership_id": "AS_EK_2012_2021",
        "carrier_1": "AS",
        "carrier_2": "EK",
        "carrier_1_name": "Alaska Airlines",
        "carrier_2_name": "Emirates",
        "program_1": "Mileage Plan",
        "program_2": "Skywards",
        "partnership_type": "Codeshare & Reciprocal Earn/Burn",
        "start_year": 2012,
        "end_year": 2021,
        "is_active": False,
        "elite_reciprocity": False,
        "lounge_reciprocity": False,
        "reciprocity_details": "Reciprocal earn and burn without elite upgrade reciprocity; famous for low-cost First Class shower-suite redemptions.",
        "historical_context": (
            "One of the most famous 'sweet spots' in frequent flyer history: Alaska Mileage Plan allowed flyers to redeem "
            "Emirates A380 First Class suites with onboard showers for just 100,000 miles. Terminated in 2021 when Alaska joined oneworld "
            "(aligning with Qatar Airways)."
        ),
        "significance": "Legendary sweet spot that drove thousands of loyalty enthusiasts to accumulate Alaska miles.",
        "tags": ["Aviation Sweet Spot", "Emirates First Class", "Middle East Feed"]
    },

    # -------------------------------------------------------------------------
    # The America West & Continental Phoenix Axis (1994 - 2002)
    # -------------------------------------------------------------------------
    {
        "partnership_id": "HP_CO_1994_2002",
        "carrier_1": "HP",
        "carrier_2": "CO",
        "carrier_1_name": "America West Airlines",
        "carrier_2_name": "Continental Airlines",
        "program_1": "FlightFund",
        "program_2": "OnePass",
        "partnership_type": "Codeshare & Reciprocal Earn/Burn",
        "start_year": 1994,
        "end_year": 2002,
        "is_active": False,
        "elite_reciprocity": True,
        "lounge_reciprocity": True,
        "reciprocity_details": "Reciprocal elite tier matching, mutual domestic First Class upgrades, and shared Club America / Presidents Club access.",
        "historical_context": (
            "In 1994, Continental Airlines invested $54 million for a 33% stake in America West to help it emerge from bankruptcy. "
            "The carriers interlocked their networks: America West dominated Phoenix (PHX) and Las Vegas (LAS), while Continental "
            "dominated Houston (IAH) and Newark (EWR). Members had full reciprocal OnePass/FlightFund elite perks. The alliance expired "
            "in 2002 after Continental sold its stake."
        ),
        "significance": "The quintessential post-deregulation bankruptcy equity rescue and reciprocal loyalty integration.",
        "tags": ["Equity Alliance", "Phoenix Axis", "Turnaround Era"]
    },

    # -------------------------------------------------------------------------
    # The Wings Alliance / Northwest-Continental Alliance (1998 - 2008)
    # -------------------------------------------------------------------------
    {
        "partnership_id": "CO_NW_1998_2008",
        "carrier_1": "CO",
        "carrier_2": "NW",
        "carrier_1_name": "Continental Airlines",
        "carrier_2_name": "Northwest Airlines",
        "program_1": "OnePass",
        "program_2": "WorldPerks",
        "partnership_type": "Full Alliance / Joint Venture",
        "start_year": 1998,
        "end_year": 2008,
        "is_active": False,
        "elite_reciprocity": True,
        "lounge_reciprocity": True,
        "reciprocity_details": "Seamless elite reciprocity: automatic reciprocal domestic First Class upgrades, reciprocal Presidents Club / WorldClub access, and combined international redemption.",
        "historical_context": (
            "In January 1998, Continental and Northwest announced a 14-year strategic alliance. Northwest acquired a controlling "
            "voting interest in Continental (later repurchased). Together with KLM, they created the domestic and transatlantic powerhouse "
            "known as the Wings Alliance. Flyers experienced indistinguishable elite treatment between OnePass and WorldPerks. "
            "Both carriers joined SkyTeam in 2004, dissolving only when Northwest merged with Delta in 2008 and Continental defected to Star Alliance."
        ),
        "significance": "The most deeply integrated domestic bilateral alliance in US aviation history prior to formal anti-trust immunity JVs.",
        "tags": ["Wings Alliance", "Reciprocal Upgrades", "KLM Joint Venture"]
    },
    {
        "partnership_id": "NW_KL_1989_2008",
        "carrier_1": "NW",
        "carrier_2": "KL",
        "carrier_1_name": "Northwest Airlines",
        "carrier_2_name": "KLM Royal Dutch Airlines",
        "program_1": "WorldPerks",
        "program_2": "Flying Dutchman / Flying Blue",
        "partnership_type": "Full Alliance / Joint Venture",
        "start_year": 1989,
        "end_year": 2008,
        "is_active": False,
        "elite_reciprocity": True,
        "lounge_reciprocity": True,
        "reciprocity_details": "Full antitrust immunity, metal-neutral revenue sharing, reciprocal WorldClub / Crown Lounge access, and shared elite qualification.",
        "historical_context": (
            "The historic foundation of modern transatlantic joint ventures. In 1989, KLM invested $400 million for a 20% stake in Northwest. "
            "In 1993, the US Department of Transportation granted them the world's first antitrust immunity (ATI). "
            "WorldPerks and KLM's Flying Dutchman operated virtually as a single global program across North America and Europe."
        ),
        "significance": "First immunized transatlantic alliance; created the operational blueprint for Star Alliance, SkyTeam, and oneworld.",
        "tags": ["Antitrust Immunity", "Pioneer Joint Venture", "Amsterdam Hub"]
    },

    # -------------------------------------------------------------------------
    # Eastern Airlines & Continental: Texas Air OnePass (1987 - 1991)
    # -------------------------------------------------------------------------
    {
        "partnership_id": "EA_CO_1987_1991",
        "carrier_1": "EA",
        "carrier_2": "CO",
        "carrier_1_name": "Eastern Air Lines",
        "carrier_2_name": "Continental Airlines",
        "program_1": "OnePass",
        "program_2": "OnePass",
        "partnership_type": "Full Alliance / Joint Venture",
        "start_year": 1987,
        "end_year": 1991,
        "is_active": False,
        "elite_reciprocity": True,
        "lounge_reciprocity": True,
        "reciprocity_details": "Single unified currency (OnePass), shared status tiers (Bronze/Silver/Gold), and reciprocal Ionosphere Club / Presidents Club access.",
        "historical_context": (
            "Following Frank Lorenzo's Texas Air acquisition of Eastern in 1986, the loyalty departments were merged in 1987 into 'OnePass'. "
            "It was the first time two major US legacy airlines shared a single frequent flyer program. Flyers could earn miles on Eastern's "
            "Miami (MIA), Atlanta (ATL), and East Coast Shuttles and redeem on Continental's Denver (DEN) and Houston (IAH) routes. "
            "When Eastern collapsed in January 1991, Continental retained the entire OnePass database."
        ),
        "significance": "The world's first shared frequent flyer program across two separate major airlines.",
        "tags": ["Texas Air", "First Unified Program", "Eastern Demise"]
    },

    # -------------------------------------------------------------------------
    # Pan Am Liquidations & Bilateral Route Transfers (1982 - 1991)
    # -------------------------------------------------------------------------
    {
        "partnership_id": "PA_UA_1985_1991",
        "carrier_1": "PA",
        "carrier_2": "UA",
        "carrier_1_name": "Pan Am",
        "carrier_2_name": "United Airlines",
        "program_1": "WorldPass",
        "program_2": "MileagePlus",
        "partnership_type": "Bilateral Reciprocal Earn/Burn",
        "start_year": 1985,
        "end_year": 1991,
        "is_active": False,
        "elite_reciprocity": False,
        "lounge_reciprocity": False,
        "reciprocity_details": "Reciprocal ticketing and mileage redemption on transpacific routes following United's acquisition of Pan Am's Pacific Division.",
        "historical_context": (
            "In 1985, financially strained Pan Am sold its entire Pacific division and Tokyo hub to United for $750 million. "
            "The carriers established reciprocal WorldPass and MileagePlus redemption so travelers could connect between Pan Am's "
            "domestic/Atlantic network and United's new transpacific flights."
        ),
        "significance": "Facilitated United's instant transformation into the dominant US carrier across the Pacific.",
        "tags": ["Pacific Division Sale", "Pan Am Route Transfer", "Tokyo Hub"]
    },
    {
        "partnership_id": "PA_DL_1991_1991",
        "carrier_1": "PA",
        "carrier_2": "DL",
        "carrier_1_name": "Pan Am",
        "carrier_2_name": "Delta Air Lines",
        "program_1": "WorldPass",
        "program_2": "Frequent Flyer (SkyMiles)",
        "partnership_type": "Full Alliance / Joint Venture",
        "start_year": 1991,
        "end_year": 1991,
        "is_active": False,
        "elite_reciprocity": True,
        "lounge_reciprocity": True,
        "reciprocity_details": "Full honor of Pan Am WorldPass miles in Delta's program, 1-to-1 conversion of accrued balances, and Clipper Club conversion to Crown Room.",
        "historical_context": (
            "In August 1991, Delta acquired Pan Am's transatlantic routes, JFK Worldport hub, and Pan Am Shuttle for $416 million. "
            "Delta guaranteed all WorldPass miles, honoring them for awards on Delta's worldwide network. When Pan Am shut down permanently "
            "on December 4, 1991, Delta absorbed the remaining loyalists, propelling Delta into a premier transatlantic powerhouse."
        ),
        "significance": "Catapulted Delta from a regional Southern carrier into a major transatlantic airline overnight.",
        "tags": ["Pan Am Liquidation", "Transatlantic Expansion", "JFK Worldport"]
    },

    # -------------------------------------------------------------------------
    # US Airways Alliance Hopscotch (1993 - 2015)
    # -------------------------------------------------------------------------
    {
        "partnership_id": "US_BA_1993_1999",
        "carrier_1": "US",
        "carrier_2": "BA",
        "carrier_1_name": "US Airways (USAir)",
        "carrier_2_name": "British Airways",
        "program_1": "Dividend Miles",
        "program_2": "Executive Club",
        "partnership_type": "Codeshare & Reciprocal Earn/Burn",
        "start_year": 1993,
        "end_year": 1999,
        "is_active": False,
        "elite_reciprocity": True,
        "lounge_reciprocity": True,
        "reciprocity_details": "Reciprocal elite status recognition, lounge access, and extensive transatlantic codesharing through London Gatwick and Heathrow.",
        "historical_context": (
            "In 1993, British Airways purchased a $300 million (24.6%) stake in USAir. Dividend Miles members enjoyed "
            "unrivaled transatlantic access via London, while BA passengers fed into USAir's dense East Coast network (CLT, PIT, PHL). "
            "The partnership unraveled in 1998 when British Airways formed oneworld with American Airlines, forcing BA to divest its USAir stake."
        ),
        "significance": "A landmark transatlantic investment that pre-dated global airline alliances.",
        "tags": ["Alliance Hopscotch", "British Airways Stake", "East Coast Feed"]
    },
    {
        "partnership_id": "US_STAR_2004_2014",
        "carrier_1": "US",
        "carrier_2": "UA",
        "carrier_1_name": "US Airways",
        "carrier_2_name": "United Airlines",
        "program_1": "Dividend Miles",
        "program_2": "MileagePlus",
        "partnership_type": "Full Alliance / Joint Venture",
        "start_year": 2004,
        "end_year": 2014,
        "is_active": False,
        "elite_reciprocity": True,
        "lounge_reciprocity": True,
        "reciprocity_details": "Star Alliance Gold / Silver reciprocity, reciprocal lounge access worldwide, and joint marketing.",
        "historical_context": (
            "US Airways joined Star Alliance on May 4, 2004, aligning closely with United Airlines. Following US Airways' 2005 "
            "merger with America West, the combined carrier remained a loyal Star Alliance member for a decade, providing Star Alliance "
            "with massive domestic capacity in Charlotte, Philadelphia, and Phoenix."
        ),
        "significance": "Anchored Star Alliance's US East Coast dominance for ten years.",
        "tags": ["Star Alliance", "Alliance Hopscotch", "United Integration"]
    },
    {
        "partnership_id": "US_ONEWORLD_2014_2015",
        "carrier_1": "US",
        "carrier_2": "AA",
        "carrier_1_name": "US Airways",
        "carrier_2_name": "American Airlines",
        "program_1": "Dividend Miles",
        "program_2": "AAdvantage",
        "partnership_type": "Full Alliance / Joint Venture",
        "start_year": 2014,
        "end_year": 2015,
        "is_active": False,
        "elite_reciprocity": True,
        "lounge_reciprocity": True,
        "reciprocity_details": "100% reciprocal elite upgrades, reciprocal Admirals Club / US Airways Club access, and seamless oneworld status integration.",
        "historical_context": (
            "Upon merging with American Airlines, US Airways formally exited Star Alliance on March 30, 2014 and joined oneworld the very next day. "
            "Dividend Miles and AAdvantage operated reciprocally for one year before Dividend Miles was completely absorbed into AAdvantage in April 2015."
        ),
        "significance": "The fastest major alliance transition in aviation history (Star Alliance to oneworld in 24 hours).",
        "tags": ["oneworld Entry", "Alliance Hopscotch", "Mega Merger"]
    },

    # -------------------------------------------------------------------------
    # TWA Partnerships & Acquisition by American (1990 - 2001)
    # -------------------------------------------------------------------------
    {
        "partnership_id": "TW_HP_1997_2001",
        "carrier_1": "TW",
        "carrier_2": "HP",
        "carrier_1_name": "TWA",
        "carrier_2_name": "America West Airlines",
        "program_1": "Aviators",
        "program_2": "FlightFund",
        "partnership_type": "Codeshare & Reciprocal Earn/Burn",
        "start_year": 1997,
        "end_year": 2001,
        "is_active": False,
        "elite_reciprocity": True,
        "lounge_reciprocity": True,
        "reciprocity_details": "Reciprocal mileage earning and burning, lounge privileges, and codesharing between TWA's St. Louis hub and HP's Western network.",
        "historical_context": (
            "Seeking to bolster domestic connectivity against United, American, and Delta, TWA and America West established "
            "a reciprocal marketing alliance connecting TWA's St. Louis (STL) mega-hub to Phoenix, Las Vegas, and California routes."
        ),
        "significance": "Defensive mid-tier carrier alliance prior to industry consolidation.",
        "tags": ["Mid-Tier Alliance", "St. Louis Hub", "TWA Transcon"]
    },
    {
        "partnership_id": "TW_AA_2001_2001",
        "carrier_1": "TW",
        "carrier_2": "AA",
        "carrier_1_name": "TWA",
        "carrier_2_name": "American Airlines",
        "program_1": "Aviators",
        "program_2": "AAdvantage",
        "partnership_type": "Full Alliance / Joint Venture",
        "start_year": 2001,
        "end_year": 2001,
        "is_active": False,
        "elite_reciprocity": True,
        "lounge_reciprocity": True,
        "reciprocity_details": "1-to-1 conversion of Aviators miles into AAdvantage miles; elite status tiers mapped to AAdvantage Gold, Platinum, and Executive Platinum.",
        "historical_context": (
            "American Airlines acquired TWA's assets in April 2001 out of bankruptcy. Aviators accounts were transitioned into AAdvantage, "
            "and TWA's Ambassadors Clubs were converted into Admirals Clubs. The acquisition briefly made American the world's largest airline."
        ),
        "significance": "Brought one of aviation's founding pioneers into the American Airlines AAdvantage family.",
        "tags": ["TWA Absorption", "AAdvantage Expansion", "Bankruptcy Purchase"]
    },

    # -------------------------------------------------------------------------
    # Foundation of Global Alliances (UA-LH Star, AA-BA oneworld, DL-AF SkyTeam)
    # -------------------------------------------------------------------------
    {
        "partnership_id": "UA_LH_1993_ACTIVE",
        "carrier_1": "UA",
        "carrier_2": "LH",
        "carrier_1_name": "United Airlines",
        "carrier_2_name": "Lufthansa",
        "program_1": "MileagePlus",
        "program_2": "Miles & More",
        "partnership_type": "Full Alliance / Joint Venture",
        "start_year": 1993,
        "end_year": None,
        "is_active": True,
        "elite_reciprocity": True,
        "lounge_reciprocity": True,
        "reciprocity_details": "Antitrust immunized joint venture (A++), transatlantic revenue sharing, reciprocal Senator / United Club lounge access, and Premier upgrade instruments.",
        "historical_context": (
            "Forged in 1993, United and Lufthansa's bilateral ties directly inspired the creation of Star Alliance in 1997. "
            "It remains one of commercial aviation's most lucrative and enduring immunized transatlantic partnerships."
        ),
        "significance": "Founding pillar of the modern multilateral alliance era.",
        "tags": ["Star Alliance Founder", "Antitrust Immunity", "Transatlantic JV"]
    },
    {
        "partnership_id": "AA_BA_1999_ACTIVE",
        "carrier_1": "AA",
        "carrier_2": "BA",
        "carrier_1_name": "American Airlines",
        "carrier_2_name": "British Airways",
        "program_1": "AAdvantage",
        "program_2": "Executive Club",
        "partnership_type": "Full Alliance / Joint Venture",
        "start_year": 1999,
        "end_year": None,
        "is_active": True,
        "elite_reciprocity": True,
        "lounge_reciprocity": True,
        "reciprocity_details": "Full oneworld Emerald/Sapphire reciprocity, transatlantic revenue-sharing joint venture, Concorde Room / Flagship First lounge access.",
        "historical_context": (
            "Founding cornerstone of oneworld. After years of regulatory review, American and British Airways secured DOT antitrust immunity "
            "in 2010 for their transatlantic Joint Business Agreement (JBA), aligning JFK-LHR shuttles and joint frequent flyer benefits."
        ),
        "significance": "Dominant transatlantic partnership across London Heathrow and New York JFK.",
        "tags": ["oneworld Founder", "Joint Business Agreement", "JFK-LHR Corridor"]
    },
    {
        "partnership_id": "DL_AF_2000_ACTIVE",
        "carrier_1": "DL",
        "carrier_2": "AF",
        "carrier_1_name": "Delta Air Lines",
        "carrier_2_name": "Air France",
        "program_1": "SkyMiles",
        "program_2": "Flying Blue",
        "partnership_type": "Full Alliance / Joint Venture",
        "start_year": 2000,
        "end_year": None,
        "is_active": True,
        "elite_reciprocity": True,
        "lounge_reciprocity": True,
        "reciprocity_details": "Immunized transatlantic joint venture, reciprocal SkyTeam Elite Plus benefits, Sky Club and Air France Salon access.",
        "historical_context": (
            "Delta Air Lines and Air France co-founded SkyTeam on June 22, 2000. In 2008, following Air France's merger with KLM, "
            "Delta, Air France, and KLM established the aviation industry's largest immunized transatlantic joint venture."
        ),
        "significance": "Founding core of SkyTeam and the transatlantic joint venture network.",
        "tags": ["SkyTeam Founder", "Antitrust Immunity", "Paris CDG Hub"]
    },
]


# -----------------------------------------------------------------------------
# 3. Curated In-Depth Historical Case Studies
# -----------------------------------------------------------------------------
CURATED_CASE_STUDIES: List[Dict[str, Any]] = [
    {
        "case_id": "alaska_free_agent",
        "title": "Alaska Airlines: The Great 'Free Agent' Web (1995–2020)",
        "subtitle": "How Seattle's hometown airline built loyalty royalty by playing all major carriers against each other.",
        "primary_carrier": "AS",
        "icon": "🐺",
        "narrative": (
            "For more than two decades, Alaska Airlines achieved something considered impossible in deregulated commercial aviation: "
            "remaining fiercely independent while establishing bilateral elite partnerships with virtually every major US legacy airline "
            "simultaneously.\n\n"
            "Between 1998 and 2010, an Alaska Mileage Plan member could board a Continental flight in Houston, a Northwest flight in Minneapolis, "
            "a Delta flight in Atlanta, or an American flight in Dallas—earning elite qualifying miles and enjoying space-available domestic First Class "
            "upgrades on all of them. Alaska leveraged its absolute dominance of the Pacific Northwest (Seattle, Portland, Anchorage) to offer "
            "critical feeder traffic to carriers who lacked a West Coast hub.\n\n"
            "Internationally, Alaska curated an eclectic dream-team of partners: British Airways, Cathay Pacific, Qantas, Air France, KLM, "
            "Fiji Airways, and Emirates. Mileage Plan became universally celebrated as the most valuable frequent flyer currency on Earth. "
            "Only when Delta invaded Seattle in 2013 and transformed it into a fortress transpacific hub did this peaceful coexistence collapse, "
            "eventually leading Alaska to solidify its alliance with American Airlines and formally join oneworld in 2021."
        ),
        "key_takeaways": [
            "Feeder Leverage: Monopolizing high-yield regional routes (Alaska/PNW) gave Alaska outsized leverage with mainline giants.",
            "Independent Advantage: Avoiding alliance overhead allowed Alaska to craft bespoke earn/burn charts without rigid alliance tier rules.",
            "The End of Neutrality: Once Delta built a competing international gateway at SEA, neutral 'free agency' became strategically unsustainable.",
        ],
    },
    {
        "case_id": "wings_alliance",
        "title": "The Wings Alliance & The Continental-Northwest Axis (1998–2008)",
        "subtitle": "The pioneer of mutual domestic First Class upgrades and seamless transatlantic integration.",
        "primary_carrier": "NW",
        "icon": "🦅",
        "narrative": (
            "In 1998, Northwest Airlines and Continental Airlines stunned the aviation industry by announcing a comprehensive 14-year "
            "strategic alliance, coupled with Northwest acquiring a voting equity stake in Continental. Combined with Northwest's landmark "
            "1989 joint venture with KLM Royal Dutch Airlines, this network was known as the 'Wings Alliance'.\n\n"
            "For frequent flyers, the OnePass and WorldPerks programs operated with an unprecedented degree of mutual elite reciprocity. "
            "A Northwest Platinum Elite was treated with the exact same upgrade priority as a Continental Platinum Elite on flights departing "
            "Houston, Newark, Minneapolis, or Detroit. Elite members received complimentary, automatic, unlimited domestic First Class upgrades "
            "across both airlines—a level of bilateral coordination never before seen in the US.\n\n"
            "The Wings carriers formally integrated into SkyTeam in September 2004, establishing the combined SkyTeam mega-alliance. "
            "The partnership was only dismantled when Delta acquired Northwest in 2008, prompting Continental to exit SkyTeam in 2009 "
            "and join United in Star Alliance."
        ),
        "key_takeaways": [
            "Complete Domestic Reciprocity: Unlimited automatic First Class upgrades across both carriers' separate fleets.",
            "Joint Antitrust Power: NW and KLM proved the economic value of immunized transatlantic revenue sharing.",
            "Catalyst for SkyTeam: The entry of NW, CO, and KLM transformed SkyTeam into a premier global alliance.",
        ],
    },
    {
        "case_id": "hp_co_phoenix_axis",
        "title": "The America West & Continental Phoenix Axis (1994–2002)",
        "subtitle": "How an equity bailout created one of aviation's most effective domestic hub-and-spoke feed partnerships.",
        "primary_carrier": "HP",
        "icon": "🌵",
        "narrative": (
            "When America West Airlines plunged into Chapter 11 bankruptcy in the early 1990s, it found an unexpected savior in Continental Airlines. "
            "In 1994, Continental contributed $54 million as part of an investor consortium that acquired a 33% equity stake in the reorganized carrier.\n\n"
            "The resulting commercial partnership was extraordinarily synergistic. Continental had virtually no presence in the Desert Southwest, "
            "while America West operated high-frequency fortress operations at Phoenix Sky Harbor (PHX) and Las Vegas McCarran (LAS). "
            "Continental integrated FlightFund with OnePass, granting reciprocal elite status qualification, club access between Phoenix Club America "
            "and Continental Presidents Clubs, and extensive codeshare connectivity.\n\n"
            "Flyers across Arizona and Nevada could effortlessly connect to Continental's transatlantic departures from Newark or Latin American "
            "gateways in Houston. The alliance thrived for eight years until Continental liquidated its equity holding in 2002 as America West "
            "embarked on the strategic turnaround that ultimately led to its 2005 takeover of US Airways."
        ),
        "key_takeaways": [
            "Zero Network Overlap: Continental was strong in the East/South; America West commanded the Desert Southwest.",
            "Frequent Flyer Unity: OnePass members enjoyed seamless status recognition across America West's Boeing 737 and 757 fleet.",
            "Stepping Stone to Merger: The operational lessons from the HP-CO partnership prepared America West management to run US Airways and later American Airlines.",
        ],
    },
    {
        "case_id": "dl_as_seattle_divorce",
        "title": "The Delta-Alaska Seattle Hub War & 2017 Loyalty Divorce",
        "subtitle": "From cozy partners to bitter enemies: how Delta's Pacific hub ambitions destroyed a 13-year partnership.",
        "primary_carrier": "DL",
        "icon": "⚔️",
        "narrative": (
            "For nearly a decade, Delta Air Lines and Alaska Airlines enjoyed a peaceful, highly profitable partnership. "
            "Delta operated limited long-haul flights from Seattle to Tokyo and relied heavily on Alaska's dense regional network to fill its widebody jets. "
            "Mileage Plan and SkyMiles members enjoyed mutual elite benefits, lounge access, and reciprocal mileage accrual.\n\n"
            "Everything changed in 2012 when Delta made the strategic decision to build Seattle-Tacoma (SEA) into its premier West Coast global hub. "
            "Rather than negotiating a joint venture, Delta launched aggressive non-stop flights on Alaska's core trunk routes—flying head-to-head "
            "between Seattle and Los Angeles, San Francisco, Anchorage, Las Vegas, and Portland. Delta blanketed the Seattle market with advertisements "
            "declaring itself 'Seattle's Global Airline'.\n\n"
            "Alaska fought back fiercely, out-gauging Delta, defending its home turf with fierce customer loyalty, and retaliating by acquiring "
            "Virgin America in 2016. As hostility peaked, Delta devalued SkyMiles earning on Alaska flights, and on April 30, 2017, the partnership was "
            "officially dissolved. Alaska immediately doubled down on its American Airlines partnership and eventually joined oneworld."
        ),
        "key_takeaways": [
            "Cannibalization of Feeder Alliances: When mainline partners decide to operate their own feed, bilateral alliances inevitably collapse.",
            "The Power of Hometown Loyalty: Alaska defended Seattle market share against a carrier tenfold its size through customer service and loyalty retention.",
            "Reshaping Alliances: The breakup accelerated Alaska's Virgin America merger and its 2021 entry into oneworld.",
        ],
    },
    {
        "case_id": "us_airways_hopscotch",
        "title": "The US Airways Alliance Hopscotch: BA → Star Alliance → oneworld",
        "subtitle": "The only US major airline to hold deep affiliations with two global alliances and a foundational transatlantic carrier.",
        "primary_carrier": "US",
        "icon": "🦘",
        "narrative": (
            "US Airways' frequent flyer program, Dividend Miles, lived one of the most adventurous geopolitical lives in commercial aviation history.\n\n"
            "In 1993, British Airways acquired a nearly 25% stake in USAir, creating a tight transatlantic alliance that routed East Coast travelers "
            "through London. But when BA partnered with American Airlines in 1998 to launch oneworld, USAir was left out in the cold.\n\n"
            "In 2004, US Airways sought refuge by joining Star Alliance, forging a close relationship with United Airlines. When America West acquired "
            "US Airways out of bankruptcy in 2005, management opted to keep the combined airline in Star Alliance. For a decade, Dividend Miles "
            "became beloved for its generous off-peak international award charts, lucrative 100% buy-miles promotions, and elite reciprocity across "
            "Lufthansa, Singapore Airlines, and Air Canada.\n\n"
            "When US Airways merged with American Airlines in December 2013, it executed a historic maneuver: on March 30, 2014, US Airways officially "
            "exited Star Alliance; at 12:01 AM on March 31, 2014, it became a member of oneworld. Within 12 months, Dividend Miles was consolidated "
            "into AAdvantage, ending one of the industry's great loyalty sagas."
        ),
        "key_takeaways": [
            "Alliance Agnosticism: US Airways proved that an airline could successfully switch global alliances without alienating its customer base.",
            "Dividend Miles Folk Legend: Famous for customer-friendly award routings and aggressive mileage sales.",
            "Flawless Cutover: Executed a complex overnight alliance transition from Star Alliance to oneworld with zero operational downtime.",
        ],
    },
    {
        "case_id": "texas_air_onepass",
        "title": "Texas Air & The Birth of OnePass: Eastern & Continental (1987–1991)",
        "subtitle": "How Frank Lorenzo merged Eastern and Continental's programs to invent the multi-carrier loyalty model.",
        "primary_carrier": "EA",
        "icon": "⚡",
        "narrative": (
            "In the mid-1980s, corporate raider Frank Lorenzo assembled the largest airline empire in the world under Texas Air Corporation, "
            "bringing Continental, Eastern, People Express, and New York Air under a single corporate umbrella.\n\n"
            "In 1987, Texas Air launched 'OnePass'—the world's first unified frequent flyer program serving two massive, distinct legacy carriers. "
            "Eastern Air Lines, with its iconic Ionosphere Club and dominant East Coast Shuttle, shared a single mileage currency and tier hierarchy "
            "with Continental Airlines. Frequent flyers in New York or Miami could earn miles on Eastern Whisperjets and redeem them for vacations "
            "on Continental's Rocky Mountain or Micronesia routes.\n\n"
            "While Eastern was torn apart by catastrophic labor strikes and ceased operations in January 1991, Continental kept OnePass alive. "
            "The program survived bankruptcy, Gordon Bethune's 'Go Forward' turnaround, and two decades of expansion before becoming the technological "
            "backbone of modern United MileagePlus in 2012."
        ),
        "key_takeaways": [
            "The Multi-Airline Blueprint: Proved that customers valued a single loyalty currency across separate airline certificates.",
            "Enduring Technology: The OnePass database architecture survived Eastern's collapse and now powers United Airlines.",
            "Lounge Heritage: Eastern's Ionosphere Club pioneered airport VIP hospitality that evolved into today's United Club.",
        ],
    },
    {
        "case_id": "pan_am_worldpass",
        "title": "Pan Am WorldPass: The Pioneer of Intercontinental Redemption (1982–1991)",
        "subtitle": "The golden age of globe-trotting rewards and the asset liquidations that built United and Delta.",
        "primary_carrier": "PA",
        "icon": "🌍",
        "narrative": (
            "Launched in February 1982, Pan Am WorldPass was the luxury benchmark of the early frequent flyer era. "
            "Because Pan Am possessed an unrivaled intercontinental route network connecting six continents, WorldPass could offer rewards "
            "that domestic carriers could only dream of.\n\n"
            "WorldPass was famous for the 'Around the World in 30 Days' First Class award: for 175,000 miles, a member received unlimited "
            "First Class travel on Pan Am's global network, companion tickets, and stays at luxury InterContinental Hotels. "
            "Members could even redeem miles for transatlantic supersonic travel aboard the Concorde via Pan Am's marketing partnership with Air France.\n\n"
            "As Pan Am's financial crisis deepened, its loyalty network became the mechanism through which competitors absorbed its passengers. "
            "United's 1985 purchase of the Pacific Division and Delta's 1991 acquisition of the transatlantic network both relied on honoring "
            "WorldPass miles to retain passenger loyalty, effectively transferring Pan Am's historic customer base into modern mega-carriers."
        ),
        "key_takeaways": [
            "Aspiration as Currency: Proved that high-end intercontinental redemptions drive far greater loyalty than domestic short-haul awards.",
            "Concorde & Luxury Integration: First program to partner with luxury hotel chains and supersonic operators.",
            "Lineage Legacy: Pan Am's customer base formed the transatlantic foundation of modern Delta SkyMiles.",
        ],
    },
]


# -----------------------------------------------------------------------------
# 4. Helper Retrieval & Filtering Functions
# -----------------------------------------------------------------------------
def get_all_programs() -> Dict[str, Dict[str, Any]]:
    """Returns all cataloged loyalty programs."""
    return PROGRAMS


def get_program_by_id(program_id: str) -> Optional[Dict[str, Any]]:
    """Returns program metadata by program ID."""
    return PROGRAMS.get(program_id)


def get_program_by_carrier(carrier_code: str) -> Optional[Dict[str, Any]]:
    """Returns program metadata for a given 2-letter carrier code."""
    c = carrier_code.strip().upper()
    prog_id = CARRIER_TO_PROGRAM.get(c)
    if prog_id:
        return PROGRAMS.get(prog_id)
    return None


def get_active_programs_for_year(year: int) -> List[Dict[str, Any]]:
    """Returns list of programs that were active during the specified year."""
    active = []
    for prog in PROGRAMS.values():
        start = prog["founded_year"]
        end = prog["dissolved_year"]
        if start <= year:
            if end is None or year <= end:
                active.append(prog)
    return active


def get_tiers_for_program(program_id: str) -> List[Dict[str, Any]]:
    """Returns list of status tiers for a given program ID."""
    prog = PROGRAMS.get(program_id)
    if prog:
        return prog.get("status_tiers", [])
    return []


def get_all_partnerships() -> List[Dict[str, Any]]:
    """Returns full catalog of bilateral partnerships."""
    return BILATERAL_PARTNERSHIPS


def get_partnerships_for_year(year: int, carrier_code: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Returns bilateral partnerships active in a specific calendar year.
    Optionally filters to partnerships involving carrier_code.
    """
    results = []
    c = carrier_code.strip().upper() if carrier_code else None

    for p in BILATERAL_PARTNERSHIPS:
        start = p["start_year"]
        end = p["end_year"]
        is_year_active = (start <= year) and (end is None or year <= end)

        if is_year_active:
            if c:
                if p["carrier_1"] == c or p["carrier_2"] == c:
                    results.append(p)
            else:
                results.append(p)
    return results


def get_partnerships_for_carrier(carrier_code: str) -> List[Dict[str, Any]]:
    """Returns all historical and active partnerships involving carrier_code."""
    c = carrier_code.strip().upper()
    return [
        p for p in BILATERAL_PARTNERSHIPS
        if p["carrier_1"] == c or p["carrier_2"] == c
    ]


def get_curated_case_studies(carrier_code: Optional[str] = None) -> List[Dict[str, Any]]:
    """Returns curated deep-dive historical case studies."""
    if not carrier_code:
        return CURATED_CASE_STUDIES
    c = carrier_code.strip().upper()
    return [cs for cs in CURATED_CASE_STUDIES if cs.get("primary_carrier") == c]
