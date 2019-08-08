
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
