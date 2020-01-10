import pytest


@pytest.fixture
def stop(request):
    return request.config.getoption("--no-stop")


def pytest_addoption(parser):
    parser.addoption(
        "--no-stop",
        action="store_false",
        help="Don't stop to show plots",
    )


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "onlylocal: mark test to run only as they require the data ",
    )
    config.addinivalue_line(
        "markers",
        "interactive: exclude scripts with ROOT pop-up windows",
    )
    config.addinivalue_line(
        "markers",
        "thesis: script produces the final images",
    )
