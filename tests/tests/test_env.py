def test_api_key_present():
    import os
    assert os.getenv("ALPHA_VANTAGE_API_KEY") is not None
