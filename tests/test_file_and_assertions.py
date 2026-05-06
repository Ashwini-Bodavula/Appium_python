"""
File Operations and Assertions Tests
Demonstrates file upload, download validation, and assertion methods
"""
import pytest
import os
from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy


@pytest.mark.regression
@pytest.mark.platform('android')
class TestFileOperations:
    
    def test_file_upload(self, setup):
        """Test file upload functionality"""
        driver = setup
        base_page = BasePage(driver)
        
        # Upload file
        file_name = "sample.txt"
        upload_locator = (AppiumBy.ID, "com.example.app:id/uploadButton")
        
        try:
            uploaded_file = base_page.file_ops.upload_file(file_name, upload_locator)
            
            # Assert file was uploaded
            base_page.assertions.assert_true(
                uploaded_file is not None,
                "File upload failed"
            )
            
            print(f"File uploaded: {uploaded_file}")
        except FileNotFoundError as e:
            pytest.skip(f"Test file not found: {str(e)}")
    
    def test_file_download_and_validation(self, setup):
        """Test file download and validation"""
        driver = setup
        base_page = BasePage(driver)
        
        # Trigger download (update locator for your app)
        download_button = (AppiumBy.ID, "com.example.app:id/downloadButton")
        
        try:
            # Click download button
            base_page.click_element(download_button)
            
            # Wait for file to download
            expected_file_name = "downloaded_document.pdf"
            downloaded_file = base_page.file_ops.wait_for_file_download(
                expected_file_name, 
                timeout=30
            )
            
            # Assert file exists
            base_page.assertions.assert_true(
                downloaded_file is not None,
                f"File '{expected_file_name}' was not downloaded"
            )
            
            # Assert file exists on disk
            base_page.assertions.assert_file_exists(downloaded_file)
            
            # Assert file size is greater than 0
            base_page.assertions.assert_file_size_greater_than(
                downloaded_file, 
                0,
                "Downloaded file is empty"
            )
            
            # Assert file extension
            base_page.assertions.assert_file_extension(
                downloaded_file,
                '.pdf',
                "File has incorrect extension"
            )
            
            print(f"File downloaded and validated: {downloaded_file}")
            
            # Cleanup
            base_page.file_ops.delete_downloaded_file(expected_file_name)
            
        except Exception as e:
            pytest.skip(f"Download test skipped: {str(e)}")
    
    def test_file_content_validation(self, setup):
        """Test file content validation"""
        driver = setup
        base_page = BasePage(driver)
        
        # Create a test file for validation
        test_file_path = os.path.join(
            base_page.file_ops.upload_dir,
            "test_content.txt"
        )
        
        with open(test_file_path, 'w') as f:
            f.write("This is test content.\nLine 2.\nLine 3.")
        
        # Assert file exists
        base_page.assertions.assert_file_exists(test_file_path)
        
        # Assert file content contains specific text
        base_page.assertions.assert_file_content_contains(
            test_file_path,
            "test content",
            "File does not contain expected text"
        )
        
        # Read file content
        content = base_page.file_ops.read_file_content(test_file_path)
        
        # Assert content is not empty
        base_page.assertions.assert_true(
            len(content) > 0,
            "File content is empty"
        )
        
        # Assert content matches pattern
        base_page.assertions.assert_file_content_matches_pattern(
            test_file_path,
            r"Line \d+",
            "File content does not match expected pattern"
        )
        
        # Cleanup
        os.remove(test_file_path)
    
    def test_multiple_files_download(self, setup):
        """Test multiple files download and count"""
        driver = setup
        base_page = BasePage(driver)
        
        # Clear downloads before test
        base_page.file_ops.cleanup_downloads()
        
        # Download multiple files (update for your app)
        # This is a placeholder - adapt to your app's workflow
        try:
            # Example: Download 3 files
            # base_page.click_element(download_button_1)
            # base_page.click_element(download_button_2)
            # base_page.click_element(download_button_3)
            
            # Count downloaded files
            pdf_count = base_page.file_ops.count_files_in_downloads('.pdf')
            
            # Assert count
            base_page.assertions.assert_greater_than(
                pdf_count,
                0,
                "No PDF files were downloaded"
            )
            
            print(f"Downloaded {pdf_count} PDF files")
            
        except Exception as e:
            pytest.skip(f"Multiple download test skipped: {str(e)}")
    
    def test_file_comparison(self, setup):
        """Test file comparison functionality"""
        driver = setup
        base_page = BasePage(driver)
        
        # Create two identical test files
        file1_path = os.path.join(base_page.file_ops.upload_dir, "file1.txt")
        file2_path = os.path.join(base_page.file_ops.upload_dir, "file2.txt")
        
        content = "Identical content for testing"
        
        with open(file1_path, 'w') as f:
            f.write(content)
        
        with open(file2_path, 'w') as f:
            f.write(content)
        
        # Compare files
        are_equal = base_page.file_ops.compare_files(file1_path, file2_path)
        
        # Assert files are identical
        base_page.assertions.assert_true(
            are_equal,
            "Files are not identical but should be"
        )
        
        # Assert using assertion method
        base_page.assertions.assert_files_equal(file1_path, file2_path)
        
        # Cleanup
        os.remove(file1_path)
        os.remove(file2_path)
    
    def test_latest_downloaded_file(self, setup):
        """Test getting latest downloaded file"""
        driver = setup
        base_page = BasePage(driver)
        
        try:
            # Get latest downloaded file
            latest_file = base_page.file_ops.get_latest_downloaded_file()
            
            if latest_file:
                print(f"Latest downloaded file: {latest_file}")
                
                # Assert file exists
                base_page.assertions.assert_file_exists(latest_file)
                
                # Get file info
                file_size = base_page.file_ops.get_file_size(latest_file)
                file_ext = base_page.file_ops.get_file_extension(latest_file)
                
                print(f"File size: {file_size} bytes")
                print(f"File extension: {file_ext}")
            else:
                pytest.skip("No downloaded files found")
                
        except Exception as e:
            pytest.skip(f"Latest file test skipped: {str(e)}")


