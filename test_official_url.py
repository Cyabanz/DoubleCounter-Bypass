#!/usr/bin/env python3
"""
Test script to run DCBypass with the official Double Counter URL
"""

import sys
import os
import subprocess
import threading
import time
from io import StringIO

def test_with_official_url():
    """Test the DCBypass script with the official URL."""
    print("🎯 Testing Double Counter Bypass with Official URL")
    print("=" * 60)
    print(f"URL: https://beta.doublecounter.gg/v/231p40jm59")
    print("=" * 60)
    
    # Prepare inputs for the script
    inputs = [
        "https://beta.doublecounter.gg/v/231p40jm59",  # DC verify url
        "2"  # Number of threads
    ]
    
    input_string = "\n".join(inputs) + "\n"
    
    try:
        # Run the DCBypass script with the inputs
        process = subprocess.Popen(
            [sys.executable, "DCBypass.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd="/workspace"
        )
        
        # Send inputs and get output
        stdout, stderr = process.communicate(input=input_string, timeout=30)
        
        print("📤 Script Output:")
        print("-" * 40)
        print(stdout)
        
        if stderr:
            print("⚠️ Script Errors:")
            print("-" * 40)
            print(stderr)
        
        print(f"📊 Exit Code: {process.returncode}")
        
        # Analyze the results
        analyze_results(stdout, stderr, process.returncode)
        
    except subprocess.TimeoutExpired:
        print("⏰ Script timed out after 30 seconds")
        process.kill()
    except Exception as e:
        print(f"❌ Error running script: {e}")

def analyze_results(stdout, stderr, returncode):
    """Analyze the results of the DCBypass execution."""
    print("\n🔍 Results Analysis:")
    print("-" * 40)
    
    # Check for success indicators
    if "Successfully bypassed DC" in stdout:
        print("✅ SUCCESS: DC bypass was successful!")
        print("🎉 The script successfully bypassed the Double Counter verification")
    elif "URL is expired" in stdout:
        print("⚠️ EXPIRED: The verification URL has expired")
        print("💡 You may need to get a fresh verification link")
    elif "DC detected the alt account" in stdout:
        print("🚫 DETECTED: Double Counter detected the alt account")
        print("💡 You may need to use a different account or get a new link")
    elif "DC detected the proxy" in stdout:
        print("🚫 PROXY DETECTED: Double Counter detected the proxy")
        print("💡 The proxy was blocked, but the script should try others")
    elif "Blocked by Cloudflare" in stdout:
        print("🛡️ CLOUDFLARE: Request was blocked by Cloudflare")
        print("💡 This is expected behavior for some proxies")
    elif "Proxy error" in stdout:
        print("❌ PROXY ERROR: Connection issues with proxies")
        print("💡 The proxies may be invalid or unreachable")
    else:
        print("❓ UNKNOWN: Unexpected response")
        print(f"📝 Raw output: {stdout[:200]}...")
    
    # Check return code
    if returncode == 0:
        print("✅ Script exited successfully (exit code 0)")
    else:
        print(f"⚠️ Script exited with code {returncode}")
    
    # Count proxy attempts
    proxy_attempts = stdout.count("Proxy:")
    print(f"🔄 Total proxy attempts: {proxy_attempts}")

def test_url_accessibility():
    """Test if the URL is accessible without proxies first."""
    print("\n🌐 Testing URL Accessibility")
    print("-" * 40)
    
    try:
        import requests
        
        # Test direct access to the URL
        response = requests.get("https://beta.doublecounter.gg/v/231p40jm59", timeout=10)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📏 Content Length: {len(response.text)} characters")
        
        # Check for specific indicators in the response
        if "Success!" in response.text:
            print("✅ Direct access shows 'Success!' - URL may already be verified")
        elif "Expired link" in response.text:
            print("⚠️ Direct access shows 'Expired link' - URL has expired")
        elif "RR02" in response.text:
            print("🚫 Direct access shows 'RR02' - Alt account detected")
        elif "RV01" in response.text:
            print("🚫 Direct access shows 'RV01' - Proxy detection")
        else:
            print("❓ Direct access shows unknown response")
            print(f"📝 Response preview: {response.text[:200]}...")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error accessing URL directly: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def main():
    """Main test function."""
    print("🚀 Double Counter Bypass - Official URL Test")
    print("=" * 60)
    
    # First test URL accessibility
    test_url_accessibility()
    
    # Then test with the bypass script
    test_with_official_url()
    
    print("\n" + "=" * 60)
    print("🎯 Official URL Test Complete")
    print("\n💡 Notes:")
    print("• This test uses localhost proxies (127.0.0.1) which won't work for real bypassing")
    print("• For actual bypassing, you would need real, working proxy servers")
    print("• The test demonstrates the script's behavior and error handling")

if __name__ == "__main__":
    main()