import Foundation

public struct LoyaltyProgram: Identifiable, Codable, Hashable, Sendable {
    public var id: String { carrierCode }
    public let carrierCode: String
    public let carrierName: String
    public let programName: String
    public let activeAlliance: String?
    public let tiers: [LoyaltyTier]
    public let partnerships: [LoyaltyPartnership]

    public init(
        carrierCode: String,
        carrierName: String,
        programName: String,
        activeAlliance: String?,
        tiers: [LoyaltyTier],
        partnerships: [LoyaltyPartnership] = []
    ) {
        self.carrierCode = carrierCode
        self.carrierName = carrierName
        self.programName = programName
        self.activeAlliance = activeAlliance
        self.tiers = tiers
        self.partnerships = partnerships
    }
}

public struct LoyaltyTier: Identifiable, Codable, Hashable, Sendable {
    public var id: String { name }
    public let name: String
    public let eqmRequired: Int
    public let eqsRequired: Int
    public let upgradeWindowHours: Int
    public let bonusMilesPercent: Int
    public let loungeAccess: Bool
    public let keyPerks: String

    public init(
        name: String,
        eqmRequired: Int,
        eqsRequired: Int,
        upgradeWindowHours: Int,
        bonusMilesPercent: Int,
        loungeAccess: Bool,
        keyPerks: String
    ) {
        self.name = name
        self.eqmRequired = eqmRequired
        self.eqsRequired = eqsRequired
        self.upgradeWindowHours = upgradeWindowHours
        self.bonusMilesPercent = bonusMilesPercent
        self.loungeAccess = loungeAccess
        self.keyPerks = keyPerks
    }
}

public struct LoyaltyPartnership: Identifiable, Codable, Hashable, Sendable {
    public var id: String { "\(partnerCarrierCode)-\(relationshipDepth)" }
    public let partnerCarrierCode: String
    public let partnerCarrierName: String
    public let relationshipDepth: String
    public let startYear: Int
    public let endYear: Int?
    public let eliteReciprocal: Bool
    public let loungeReciprocal: Bool
    public let historicalNote: String

    public init(
        partnerCarrierCode: String,
        partnerCarrierName: String,
        relationshipDepth: String,
        startYear: Int,
        endYear: Int?,
        eliteReciprocal: Bool,
        loungeReciprocal: Bool,
        historicalNote: String
    ) {
        self.partnerCarrierCode = partnerCarrierCode
        self.partnerCarrierName = partnerCarrierName
        self.relationshipDepth = relationshipDepth
        self.startYear = startYear
        self.endYear = endYear
        self.eliteReciprocal = eliteReciprocal
        self.loungeReciprocal = loungeReciprocal
        self.historicalNote = historicalNote
    }
}

