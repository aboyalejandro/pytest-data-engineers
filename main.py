import json
import pandas as pd
from datetime import datetime
from unittest.mock import Mock, patch

# --- Example 1: Convert Campaigns to DataFrame ---

def campaigns_to_dataframe(campaigns):
    """Convert list of campaign dictionaries to pandas DataFrame."""
    if not campaigns:
        return pd.DataFrame()
    return pd.DataFrame(campaigns)

def test_convert_campaigns_to_df(clean_campaign):
    """
    TEST: Convert campaign dict to DataFrame and verify structure.

    What: Takes clean_campaign fixture, converts to DataFrame
    Why: Data engineers convert JSON/dict data to DataFrames for analysis
    Fixture: clean_campaign
    """
    df = campaigns_to_dataframe([clean_campaign])
    assert df.shape[0] == 1
    assert 'campaign_id' in df.columns
    assert df.iloc[0]['name'] == 'Summer Sale Campaign'

# --- Example 2: Campaign Data Validation (uses campaigns.json) ---

def validate_campaign_data(campaign, required_fields):
    """Validate campaign has all required fields and they are not None."""
    for field in required_fields:
        if field not in campaign or campaign[field] is None:
            return False
    return True

def validate_campaign_dates(campaign):
    """Validate that start_date is before or equal to end_date."""
    start = campaign.get('start_date')
    end = campaign.get('end_date')
    if start is None or end is None:
        return True  # Skip validation if dates are missing
    start_dt = datetime.strptime(start, '%Y-%m-%d')
    end_dt = datetime.strptime(end, '%Y-%m-%d')
    return start_dt <= end_dt

def test_valid_campaign_passes(clean_campaign, required_fields):
    """
    TEST: Clean campaign passes required field validation.

    What: Verifies all required fields present and not None
    Why: Positive test - confirms valid data is accepted
    Fixtures: clean_campaign, required_fields
    """
    # TODO: Fix this test - intentionally failing for CI/CD demo
    assert validate_campaign_data(clean_campaign, required_fields) is False  # Should be True!

def test_invalid_dates_fail(campaign_bad_dates):
    """
    TEST: Campaigns with end_date before start_date fail validation.

    What: Tests date logic validation (start <= end)
    Why: Catches ETL bugs, manual entry errors, timezone issues
    Fixture: campaign_bad_dates
    """
    assert validate_campaign_dates(campaign_bad_dates) is False

# --- Example 3: Mocking API Calls ---

def get_campaign_metrics(api_key, campaign_id):
    """Fetch campaign performance metrics from external API."""
    import requests
    response = requests.get(
        f"https://api.adplatform.com/campaigns/{campaign_id}/metrics",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    return response.json()

@patch('requests.get')
def test_mock_api_call(mock_get):
    """
    MOCK TEST: Test API call without hitting real API.

    What: Mock requests.get to return fake campaign metrics
    Why: Fast, free, offline, test-only your code not external APIs
    How: @patch replaces requests.get with mock_get
    """
    mock_response = Mock()
    mock_response.json.return_value = {
        'campaign_id': '12345',
        'impressions': 10000,
        'clicks': 250
    }
    mock_get.return_value = mock_response

    result = get_campaign_metrics("fake-key", "12345")
    assert result['impressions'] == 10000

# --- Example 4: Mocking S3 ---

def load_campaigns_from_s3(bucket, key):
    """Load campaign data from AWS S3 bucket."""
    import boto3
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket, Key=key)
    return json.loads(response['Body'].read().decode('utf-8'))

@patch('boto3.client')
def test_mock_s3_load(mock_boto3, clean_campaign):
    """
    MOCK TEST: Test S3 loading without connecting to AWS.

    What: Mock boto3.client to return fake S3 response with campaign JSON
    Why: No AWS creds needed, free, fast, offline testing
    How: @patch replaces boto3.client, we control what S3 "returns"
    Fixture: clean_campaign
    """
    mock_s3 = Mock()
    mock_response = {'Body': Mock()}
    mock_response['Body'].read.return_value = json.dumps([clean_campaign]).encode()
    mock_s3.get_object.return_value = mock_response
    mock_boto3.return_value = mock_s3

    result = load_campaigns_from_s3('bucket', 'campaigns.json')
    assert len(result) == 1