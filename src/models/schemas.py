from typing import Optional
from pydantic import BaseModel, Field


class SilverBase(BaseModel):
    run_id: Optional[str] = None
    source_system: Optional[str] = None
    ingestion_timestamp: Optional[str] = None
    
    model_config = {
        "extra": "allow"
    }


class SilverOpenFDA(SilverBase):
    report_id: Optional[str] = None
    sex: Optional[str] = None
    drug: Optional[str] = None
    drug_key: Optional[str] = None
    drug_role: Optional[str] = None
    reaction: Optional[str] = None
    serious: Optional[bool] = None
    death: Optional[bool] = None
    hospitalization: Optional[bool] = None
    received_date: Optional[str] = None


class SilverDuckDB(SilverBase):
    drug_name: Optional[str] = None
    drug_key: Optional[str] = None
    manufacturer: Optional[str] = None
    indication: Optional[str] = None
    approval_year: Optional[int] = None


class SilverPayload(BaseModel):
    metadata: dict = Field(default_factory=dict)
    data: list = Field(default_factory=list)
