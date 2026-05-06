"""
Home Page Object
Contains all elements and methods for Home screen
"""
from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy


class HomePage(BasePage):
    # Locators - Update these based on your app
    WELCOME_MESSAGE = (AppiumBy.ID, "com.example.app:id/welcomeText")
    PROFILE_ICON = (AppiumBy.ID, "com.example.app:id/profileIcon")
    MENU_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "menuButton")
    LOGOUT_BUTTON = (AppiumBy.XPATH, "//android.widget.Button[@text='Logout']")
    SETTINGS_ICON = (AppiumBy.ID, "com.example.app:id/settingsIcon")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def is_home_page_displayed(self):
        """
        Check if home page is displayed
        
        Returns:
            bool: True if displayed
        """
        return self.is_element_displayed(self.WELCOME_MESSAGE)
    
    def get_welcome_message(self):
        """
        Get welcome message text
        
        Returns:
            str: Welcome message
        """
        return self.get_element_text(self.WELCOME_MESSAGE)
    
    def click_profile_icon(self):
        """Click on profile icon"""
        self.click_element(self.PROFILE_ICON)
    
    def click_menu_button(self):
        """Click on menu button"""
        self.click_element(self.MENU_BUTTON)
    
    def click_settings(self):
        """Click on settings icon"""
        self.click_element(self.SETTINGS_ICON)
    
    def logout(self):
        """Perform logout action"""
        self.click_menu_button()
        self.click_element(self.LOGOUT_BUTTON)
