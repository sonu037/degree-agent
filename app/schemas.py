from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class FeeItem(BaseModel):
    type: str
    amount: float
    currency: str = "USD"
    notes: Optional[str] = None

class Scholarship(BaseModel):
    name: str
    coverage: str
    link: Optional[str] = None

class Accreditation(BaseModel):
    body: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class Admissions(BaseModel):
    requirements: List[str] = []
    deadlines: List[str] = []
    duration_months: Optional[int] = None

class Program(BaseModel):
    program_id: str
    title: str
    discipline: List[str] = []
    degree_level: str
    university: str
    country: Optional[str] = None
    modality: str = "Online"
    language: Optional[str] = "English"
    tuition_type: str = "standard"  # tuition_free | low_cost | standard
    tuition_detail: Dict[str, Any] = Field(default_factory=dict)
    fees: List[FeeItem] = []
    scholarships: List[Scholarship] = []
    accreditation: Accreditation = Accreditation()
    admissions: Admissions = Admissions()
    source_urls: List[str] = []
    last_checked_utc: Optional[str] = None
