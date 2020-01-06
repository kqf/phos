import pytest
import json


@pytest.fixture
def settings():
    with open("config/test_software.json") as f:
        data = json.load(f)
    return data
