"""
Sample Page Object
Example page object demonstrating the framework structure
Replace this with your actual app page objects
"""
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class SamplePage(BasePage):
    
    # ==================== LOCATORS ====================
    # Replace these with your actual app locators
    
    # Example Android locators
    USERNAME_INPUT = (AppiumBy.ID, "com.example.app:id/username")
    PASSWORD_INPUT = (AppiumBy.ID, "com.example.app:id/password")
    LOGIN_BUTTON = (AppiumBy.ID, "com.example.app:id/login_button")
    WELCOME_TEXT = (AppiumBy.ID, "com.example.app:id/welcome_message")
    
    # Example using XPATH
    SUBMIT_BTN = (AppiumBy.XPATH, "//android.widget.Button[@text='Submit']")
    
    # Example using Accessibility ID
    SETTINGS_ICON = (AppiumBy.ACCESSIBILITY_ID, "Settings")
    
    # Example using Class Name
    TEXT_VIEWS = (AppiumBy.CLASS_NAME, "android.widget.TextView")
    
    # ==================== PAGE ACTIONS ====================
    
    def enter_username(self, username):
        """
        Enter username in the username field
        
        Args:
            username (str): Username to enter
        """
        self.send_keys(self.USERNAME_INPUT, username)
    
    def enter_password(self, password):
        """
        Enter password in the password field
        
        Args:
            password (str): Password to enter
        """
        self.send_keys(self.PASSWORD_INPUT, password)
    
    def click_login(self):
        """Click the login button"""
        self.click(self.LOGIN_BUTTON)
    
    def perform_login(self, username, password):
        """
        Complete login action
        
        Args:
            username (str): Username
            password (str): Password
        """
        self.enter_username(username)
        self.enter_password(password)
        self.hide_keyboard()
        self.click_login()
    
    def get_welcome_message(self):
        """
        Get welcome message text
        
        Returns:
            str: Welcome message
        """
        return self.get_text(self.WELCOME_TEXT)
    
    def is_login_button_displayed(self):
        """
        Check if login button is displayed
        
        Returns:
            bool: True if displayed, False otherwise
        """
        return self.is_element_displayed(self.LOGIN_BUTTON)
    
    # ==================== GESTURE EXAMPLES ====================
    
    def swipe_to_settings(self):
        """Example: Swipe left to navigate to settings"""
        self.swipe_left()
    
    def scroll_to_item(self, item_text):
        """
        Example: Scroll to find an item
        
        Args:
            item_text (str): Text of the item to find
            
        Returns:
            WebElement: Found element or None
        """
        return self.scroll_to_element(item_text)
    
    def long_press_item(self, item_text):
        """
        Example: Long press on an item
        
        Args:
            item_text (str): Text of the item
        """
        element = self.scroll_to_element(item_text)
        if element:
            self.gesture.long_press(element)
