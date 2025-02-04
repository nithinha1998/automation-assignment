import pytest
from pages.page_objects import Pageobject

@pytest.fixture(scope="session")
def page():
    driver = Pageobject()
    yield driver
    driver.exit()
