"""
Login Tests
Contains test cases for login functionality
"""
import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage


@pytest.mark.smoke
@pytest.mark.login
@pytest.mark.platform('android')
class TestLogin:
    
    def test_successful_login(self, setup):
        """Test successful login with valid credentials"""
        driver = setup
        
        # Initialize page objects
        login_page = LoginPage(driver)
        home_page = HomePage(driver)
        
        # Perform login
        login_page.login("testuser", "testpass123")
        
        # Verify home page is displayed
        assert home_page.is_home_page_displayed(), "Home page not displayed after login"
        
        # Verify welcome message
        welcome_msg = home_page.get_welcome_message()
        assert "Welcome" in welcome_msg, f"Unexpected welcome message: {welcome_msg}"
    
    @pytest.mark.regression
    def test_login_with_invalid_credentials(self, setup):
        """Test login with invalid credentials"""
        driver = setup
        
        login_page = LoginPage(driver)
        
        # Attempt login with invalid credentials
        login_page.login("invalid_user", "wrong_password")
        
        # Verify error message is displayed
        assert login_page.is_error_message_displayed(), "Error message not displayed"
        
        # Verify error message text
        error_msg = login_page.get_error_message()
        assert "Invalid" in error_msg or "incorrect" in error_msg.lower(), \
            f"Unexpected error message: {error_msg}"
    
    @pytest.mark.regression
    def test_login_with_empty_username(self, setup):
        """Test login with empty username"""
        driver = setup
        
        login_page = LoginPage(driver)
        
        # Enter only password
        login_page.enter_password("testpass123")
        
        # Verify login button is disabled or shows error
        # Adjust assertion based on app behavior
        login_page.click_login_button()
        assert login_page.is_error_message_displayed(), "No error for empty username"
    
    @pytest.mark.regression
    def test_login_with_empty_password(self, setup):
        """Test login with empty password"""
        driver = setup
        
        login_page = LoginPage(driver)
        
        # Enter only username
        login_page.enter_username("testuser")
        
        # Verify login button is disabled or shows error
        login_page.click_login_button()
        assert login_page.is_error_message_displayed(), "No error for empty password"
    
    def test_forgot_password_link(self, setup):
        """Test forgot password functionality"""
        driver = setup
        
        login_page = LoginPage(driver)
        
        # Click forgot password
        login_page.click_forgot_password()
        
        # Verify navigation to forgot password screen
        # Add appropriate assertion based on your app
        # Example: assert forgot_password_page.is_displayed()
    
    def test_signup_link(self, setup):
        """Test signup link navigation"""
        driver = setup
        
        login_page = LoginPage(driver)
        
        # Click signup link
        login_page.click_signup_link()
        
        # Verify navigation to signup screen
        # Add appropriate assertion based on your app
        # Example: assert signup_page.is_displayed()
