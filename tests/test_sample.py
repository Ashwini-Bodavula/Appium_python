"""
Sample Test
Example test demonstrating framework usage
Replace this with your actual test cases
"""
import pytest
from pages.sample_page import SamplePage


class TestSampleLogin:
    """Sample test class for login functionality"""
    
    def test_login_successful(self, driver, test_data):
        """
        Test successful login
        
        Args:
            driver: Appium driver instance (from fixture)
            test_data: Test data dictionary (from fixture)
        """
        # Initialize page object
        sample_page = SamplePage(driver)
        
        # Perform login
        sample_page.perform_login(
            test_data["valid_username"],
            test_data["valid_password"]
        )
        
        # Verify login success
        welcome_msg = sample_page.get_welcome_message()
        assert "Welcome" in welcome_msg, "Login failed - Welcome message not found"
    
    def test_login_button_displayed(self, driver):
        """
        Test that login button is displayed
        
        Args:
            driver: Appium driver instance
        """
        sample_page = SamplePage(driver)
        
        assert sample_page.is_login_button_displayed(), "Login button not displayed"
    
    @pytest.mark.skip(reason="Demo test - skip in actual run")
    def test_gesture_example(self, driver):
        """
        Example test demonstrating gesture utilities
        
        Args:
            driver: Appium driver instance
        """
        sample_page = SamplePage(driver)
        
        # Swipe examples
        sample_page.swipe_up()
        sample_page.swipe_down()
        sample_page.swipe_left()
        sample_page.swipe_right()
        
        # Scroll to element
        element = sample_page.scroll_to_item("Settings")
        assert element is not None, "Settings element not found"
        
        # Long press
        sample_page.long_press_item("Settings")


class TestSampleNavigation:
    """Sample test class for navigation"""
    
    @pytest.mark.skip(reason="Demo test - replace with actual tests")
    def test_navigate_to_settings(self, driver):
        """
        Example navigation test
        
        Args:
            driver: Appium driver instance
        """
        sample_page = SamplePage(driver)
        
        # Navigate using swipe
        sample_page.swipe_to_settings()
        
        # Verify navigation (add your assertions here)
        # assert sample_page.is_settings_page_displayed()
    
    @pytest.mark.skip(reason="Demo test - replace with actual tests")
    def test_back_navigation(self, driver):
        """
        Example back navigation test
        
        Args:
            driver: Appium driver instance
        """
        sample_page = SamplePage(driver)
        
        # Navigate to another page
        sample_page.swipe_left()
        
        # Navigate back
        sample_page.go_back()
        
        # Verify back to original page
        assert sample_page.is_login_button_displayed()


# Example of parameterized test
@pytest.mark.parametrize("username,password,expected", [
    ("user1", "pass1", True),
    ("user2", "pass2", True),
    ("", "", False),
])
@pytest.mark.skip(reason="Demo test - replace with actual tests")
def test_login_with_multiple_credentials(driver, username, password, expected):
    """
    Example parameterized test
    
    Args:
        driver: Appium driver instance
        username: Username to test
        password: Password to test
        expected: Expected result (True for success, False for failure)
    """
    sample_page = SamplePage(driver)
    sample_page.perform_login(username, password)
    
    if expected:
        assert sample_page.get_welcome_message() is not None
    else:
        # Add error message verification here
        pass
