# pytest-appium-saucelabs-boilerplate

Boilerplate for testing native Android and iOS apps with Pytest + Appium on
Sauce Labs real devices. Clone it, point it at your app, and add your tests.
No page objects — each flow lives in its test file.

## Structure

```
conftest.py              # driver fixture, --platform option, Sauce pass/fail reporting
config/capabilities.py   # Sauce URL/region, Android (UiAutomator2) / iOS (XCUITest) capabilities
tests/test_smoke.py      # example tests — copy as a starting point
pytest.ini               # default options and custom markers
requirements.txt
.env.example             # copy to .env (.env itself is git-ignored)
LICENSE                  # MIT
```

## Setup

Upload your Android (`.apk`) and iOS (`.ipa`) apps to
[Sauce Labs App Storage](https://docs.saucelabs.com/mobile-apps/app-storage/)
first. The defaults expect `SauceLabs-Demo-App.apk` and
`SauceLabs-Demo-App.ipa`.

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Then in `.env`:

- `SAUCE_USERNAME` / `SAUCE_ACCESS_KEY` — or set them as system env vars.
- `SAUCE_REGION` — `eu-central-1` (default) or `us-west-1`.
- `ANDROID_APP` / `IOS_APP` — your apps in Sauce Storage, e.g. `storage:filename=my-app.apk`.
- `ANDROID_DEVICE` / `IOS_DEVICE` — device name or regex.

`.env` is listed in `.gitignore` so your credentials are never committed.

In every new terminal, run `source .venv/bin/activate` first.

## Run

```bash
pytest                                   # Android + iOS, one test at a time
pytest --platform android                # Android only
pytest -n 4                              # Android + iOS in parallel
pytest -n 2 --platform ios               # iOS only, in parallel
pytest tests/test_smoke.py::TestSmoke    # one class
pytest -k test_app_launches              # by name
pytest -m smoke                          # only tests marked @pytest.mark.smoke
pytest -n 4 --reruns 1                   # retry flaky sessions once
```

Keep `-n` within your Sauce Labs concurrency limit.

## Writing tests

Request the `driver` fixture (and `platform` if you need per-platform
locators). Each such test runs once per platform: `test_x[android]`,
`test_x[ios]`.

```python
import pytest

class TestLogin:
    def test_login(self, driver, platform):
        ...

    @pytest.mark.android_only
    def test_back_button(self, driver, platform):
        driver.back()
```

Use `@pytest.mark.android_only` or `@pytest.mark.ios_only` on a test, a
class, or a whole file (`pytestmark = pytest.mark.android_only`). Pass/fail
is reported to Sauce Labs automatically.

To group tests, add a marker (e.g. `@pytest.mark.smoke`), register it under
`markers` in `pytest.ini`, and select it with `-m`:

```bash
pytest -m smoke                          # only smoke tests
pytest -m "not smoke"                    # everything except smoke tests
pytest -m "smoke and android_only"       # combine markers
```

## License

[MIT](LICENSE)
