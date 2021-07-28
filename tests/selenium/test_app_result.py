import os
import time

import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import (
    InvalidSelectorException,
    NoSuchElementException,
    ElementNotVisibleException,
    ElementNotInteractableException,
    WebDriverException)

result_endpoint_ip = os.getenv('RESULT_ENDPOINT_IP')

# Give Selenium Hub time to start
time.sleep(15)  # TODO: figure how to do this better

@pytest.fixture(scope='module')
def browser():
    browser_name = ip = os.getenv('BROWSER')
    browser = webdriver.Remote(
        command_executor='http://selenium_hub:4444/wd/hub',
        desired_capabilities={'browserName': browser_name},
    )
    yield browser
    browser.quit()


def test_confirm_result_title(browser):
    browser.get("http://{}:80".format(result_endpoint_ip))
    assert "Cats vs Dogs -- Result" in browser.title


def test_confirm_result(browser):
    browser.get("http://{}:80".format(result_endpoint_ip))
    element = browser.find_element(By.ID, 'result')
    assert element.get_attribute('id') == 'result'


def test_confirm_result_vote_tally(browser):
    browser.get("http://{}:80".format(result_endpoint_ip))
    element = browser.find_element(By.ID, 'result')
    assert 'No votes yet' not in element.text
