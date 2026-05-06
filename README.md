# Appium Python Test Automation Framework

A comprehensive Page Object Model (POM) based test automation framework for mobile testing using Appium and Python.

## 📁 Project Structure

```
appium_framework/
├── configs/                    # Configuration files
│   └── config.ini             # App and device configurations
├── pages/                      # Page Object Models
│   ├── __init__.py
│   ├── base_page.py           # Base page class with common methods
│   ├── login_page.py          # Login page object
│   └── home_page.py           # Home page object
├── tests/                      # Test cases
│   ├── __init__.py
│   ├── conftest.py            # Pytest fixtures and hooks
│   ├── test_login.py          # Login test cases
│   └── test_gestures.py       # Gesture test examples
├── utilities/                  # Reusable utilities
│   ├── __init__.py
│   ├── config_reader.py       # Configuration reader
│   ├── driver_factory.py      # Driver initialization
│   ├── gestures.py            # Swipe, scroll, tap utilities
│   ├── common_utils.py        # Wait, screenshot, navigation utilities
│   └── test_data_reader.py    # Test data reader
├── test_data/                  # Test data files
│   └── test_data.json         # Sample test data
├── reports/                    # Test reports and screenshots
│   └── screenshots/           # Auto-captured screenshots
├── requirements.txt            # Python dependencies
├── pytest.ini                 # Pytest configuration
└── README.md                  # This file
```

## 🚀 Setup Instructions

### Prerequisites
1. **Python 3.8+** installed
2. **Node.js** and **npm** installed
3. **Appium Server** installed globally:
   ```bash
   npm install -g appium
   ```
4. **Appium drivers** installed:
   ```bash
   appium driver install uiautomator2  # For Android
   appium driver install xcuitest      # For iOS
   ```
5. **Android Studio** (for Android testing) or **Xcode** (for iOS testing)

### Installation

1. **Clone or download the framework**

2. **Install Python dependencies**:
   ```bash
   cd appium_framework
   pip install -r requirements.txt
   ```

3. **Configure your app details**:
   Edit `configs/config.ini` and update:
   - `appPackage` and `appActivity` for Android
   - `bundleId` for iOS
   - Device details (name, version)

4. **Start Appium Server**:
   ```bash
   appium
   ```
   Or start with specific port:
   ```bash
   appium -p 4723
   ```

## 🧪 Running Tests

### Run all tests:
```bash
pytest tests/
```

### Run with HTML report:
```bash
pytest tests/ --html=reports/report.html --self-contained-html
```

### Run specific test file:
```bash
pytest tests/test_login.py
```

### Run tests by marker:
```bash
# Run smoke tests
pytest -m smoke

# Run regression tests
pytest -m regression

# Run login related tests
pytest -m login
```

### Run on specific platform:
```bash
# Run on Android (default)
pytest tests/test_login.py

# Run on iOS
pytest tests/test_login.py --platform=ios
```

### Run with verbose output:
```bash
pytest tests/ -v
```

## 📝 Key Features

### 1. **Driver Factory**
Centralized driver management with platform support:
```python
from utilities.driver_factory import DriverFactory

driver_factory = DriverFactory()
driver = driver_factory.get_driver('android')  # or 'ios'
```

### 2. **Gestures Utility**
Comprehensive gesture support:
```python
from utilities.gestures import Gestures

gestures = Gestures(driver)

# Basic swipes
gestures.swipe_up()
gestures.swipe_down()
gestures.swipe_left()
gestures.swipe_right()

# Swipe on specific element
gestures.swipe_on_element(element, direction='left')

# Scrolling
gestures.scroll_to_text("Submit Button")
gestures.scroll_to_element(locator)

# Long press
gestures.long_press(element, duration=2000)

# Tap operations
gestures.tap(element)
gestures.tap_coordinates(x, y)
gestures.double_tap(element)

# Drag and drop
gestures.drag_and_drop(source_element, target_element)
```

### 3. **Common Utilities**
Essential helper methods:
```python
from utilities.common_utils import CommonUtils

utils = CommonUtils(driver)

# Waits
utils.wait_for_element(locator, timeout=20)
utils.wait_for_element_clickable(locator)
utils.is_element_visible(locator)

# Interactions
utils.click(locator)
utils.send_keys(locator, "text")
utils.clear_and_send_keys(locator, "text")

# Screenshots
utils.take_screenshot("test_name")

# Keyboard
utils.hide_keyboard()
utils.is_keyboard_shown()

# App operations
utils.activate_app("com.example.app")  # Replaces deprecated launch_app()
utils.terminate_app("com.example.app")  # Replaces deprecated close_app()
utils.background_app(seconds=5)
# reset_app() removed; use terminate_app() then activate_app()

# Device operations
utils.get_current_activity()
utils.lock_device(5)
utils.shake_device()
```

### 4. **Page Object Model**
Clean separation of page elements and test logic:

**Base Page** (pages/base_page.py):
```python
class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.gestures = Gestures(driver)
        self.utils = CommonUtils(driver)
```

