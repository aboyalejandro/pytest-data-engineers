# Pytest for Data Engineers

A practical pytest tutorial using real-world campaign data with quality issues (nulls, invalid dates, financial inconsistencies).

## 📁 Files

- `campaigns.json` - Messy marketing campaign dataset (100+ campaigns with data quality issues)
- `conftest.py` - Pytest fixtures for clean/messy campaign data
- `main.py` - 4 pytest examples demonstrating key concepts

## 📊 Dataset Issues

The `campaigns.json` from [Synthetic Data Gen] (https://syntheticdatagen.xyz/) contains realistic data quality problems:
- Missing required fields (name, channel, status)
- End dates before start dates
- ROI values without revenue/spend data
- Budget exceeded by actual spend
- Negative ROI values

## 🚀 Quick Start

```bash
# Start virtual env
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest main.py -v

# Run specific test
pytest main.py::test_valid_campaign_passes -v
```

## Output

```bash
========================================= test session starts ==========================================
platform darwin -- Python 3.13.2, pytest-8.4.2, pluggy-1.6.0 -- /Users/your-user/Desktop/pytest-data-engineers/.venv/bin/python3.13
cachedir: .pytest_cache
rootdir: /Users/your-user/path/pytest-data-engineers
collected 5 items                                                                                      

main.py::test_convert_campaigns_to_df PASSED                                                     [ 20%]
main.py::test_valid_campaign_passes PASSED                                                       [ 40%]
main.py::test_invalid_dates_fail PASSED                                                          [ 60%]
main.py::test_mock_api_call PASSED                                                               [ 80%]
main.py::test_mock_s3_load PASSED                                                                [100%]

========================================== 5 passed in 0.69s ===========================================
```

## 🧪 What We're Testing

### Example 1: DataFrame Conversion
Convert campaign dictionaries to pandas DataFrames for analysis

### Example 2: Data Validation
- Required fields (name, channel, status)
- Date logic (start_date <= end_date)
- Financial consistency (ROI requires revenue & spend)

### Example 3: Mocking API Calls
Mock external API calls using `@patch` decorator

### Example 4: Mocking AWS S3
Mock boto3 S3 client to test data loading without AWS

## 💡 Key Concepts

- **Fixtures**: Reusable test data in `conftest.py`
- **Mocking**: Test external services (APIs, S3) without real calls
- **Assertions**: Validate data quality rules
- **Real-world data**: Handle nulls, invalid dates, bad financials