"""
Assertion Utility
Provides comprehensive assertion methods for validations
"""
import os
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Assertions:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
    
    # ==================== Element Assertions ====================
    
    def assert_element_visible(self, locator, message=None):
        """
        Assert element is visible
        
        Args:
            locator (tuple): Element locator
            message (str): Custom assertion message
        """
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            assert element.is_displayed(), message or f"Element {locator} is not visible"
        except Exception as e:
            raise AssertionError(message or f"Element {locator} is not visible: {str(e)}")
    
    def assert_element_not_visible(self, locator, timeout=5, message=None):
        """
        Assert element is not visible
        
        Args:
            locator (tuple): Element locator
            timeout (int): Wait timeout
            message (str): Custom assertion message
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.invisibility_of_element_located(locator))
        except:
            raise AssertionError(message or f"Element {locator} is still visible")
    
    def assert_element_present(self, locator, message=None):
        """
        Assert element is present in DOM
        
        Args:
            locator (tuple): Element locator
            message (str): Custom assertion message
        """
        try:
            self.wait.until(EC.presence_of_element_located(locator))
        except Exception as e:
            raise AssertionError(message or f"Element {locator} is not present: {str(e)}")
    
    def assert_element_clickable(self, locator, message=None):
        """
        Assert element is clickable
        
        Args:
            locator (tuple): Element locator
            message (str): Custom assertion message
        """
        try:
            self.wait.until(EC.element_to_be_clickable(locator))
        except Exception as e:
            raise AssertionError(message or f"Element {locator} is not clickable: {str(e)}")
    
    def assert_element_enabled(self, locator, message=None):
        """
        Assert element is enabled
        
        Args:
            locator (tuple): Element locator
            message (str): Custom assertion message
        """
        element = self.driver.find_element(*locator)
        assert element.is_enabled(), message or f"Element {locator} is not enabled"
    
    def assert_element_disabled(self, locator, message=None):
        """
        Assert element is disabled
        
        Args:
            locator (tuple): Element locator
            message (str): Custom assertion message
        """
        element = self.driver.find_element(*locator)
        assert not element.is_enabled(), message or f"Element {locator} is not disabled"
    
    def assert_element_selected(self, locator, message=None):
        """
        Assert element is selected (checkboxes, radio buttons)
        
        Args:
            locator (tuple): Element locator
            message (str): Custom assertion message
        """
        element = self.driver.find_element(*locator)
        assert element.is_selected(), message or f"Element {locator} is not selected"
    
    def assert_element_not_selected(self, locator, message=None):
        """
        Assert element is not selected
        
        Args:
            locator (tuple): Element locator
            message (str): Custom assertion message
        """
        element = self.driver.find_element(*locator)
        assert not element.is_selected(), message or f"Element {locator} is selected"
    
    # ==================== Text Assertions ====================
    
    def assert_text_equals(self, locator, expected_text, message=None):
        """
        Assert element text equals expected text
        
        Args:
            locator (tuple): Element locator
            expected_text (str): Expected text
            message (str): Custom assertion message
        """
        element = self.driver.find_element(*locator)
        actual_text = element.text
        assert actual_text == expected_text, \
            message or f"Expected text '{expected_text}', but got '{actual_text}'"
    
    def assert_text_contains(self, locator, expected_text, message=None):
        """
        Assert element text contains expected text
        
        Args:
            locator (tuple): Element locator
            expected_text (str): Expected text substring
            message (str): Custom assertion message
        """
        element = self.driver.find_element(*locator)
        actual_text = element.text
        assert expected_text in actual_text, \
            message or f"Expected text '{expected_text}' not found in '{actual_text}'"
    
    def assert_text_not_contains(self, locator, unexpected_text, message=None):
        """
        Assert element text does not contain specified text
        
        Args:
            locator (tuple): Element locator
            unexpected_text (str): Text that should not be present
            message (str): Custom assertion message
        """
        element = self.driver.find_element(*locator)
        actual_text = element.text
        assert unexpected_text not in actual_text, \
            message or f"Unexpected text '{unexpected_text}' found in '{actual_text}'"
    
    def assert_text_matches_pattern(self, locator, pattern, message=None):
        """
        Assert element text matches regex pattern
        
        Args:
            locator (tuple): Element locator
            pattern (str): Regex pattern
            message (str): Custom assertion message
        """
        element = self.driver.find_element(*locator)
        actual_text = element.text
        assert re.match(pattern, actual_text), \
            message or f"Text '{actual_text}' does not match pattern '{pattern}'"
    
    def assert_text_starts_with(self, locator, prefix, message=None):
        """
        Assert element text starts with specified prefix
        
        Args:
            locator (tuple): Element locator
            prefix (str): Expected prefix
            message (str): Custom assertion message
        """
        element = self.driver.find_element(*locator)
        actual_text = element.text
        assert actual_text.startswith(prefix), \
            message or f"Text '{actual_text}' does not start with '{prefix}'"
    
    def assert_text_ends_with(self, locator, suffix, message=None):
        """
        Assert element text ends with specified suffix
        
        Args:
            locator (tuple): Element locator
            suffix (str): Expected suffix
            message (str): Custom assertion message
        """
        element = self.driver.find_element(*locator)
        actual_text = element.text
        assert actual_text.endswith(suffix), \
            message or f"Text '{actual_text}' does not end with '{suffix}'"
    
    def assert_text_empty(self, locator, message=None):
        """
        Assert element text is empty
        
        Args:
            locator (tuple): Element locator
            message (str): Custom assertion message
        """
        element = self.driver.find_element(*locator)
        actual_text = element.text
        assert actual_text == "", \
            message or f"Expected empty text, but got '{actual_text}'"
    
    def assert_text_not_empty(self, locator, message=None):
        """
        Assert element text is not empty
        
        Args:
            locator (tuple): Element locator
            message (str): Custom assertion message
        """
        element = self.driver.find_element(*locator)
        actual_text = element.text
        assert actual_text != "", \
            message or "Expected non-empty text, but got empty string"
    
    # ==================== Attribute Assertions ====================
    
    def assert_attribute_equals(self, locator, attribute, expected_value, message=None):
        """
        Assert element attribute equals expected value
        
        Args:
            locator (tuple): Element locator
            attribute (str): Attribute name
            expected_value (str): Expected value
            message (str): Custom assertion message
        """
        element = self.driver.find_element(*locator)
        actual_value = element.get_attribute(attribute)
        assert actual_value == expected_value, \
            message or f"Expected attribute '{attribute}' to be '{expected_value}', but got '{actual_value}'"
    
    def assert_attribute_contains(self, locator, attribute, expected_value, message=None):
        """
        Assert element attribute contains expected value
        
        Args:
            locator (tuple): Element locator
            attribute (str): Attribute name
            expected_value (str): Expected value substring
            message (str): Custom assertion message
        """
        element = self.driver.find_element(*locator)
        actual_value = element.get_attribute(attribute)
        assert expected_value in actual_value, \
            message or f"Attribute '{attribute}' value '{actual_value}' does not contain '{expected_value}'"
    
    def assert_attribute_present(self, locator, attribute, message=None):
        """
        Assert element has specified attribute
        
        Args:
            locator (tuple): Element locator
            attribute (str): Attribute name
            message (str): Custom assertion message
        """
        element = self.driver.find_element(*locator)
        value = element.get_attribute(attribute)
        assert value is not None, \
            message or f"Attribute '{attribute}' is not present"
    
    # ==================== Count Assertions ====================
    
    def assert_element_count(self, locator, expected_count, message=None):
        """
        Assert number of elements matching locator
        
        Args:
            locator (tuple): Element locator
            expected_count (int): Expected count
            message (str): Custom assertion message
        """
        elements = self.driver.find_elements(*locator)
        actual_count = len(elements)
        assert actual_count == expected_count, \
            message or f"Expected {expected_count} elements, but found {actual_count}"
    
    def assert_element_count_greater_than(self, locator, count, message=None):
        """
        Assert number of elements is greater than specified count
        
        Args:
            locator (tuple): Element locator
            count (int): Minimum count
            message (str): Custom assertion message
        """
        elements = self.driver.find_elements(*locator)
        actual_count = len(elements)
        assert actual_count > count, \
            message or f"Expected more than {count} elements, but found {actual_count}"
    
    def assert_element_count_less_than(self, locator, count, message=None):
        """
        Assert number of elements is less than specified count
        
        Args:
            locator (tuple): Element locator
            count (int): Maximum count
            message (str): Custom assertion message
        """
        elements = self.driver.find_elements(*locator)
        actual_count = len(elements)
        assert actual_count < count, \
            message or f"Expected less than {count} elements, but found {actual_count}"
    
    # ==================== File Assertions ====================
    
    def assert_file_exists(self, file_path, message=None):
        """
        Assert file exists
        
        Args:
            file_path (str): Path to file
            message (str): Custom assertion message
        """
        assert os.path.exists(file_path), \
            message or f"File does not exist: {file_path}"
    
    def assert_file_not_exists(self, file_path, message=None):
        """
        Assert file does not exist
        
        Args:
            file_path (str): Path to file
            message (str): Custom assertion message
        """
        assert not os.path.exists(file_path), \
            message or f"File exists but should not: {file_path}"
    
    def assert_file_size(self, file_path, expected_size, message=None):
        """
        Assert file size equals expected size
        
        Args:
            file_path (str): Path to file
            expected_size (int): Expected size in bytes
            message (str): Custom assertion message
        """
        actual_size = os.path.getsize(file_path)
        assert actual_size == expected_size, \
            message or f"Expected file size {expected_size} bytes, but got {actual_size} bytes"
    
    def assert_file_size_greater_than(self, file_path, size, message=None):
        """
        Assert file size is greater than specified size
        
        Args:
            file_path (str): Path to file
            size (int): Minimum size in bytes
            message (str): Custom assertion message
        """
        actual_size = os.path.getsize(file_path)
        assert actual_size > size, \
            message or f"Expected file size > {size} bytes, but got {actual_size} bytes"
    
    def assert_file_size_less_than(self, file_path, size, message=None):
        """
        Assert file size is less than specified size
        
        Args:
            file_path (str): Path to file
            size (int): Maximum size in bytes
            message (str): Custom assertion message
        """
        actual_size = os.path.getsize(file_path)
        assert actual_size < size, \
            message or f"Expected file size < {size} bytes, but got {actual_size} bytes"
    
    def assert_file_extension(self, file_path, expected_extension, message=None):
        """
        Assert file has expected extension
        
        Args:
            file_path (str): Path to file
            expected_extension (str): Expected extension (e.g., '.pdf')
            message (str): Custom assertion message
        """
        actual_extension = os.path.splitext(file_path)[1]
        assert actual_extension == expected_extension, \
            message or f"Expected extension '{expected_extension}', but got '{actual_extension}'"
    
    def assert_file_content_contains(self, file_path, expected_content, message=None):
        """
        Assert file content contains expected text
        
        Args:
            file_path (str): Path to file
            expected_content (str): Expected content substring
            message (str): Custom assertion message
        """
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
        
        assert expected_content in content, \
            message or f"File content does not contain '{expected_content}'"
    
    def assert_file_content_matches_pattern(self, file_path, pattern, message=None):
        """
        Assert file content matches regex pattern
        
        Args:
            file_path (str): Path to file
            pattern (str): Regex pattern
            message (str): Custom assertion message
        """
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
        
        assert re.search(pattern, content), \
            message or f"File content does not match pattern '{pattern}'"
    
    def assert_files_equal(self, file1_path, file2_path, message=None):
        """
        Assert two files have identical content
        
        Args:
            file1_path (str): First file path
            file2_path (str): Second file path
            message (str): Custom assertion message
        """
        import hashlib
        
        def file_hash(path):
            hash_md5 = hashlib.md5()
            with open(path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        
        hash1 = file_hash(file1_path)
        hash2 = file_hash(file2_path)
        
        assert hash1 == hash2, \
            message or f"Files are not identical: {file1_path} and {file2_path}"
    
    # ==================== URL Assertions ====================
    
    def assert_current_activity(self, expected_activity, message=None):
        """
        Assert current activity (Android)
        
        Args:
            expected_activity (str): Expected activity name
            message (str): Custom assertion message
        """
        actual_activity = self.driver.current_activity
        assert actual_activity == expected_activity, \
            message or f"Expected activity '{expected_activity}', but got '{actual_activity}'"
    
    def assert_current_package(self, expected_package, message=None):
        """
        Assert current package (Android)
        
        Args:
            expected_package (str): Expected package name
            message (str): Custom assertion message
        """
        actual_package = self.driver.current_package
        assert actual_package == expected_package, \
            message or f"Expected package '{expected_package}', but got '{actual_package}'"
    
    # ==================== List/Collection Assertions ====================
    
    def assert_list_contains(self, items_list, expected_item, message=None):
        """
        Assert list contains expected item
        
        Args:
            items_list (list): List to check
            expected_item: Expected item
            message (str): Custom assertion message
        """
        assert expected_item in items_list, \
            message or f"Item '{expected_item}' not found in list"
    
    def assert_list_not_contains(self, items_list, unexpected_item, message=None):
        """
        Assert list does not contain item
        
        Args:
            items_list (list): List to check
            unexpected_item: Item that should not be present
            message (str): Custom assertion message
        """
        assert unexpected_item not in items_list, \
            message or f"Item '{unexpected_item}' found in list but should not be present"
    
    def assert_list_length(self, items_list, expected_length, message=None):
        """
        Assert list has expected length
        
        Args:
            items_list (list): List to check
            expected_length (int): Expected length
            message (str): Custom assertion message
        """
        actual_length = len(items_list)
        assert actual_length == expected_length, \
            message or f"Expected list length {expected_length}, but got {actual_length}"
    
    def assert_list_empty(self, items_list, message=None):
        """
        Assert list is empty
        
        Args:
            items_list (list): List to check
            message (str): Custom assertion message
        """
        assert len(items_list) == 0, \
            message or f"Expected empty list, but got {len(items_list)} items"
    
    def assert_list_not_empty(self, items_list, message=None):
        """
        Assert list is not empty
        
        Args:
            items_list (list): List to check
            message (str): Custom assertion message
        """
        assert len(items_list) > 0, \
            message or "Expected non-empty list, but got empty list"
    
    # ==================== Boolean Assertions ====================
    
    def assert_true(self, condition, message=None):
        """
        Assert condition is True
        
        Args:
            condition (bool): Condition to check
            message (str): Custom assertion message
        """
        assert condition is True, message or "Expected True, but got False"
    
    def assert_false(self, condition, message=None):
        """
        Assert condition is False
        
        Args:
            condition (bool): Condition to check
            message (str): Custom assertion message
        """
        assert condition is False, message or "Expected False, but got True"
    
    # ==================== Numeric Assertions ====================
    
    def assert_equals(self, actual, expected, message=None):
        """
        Assert actual equals expected
        
        Args:
            actual: Actual value
            expected: Expected value
            message (str): Custom assertion message
        """
        assert actual == expected, \
            message or f"Expected {expected}, but got {actual}"
    
    def assert_not_equals(self, actual, unexpected, message=None):
        """
        Assert actual does not equal unexpected value
        
        Args:
            actual: Actual value
            unexpected: Value that should not match
            message (str): Custom assertion message
        """
        assert actual != unexpected, \
            message or f"Expected value different from {unexpected}, but got {actual}"
    
    def assert_greater_than(self, actual, value, message=None):
        """
        Assert actual is greater than value
        
        Args:
            actual: Actual value
            value: Comparison value
            message (str): Custom assertion message
        """
        assert actual > value, \
            message or f"Expected value > {value}, but got {actual}"
    
    def assert_less_than(self, actual, value, message=None):
        """
        Assert actual is less than value
        
        Args:
            actual: Actual value
            value: Comparison value
            message (str): Custom assertion message
        """
        assert actual < value, \
            message or f"Expected value < {value}, but got {actual}"