**Page Object** (pages/login_page.py):
```python
class LoginPage(BasePage):
    USERNAME_FIELD = (AppiumBy.ID, "username")
    
    def enter_username(self, username):
        self.enter_text(self.USERNAME_FIELD, username)
```

**Test** (tests/test_login.py):
```python
def test_login(setup):
    driver = setup
    login_page = LoginPage(driver)
    login_page.login("user", "pass")
    assert home_page.is_home_page_displayed()
```

### 5. **Test Data Management**
JSON-based test data:
```python
from utilities.test_data_reader import TestDataReader

data_reader = TestDataReader()
valid_users = data_reader.get_valid_users()

for user in valid_users:
    login_page.login(user['username'], user['password'])
```

### 6. **Automatic Screenshot on Failure**
Configured in `conftest.py` - automatically captures screenshots when tests fail.

### 7. **File Operations & Assertions**
Comprehensive file upload, download validation, and assertion methods for robust test validations.

## 🎯 Usage Examples

### Example 1: Creating a New Page Object

```python
# pages/settings_page.py
from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy

class SettingsPage(BasePage):
    NOTIFICATIONS_TOGGLE = (AppiumBy.ID, "notifications")
    
    def toggle_notifications(self):
        self.click_element(self.NOTIFICATIONS_TOGGLE)
```

### Example 2: Writing a Test

```python
# tests/test_settings.py
import pytest
from pages.settings_page import SettingsPage

@pytest.mark.smoke
def test_toggle_notifications(setup):
    driver = setup
    settings_page = SettingsPage(driver)
    settings_page.toggle_notifications()
    # Add assertions
```

### Example 3: Using Gestures

```python
def test_carousel_swipe(setup):
    driver = setup
    from utilities.gestures import Gestures
    
    gestures = Gestures(driver)
    
    # Find carousel
    carousel = driver.find_element(AppiumBy.ID, "carousel")
    
    # Swipe left 3 times
    for _ in range(3):
        gestures.swipe_on_element(carousel, 'left')
```

### Example 4: File Upload and Download

```python
def test_file_operations(setup):
    driver = setup
    from pages.base_page import BasePage
    
    base_page = BasePage(driver)
    
    # Upload file
    base_page.file_ops.upload_file("document.pdf", upload_button_locator)
    
    # Download and validate
    file_path = base_page.file_ops.wait_for_file_download("report.pdf", timeout=30)
    base_page.assertions.assert_file_exists(file_path)
    base_page.assertions.assert_file_extension(file_path, '.pdf')
    base_page.assertions.assert_file_size_greater_than(file_path, 1024)
```

### Example 5: Comprehensive Assertions

```python
def test_assertions(setup):
    driver = setup
    from pages.base_page import BasePage
    
    base_page = BasePage(driver)
    
    # Element assertions
    base_page.assertions.assert_element_visible(locator)
    base_page.assertions.assert_element_clickable(locator)
    
    # Text assertions
    base_page.assertions.assert_text_contains(locator, "Welcome")
    base_page.assertions.assert_text_matches_pattern(locator, r"\d{3}-\d{3}-\d{4}")
    
    # Count assertions
    base_page.assertions.assert_element_count_greater_than(list_locator, 0)
```

## 🔧 Configuration

### Update Device Configuration
Edit `configs/config.ini`:

```ini
[ANDROID]
platformName = Android
platformVersion = 13
deviceName = emulator-5554
appPackage = com.yourapp.package
appActivity = com.yourapp.MainActivity

[APPIUM]
appium_server = http://127.0.0.1:4723

[TIMEOUTS]
implicit_wait = 10
explicit_wait = 20
```

## 📊 Reports

- **HTML Reports**: Generated in `reports/` directory
- **Screenshots**: Auto-saved in `reports/screenshots/` on test failures
- **Console Logs**: Configured in `pytest.ini`

## 🏷️ Pytest Markers

Available markers:
- `@pytest.mark.smoke` - Critical tests
- `@pytest.mark.regression` - Comprehensive tests
- `@pytest.mark.login` - Login related tests
- `@pytest.mark.platform('android')` or `@pytest.mark.platform('ios')`

## 🤝 Contributing

To add new features:
1. Add utilities in `utilities/`
2. Create page objects in `pages/`
3. Write tests in `tests/`
4. Update test data in `test_data/`

## 📚 Additional Resources

- [Appium Documentation](http://appium.io/docs/en/latest/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Selenium Python Bindings](https://selenium-python.readthedocs.io/)
- [File Operations Guide](FILE_OPERATIONS_GUIDE.md) - Comprehensive guide for file handling
- [Framework Structure Guide](FRAMEWORK_GUIDE.md) - Detailed framework overview

## 🐛 Troubleshooting

**Issue**: Driver not starting
- Ensure Appium server is running
- Check device/emulator is connected: `adb devices`

**Issue**: Element not found
- Verify locators using Appium Inspector
- Increase wait times in config.ini

**Issue**: Import errors
- Ensure all dependencies installed: `pip install -r requirements.txt`
- Check Python path includes project root

## 📄 License

This framework is provided as-is for educational and testing purposes.
