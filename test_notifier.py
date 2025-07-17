#!/usr/bin/env python3
"""
Test script for Food Diary Notifier
This script tests the core functionality without running the full service
"""

import logging
import requests
from bs4 import BeautifulSoup
import config
import webbrowser
import hashlib

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_website_access():
    """Test if we can access the food diary website"""
    try:
        logger.info(f"Testing access to: {config.FOOD_DIARY_URL}")
        response = requests.get(config.FOOD_DIARY_URL)
        logger.info(f"✅ Website accessible! Status: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"❌ Failed to access website: {e}")
        return None

def test_html_parsing(response):
    """Test HTML parsing functionality"""
    try:
        soup = BeautifulSoup(response.content, 'html.parser')
        logger.info(f"✅ HTML parsing successful!")
        logger.info(f"Page title: {soup.title.string if soup.title else 'No title found'}")
        logger.info(f"Found {len(soup.find_all('div'))} div elements")
        return soup
    except Exception as e:
        logger.error(f"❌ Failed to parse HTML: {e}")
        return None

def test_browser_opening():
    """Test browser opening functionality"""
    try:
        logger.info("Testing browser opening...")
        webbrowser.open(config.FOOD_DIARY_URL)
        logger.info("✅ Browser opened successfully!")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to open browser: {e}")
        return False

def test_content_monitoring():
    """Test content monitoring functionality"""
    try:
        response = requests.get(config.FOOD_DIARY_URL)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Create a hash of the current content
        current_content = str(soup.find_all('div'))
        current_hash = hashlib.md5(current_content.encode()).hexdigest()
        
        logger.info(f"✅ Content monitoring test successful!")
        logger.info(f"Content hash: {current_hash[:10]}...")
        logger.info(f"Content length: {len(current_content)} characters")
        return True
    except Exception as e:
        logger.error(f"❌ Failed content monitoring test: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("🧪 Starting Food Diary Notifier tests...")
    
    # Test 1: Website access
    response = test_website_access()
    if not response:
        return False
    
    # Test 2: HTML parsing
    soup = test_html_parsing(response)
    if not soup:
        return False
    
    # Test 3: Browser opening
    browser_ok = test_browser_opening()
    if not browser_ok:
        logger.warning("⚠️ Browser opening failed, but continuing tests...")
    
    # Test 4: Content monitoring
    monitoring_ok = test_content_monitoring()
    if not monitoring_ok:
        return False
    
    logger.info("🎉 All tests passed! The notifier should work correctly.")
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ All tests passed! You can now run the full notifier with: python3 main.py")
    else:
        print("\n❌ Some tests failed. Please check the errors above.") 