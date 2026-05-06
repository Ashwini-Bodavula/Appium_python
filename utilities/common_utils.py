"""
Common Utilities
Contains helper methods for waits, screenshots, alerts, keyboards, app management, etc.

Updated for Appium 2.x:
- launch_app() / close_app() / reset() → activate_app() / terminate_app()
- set_network_connection() / network_connection → execute_script('mobile: setConnectivity', ...)
- shake() still valid on iOS (XCUITest)
- lock() / unlock() / is_locked() still valid (driver methods)
- Added: get_clipboard_text(), set_clipboard_text()
- Added: execute_mobile() convenience wrapper for mobile: commands
- get_device_time() still valid
- install_app() / remove_app() / is_app_installed() still valid
"""
import os
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from appium.webdriver.common.appiumby import AppiumBy


class CommonUtils:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    # ==================== WAIT HELPERS ====================

    def wait_for_element(self, locator, timeout=20):
        """
        Wait for element to be visible.

        Args:
            locator (tuple): Locator strategy and value
            timeout (int): Wait timeout in seconds

        Returns:
            WebElement: Found element
        """
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_element_clickable(self, locator, timeout=20):
        """
        Wait for element to be clickable.

        Args:
            locator (tuple): Locator strategy and value
            timeout (int): Wait timeout in seconds

        Returns:
            WebElement: Clickable element
        """
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_for_element_presence(self, locator, timeout=20):
        """
        Wait for element to be present in the DOM.

        Args:
            locator (tuple): Locator strategy and value
            timeout (int): Wait timeout in seconds

        Returns:
            WebElement: Found element
        """
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def wait_for_elements(self, locator, timeout=20):
        """
        Wait for multiple elements to be visible.

        Args:
            locator (tuple): Locator strategy and value
            timeout (int): Wait timeout in seconds

        Returns:
            list: List of WebElements
        """
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_all_elements_located(locator)
        )

    def is_element_visible(self, locator, timeout=5):
        """
        Check if element is visible within timeout.

        Args:
            locator (tuple): Locator strategy and value
            timeout (int): Wait timeout in seconds

        Returns:
            bool: True if visible, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def is_element_present(self, locator, timeout=5):
        """
        Check if element is present in the DOM.

        Args:
            locator (tuple): Locator strategy and value
            timeout (int): Wait timeout in seconds

        Returns:
            bool: True if present, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    # ==================== ELEMENT INTERACTION ====================

    def get_text(self, locator):
        """
        Get visible text from element.

        Args:
            locator (tuple): Locator strategy and value

        Returns:
            str: Element text
        """
        element = self.wait_for_element(locator)
        return element.text

    def get_attribute(self, locator, attribute):
        """
        Get attribute value from element.

        Args:
            locator (tuple): Locator strategy and value
            attribute (str): Attribute name

        Returns:
            str: Attribute value
        """
        element = self.wait_for_element(locator)
        return element.get_attribute(attribute)

    def clear_and_send_keys(self, locator, text):
        """
        Clear field and enter text.

        Args:
            locator (tuple): Locator strategy and value
            text (str): Text to enter
        """
        element = self.wait_for_element_clickable(locator)
        element.clear()
        element.send_keys(text)

    def send_keys(self, locator, text):
        """
        Send keys to element without clearing first.

        Args:
            locator (tuple): Locator strategy and value
            text (str): Text to enter
        """
        element = self.wait_for_element(locator)
        element.send_keys(text)

    def click(self, locator):
        """
        Wait for element to be clickable and click it.

        Args:
            locator (tuple): Locator strategy and value
        """
        element = self.wait_for_element_clickable(locator)
        element.click()

    # ==================== SCREENSHOT ====================

    def take_screenshot(self, name="screenshot"):
        """
        Take screenshot and save to reports/screenshots directory.

        Args:
            name (str): Screenshot name prefix

        Returns:
            str: Screenshot file path
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_dir = os.path.join(
            os.path.dirname(__file__), '..', 'reports', 'screenshots'
        )
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshot_dir, f"{name}_{timestamp}.png")
        self.driver.save_screenshot(screenshot_path)
        return screenshot_path

    # ==================== KEYBOARD ====================

    def hide_keyboard(self):
        """Hide the keyboard if visible."""
        try:
            self.driver.hide_keyboard()
        except Exception:
            pass

    def is_keyboard_shown(self):
        """
        Check if the on-screen keyboard is visible.

        Returns:
            bool: True if keyboard is shown
        """
        return self.driver.is_keyboard_shown()

    # ==================== DEVICE INFO ====================

    def get_current_activity(self):
        """
        Get the current foreground activity name (Android only).

        Returns:
            str: Current activity name
        """
        return self.driver.current_activity

    def get_current_package(self):
        """
        Get the current foreground package name (Android only).

        Returns:
            str: Current package name
        """
        return self.driver.current_package

    def get_device_time(self):
        """
        Get the current device time.

        Returns:
            str: Device time string
        """
        return self.driver.get_device_time()

    # ==================== APP MANAGEMENT (Appium 2.x) ====================

    def activate_app(self, app_id):
        """
        Activate (bring to foreground) an already-installed app.
        Replaces deprecated driver.launch_app().

        Args:
            app_id (str): Bundle ID (iOS) or package name (Android)
        """
        self.driver.activate_app(app_id)

    def terminate_app(self, app_id, timeout=500):
        """
        Terminate a running app.
        Replaces deprecated driver.close_app().

        Args:
            app_id (str): Bundle ID (iOS) or package name (Android)
            timeout (int): Timeout in ms to wait for termination
        """
        self.driver.terminate_app(app_id, timeout=timeout)

    def query_app_state(self, app_id):
        """
        Query the current lifecycle state of an app.
        Returns: 0=not installed, 1=not running, 2=bg-suspended,
                 3=bg-running, 4=foreground.

        Args:
            app_id (str): Bundle ID (iOS) or package name (Android)

        Returns:
            int: App state code
        """
        return self.driver.query_app_state(app_id)

    def background_app(self, seconds=5):
        """
        Put app in background for specified seconds.

        Args:
            seconds (int): Duration in seconds
        """
        self.driver.background_app(seconds)

    def is_app_installed(self, bundle_id):
        """
        Check if app is installed on device.

        Args:
            bundle_id (str): Bundle ID or package name

        Returns:
            bool: True if installed
        """
        return self.driver.is_app_installed(bundle_id)

    def install_app(self, app_path):
        """
        Install application from local path.

        Args:
            app_path (str): Path to .apk or .ipa file
        """
        self.driver.install_app(app_path)

    def remove_app(self, bundle_id):
        """
        Uninstall application from device.

        Args:
            bundle_id (str): Bundle ID or package name
        """
        self.driver.remove_app(bundle_id)

    # ==================== NETWORK (Appium 2.x Android) ====================

    def set_network_connection(self, wifi=None, data=None, airplane_mode=None):
        """
        Set network connectivity state (Android only).
        Replaces deprecated driver.set_network_connection(int).

        Use mobile: setConnectivity execute_script via Appium 2.x UiAutomator2.

        Args:
            wifi (bool): Enable/disable Wi-Fi
            data (bool): Enable/disable mobile data
            airplane_mode (bool): Enable/disable airplane mode
        """
        params = {}
        if wifi is not None:
            params['wifi'] = wifi
        if data is not None:
            params['data'] = data
        if airplane_mode is not None:
            params['airplaneMode'] = airplane_mode
        self.driver.execute_script('mobile: setConnectivity', params)

    def get_network_connection(self):
        """
        Get current network connectivity state (Android only).
        Returns a dict with wifi, data, airplaneMode keys.

        Returns:
            dict: Connectivity state
        """
        return self.driver.execute_script('mobile: getConnectivity', {})

    # ==================== DEVICE CONTROL ====================

    def shake_device(self):
        """Shake the device (iOS / XCUITest only)."""
        self.driver.shake()

    def lock_device(self, seconds=5):
        """
        Lock device for specified seconds.

        Args:
            seconds (int): Duration in seconds
        """
        self.driver.lock(seconds)

    def unlock_device(self):
        """Unlock the device."""
        self.driver.unlock()

    def is_locked(self):
        """
        Check if the device screen is locked.

        Returns:
            bool: True if locked
        """
        return self.driver.is_locked()

    # ==================== CLIPBOARD ====================

    def set_clipboard_text(self, text):
        """
        Set text to device clipboard.

        Args:
            text (str): Text to copy to clipboard
        """
        self.driver.set_clipboard_text(text)

    def get_clipboard_text(self):
        """
        Get text from device clipboard.

        Returns:
            str: Clipboard text content
        """
        return self.driver.get_clipboard_text()

    # ==================== MOBILE EXECUTE HELPER ====================

    def execute_mobile(self, command, params=None):
        """
        Convenience wrapper for driver.execute_script('mobile: <command>', params).
        Supports all Appium 2.x mobile: commands.

        Args:
            command (str): Mobile command name (without 'mobile: ' prefix)
            params (dict): Command parameters

        Returns:
            Any: Command result
        """
        return self.driver.execute_script(f'mobile: {command}', params or {})
