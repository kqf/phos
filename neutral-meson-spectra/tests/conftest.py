import sys
import pytest


@pytest.fixture
def stop():
    not_discover = 'discover' not in sys.argv
    not_pytest = 'pytest' not in sys.argv[0]
    return not_discover and not_pytest


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "onlylocal: mark test to run only as they require the data ",
    )
    config.addinivalue_line(
        "markers",
        "interactive: exclude scripts with ROOT pop-up windows",
    )
