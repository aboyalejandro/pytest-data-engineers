import pytest

@pytest.fixture
def clean_campaign():
    """
    FIXTURE: Valid campaign with all required fields and consistent data.

    Purpose: Provides a "golden example" of what clean campaign data should look like.
    Use case: Test that validation functions correctly accept valid data.
    """
    return {
        "campaign_id": "test-uuid-1234",
        "name": "Summer Sale Campaign",
        "channel": "Instagram",
        "start_date": "2025-01-01",
        "end_date": "2025-03-01",
        "budget": 10000.00,
        "lifetime_spend": 8500.00,
        "total_revenue": 25000.00,
        "roi": 1.94,
        "target_cpa": 50.00,
        "status": "Active",
        "objective": "Conversions",
        "campaign_manager": "john_doe",
        "created_at": "2025-01-01 10:00:00",
        "notes": "Q1 campaign"
    }

@pytest.fixture
def campaign_missing_fields():
    """
    FIXTURE: Campaign missing critical required fields.

    Purpose: Simulates incomplete data often found in real-world datasets.
    Use case: Test that validation rejects campaigns with missing required fields.
    """
    return {
        "campaign_id": "test-uuid-5678",
        "name": None,
        "channel": None,
        "start_date": "2025-01-01",
        "end_date": "2025-03-01",
        "budget": 5000.00,
        "status": None
    }

@pytest.fixture
def campaign_bad_dates():
    """
    FIXTURE: Campaign with illogical date range (end before start).

    Purpose: Tests date validation logic.
    Use case: Ensure validation catches impossible date ranges.
    """
    return {
        "campaign_id": "test-uuid-9999",
        "name": "Invalid Date Campaign",
        "channel": "Facebook",
        "start_date": "2025-05-13",
        "end_date": "2025-04-26",  # Before start!
        "status": "Active"
    }

@pytest.fixture
def campaign_bad_financials():
    """
    FIXTURE: Campaign with inconsistent financial data.

    Purpose: Tests financial validation logic.
    Use case: Ensure ROI cannot exist without supporting revenue/spend data.
    """
    return {
        "campaign_id": "test-uuid-7777",
        "name": "Bad Finance Campaign",
        "channel": "Email",
        "budget": 10000.00,
        "lifetime_spend": None,
        "total_revenue": None,
        "roi": 2.5,  # ROI exists but no revenue/spend!
        "status": "Draft"
    }

@pytest.fixture
def required_fields():
    """
    FIXTURE: List of fields that must be present in every campaign.

    Purpose: Defines the schema requirements for campaign data.
    Use case: Passed to validation functions to check field presence.
    """
    return ["campaign_id", "name", "channel", "status"]
