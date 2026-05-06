"""
Pages Package
Contains all Page Object Model classes
"""
from .base_page import BasePage
from .login_page import LoginPage
from .home_page import HomePage

__all__ = ['BasePage', 'LoginPage', 'HomePage']
