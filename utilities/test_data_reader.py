"""
Test Data Reader
Utility to read test data from JSON files
"""
import json
import os


class TestDataReader:
    def __init__(self, file_name='test_data.json'):
        """
        Initialize test data reader
        
        Args:
            file_name (str): Name of the test data file
        """
        self.data_path = os.path.join(
            os.path.dirname(__file__), 
            '..', 
            'test_data', 
            file_name
        )
        self.data = self._load_data()
    
    def _load_data(self):
        """
        Load test data from JSON file
        
        Returns:
            dict: Test data
        """
        try:
            with open(self.data_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Test data file not found: {self.data_path}")
            return {}
        except json.JSONDecodeError:
            print(f"Invalid JSON in file: {self.data_path}")
            return {}
    
    def get_valid_users(self):
        """
        Get valid user credentials
        
        Returns:
            list: List of valid user data
        """
        return self.data.get('valid_users', [])
    
    def get_invalid_users(self):
        """
        Get invalid user credentials
        
        Returns:
            list: List of invalid user data
        """
        return self.data.get('invalid_users', [])
    
    def get_test_config(self):
        """
        Get test configuration
        
        Returns:
            dict: Test configuration
        """
        return self.data.get('test_config', {})
    
    def get_data_by_key(self, key):
        """
        Get data by specific key
        
        Args:
            key (str): Data key
            
        Returns:
            any: Data value
        """
        return self.data.get(key)


# Usage example:
# data_reader = TestDataReader()
# valid_users = data_reader.get_valid_users()
# for user in valid_users:
#     username = user['username']
#     password = user['password']
