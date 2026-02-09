# Categorization Service Tests

This directory contains tests for the email categorization service.

## Quick Start

### Option 1: Run the standalone test script (Recommended for quick testing)

```bash
cd server
python __tests__/run_categorization_test.py
```

Or with uv:

```bash
cd server
uv run python __tests__/run_categorization_test.py
```

This will:
- Load sample emails and buckets from the data files
- Run categorization on a small subset (3 emails)
- Run categorization on the full email set
- Display results with email distribution across buckets

### Option 2: Run with pytest (For comprehensive testing)

First, install pytest if you haven't already:

```bash
# Using pip
pip install pytest pytest-asyncio

# Or add to pyproject.toml and run:
# uv add --dev pytest pytest-asyncio
```

Then run the tests:

```bash
cd server
pytest __tests__/test_categorization.py -v
```

Or run specific tests:

```bash
# Run just the basic test
pytest __tests__/test_categorization.py::test_categorize_emails_basic -v

# Run with output shown
pytest __tests__/test_categorization.py -v -s
```

## Test Files

### `test_categorization.py`
Comprehensive test suite with multiple test cases:
- **test_categorize_emails_basic**: Basic functionality with 3 test emails
- **test_categorize_full_email_set**: Test with all sample emails from `data/emails.json`
- **test_categorize_emails_output_structure**: Validates output structure and categories
- **test_pydantic_model_conversion**: Tests Pydantic model conversion
- **test_categorization_agent_response**: Tests specific categorization logic

### `run_categorization_test.py` (in parent directory)
Standalone test runner that doesn't require pytest. Good for quick manual testing and debugging.

## Prerequisites

1. **Environment Variables**: Make sure your `.env` file has the required API keys:
   ```
   ANTHROPIC_API_KEY=your_key_here
   ```

2. **Dependencies**: Ensure all dependencies are installed:
   ```bash
   uv sync
   ```

3. **Test Data**: The tests use data from:
   - `server/data/emails.json` - Sample emails
   - `server/data/buckets.json` - Available categorization buckets

## Expected Output

The categorization service should:
1. Accept a list of email dicts and bucket dicts
2. Convert them to Pydantic models (EmailThread and Bucket)
3. Use the AI agent to categorize each email into appropriate buckets
4. Return the emails with updated `category` fields

Example result:
```python
[
  {
    "id": "test-1",
    "subject": "URGENT: Server Down",
    "snippet": "...",
    "from": "ops@company.com",
    "date": "...",
    "category": "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d"  # Important bucket
  },
  # ...
]
```

## Available Buckets

The default buckets are:
- **Important**: Emails requiring immediate attention or action
- **Can Wait**: Emails that can be addressed later without urgency
- **Auto-archive**: Low-priority emails that can be automatically archived
- **Newsletter**: Newsletters, subscriptions, and promotional content

## Troubleshooting

### API Key Issues
If you see authentication errors, make sure your `ANTHROPIC_API_KEY` is set in `.env`:
```bash
echo "ANTHROPIC_API_KEY=your_key_here" >> .env
```

### Import Errors
Make sure you're running from the `server` directory:
```bash
cd server
python run_categorization_test.py
```

### Async Errors
The tests use async/await. Make sure you have Python 3.11+ which is required by the project.

## Next Steps

After confirming the categorization works:
1. Integrate with the API endpoints in `routes/emails.py`
2. Add error handling for edge cases
3. Consider adding tests for:
   - Empty email lists
   - Invalid bucket IDs
   - Malformed email data
   - API rate limiting
