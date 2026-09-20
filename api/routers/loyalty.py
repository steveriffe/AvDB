"""
Loyalty Endpoints: Frequent Flyer Programs, Status Tiers, and Bilateral Partnerships
Self-contained router with bundled historical loyalty catalog for the AvDB API.
"""
import json
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/loyalty", tags=["Loyalty"])


class LoyaltyTierSchema(BaseModel):
    name: str
    eqmRequired: int
    eqsRequired: int
    upgradeWindowHours: int
    bonusMilesPercent: int
    loungeAccess: bool
    keyPerks: str


class LoyaltyPartnershipSchema(BaseModel):
    partnerCarrierCode: str
    partnerCarrierName: str
    relationshipDepth: str
    startYear: int
    endYear: Optional[int] = None
    eliteReciprocal: bool
    loungeReciprocal: bool
    historicalNote: str


class LoyaltyProgramSchema(BaseModel):
    carrierCode: str
    carrierName: str
    programName: str
    activeAlliance: Optional[str] = None
    tiers: List[LoyaltyTierSchema] = []
    partnerships: List[LoyaltyPartnershipSchema] = []


def _load_catalog() -> List[LoyaltyProgramSchema]:
    json_path = Path(__file__).parent.parent / "loyalty_catalog.json"
    if json_path.exists():
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [LoyaltyProgramSchema(**item) for item in data]
    return []


LOYALTY_CATALOG = _load_catalog()


@router.get("", response_model=List[LoyaltyProgramSchema])
def list_loyalty_programs() -> List[LoyaltyProgramSchema]:
    """Returns curated list of US airline frequent flyer loyalty programs, tiers, and partnerships."""
    return LOYALTY_CATALOG
