"""Shared fixtures for M1-B2 tests."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def client() -> TestClient:
    """TestClient with lifespan triggered (model loaded)."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def valid_payload() -> dict:
    """Valid loan application payload.

    TODO — Align with the actual LoanApplication schema and feature_columns
    of pyrenex_risk_v2.json. The example below is a placeholder.
    """
    return {
        "loan_amnt": 500,
        "term": "string",
        "int_rate": 50,
        "installment": 5000,
        "annual_inc": 10000000,
        "dti": 100,
        "delinq_2yrs": 50,
        "fico_range_low": 300,
        "revol_util": 150,
        "grade": "string",
        "home_ownership": "string",
        "verification_status": "string",
        "purpose": "string",
        "emp_length": "string"
}