"""Pydantic schemas for the Pyrenex Risk API.

LoanApplication is aligned with the feature_columns from your
pyrenex_risk_v2.json metadata (M1-B1 output).
"""
from __future__ import annotations

from pydantic import BaseModel, Field


class LoanApplication(BaseModel):
    """Input schema for /predict.

    Feature_columns from your pyrenex_risk_v2.json. 
    """

    loan_amnt: float = Field(..., ge=500, le=40_000, description="Loan amount (USD)")
    term: str = Field(..., description="Loan term, e.g. '36 months' or '60 months'")
    int_rate: float = Field(..., ge=0, le=50, description="Interest rate (%)")
    installment: float = Field(..., ge=0, le=5_000, description="Monthly installment (USD)")
    annual_inc: float = Field(..., ge=0, le=10_000_000, description="Annual income (USD)")
    dti: float = Field(..., ge=0, le=100, description="Debt-to-income ratio")
    delinq_2yrs: int = Field(..., ge=0, le=50, description="Delinquencies in the last 2 years")
    fico_range_low: int = Field(..., ge=300, le=850, description="Lower bound of FICO range")
    revol_util: float = Field(..., ge=0, le=150, description="Revolving line utilization (%)")
    grade: str = Field(..., description="Loan grade")
    home_ownership: str = Field(..., description="Home ownership status")
    verification_status: str = Field(..., description="Income verification status")
    purpose: str = Field(..., description="Purpose of the loan")
    emp_length: str = Field(..., description="Employment length")
    

    



class Prediction(BaseModel):
    """Output schema for /predict."""

    prediction: int = Field(..., description="0 = Fully Paid, 1 = Charged Off")
    probability: float = Field(..., ge=0.0, le=1.0)
    model_version: str
    request_id: str


class HealthResponse(BaseModel):
    status: str
