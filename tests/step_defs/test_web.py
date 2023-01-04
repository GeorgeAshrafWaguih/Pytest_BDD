import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Constants
DUCKDUCKGO_HOME = 'https;//duckduckgo.com/'

# Scenarios
scenarios('../features/web.feature')


# Fixtures
@pytest.fixture
def browser():
    b = webdriver.Chrome()
    b.implicitly_wait(10)
    yield b
    b.quit()


# Given Steps
@given('the DuckDuckGo home page is displayed', target_fixture='ddg_home')
def ddg_home(browser):
    browser.get(DUCKDUCKGO_HOME)


# When Steps
@when(parsers.parse('the user searches for "{text}"'))
@when(parsers.parse('the user searches for the phrase:\n{text}'))
def search_phrase(browser, text):
    search_input = browser.find_element(By.NAME, "q")
    search_input.send_keys(text + Keys.RETURN)


# Then Steps
@then(parsers.parse('results are shown for "{phrase}"'))
def search_results(browser, phrase):
    # Check search result list
    links_div = browser.find_element(By.ID, "links")
    assert len(links_div.find_elements(By.XPATH, "//div")) > 0
    # Check search phrase
    search_input = browser.find_element(By.NAME, "q")
    assert search_input.get_attribute('value') == phrase


@then(parsers.parse('one of the results contains "{phrase}"'))
def results_have_one(browser, phrase):
    xpath = "//div[@id='links']//*[contains(text(), '%s')]" % phrase
    results = browser.find_elements(By.XPATH, xpath)
    assert len(results) > 0
