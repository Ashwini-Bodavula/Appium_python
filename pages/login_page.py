"""
Login Page Object
Contains all elements and methods for Login screen
"""
from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy


class LoginPage(BasePage):
    # Locators - Update these based on your app
    USERNAME_FIELD = (AppiumBy.ID, "com.example.app:id/username")
    PASSWORD_FIELD = (AppiumBy.ID, "com.example.app:id/password")
    LOGIN_BUTTON = (AppiumBy.ID, "com.example.app:id/loginButton")
    ERROR_MESSAGE = (AppiumBy.ID, "com.example.app:id/errorMessage")
    FORGOT_PASSWORD = (AppiumBy.XPATH, "//android.widget.TextView[@text='Forgot Password?']")
    SIGNUP_LINK = (AppiumBy.ACCESSIBILITY_ID, "signUpLink")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def enter_username(self, username):
        """
        Enter username
        
        Args:
            username (str): Username to enter
        """
        self.enter_text(self.USERNAME_FIELD, username)
    
    def enter_password(self, password):
        """
        Enter password
        
        Args:
            password (str): Password to enter
        """
        self.enter_text(self.PASSWORD_FIELD, password)
    
    def click_login_button(self):
        """Click login button"""
        self.click_element(self.LOGIN_BUTTON)
    
    def login(self, username, password):
        """
        Perform complete login action
        
        Args:
            username (str): Username
            password (str): Password
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
    
    def is_error_message_displayed(self):
        """
        Check if error message is displayed
        
        Returns:
            bool: True if error displayed
        """
        return self.is_element_displayed(self.ERROR_MESSAGE)
    
    def get_error_message(self):
        """
        Get error message text
        
        Returns:
            str: Error message
        """
        return self.get_element_text(self.ERROR_MESSAGE)
    
    def click_forgot_password(self):
        """Click forgot password link"""
        self.click_element(self.FORGOT_PASSWORD)
    
    def click_signup_link(self):
        """Click signup link"""
        self.click_element(self.SIGNUP_LINK)
    
    def is_login_button_enabled(self):
        """
        Check if login button is enabled
        
        Returns:
            bool: True if enabled
        """
        element = self.find_element(self.LOGIN_BUTTON)
        return element.is_enabled()
