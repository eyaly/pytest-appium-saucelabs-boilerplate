"""Sauce Labs Real Device Cloud capabilities for Android and iOS."""
import os

from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions


# Accepts both the hostname form (eu-central-1) and the form used by other
# Sauce tools (EU_CENTRAL).
REGIONS = {
    "eu-central-1": "eu-central-1",
    "eu_central": "eu-central-1",
    "us-west-1": "us-west-1",
    "us_west": "us-west-1",
}


def sauce_url() -> str:
    raw = os.getenv("SAUCE_REGION") or "eu-central-1"
    region = REGIONS.get(raw.strip().lower())
    if region is None:
        raise ValueError(
            f"Unknown SAUCE_REGION {raw!r}; use one of: {', '.join(REGIONS)}"
        )
    return f"https://ondemand.{region}.saucelabs.com:443/wd/hub"


def _sauce_options(test_name: str) -> dict:
    return {
        "username": os.environ["SAUCE_USERNAME"],
        "accessKey": os.environ["SAUCE_ACCESS_KEY"],
        "build": os.environ["SAUCE_BUILD_NAME"],
        "name": test_name,
        "appiumVersion": "latest",
    }


def android_options(test_name: str) -> UiAutomator2Options:
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = os.getenv("ANDROID_DEVICE", "Google.*")
    if os.getenv("ANDROID_PLATFORM_VERSION"):
        options.platform_version = os.environ["ANDROID_PLATFORM_VERSION"]
    options.app = os.getenv("ANDROID_APP", "storage:filename=SauceLabs-Demo-App.apk")
    options.set_capability("appium:autoGrantPermissions", True)
    options.set_capability("sauce:options", _sauce_options(test_name))
    return options


def ios_options(test_name: str) -> XCUITestOptions:
    options = XCUITestOptions()
    options.platform_name = "iOS"
    options.device_name = os.getenv("IOS_DEVICE", "iPhone.*")
    if os.getenv("IOS_PLATFORM_VERSION"):
        options.platform_version = os.environ["IOS_PLATFORM_VERSION"]
    options.app = os.getenv("IOS_APP", "storage:filename=SauceLabs-Demo-App.ipa")
    options.set_capability("appium:autoAcceptAlerts", True)
    options.set_capability("sauce:options", _sauce_options(test_name))
    return options


OPTIONS_BY_PLATFORM = {
    "android": android_options,
    "ios": ios_options,
}
