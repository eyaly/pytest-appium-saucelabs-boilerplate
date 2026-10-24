"""
Example tests. Flows live directly in the test — no page objects.

Locators that differ per platform are picked with a simple dict keyed by
`platform` (the fixture parameter: "android" or "ios"), e.g.:

    LOGIN_BUTTON = {
        "android": (AppiumBy.ID, "com.example:id/login"),
        "ios": (AppiumBy.ACCESSIBILITY_ID, "login"),
    }
    driver.find_element(*LOGIN_BUTTON[platform]).click()

Copy this file as a starting point for your own tests.
"""
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TestSmoke:
    @pytest.mark.smoke
    def test_app_launches(self, driver, platform):
        assert driver.session_id, f"No Appium session on {platform}"

    def test_screen_has_elements(self, driver, platform):
        wait = WebDriverWait(driver, 10)
        elements = wait.until(
            EC.presence_of_all_elements_located((AppiumBy.XPATH, "//*"))
        )
        assert elements, f"No UI elements found on {platform} launch screen"
