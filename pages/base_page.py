"""
Base Page
Parent class for all page objects.
Contains common methods that all pages can use.

Updated for Appium 2.x:
- swipe helpers now delegate to Gestures (which use W3C ActionBuilder internally)
- Added activate_app() / terminate_app() replacing launch_app() / close_app()
- Added execute_mobile() convenience passthrough
- Added get_clipboard_text() / set_clipboard_text()
"""
from utilities.gestures import Gestures
from utilities.common_utils import CommonUtils
from utilities.file_operations import FileOperations
from utilities.assertions import Assertions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.gestures = Gestures(driver)
        self.utils = CommonUtils(driver)
        self.file_ops = FileOperations(driver)
        self.assertions = Assertions(driver)

    # ==================== ELEMENT INTERACTION ====================

    def find_element(self, locator):
        """
        Find element using locator (waits for visibility).

        Args:
            locator (tuple): Locator strategy and value

        Returns:
            WebElement: Found element
        """
        return self.utils.wait_for_element(locator)

    def find_elements(self, locator):
        """
        Find multiple elements using locator.

        Args:
            locator (tuple): Locator strategy and value

        Returns:
            list: List of WebElements
        """
        return self.utils.wait_for_elements(locator)

    def click_element(self, locator):
        """
        Click on element (waits for clickable).

        Args:
            locator (tuple): Locator strategy and value
        """
        self.utils.click(locator)

    def enter_text(self, locator, text):
        """
        Clear field and enter text.

        Args:
            locator (tuple): Locator strategy and value
            text (str): Text to enter
        """
        self.utils.clear_and_send_keys(locator, text)

    def get_element_text(self, locator):
        """
        Get text from element.

        Args:
            locator (tuple): Locator strategy and value

        Returns:
            str: Element text
        """
        return self.utils.get_text(locator)

    def is_element_displayed(self, locator):
        """
        Check if element is displayed.

        Args:
            locator (tuple): Locator strategy and value

        Returns:
            bool: True if displayed, False otherwise
        """
        return self.utils.is_element_visible(locator)

    def wait_for_element(self, locator, timeout=20):
        """
        Wait for element to be visible.

        Args:
            locator (tuple): Locator strategy and value
            timeout (int): Wait timeout in seconds

        Returns:
            WebElement: Found element
        """
        return self.utils.wait_for_element(locator, timeout)

    def take_screenshot(self, name):
        """
        Take a screenshot.

        Args:
            name (str): Screenshot name prefix

        Returns:
            str: Screenshot file path
        """
        return self.utils.take_screenshot(name)

    # ==================== GESTURE SHORTCUTS ====================

    def swipe_up(self, duration=800):
        """Swipe up on screen (scrolls content down)."""
        self.gestures.swipe_up(duration)

    def swipe_down(self, duration=800):
        """Swipe down on screen (scrolls content up)."""
        self.gestures.swipe_down(duration)

    def swipe_left(self, duration=800):
        """Swipe left on screen."""
        self.gestures.swipe_left(duration)

    def swipe_right(self, duration=800):
        """Swipe right on screen."""
        self.gestures.swipe_right(duration)

    def scroll_to_element(self, locator, max_scrolls=10, direction='up'):
        """
        Scroll until element is visible.

        Args:
            locator (tuple): Locator strategy and value
            max_scrolls (int): Maximum scroll attempts
            direction (str): 'up' or 'down'

        Returns:
            WebElement or None: Found element or None
        """
        return self.gestures.scroll_to_element(locator, max_scrolls, direction)

    def long_press(self, element, duration=1000):
        """
        Long press on an element.

        Args:
            element: WebElement to long press
            duration (int): Duration in milliseconds
        """
        self.gestures.long_press(element, duration)

    def drag_and_drop(self, source_element, target_element, duration=1000):
        """
        Drag source element to target element.

        Args:
            source_element: Source WebElement
            target_element: Target WebElement
            duration (int): Duration in milliseconds
        """
        self.gestures.drag_and_drop(source_element, target_element, duration)

    def zoom_in(self, element, spread=150):
        """
        Zoom in (two-finger spread) on element.

        Args:
            element: WebElement to zoom
            spread (int): Pixel spread per finger
        """
        self.gestures.zoom_in(element, spread)

    def zoom_out(self, element, spread=150):
        """
        Zoom out (two-finger pinch) on element.

        Args:
            element: WebElement to zoom
            spread (int): Starting pixel spread per finger
        """
        self.gestures.zoom_out(element, spread)

    # ==================== APP MANAGEMENT (Appium 2.x) ====================

    def activate_app(self, app_id):
        """
        Activate an app (bring to foreground).
        Replaces deprecated launch_app().

        Args:
            app_id (str): Bundle ID (iOS) or package name (Android)
        """
        self.utils.activate_app(app_id)

    def terminate_app(self, app_id):
        """
        Terminate a running app.
        Replaces deprecated close_app().

        Args:
            app_id (str): Bundle ID (iOS) or package name (Android)
        """
        self.utils.terminate_app(app_id)

    def query_app_state(self, app_id):
        """
        Query the lifecycle state of an app (0–4).

        Args:
            app_id (str): Bundle ID or package name

        Returns:
            int: App state code
        """
        return self.utils.query_app_state(app_id)

    # ==================== CLIPBOARD ====================

    def set_clipboard_text(self, text):
        """
        Set text to the device clipboard.

        Args:
            text (str): Text to copy
        """
        self.utils.set_clipboard_text(text)

    def get_clipboard_text(self):
        """
        Get text from the device clipboard.

        Returns:
            str: Clipboard text
        """
        return self.utils.get_clipboard_text()

    # ==================== MOBILE EXECUTE ====================

    def execute_mobile(self, command, params=None):
        """
        Execute a mobile: script command (Appium 2.x).

        Args:
            command (str): Command name without 'mobile: ' prefix
            params (dict): Command parameters

        Returns:
            Any: Command result
        """
        return self.utils.execute_mobile(command, params)
