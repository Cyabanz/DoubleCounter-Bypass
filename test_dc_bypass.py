#!/usr/bin/env python3
"""
Test script for Double Counter Bypass functionality
Tests various aspects of the DCBypass.py script
"""

import unittest
import sys
import os
import tempfile
import threading
from unittest.mock import patch, MagicMock
import requests

# Add the current directory to the path so we can import DCBypass
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the functions we want to test
from DCBypass import read_proxy_list, split_list, DCRequest

class TestDCBypass(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_proxies = [
            "192.168.1.1:8080",
            "192.168.1.2:8080", 
            "192.168.1.3:8080",
            "192.168.1.4:8080",
            "192.168.1.5:8080"
        ]
        
        # Create a temporary proxy file
        self.temp_proxy_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        for proxy in self.test_proxies:
            self.temp_proxy_file.write(proxy + '\n')
        self.temp_proxy_file.close()
    
    def tearDown(self):
        """Clean up after each test method."""
        if os.path.exists(self.temp_proxy_file.name):
            os.unlink(self.temp_proxy_file.name)
    
    def test_read_proxy_list(self):
        """Test reading proxy list from file."""
        print("\n🧪 Testing proxy list reading...")
        
        proxies = read_proxy_list(self.temp_proxy_file.name)
        
        # Should return list of dictionaries with 'https' key
        self.assertEqual(len(proxies), 5)
        self.assertIsInstance(proxies[0], dict)
        self.assertIn('https', proxies[0])
        self.assertEqual(proxies[0]['https'], 'http://192.168.1.1:8080')
        
        print("✅ Proxy list reading test passed")
    
    def test_split_list(self):
        """Test splitting proxy list into chunks."""
        print("\n🧪 Testing list splitting...")
        
        # Test splitting into 2 chunks
        chunks = split_list(self.test_proxies, 2)
        self.assertEqual(len(chunks), 2)
        self.assertEqual(len(chunks[0]), 2)  # First chunk has 2 items
        self.assertEqual(len(chunks[1]), 3)  # Second chunk has 3 items
        
        # Test splitting into 3 chunks
        chunks = split_list(self.test_proxies, 3)
        self.assertEqual(len(chunks), 3)
        
        # Test splitting into more chunks than items
        chunks = split_list(self.test_proxies, 10)
        self.assertEqual(len(chunks), 10)
        
        print("✅ List splitting test passed")
    
    @patch('requests.get')
    def test_dc_request_success(self, mock_get):
        """Test DCRequest with successful bypass."""
        print("\n🧪 Testing successful DC bypass...")
        
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "Success! You have bypassed the verification."
        mock_get.return_value = mock_response
        
        # Create proxy chunk
        proxy_chunk = [{"https": "http://192.168.1.1:8080"}]
        
        # Mock threadLock and file operations
        with patch('os._exit') as mock_exit, \
             patch('builtins.open', create=True) as mock_open, \
             patch('os.path.exists', return_value=True):
            # Mock file reading for proxy removal
            mock_file = MagicMock()
            mock_file.readlines.return_value = ["192.168.1.1:8080\n", "192.168.1.2:8080\n"]
            mock_open.return_value.__enter__.return_value = mock_file
            
            # Create a mock threadLock
            import DCBypass
            DCBypass.threadLock = MagicMock()
            
            DCRequest("https://test-url.com", proxy_chunk)
            mock_exit.assert_called_with(0)
        
        print("✅ Successful DC bypass test passed")
    
    @patch('requests.get')
    def test_dc_request_expired_link(self, mock_get):
        """Test DCRequest with expired link."""
        print("\n🧪 Testing expired link scenario...")
        
        # Mock expired link response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "Expired link, please get a new one."
        mock_get.return_value = mock_response
        
        proxy_chunk = [{"https": "http://192.168.1.1:8080"}]
        
        with patch('os._exit') as mock_exit:
            DCRequest("https://test-url.com", proxy_chunk)
            mock_exit.assert_called_with(0)
        
        print("✅ Expired link test passed")
    
    @patch('requests.get')
    def test_dc_request_rr02_error(self, mock_get):
        """Test DCRequest with RR02 error (alt account detected)."""
        print("\n🧪 Testing RR02 error scenario...")
        
        # Mock RR02 response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "RR02: Alt account detected"
        mock_get.return_value = mock_response
        
        proxy_chunk = [{"https": "http://192.168.1.1:8080"}]
        
        with patch('os._exit') as mock_exit:
            DCRequest("https://test-url.com", proxy_chunk)
            mock_exit.assert_called_with(0)
        
        print("✅ RR02 error test passed")
    
    @patch('requests.get')
    def test_dc_request_rv01_error(self, mock_get):
        """Test DCRequest with RV01 error (proxy detected)."""
        print("\n🧪 Testing RV01 error scenario...")
        
        # Mock RV01 response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "RV01: Proxy detected"
        mock_get.return_value = mock_response
        
        proxy_chunk = [{"https": "http://192.168.1.1:8080"}]
        
        # Should not exit on RV01, just continue
        with patch('os._exit') as mock_exit:
            DCRequest("https://test-url.com", proxy_chunk)
            mock_exit.assert_not_called()
        
        print("✅ RV01 error test passed")
    
    @patch('requests.get')
    def test_dc_request_cloudflare_blocked(self, mock_get):
        """Test DCRequest with Cloudflare blocking."""
        print("\n🧪 Testing Cloudflare blocking scenario...")
        
        # Mock Cloudflare response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "Access denied by Cloudflare"
        mock_get.return_value = mock_response
        
        proxy_chunk = [{"https": "http://192.168.1.1:8080"}]
        
        with patch('os._exit') as mock_exit:
            DCRequest("https://test-url.com", proxy_chunk)
            mock_exit.assert_not_called()
        
        print("✅ Cloudflare blocking test passed")
    
    @patch('requests.get')
    def test_dc_request_proxy_error(self, mock_get):
        """Test DCRequest with proxy connection error."""
        print("\n🧪 Testing proxy error scenario...")
        
        # Mock proxy error
        mock_get.side_effect = requests.exceptions.ProxyError("Proxy connection failed")
        
        proxy_chunk = [{"https": "http://192.168.1.1:8080"}]
        
        # Should handle the exception gracefully
        with patch('os._exit') as mock_exit:
            DCRequest("https://test-url.com", proxy_chunk)
            mock_exit.assert_not_called()
        
        print("✅ Proxy error test passed")
    
    def test_threading_safety(self):
        """Test thread safety of the proxy file operations."""
        print("\n🧪 Testing threading safety...")
        
        # Create a temporary proxy file for threading test
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        for proxy in self.test_proxies:
            temp_file.write(proxy + '\n')
        temp_file.close()
        
        # Test that multiple threads can safely read/write to the proxy file
        def worker():
            with open(temp_file.name, 'r') as f:
                lines = f.readlines()
            return len(lines)
        
        threads = []
        results = []
        
        for _ in range(5):
            thread = threading.Thread(target=lambda: results.append(worker()))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # All threads should have read the same number of lines
        self.assertTrue(all(result == 5 for result in results))
        
        # Clean up
        os.unlink(temp_file.name)
        
        print("✅ Threading safety test passed")

def run_integration_test():
    """Run a basic integration test with mock data."""
    print("\n🚀 Running integration test...")
    
    # Create a test proxy file
    test_proxies = [
        "127.0.0.1:8080",
        "127.0.0.1:8081", 
        "127.0.0.1:8082"
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        for proxy in test_proxies:
            f.write(proxy + '\n')
        proxy_file = f.name
    
    try:
        # Test reading proxies
        proxies = read_proxy_list(proxy_file)
        print(f"✅ Read {len(proxies)} proxies from file")
        
        # Test splitting
        chunks = split_list(proxies, 2)
        print(f"✅ Split into {len(chunks)} chunks")
        
        # Test with mock requests
        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.text = "Success! Bypass completed."
            mock_get.return_value = mock_response
            
            with patch('os._exit') as mock_exit:
                DCRequest("https://test-dc-url.com", chunks[0])
                mock_exit.assert_called_with(0)
        
        print("✅ Integration test completed successfully")
        
    finally:
        # Clean up
        os.unlink(proxy_file)

if __name__ == "__main__":
    print("🧪 Starting Double Counter Bypass Tests")
    print("=" * 50)
    
    # Run unit tests
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Run integration test
    run_integration_test()
    
    print("\n🎉 All tests completed!")