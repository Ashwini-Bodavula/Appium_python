"""
Driver Factory
Manages Appium driver initialization and teardown

Updated for Appium 2.x:
- Replaced deprecated desired_caps dict with AppiumOptions
- appium.webdriver.Remote requires options= kwarg (not positional desired_capabilities)
- Appium 2.x server base URL: http://127.0.0.1:4723 (no /wd/hub suffix needed)
"""
from appium import webdriver
from appium.options import AppiumOptions
from utilities.config_reader import ConfigReader


class DriverFactory:
    def __init__(self):
        self.driver = None
        self.config_reader = ConfigReader()

    def get_driver(self, platform='android'):
        """
        Initialize and return Appium driver using AppiumOptions (Appium 2.x)

        Args:
            platform (str): 'android' or 'ios'

        Returns:
            webdriver.Remote: Appium WebDriver instance
        """
        appium_server = self.config_reader.get_appium_server()

        if platform.lower() == 'android':
            caps_dict = self.config_reader.get_android_config()
        elif platform.lower() == 'ios':
            caps_dict = self.config_reader.get_ios_config()
        else:
            raise ValueError(f"Unsupported platform: {platform}")

        # Appium 2.x: Use AppiumOptions instead of raw desired_caps dict
        options = AppiumOptions()
        options.load_capabilities(caps_dict)

        self.driver = webdriver.Remote(appium_server, options=options)
        self.driver.implicitly_wait(self.config_reader.get_implicit_wait())

        return self.driver

    def quit_driver(self):
        """Quit the driver session"""
        if self.driver:
            self.driver.quit()
            self.driver = None
