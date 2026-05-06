"""
Gestures and Navigation Tests
Demonstrates usage of gestures and navigation utilities
"""
import pytest
from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy


@pytest.mark.regression
@pytest.mark.platform('android')
class TestGesturesAndNavigation:
    
    def test_swipe_gestures(self, setup):
        """Test various swipe gestures"""
        driver = setup
        base_page = BasePage(driver)
        
        # Swipe up
        base_page.swipe_up()
        
        # Swipe down
        base_page.swipe_down()
        
        # Swipe left
        base_page.swipe_left()
        
        # Swipe right
        base_page.swipe_right()
    
    def test_scroll_to_element(self, setup):
        """Test scrolling to find an element"""
        driver = setup
        base_page = BasePage(driver)
        
        # Example: Scroll to find a specific element
        # Update locator based on your app
        target_locator = (AppiumBy.XPATH, "//android.widget.TextView[@text='Target Element']")
        
        element = base_page.scroll_to_element(target_locator, max_scrolls=5)
        
        if element:
            assert element.is_displayed(), "Element not visible after scrolling"
        else:
            pytest.skip("Target element not found in view")
    
    def test_long_press(self, setup):
        """Test long press gesture"""
        driver = setup
        base_page = BasePage(driver)
        
        # Find element to long press
        # Update locator based on your app
        element_locator = (AppiumBy.ID, "com.example.app:id/longPressItem")
        
        element = base_page.find_element(element_locator)
        
        # Perform long press
        base_page.long_press(element, duration=2000)
        
        # Verify long press action (e.g., context menu appeared)
        # Add appropriate assertion
    
    def test_app_navigation(self, setup):
        """Test app navigation utilities"""
        driver = setup
        base_page = BasePage(driver)
        
        # Get current activity
        current_activity = base_page.utils.get_current_activity()
        print(f"Current activity: {current_activity}")
        
        # Background app
        base_page.utils.background_app(3)  # still valid in Appium 2.x
        
        # Verify app is active again
        assert driver.current_activity is not None
    
    def test_keyboard_operations(self, setup):
        """Test keyboard operations"""
        driver = setup
        base_page = BasePage(driver)
        
        # Find input field and enter text
        input_locator = (AppiumBy.ID, "com.example.app:id/searchField")
        base_page.enter_text(input_locator, "Test search")
        
        # Check if keyboard is shown
        is_keyboard_visible = base_page.utils.is_keyboard_shown()
        print(f"Keyboard visible: {is_keyboard_visible}")
        
        # Hide keyboard
        base_page.utils.hide_keyboard()
        
        # Verify keyboard is hidden
        # Add appropriate assertion
    
    def test_screenshot_capture(self, setup):
        """Test screenshot capture functionality"""
        driver = setup
        base_page = BasePage(driver)
        
        # Take screenshot
        screenshot_path = base_page.take_screenshot("test_screenshot")
        
        # Verify screenshot was saved
        import os
        assert os.path.exists(screenshot_path), "Screenshot not saved"
        print(f"Screenshot saved at: {screenshot_path}")
    
    @pytest.mark.skip(reason="Demonstrates element-specific swipe")
    def test_swipe_on_element(self, setup):
        """Test swiping on a specific element (like carousel)"""
        driver = setup
        
        # Find carousel or scrollable element
        carousel_locator = (AppiumBy.ID, "com.example.app:id/carousel")
        carousel_element = driver.find_element(*carousel_locator)
        
        # Use gestures utility directly
        from utilities.gestures import Gestures
        gestures = Gestures(driver)
        
        # Swipe left on carousel
        gestures.swipe_on_element(carousel_element, direction='left')
        
        # Swipe right on carousel
        gestures.swipe_on_element(carousel_element, direction='right')
