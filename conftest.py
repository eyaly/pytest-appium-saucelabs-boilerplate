"""
Pytest fixtures for Appium on Sauce Labs real devices.

Every test that uses the `driver` fixture is parametrized per platform, so
`pytest -n 4` runs the Android and iOS variants in parallel.
"""
import os
from datetime import datetime

import pytest
from appium import webdriver
from dotenv import load_dotenv

from config.capabilities import OPTIONS_BY_PLATFORM, sauce_url

load_dotenv()


def pytest_addoption(parser):
    parser.addoption(
        "--platform",
        action="store",
        default="both",
        choices=["android", "ios", "both"],
        help="Platform(s) to run on.",
    )


def pytest_configure(config):
    # Set once on the controller; xdist workers inherit the env, so all
    # sessions from one run land in the same Sauce build.
    os.environ.setdefault(
        "SAUCE_BUILD_NAME",
        f"pytest-appium-boilerplate-{datetime.now():%Y%m%d-%H%M%S}",
    )


def pytest_generate_tests(metafunc):
    if "platform" not in metafunc.fixturenames:
        return
    selected = metafunc.config.getoption("--platform")
    platforms = ["android", "ios"] if selected == "both" else [selected]
    if metafunc.definition.get_closest_marker("android_only"):
        platforms = [p for p in platforms if p == "android"]
    if metafunc.definition.get_closest_marker("ios_only"):
        platforms = [p for p in platforms if p == "ios"]
    metafunc.parametrize("platform", platforms)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Expose each phase's report on the item so the driver fixture can
    # report pass/fail back to Sauce Labs.
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture
def driver(request, platform):
    for var in ("SAUCE_USERNAME", "SAUCE_ACCESS_KEY"):
        if not os.getenv(var):
            pytest.fail(f"{var} is not set (see .env.example)")

    options = OPTIONS_BY_PLATFORM[platform](request.node.name)
    drv = webdriver.Remote(sauce_url(), options=options)
    drv.implicitly_wait(0)

    yield drv

    passed = getattr(request.node, "rep_call", None) and request.node.rep_call.passed
    try:
        drv.execute_script(f"sauce:job-result={'passed' if passed else 'failed'}")
    finally:
        drv.quit()