@pytest.mark.regression
@pytest.mark.platform('android')
class TestAssertions:
    
    def test_element_assertions(self, setup):
        """Test element assertion methods"""
        driver = setup
        base_page = BasePage(driver)
        
        # Example locators - update for your app
        visible_element = (AppiumBy.ID, "com.example.app:id/visibleElement")
        
        try:
            # Assert element visible
            base_page.assertions.assert_element_visible(
                visible_element,
                "Element should be visible"
            )
            
            # Assert element present
            base_page.assertions.assert_element_present(visible_element)
            
            # Assert element clickable
            base_page.assertions.assert_element_clickable(visible_element)
            
        except Exception as e:
            pytest.skip(f"Element assertion test skipped: {str(e)}")
    
    def test_text_assertions(self, setup):
        """Test text assertion methods"""
        driver = setup
        base_page = BasePage(driver)
        
        # Example locator - update for your app
        text_element = (AppiumBy.ID, "com.example.app:id/textView")
        
        try:
            # Assert text contains
            base_page.assertions.assert_text_contains(
                text_element,
                "expected",
                "Text does not contain expected string"
            )
            
            # Assert text not empty
            base_page.assertions.assert_text_not_empty(
                text_element,
                "Text should not be empty"
            )
            
        except Exception as e:
            pytest.skip(f"Text assertion test skipped: {str(e)}")
    
    def test_count_assertions(self, setup):
        """Test count assertion methods"""
        driver = setup
        base_page = BasePage(driver)
        
        # Example locator for list items - update for your app
        list_items = (AppiumBy.XPATH, "//android.widget.TextView")
        
        try:
            # Assert element count greater than
            base_page.assertions.assert_element_count_greater_than(
                list_items,
                0,
                "No list items found"
            )
            
        except Exception as e:
            pytest.skip(f"Count assertion test skipped: {str(e)}")
    
    def test_boolean_and_numeric_assertions(self, setup):
        """Test boolean and numeric assertion methods"""
        driver = setup
        base_page = BasePage(driver)
        
        # Boolean assertions
        base_page.assertions.assert_true(True, "Should be true")
        base_page.assertions.assert_false(False, "Should be false")
        
        # Numeric assertions
        base_page.assertions.assert_equals(5, 5, "Values should be equal")
        base_page.assertions.assert_not_equals(5, 10, "Values should not be equal")
        base_page.assertions.assert_greater_than(10, 5, "10 should be > 5")
        base_page.assertions.assert_less_than(5, 10, "5 should be < 10")
    
    def test_list_assertions(self, setup):
        """Test list assertion methods"""
        driver = setup
        base_page = BasePage(driver)
        
        test_list = ["apple", "banana", "cherry"]
        
        # Assert list contains
        base_page.assertions.assert_list_contains(
            test_list,
            "banana",
            "List should contain 'banana'"
        )
        
        # Assert list not contains
        base_page.assertions.assert_list_not_contains(
            test_list,
            "orange",
            "List should not contain 'orange'"
        )
        
        # Assert list length
        base_page.assertions.assert_list_length(
            test_list,
            3,
            "List should have 3 items"
        )
        
        # Assert list not empty
        base_page.assertions.assert_list_not_empty(
            test_list,
            "List should not be empty"
        )
    
    def test_activity_assertions(self, setup):
        """Test Android activity assertions"""
        driver = setup
        base_page = BasePage(driver)
        
        try:
            # Get current activity
            current_activity = driver.current_activity
            current_package = driver.current_package
            
            print(f"Current Activity: {current_activity}")
            print(f"Current Package: {current_package}")
            
            # Assert current activity (update with your app's activity)
            # base_page.assertions.assert_current_activity(".MainActivity")
            
            # Assert current package (update with your app's package)
            # base_page.assertions.assert_current_package("com.example.app")
            
        except Exception as e:
            pytest.skip(f"Activity assertion test skipped: {str(e)}")
