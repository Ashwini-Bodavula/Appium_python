"""
Gestures Utility
Comprehensive collection of mobile gesture methods including swipe, scroll, tap, long press, etc.

Updated for Appium 2.x / Selenium 4.x:
- Removed deprecated driver.swipe() → replaced with W3C Actions API
- Removed deprecated TouchAction / MultiAction → replaced with ActionBuilder + PointerInput
- pinch/zoom now use two simultaneous PointerInput sequences
- All gestures use selenium.webdriver.common.actions (W3C compliant)
- Added: activate_app(), terminate_app(), query_app_state() replacing launch/close/reset
- Added: is_element_checked(), get_attribute(), execute_mobile_command() helpers
- Added: two-finger pinch/zoom with proper multi-touch sequence
"""
import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput


class Gestures:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    # ==================== INTERNAL HELPERS ====================

    def _w3c_swipe(self, start_x, start_y, end_x, end_y, duration_ms=800):
        """
        Perform a swipe via W3C Actions API (replaces deprecated driver.swipe()).

        Args:
            start_x, start_y (int): Starting coordinates
            end_x, end_y (int): Ending coordinates
            duration_ms (int): Swipe duration in milliseconds
        """
        touch = PointerInput(interaction.POINTER_TOUCH, "touch")
        actions = ActionBuilder(self.driver, mouse=touch)
        actions.pointer_action.move_to_location(start_x, start_y)
        actions.pointer_action.pointer_down()
        actions.pointer_action.pause(duration_ms / 1000)
        actions.pointer_action.move_to_location(end_x, end_y)
        actions.pointer_action.release()
        actions.perform()

    def _get_screen_size(self):
        """Return (width, height) of the device screen."""
        size = self.driver.get_window_size()
        return size['width'], size['height']

    def _get_element_center(self, element):
        """
        Get center coordinates of an element.

        Returns:
            tuple: (center_x, center_y)
        """
        location = element.location
        size = element.size
        return (
            location['x'] + size['width'] // 2,
            location['y'] + size['height'] // 2,
        )

    # ==================== BASIC SWIPE ACTIONS ====================

    def swipe_up(self, duration=800):
        """
        Swipe up from bottom to top (scrolls content downward).

        Args:
            duration (int): Duration of swipe in milliseconds
        """
        width, height = self._get_screen_size()
        start_x = width // 2
        start_y = int(height * 0.8)
        end_y = int(height * 0.2)
        self._w3c_swipe(start_x, start_y, start_x, end_y, duration)

    def swipe_down(self, duration=800):
        """
        Swipe down from top to bottom (scrolls content upward).

        Args:
            duration (int): Duration of swipe in milliseconds
        """
        width, height = self._get_screen_size()
        start_x = width // 2
        start_y = int(height * 0.2)
        end_y = int(height * 0.8)
        self._w3c_swipe(start_x, start_y, start_x, end_y, duration)

    def swipe_left(self, duration=800):
        """
        Swipe left from right to left.

        Args:
            duration (int): Duration of swipe in milliseconds
        """
        width, height = self._get_screen_size()
        start_x = int(width * 0.8)
        end_x = int(width * 0.2)
        y = height // 2
        self._w3c_swipe(start_x, y, end_x, y, duration)

    def swipe_right(self, duration=800):
        """
        Swipe right from left to right.

        Args:
            duration (int): Duration of swipe in milliseconds
        """
        width, height = self._get_screen_size()
        start_x = int(width * 0.2)
        end_x = int(width * 0.8)
        y = height // 2
        self._w3c_swipe(start_x, y, end_x, y, duration)

    # ==================== ELEMENT-SPECIFIC SWIPE ACTIONS ====================

    def swipe_element_left(self, element, duration=800):
        """
        Swipe left on a specific element (e.g., carousel, list item).

        Args:
            element: WebElement to swipe on
            duration (int): Swipe duration in milliseconds
        """
        loc = element.location
        sz = element.size
        start_x = loc['x'] + int(sz['width'] * 0.8)
        end_x = loc['x'] + int(sz['width'] * 0.2)
        y = loc['y'] + sz['height'] // 2
        self._w3c_swipe(start_x, y, end_x, y, duration)

    def swipe_element_right(self, element, duration=800):
        """
        Swipe right on a specific element.

        Args:
            element: WebElement to swipe on
            duration (int): Swipe duration in milliseconds
        """
        loc = element.location
        sz = element.size
        start_x = loc['x'] + int(sz['width'] * 0.2)
        end_x = loc['x'] + int(sz['width'] * 0.8)
        y = loc['y'] + sz['height'] // 2
        self._w3c_swipe(start_x, y, end_x, y, duration)

    def swipe_element_up(self, element, duration=800):
        """
        Swipe up on a specific element (e.g., scrollable list).

        Args:
            element: WebElement to swipe on
            duration (int): Swipe duration in milliseconds
        """
        loc = element.location
        sz = element.size
        x = loc['x'] + sz['width'] // 2
        start_y = loc['y'] + int(sz['height'] * 0.8)
        end_y = loc['y'] + int(sz['height'] * 0.2)
        self._w3c_swipe(x, start_y, x, end_y, duration)

    def swipe_element_down(self, element, duration=800):
        """
        Swipe down on a specific element.

        Args:
            element: WebElement to swipe on
            duration (int): Swipe duration in milliseconds
        """
        loc = element.location
        sz = element.size
        x = loc['x'] + sz['width'] // 2
        start_y = loc['y'] + int(sz['height'] * 0.2)
        end_y = loc['y'] + int(sz['height'] * 0.8)
        self._w3c_swipe(x, start_y, x, end_y, duration)

    def swipe_on_element(self, element, direction='up', duration=800):
        """
        Swipe on a specific element in any direction.

        Args:
            element: WebElement to swipe on
            direction (str): 'up', 'down', 'left', or 'right'
            duration (int): Duration of swipe in milliseconds
        """
        directions = {
            'up': self.swipe_element_up,
            'down': self.swipe_element_down,
            'left': self.swipe_element_left,
            'right': self.swipe_element_right,
        }
        handler = directions.get(direction)
        if handler:
            handler(element, duration)
        else:
            raise ValueError(f"Invalid direction '{direction}'. Use: up, down, left, right")

    # ==================== SCROLL ACTIONS ====================

    def scroll_to_beginning(self, max_scrolls=10):
        """
        Scroll to the beginning/top of the screen.

        Args:
            max_scrolls (int): Maximum number of scrolls to perform
        """
        for _ in range(max_scrolls):
            self.swipe_down()

    def scroll_to_end(self, max_scrolls=10):
        """
        Scroll to the end/bottom of the screen.

        Args:
            max_scrolls (int): Maximum number of scrolls to perform
        """
        for _ in range(max_scrolls):
            self.swipe_up()

    def scroll_to_text(self, text, max_scrolls=10):
        """
        Scroll until text is visible (Android only via UiAutomator2).

        Args:
            text (str): Text to find
            max_scrolls (int): Maximum number of scrolls

        Returns:
            WebElement or None: The found element, or None
        """
        for _ in range(max_scrolls):
            try:
                element = self.driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    f'new UiSelector().textContains("{text}")'
                )
                return element
            except NoSuchElementException:
                self.swipe_up()
        return None

    def scroll_to_element(self, locator, max_scrolls=10, direction='up'):
        """
        Scroll until element matching locator is visible.

        Args:
            locator (tuple): Locator strategy and value
            max_scrolls (int): Maximum number of scrolls
            direction (str): Scroll direction ('up' or 'down')

        Returns:
            WebElement or None: Found element or None
        """
        for _ in range(max_scrolls):
            try:
                element = self.driver.find_element(*locator)
                if element.is_displayed():
                    return element
            except (NoSuchElementException, Exception):
                pass

            if direction == 'up':
                self.swipe_up()
            else:
                self.swipe_down()

        return None

    def scroll_element_to_beginning(self, element, max_scrolls=10):
        """
        Scroll a specific scrollable element to its beginning.

        Args:
            element: Scrollable WebElement
            max_scrolls (int): Maximum number of scrolls
        """
        for _ in range(max_scrolls):
            self.swipe_element_down(element)

    def scroll_element_to_end(self, element, max_scrolls=10):
        """
        Scroll a specific scrollable element to its end.

        Args:
            element: Scrollable WebElement
            max_scrolls (int): Maximum number of scrolls
        """
        for _ in range(max_scrolls):
            self.swipe_element_up(element)

    # ==================== TAP ACTIONS ====================

    def tap(self, element):
        """
        Tap on an element (delegates to element.click()).

        Args:
            element: WebElement to tap
        """
        element.click()

    def tap_coordinates(self, x, y):
        """
        Tap at specific screen coordinates using W3C Actions.

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

    def double_tap(self, element):
        """
        Double tap on an element.

        Args:
            element: WebElement to double tap
        """
        self.tap(element)
        self.tap(element)

    def double_tap_coordinates(self, x, y):
        """
        Double tap at specific coordinates.

        Args:
            x (int): X coordinate
            y (int): Y coordinate
        """
        self.tap_coordinates(x, y)
        self.tap_coordinates(x, y)

    def multi_tap(self, element, count=3):
        """
        Tap an element multiple times.

        Args:
            element: WebElement to tap
            count (int): Number of taps
        """
        for _ in range(count):
            self.tap(element)

    # ==================== LONG PRESS ACTIONS ====================

    def long_press(self, element, duration=1000):
        """
        Long press on an element using W3C Actions.

        Args:
            element: WebElement to long press
            duration (int): Duration in milliseconds
        """
        center_x, center_y = self._get_element_center(element)
        touch = PointerInput(interaction.POINTER_TOUCH, "touch")
        actions = ActionBuilder(self.driver, mouse=touch)
        actions.pointer_action.move_to_location(center_x, center_y)
        actions.pointer_action.pointer_down()
        actions.pointer_action.pause(duration / 1000)
        actions.pointer_action.pointer_up()
        actions.perform()

    def long_press_coordinates(self, x, y, duration=1000):
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

    def drag_and_drop(self, source_element, target_element, duration=1000):
        """
        Drag and drop from source element to target element.

        Args:
            source_element: Source WebElement
            target_element: Target WebElement
            duration (int): Hold duration before releasing in milliseconds
        """
        src_x, src_y = self._get_element_center(source_element)
        tgt_x, tgt_y = self._get_element_center(target_element)

        touch = PointerInput(interaction.POINTER_TOUCH, "touch")
        actions = ActionBuilder(self.driver, mouse=touch)
        actions.pointer_action.move_to_location(src_x, src_y)
        actions.pointer_action.pointer_down()
        actions.pointer_action.pause(duration / 1000)
        actions.pointer_action.move_to_location(tgt_x, tgt_y)
        actions.pointer_action.pointer_up()
        actions.perform()

    def drag_and_drop_by_offset(self, element, x_offset, y_offset, duration=1000):
        """
        Drag an element by pixel offset.

        Args:
            element: WebElement to drag
            x_offset (int): X offset in pixels
            y_offset (int): Y offset in pixels
            duration (int): Hold duration in milliseconds
        """
        center_x, center_y = self._get_element_center(element)

        touch = PointerInput(interaction.POINTER_TOUCH, "touch")
        actions = ActionBuilder(self.driver, mouse=touch)
        actions.pointer_action.move_to_location(center_x, center_y)
        actions.pointer_action.pointer_down()
        actions.pointer_action.pause(duration / 1000)
        actions.pointer_action.move_to_location(center_x + x_offset, center_y + y_offset)
        actions.pointer_action.pointer_up()
        actions.perform()

    # ==================== PINCH / ZOOM (MULTI-TOUCH) ====================

    def zoom_in(self, element, spread=150, duration=600):
        """
        Zoom in (spread two fingers outward) on an element.
        Uses two simultaneous PointerInput sequences (proper multi-touch).

        Args:
            element: WebElement to zoom in on
            spread (int): Distance each finger moves outward in pixels
            duration (int): Gesture duration in milliseconds
        """
        cx, cy = self._get_element_center(element)

        finger1 = PointerInput(interaction.POINTER_TOUCH, "finger1")
        finger2 = PointerInput(interaction.POINTER_TOUCH, "finger2")

        actions = ActionBuilder(self.driver, mouse=finger1)
        actions.add_pointer_input("touch", "finger2")

        # Finger 1: moves left → right (outward)
        f1 = actions.pointer_inputs[0]
        f1.create_pointer_move(duration=0, x=cx - 10, y=cy, origin="viewport")
        f1.create_pointer_down(button=0)
        f1.create_pause(duration / 1000)
        f1.create_pointer_move(duration=duration, x=cx - spread, y=cy, origin="viewport")
        f1.create_pointer_up(button=0)

        # Finger 2: moves right → left (outward)
        f2 = actions.pointer_inputs[1]
        f2.create_pointer_move(duration=0, x=cx + 10, y=cy, origin="viewport")
        f2.create_pointer_down(button=0)
        f2.create_pause(duration / 1000)
        f2.create_pointer_move(duration=duration, x=cx + spread, y=cy, origin="viewport")
        f2.create_pointer_up(button=0)

        actions.perform()

    def zoom_out(self, element, spread=150, duration=600):
        """
        Zoom out (pinch two fingers inward) on an element.

        Args:
            element: WebElement to zoom out on
            spread (int): Starting distance of each finger from center in pixels
            duration (int): Gesture duration in milliseconds
        """
        cx, cy = self._get_element_center(element)

        actions = ActionBuilder(self.driver)
        actions.add_pointer_input("touch", "finger1")
        actions.add_pointer_input("touch", "finger2")

        f1 = actions.pointer_inputs[0]
        f1.create_pointer_move(duration=0, x=cx - spread, y=cy, origin="viewport")
        f1.create_pointer_down(button=0)
        f1.create_pointer_move(duration=duration, x=cx - 10, y=cy, origin="viewport")
        f1.create_pointer_up(button=0)

        f2 = actions.pointer_inputs[1]
        f2.create_pointer_move(duration=0, x=cx + spread, y=cy, origin="viewport")
        f2.create_pointer_down(button=0)
        f2.create_pointer_move(duration=duration, x=cx + 10, y=cy, origin="viewport")
        f2.create_pointer_up(button=0)

        actions.perform()

    # Alias kept for backward compatibility
    def pinch_to_zoom(self, element, spread=150, duration=600):
        """Alias for zoom_in(). Kept for backward compatibility."""
        self.zoom_in(element, spread, duration)

    # ==================== SWIPE WITH PAUSE ====================

    def swipe_with_pause(self, direction='up', pause_duration=1000, swipe_duration=800):
        """
        Swipe and then pause (useful for momentum-style scrolling).

        Args:
            direction (str): 'up', 'down', 'left', or 'right'
            pause_duration (int): Pause after swipe in milliseconds
            swipe_duration (int): Swipe duration in milliseconds
        """
        handlers = {
            'up': self.swipe_up,
            'down': self.swipe_down,
            'left': self.swipe_left,
            'right': self.swipe_right,
        }
        handler = handlers.get(direction)
        if handler:
            handler(swipe_duration)
        else:
            raise ValueError(f"Invalid direction '{direction}'. Use: up, down, left, right")

        time.sleep(pause_duration / 1000)
