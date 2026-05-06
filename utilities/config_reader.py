"""
Configuration Reader Utility
Reads configuration from config.ini file
"""
import configparser
import os


class ConfigReader:
    def __init__(self):
        self.config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(__file__), '..', 'configs', 'config.ini')
        self.config.read(config_path)

    def get_android_config(self):
        """
        Get Android capabilities as a W3C-compatible dict.
        AppiumOptions.load_capabilities() will auto-prefix non-standard keys with 'appium:'.
        """
        return {
            'platformName': self.config.get('ANDROID', 'platformName'),
            'appium:platformVersion': self.config.get('ANDROID', 'platformVersion'),
            'appium:deviceName': self.config.get('ANDROID', 'deviceName'),
            'appium:automationName': self.config.get('ANDROID', 'automationName'),
            'appium:appPackage': self.config.get('ANDROID', 'appPackage'),
            'appium:appActivity': self.config.get('ANDROID', 'appActivity'),
            'appium:noReset': self.config.getboolean('ANDROID', 'noReset'),
            'appium:fullReset': self.config.getboolean('ANDROID', 'fullReset'),
        }

    def get_ios_config(self):
        """
        Get iOS capabilities as a W3C-compatible dict.
        AppiumOptions.load_capabilities() will auto-prefix non-standard keys with 'appium:'.
        """
        return {
            'platformName': self.config.get('IOS', 'platformName'),
            'appium:platformVersion': self.config.get('IOS', 'platformVersion'),
            'appium:deviceName': self.config.get('IOS', 'deviceName'),
            'appium:automationName': self.config.get('IOS', 'automationName'),
            'appium:bundleId': self.config.get('IOS', 'bundleId'),
            'appium:noReset': self.config.getboolean('IOS', 'noReset'),
            'appium:fullReset': self.config.getboolean('IOS', 'fullReset'),
        }

    def get_appium_server(self):
        """Get Appium server URL"""
        return self.config.get('APPIUM', 'appium_server')

    def get_implicit_wait(self):
        """Get implicit wait timeout"""
        return self.config.getint('TIMEOUTS', 'implicit_wait')

    def get_explicit_wait(self):
        """Get explicit wait timeout"""
        return self.config.getint('TIMEOUTS', 'explicit_wait')
