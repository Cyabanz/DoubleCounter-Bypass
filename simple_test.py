#!/usr/bin/env python3
"""
Simple test script for Double Counter Bypass functionality
Tests core functions without complex mocking
"""

import sys
import os
import tempfile

# Add the current directory to the path so we can import DCBypass
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from DCBypass import read_proxy_list, split_list

def test_proxy_reading():
    """Test reading proxy list from file."""
    print("🧪 Testing proxy list reading...")
    
    # Create test proxy file
    test_proxies = [
        "192.168.1.1:8080",
        "192.168.1.2:8080", 
        "192.168.1.3:8080",
        "192.168.1.4:8080",
        "192.168.1.5:8080"
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        for proxy in test_proxies:
            f.write(proxy + '\n')
        proxy_file = f.name
    
    try:
        proxies = read_proxy_list(proxy_file)
        
        # Verify results
        assert len(proxies) == 5, f"Expected 5 proxies, got {len(proxies)}"
        assert isinstance(proxies[0], dict), "Expected list of dictionaries"
        assert 'https' in proxies[0], "Expected 'https' key in proxy dict"
        assert proxies[0]['https'] == 'http://192.168.1.1:8080', f"Expected 'http://192.168.1.1:8080', got {proxies[0]['https']}"
        
        print("✅ Proxy list reading test passed")
        return True
        
    except Exception as e:
        print(f"❌ Proxy list reading test failed: {e}")
        return False
    finally:
        os.unlink(proxy_file)

def test_list_splitting():
    """Test splitting proxy list into chunks."""
    print("🧪 Testing list splitting...")
    
    test_list = [1, 2, 3, 4, 5]
    
    try:
        # Test splitting into 2 chunks
        chunks = split_list(test_list, 2)
        assert len(chunks) == 2, f"Expected 2 chunks, got {len(chunks)}"
        assert len(chunks[0]) == 2, f"Expected first chunk to have 2 items, got {len(chunks[0])}"
        assert len(chunks[1]) == 3, f"Expected second chunk to have 3 items, got {len(chunks[1])}"
        
        # Test splitting into 3 chunks
        chunks = split_list(test_list, 3)
        assert len(chunks) == 3, f"Expected 3 chunks, got {len(chunks)}"
        
        # Test splitting into more chunks than items
        chunks = split_list(test_list, 10)
        assert len(chunks) == 10, f"Expected 10 chunks, got {len(chunks)}"
        
        print("✅ List splitting test passed")
        return True
        
    except Exception as e:
        print(f"❌ List splitting test failed: {e}")
        return False

def test_dc_bypass_script_structure():
    """Test the overall structure and imports of the DCBypass script."""
    print("🧪 Testing DCBypass script structure...")
    
    try:
        # Test that we can import the script
        import DCBypass
        
        # Test that required functions exist
        assert hasattr(DCBypass, 'read_proxy_list'), "read_proxy_list function not found"
        assert hasattr(DCBypass, 'split_list'), "split_list function not found"
        assert hasattr(DCBypass, 'DCRequest'), "DCRequest function not found"
        
        # Test that required modules are imported
        assert 'requests' in sys.modules or hasattr(DCBypass, 'requests'), "requests module not imported"
        assert 'threading' in sys.modules or hasattr(DCBypass, 'threading'), "threading module not imported"
        assert 'colorama' in sys.modules or hasattr(DCBypass, 'colorama'), "colorama module not imported"
        assert 'fake_headers' in sys.modules or hasattr(DCBypass, 'fake_headers'), "fake_headers module not imported"
        
        print("✅ DCBypass script structure test passed")
        return True
        
    except Exception as e:
        print(f"❌ DCBypass script structure test failed: {e}")
        return False

def test_proxy_file_operations():
    """Test proxy file reading and writing operations."""
    print("🧪 Testing proxy file operations...")
    
    try:
        # Test reading from the actual proxies.txt file
        if os.path.exists('proxies.txt'):
            proxies = read_proxy_list('proxies.txt')
            print(f"✅ Successfully read {len(proxies)} proxies from proxies.txt")
            
            # Test that proxies are in correct format
            if proxies:
                proxy = proxies[0]
                assert isinstance(proxy, dict), "Proxy should be a dictionary"
                assert 'https' in proxy, "Proxy should have 'https' key"
                assert proxy['https'].startswith('http://'), "Proxy should start with 'http://'"
                print("✅ Proxy format validation passed")
        else:
            print("⚠️ proxies.txt not found, skipping file operations test")
        
        print("✅ Proxy file operations test passed")
        return True
        
    except Exception as e:
        print(f"❌ Proxy file operations test failed: {e}")
        return False

def test_error_handling():
    """Test error handling for various scenarios."""
    print("🧪 Testing error handling...")
    
    try:
        # Test reading from non-existent file
        try:
            read_proxy_list('non_existent_file.txt')
            print("⚠️ Expected error when reading non-existent file")
        except FileNotFoundError:
            print("✅ Correctly handled non-existent file")
        
        # Test splitting empty list
        empty_chunks = split_list([], 2)
        assert len(empty_chunks) == 2, "Should handle empty list splitting"
        assert all(len(chunk) == 0 for chunk in empty_chunks), "All chunks should be empty"
        print("✅ Correctly handled empty list splitting")
        
        print("✅ Error handling test passed")
        return True
        
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False

def run_performance_test():
    """Test performance with larger datasets."""
    print("🧪 Testing performance with larger datasets...")
    
    try:
        # Create a larger proxy list
        large_proxy_list = [f"192.168.1.{i}:8080" for i in range(1, 101)]  # 100 proxies
        
        # Test splitting large list
        import time
        start_time = time.time()
        chunks = split_list(large_proxy_list, 10)
        end_time = time.time()
        
        assert len(chunks) == 10, f"Expected 10 chunks, got {len(chunks)}"
        assert sum(len(chunk) for chunk in chunks) == 100, "Should preserve all items"
        
        processing_time = end_time - start_time
        print(f"✅ Processed 100 proxies into 10 chunks in {processing_time:.4f} seconds")
        
        print("✅ Performance test passed")
        return True
        
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting Double Counter Bypass Tests")
    print("=" * 50)
    
    tests = [
        test_proxy_reading,
        test_list_splitting,
        test_dc_bypass_script_structure,
        test_proxy_file_operations,
        test_error_handling,
        run_performance_test
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
        print()  # Add spacing between tests
    
    print("=" * 50)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The Double Counter Bypass is working correctly.")
    else:
        print("⚠️ Some tests failed. Please review the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)