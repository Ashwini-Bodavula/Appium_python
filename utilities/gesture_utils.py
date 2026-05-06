"""
Gesture Utilities (GestureUtils)
Reusable standalone gesture helpers for mobile automation.
"""
import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from utilities.config_reader import ConfigReader

config_reader = ConfigReader()


class GestureUtils:

    def __init__(self, driver):
        self.driver = driver
        self.wait_timeout = config_reader.get_explicit_wait()

    # ==================== INTERNAL HELPERS ====================

    def _w3c_swipe(self, start_x, start_y, end_x, end_y, duration_ms=800):
        """
        Perform a swipe via W3C Actions API.
        Replaces deprecated driver.swipe() which was removed in Appium 2.x.
        """
        touch = PointerInput(interaction.POINTER_TOUCH, "touch")
        actions = ActionBuilder(self.driver, mouse=touch)
        actions.pointer_action.move_to_location(start_x, start_y)
        actions.pointer_action.pointer_down()
        actions.pointer_action.pause(duration_ms / 1000)
        actions.pointer_action.move_to_location(end_x, end_y)
        actions.pointer_action.release()
        actions.perform()

    # ==================== SWIPE ACTIONS ====================

    def swipe_up(self, duration=800):
        """Swipe up from bottom to top (scroll down)."""
        size = self.driver.get_window_size()
        start_x = size['width'] // 2
        start_y = int(size['height'] * 0.8)
        end_y = int(size['height'] * 0.2)
        self._w3c_swipe(start_x, start_y, start_x, end_y, duration)

    def swipe_down(self, duration=800):
        """Swipe down from top to bottom (scroll up)."""
        size = self.driver.get_window_size()
        start_x = size['width'] // 2
        start_y = int(size['height'] * 0.2)
        end_y = int(size['height'] * 0.8)
        self._w3c_swipe(start_x, start_y, start_x, end_y, duration)

    def swipe_left(self, duration=800):
        """Swipe left (navigate to next screen)."""
        size = self.driver.get_window_size()
        start_x = int(size['width'] * 0.8)
        end_x = int(size['width'] * 0.2)
        y = size['height'] // 2
        self._w3c_swipe(start_x, y, end_x, y, duration)

    def swipe_right(self, duration=800):
        """Swipe right (navigate to previous screen)."""
        size = self.driver.get_window_size()
        start_x = int(size['width'] * 0.2)
        end_x = int(size['width'] * 0.8)
        y = size['height'] // 2
        self._w3c_swipe(start_x, y, end_x, y, duration)

    def swipe_element_left(self, element, duration=800):
        """Swipe left on a specific element."""
        loc = element.location
        sz = element.size
        start_x = loc['x'] + int(sz['width'] * 0.8)
        end_x = loc['x'] + int(sz['width'] * 0.2)
        y = loc['y'] + sz['height'] // 2
        self._w3c_swipe(start_x, y, end_x, y, duration)

    def swipe_element_right(self, element, duration=800):
        """Swipe right on a specific element."""
        loc = element.location
        sz = element.size
        start_x = loc['x'] + int(sz['width'] * 0.2)
        end_x = loc['x'] + int(sz['width'] * 0.8)
        y = loc['y'] + sz['height'] // 2
        self._w3c_swipe(start_x, y, end_x, y, duration)

    # ==================== SCROLL ACTIONS ====================

    def scroll_to_element(self, element_text, max_scrolls=10):
        """
        Scroll until element with matching text is found.

        Args:
            element_text (str): Text of the element to find
            max_scrolls (int): Maximum number of scrolls to attempt

        Returns:
            WebElement or None
        """
        for _ in range(max_scrolls):
            try:
                element = self.driver.find_element(
                    AppiumBy.XPATH,
                    f"//*[@text='{element_text}' or @content-desc='{element_text}']"
                )
                return element
            except Exception:
                self.swipe_up()
        return None

    def scroll_to_end(self, max_scrolls=20):
        """Scroll to the end of the screen (detects when page source stops changing)."""
        previous_source = ""
        for _ in range(max_scrolls):
            current_source = self.driver.page_source
            if current_source == previous_source:
                break
            previous_source = current_source
            self.swipe_up()

    def scroll_to_beginning(self, max_scrolls=20):
        """Scroll to the beginning/top of the screen."""
        for _ in range(max_scrolls):
            self.swipe_down()

    # ==================== TAP ACTIONS ====================

    def tap_by_coordinates(self, x, y):
        """
        Tap at specific coordinates using W3C Actions.

        Args:
            x (int): X coordinate
            y (int): Y coordinate
        """
        touch = PointerInput(interaction.POINTER_TOUCH, "touch")
        actions = ActionBuilder(self.driver, mouse=touch)
        actions.pointer_action.move_to_location(x, y)
        actions.pointer_action.pointer_down()
        actions.pointer_action.pointer_up()
        actions.perform()

    def tap_element(self, element):
        """
        Tap at the center of a WebElement.

        Args:
            element: WebElement to tap
        """
        loc = element.location
        sz = element.size
        x = loc['x'] + sz['width'] // 2
        y = loc['y'] + sz['height'] // 2
        self.tap_by_coordinates(x, y)

    def double_tap(self, element):
        """Double tap on an element."""
        self.tap_element(element)
        self.tap_element(element)

    # ==================== LONG PRESS ACTIONS ====================

    def long_press(self, element, duration=2000):
        """
        Long press on an element using W3C Actions.

        Args:
            element: WebElement to long press
            duration (int): Duration in milliseconds
        """
        loc = element.location
        sz = element.size
        x = loc['x'] + sz['width'] // 2
        y = loc['y'] + sz['height'] // 2

        touch = PointerInput(interaction.POINTER_TOUCH, "touch")
        actions = ActionBuilder(self.driver, mouse=touch)
        actions.pointer_action.move_to_location(x, y)
        actions.pointer_action.pointer_down()
        actions.pointer_action.pause(duration / 1000)
        actions.pointer_action.pointer_up()
        actions.perform()

    def long_press_by_coordinates(self, x, y, duration=2000):
        """
        Long press at specific coordinates.

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            duration (int): Duration in milliseconds
        """
        touch = PointerInput(interaction.POINTER_TOUCH, "touch")
        actions = ActionBuilder(self.driver, mouse=touch)
        actions.pointer_action.move_to_location(x, y)
        actions.pointer_action.pointer_down()
        actions.pointer_action.pause(duration / 1000)
        actions.pointer_action.pointer_up()
        actions.perform()

    # ==================== DRAG AND DROP ====================

    def drag_and_drop(self, source_element, target_element, duration=800):
        """
        Drag element from source to target.

        Args:
            source_element: Source WebElement
            target_element: Target WebElement
            duration (int): Duration in milliseconds
        """
        src_loc = source_element.location
        src_sz = source_element.size
        start_x = src_loc['x'] + src_sz['width'] // 2
        start_y = src_loc['y'] + src_sz['height'] // 2

        tgt_loc = target_element.location
        tgt_sz = target_element.size
        end_x = tgt_loc['x'] + tgt_sz['width'] // 2
        end_y = tgt_loc['y'] + tgt_sz['height'] // 2

        self._w3c_swipe(start_x, start_y, end_x, end_y, duration)

    # ==================== NAVIGATION ====================

    def navigate_back(self):
        """Navigate back (Android hardware back / iOS swipe back)."""
        self.driver.back()

    def navigate_forward(self):
        """Navigate forward (if applicable)."""
        self.driver.forward()

    def press_home(self):
        """
        Press the Home button.
        Uses execute_script with mobile: pressKey (Appium 2.x UiAutomator2).
        Falls back to keycode 3 for older setups.
        """
        try:
            self.driver.execute_script('mobile: pressKey', {'keycode': 3})
        except Exception:
            self.driver.press_keycode(3)  # KEYCODE_HOME fallback

    def press_enter(self):
        """
        Press the Enter/Return key.
        Uses execute_script with mobile: pressKey (Appium 2.x UiAutomator2).
        """
        try:
            self.driver.execute_script('mobile: pressKey', {'keycode': 66})
        except Exception:
            self.driver.press_keycode(66)  # KEYCODE_ENTER fallback

    def press_keycode(self, keycode, metastate=None):
        """
        Press any Android keycode.

        Args:
            keycode (int): Android keycode
            metastate (int, optional): Meta state flags
        """
        params = {'keycode': keycode}
        if metastate is not None:
            params['metastate'] = metastate
        try:
            self.driver.execute_script('mobile: pressKey', params)
        except Exception:
            self.driver.press_keycode(keycode, metastate=metastate)

    def hide_keyboard(self):
        """Hide keyboard if visible."""
        try:
            self.driver.hide_keyboard()
        except Exception:
            pass

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
        Query the current state of an app.
        Returns: 0=not installed, 1=not running, 2=background-suspended,
                 3=background-running, 4=foreground.

        Args:
            app_id (str): Bundle ID (iOS) or package name (Android)

        Returns:
            int: App state
        """
        return self.driver.query_app_state(app_id)

    def background_app(self, seconds):
        """
        Put app in background for specified seconds.

        Args:
            seconds (int): Number of seconds
        """
        self.driver.background_app(seconds)

    def install_app(self, app_path):
        """
        Install an application from path.

        Args:
            app_path (str): Path to .apk or .ipa file
        """
        self.driver.install_app(app_path)

    def remove_app(self, app_id):
        """
        Remove/uninstall an application.

        Args:
            app_id (str): Bundle ID (iOS) or package name (Android)
        """
        self.driver.remove_app(app_id)

    def is_app_installed(self, app_id):
        """
        Check if an app is installed.

        Args:
            app_id (str): Bundle ID or package name

        Returns:
            bool: True if installed
        """
        return self.driver.is_app_installed(app_id)

    # ==================== CLIPBOARD ====================

    def set_clipboard(self, text):
        """
        Set text content to device clipboard.

        Args:
            text (str): Text to set
        """
        self.driver.set_clipboard_text(text)

    def get_clipboard(self):
        """
        Get text content from device clipboard.

        Returns:
            str: Clipboard text
        """
        return self.driver.get_clipboard_text()

    # ==================== WAIT UTILITIES ====================

    def wait_for_element(self, locator, timeout=None):
        """
        Wait for element to be visible.

        Args:
            locator (tuple): Locator tuple (By, value)
            timeout (int): Custom timeout in seconds

        Returns:
            WebElement: Found element
        """
        t = timeout if timeout is not None else self.wait_timeout
        return WebDriverWait(self.driver, t).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_element_clickable(self, locator, timeout=None):
        """
        Wait for element to be clickable.

        Args:
            locator (tuple): Locator tuple (By, value)
            timeout (int): Custom timeout in seconds

        Returns:
            WebElement: Found element
        """
        t = timeout if timeout is not None else self.wait_timeout
        return WebDriverWait(self.driver, t).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_for_element_invisible(self, locator, timeout=None):
        """
        Wait for element to become invisible.

        Args:
            locator (tuple): Locator tuple (By, value)
            timeout (int): Custom timeout in seconds

        Returns:
            bool: True when invisible
        """
        t = timeout if timeout is not None else self.wait_timeout
        return WebDriverWait(self.driver, t).until(
            EC.invisibility_of_element_located(locator)
        )

    def is_element_present(self, locator, timeout=5):
        """
        Check if element is present in the DOM.

        Args:
            locator (tuple): Locator tuple (By, value)
            timeout (int): Timeout in seconds

        Returns:
            bool: True if present
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    # ==================== SCREENSHOT ====================

    def take_screenshot(self, file_name):
        """
        Take a screenshot and save to file.

        Args:
            file_name (str): File path for the screenshot
        """
        self.driver.save_screenshot(file_name)
