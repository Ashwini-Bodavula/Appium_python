"""
File Operations Utility
Handles file upload, download validation, and file assertions
"""
import os
import time
import hashlib
from pathlib import Path


class FileOperations:
    def __init__(self, driver):
        self.driver = driver
        self.download_dir = self._get_download_directory()
        self.upload_dir = self._get_upload_directory()
    
    def _get_download_directory(self):
        """
        Get default download directory path
        
        Returns:
            str: Download directory path
        """
        # Default download paths for different platforms
        downloads = os.path.join(os.path.expanduser('~'), 'Downloads')
        
        # Create if doesn't exist
        os.makedirs(downloads, exist_ok=True)
        return downloads
    
    def _get_upload_directory(self):
        """
        Get upload test files directory
        
        Returns:
            str: Upload directory path
        """
        upload_dir = os.path.join(
            os.path.dirname(__file__), 
            '..', 
            'test_data', 
            'upload_files'
        )
        os.makedirs(upload_dir, exist_ok=True)
        return upload_dir
    
    def set_download_directory(self, directory):
        """
        Set custom download directory
        
        Args:
            directory (str): Path to download directory
        """
        os.makedirs(directory, exist_ok=True)
        self.download_dir = directory
    
    def set_upload_directory(self, directory):
        """
        Set custom upload directory
        
        Args:
            directory (str): Path to upload directory
        """
        self.upload_dir = directory
    
    def push_file_to_device(self, local_file_path, device_path):
        """
        Push file to device (Android)
        
        Args:
            local_file_path (str): Local file path
            device_path (str): Device destination path
            
        Returns:
            bool: True if successful
        """
        try:
            with open(local_file_path, 'rb') as file:
                data = file.read()
            
            self.driver.push_file(device_path, data)
            return True
        except Exception as e:
            print(f"Error pushing file to device: {str(e)}")
            return False
    
    def pull_file_from_device(self, device_path, local_destination=None):
        """
        Pull file from device (Android)
        
        Args:
            device_path (str): Device file path
            local_destination (str): Local destination path (optional)
            
        Returns:
            str: Local file path or None if failed
        """
        try:
            data = self.driver.pull_file(device_path)
            
            if local_destination is None:
                local_destination = os.path.join(
                    self.download_dir, 
                    os.path.basename(device_path)
                )
            
            with open(local_destination, 'wb') as file:
                file.write(data)
            
            return local_destination
        except Exception as e:
            print(f"Error pulling file from device: {str(e)}")
            return None
    
    def upload_file(self, file_name, upload_element_locator=None):
        """
        Upload file to app
        
        Args:
            file_name (str): Name of file in upload_files directory
            upload_element_locator (tuple): Locator for upload element
            
        Returns:
            str: Path of uploaded file
        """
        file_path = os.path.join(self.upload_dir, file_name)
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Upload file not found: {file_path}")
        
        # For Android: Push file to device
        device_path = f"/sdcard/Download/{file_name}"
        self.push_file_to_device(file_path, device_path)
        
        # If upload element provided, interact with it
        if upload_element_locator:
            element = self.driver.find_element(*upload_element_locator)
            element.send_keys(file_path)
        
        return file_path
    
    def wait_for_file_download(self, file_name, timeout=30, partial_match=False):
        """
        Wait for file to be downloaded
        
        Args:
            file_name (str): Expected file name
            timeout (int): Wait timeout in seconds
            partial_match (bool): Match partial file name
            
        Returns:
            str: Downloaded file path or None
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            files = os.listdir(self.download_dir)
            
            for file in files:
                # Skip temporary download files
                if file.endswith('.crdownload') or file.endswith('.tmp'):
                    continue
                
                if partial_match:
                    if file_name in file:
                        return os.path.join(self.download_dir, file)
                else:
                    if file == file_name:
                        return os.path.join(self.download_dir, file)
            
            time.sleep(1)
        
        return None
    
    def is_file_downloaded(self, file_name, timeout=10):
        """
        Check if file is downloaded
        
        Args:
            file_name (str): File name to check
            timeout (int): Wait timeout
            
        Returns:
            bool: True if file exists
        """
        file_path = self.wait_for_file_download(file_name, timeout)
        return file_path is not None
    
    def get_downloaded_file_path(self, file_name):
        """
        Get full path of downloaded file
        
        Args:
            file_name (str): File name
            
        Returns:
            str: Full file path or None
        """
        file_path = os.path.join(self.download_dir, file_name)
        return file_path if os.path.exists(file_path) else None
    
    def delete_downloaded_file(self, file_name):
        """
        Delete downloaded file
        
        Args:
            file_name (str): File name to delete
            
        Returns:
            bool: True if deleted successfully
        """
        file_path = os.path.join(self.download_dir, file_name)
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            print(f"Error deleting file: {str(e)}")
            return False
    
    def cleanup_downloads(self):
        """
        Clean up all files in download directory
        """
        try:
            files = os.listdir(self.download_dir)
            for file in files:
                file_path = os.path.join(self.download_dir, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        except Exception as e:
            print(f"Error cleaning up downloads: {str(e)}")
    
    def get_file_size(self, file_path):
        """
        Get file size in bytes
        
        Args:
            file_path (str): Path to file
            
        Returns:
            int: File size in bytes or None
        """
        try:
            return os.path.getsize(file_path)
        except Exception as e:
            print(f"Error getting file size: {str(e)}")
            return None
    
    def get_file_extension(self, file_path):
        """
        Get file extension
        
        Args:
            file_path (str): Path to file
            
        Returns:
            str: File extension
        """
        return os.path.splitext(file_path)[1]
    
    def calculate_file_hash(self, file_path, algorithm='md5'):
        """
        Calculate file hash
        
        Args:
            file_path (str): Path to file
            algorithm (str): Hash algorithm (md5, sha1, sha256)
            
        Returns:
            str: File hash or None
        """
        try:
            hash_func = hashlib.new(algorithm)
            
            with open(file_path, 'rb') as file:
                while chunk := file.read(8192):
                    hash_func.update(chunk)
            
            return hash_func.hexdigest()
        except Exception as e:
            print(f"Error calculating file hash: {str(e)}")
            return None
    
    def compare_files(self, file1_path, file2_path):
        """
        Compare two files by content
        
        Args:
            file1_path (str): First file path
            file2_path (str): Second file path
            
        Returns:
            bool: True if files are identical
        """
        hash1 = self.calculate_file_hash(file1_path)
        hash2 = self.calculate_file_hash(file2_path)
        
        return hash1 == hash2 if hash1 and hash2 else False
    
    def read_file_content(self, file_path, encoding='utf-8'):
        """
        Read file content as text
        
        Args:
            file_path (str): Path to file
            encoding (str): File encoding
            
        Returns:
            str: File content or None
        """
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        except Exception as e:
            print(f"Error reading file: {str(e)}")
            return None
    
    def read_file_lines(self, file_path, encoding='utf-8'):
        """
        Read file content as list of lines
        
        Args:
            file_path (str): Path to file
            encoding (str): File encoding
            
        Returns:
            list: List of lines or None
        """
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.readlines()
        except Exception as e:
            print(f"Error reading file lines: {str(e)}")
            return None
    
    def get_latest_downloaded_file(self):
        """
        Get the most recently downloaded file
        
        Returns:
            str: Path to latest file or None
        """
        try:
            files = [
                os.path.join(self.download_dir, f) 
                for f in os.listdir(self.download_dir)
                if os.path.isfile(os.path.join(self.download_dir, f))
                and not f.endswith(('.crdownload', '.tmp'))
            ]
            
            if not files:
                return None
            
            # Sort by modification time
            latest_file = max(files, key=os.path.getmtime)
            return latest_file
        except Exception as e:
            print(f"Error getting latest file: {str(e)}")
            return None
    
    def count_files_in_downloads(self, extension=None):
        """
        Count files in download directory
        
        Args:
            extension (str): Filter by extension (e.g., '.pdf')
            
        Returns:
            int: Number of files
        """
        try:
            files = os.listdir(self.download_dir)
            
            if extension:
                files = [f for f in files if f.endswith(extension)]
            
            # Exclude temporary files
            files = [
                f for f in files 
                if not f.endswith(('.crdownload', '.tmp'))
            ]
            
            return len(files)
        except Exception as e:
            print(f"Error counting files: {str(e)}")
            return 0
