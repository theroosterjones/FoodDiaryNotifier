import logging
import time
import schedule
from datetime import datetime
import requests
from pushover import Client as PushoverClient
import config
import webbrowser
import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import urllib.parse
from bs4 import BeautifulSoup
import hashlib

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle the OAuth callback"""
        # Parse the query parameters
        query_components = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        
        if 'code' in query_components:
            # Store the authorization code
            self.server.auth_code = query_components['code'][0]
            
            # Send success response to browser
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Authentication successful! You can close this window.")
        else:
            # Send error response
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Authentication failed! Please try again.")

class FoodDiaryNotifier:
    def __init__(self):
        self.last_check_time = None
        self.pushover_client = PushoverClient(config.PUSHOVER_USER_KEY, api_token=config.PUSHOVER_API_TOKEN)
        self.last_content_hash = None
        self.session = requests.Session()
        
    def open_food_diary(self):
        """Open the food diary website in browser for manual login"""
        try:
            logger.info("Opening food diary website in browser...")
            webbrowser.open(config.FOOD_DIARY_URL)
            logger.info("Please log in to the food diary website manually.")
            logger.info("The program will monitor the page for new entries.")
            return True
        except Exception as e:
            logger.error(f"Error opening food diary website: {str(e)}")
            return False

    def check_new_entries(self):
        """Check for new food diary entries by monitoring the webpage"""
        try:
            # Get the current page content
            response = self.session.get(config.FOOD_DIARY_URL)
            
            if response.status_code == 200:
                # Parse the HTML content
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract food diary entries (you'll need to customize this based on the website structure)
                entries = self.extract_entries(soup)
                
                # Create a hash of the current content to detect changes
                current_content = str(entries)
                current_hash = hashlib.md5(current_content.encode()).hexdigest()
                
                # Check if content has changed since last check
                if self.last_content_hash and self.last_content_hash != current_hash:
                    logger.info("New entries detected!")
                    
                    # Find new entries by comparing with previous state
                    new_entries = self.find_new_entries(entries)
                    
                    for entry in new_entries:
                        self.send_notification(entry)
                
                self.last_content_hash = current_hash
                self.last_check_time = datetime.utcnow()
                logger.info(f"Successfully checked for new entries at {self.last_check_time}")
                
            else:
                logger.error(f"Failed to access food diary website: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error checking for new entries: {str(e)}")

    def extract_entries(self, soup):
        """Extract food diary entries from the webpage HTML"""
        entries = []
        
        # This is a template - you'll need to customize based on the actual website structure
        # Look for elements that contain food diary entries
        entry_elements = soup.find_all('div', class_='food-entry')  # Adjust class name
        
        for element in entry_elements:
            entry = {
                'client_name': element.find('span', class_='client-name').text.strip() if element.find('span', class_='client-name') else 'Unknown',
                'timestamp': element.find('span', class_='timestamp').text.strip() if element.find('span', class_='timestamp') else 'Unknown',
                'food_item': element.find('span', class_='food-item').text.strip() if element.find('span', class_='food-item') else 'Unknown',
                'calories': element.find('span', class_='calories').text.strip() if element.find('span', class_='calories') else 'Unknown'
            }
            entries.append(entry)
        
        return entries

    def find_new_entries(self, current_entries):
        """Find entries that are new since the last check"""
        # For now, return all current entries as "new"
        # In a more sophisticated implementation, you'd compare with a stored previous state
        return current_entries

    def check_new_entries(self):
        """Check for new food diary entries by monitoring the webpage"""
        try:
            # Get the current page content
            response = self.session.get(config.FOOD_DIARY_URL)
            
            if response.status_code == 200:
                # Parse the HTML content
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract food diary entries (you'll need to customize this based on the website structure)
                entries = self.extract_entries(soup)
                
                # Create a hash of the current content to detect changes
                current_content = str(entries)
                current_hash = hashlib.md5(current_content.encode()).hexdigest()
                
                # Check if content has changed since last check
                if self.last_content_hash and self.last_content_hash != current_hash:
                    logger.info("New entries detected!")
                    
                    # Find new entries by comparing with previous state
                    new_entries = self.find_new_entries(entries)
                    
                    for entry in new_entries:
                        self.send_notification(entry)
                
                self.last_content_hash = current_hash
                self.last_check_time = datetime.utcnow()
                logger.info(f"Successfully checked for new entries at {self.last_check_time}")
                
            else:
                logger.error(f"Failed to access food diary website: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error checking for new entries: {str(e)}")

    def send_notification(self, entry):
        """Send notification to iPhone using Pushover"""
        try:
            # Format the notification message
            message = f"New food diary entry from {entry.get('client_name', 'Unknown')}:\n"
            message += f"Time: {entry.get('timestamp', 'Unknown')}\n"
            message += f"Food: {entry.get('food_item', 'Unknown')}\n"
            message += f"Calories: {entry.get('calories', 'Unknown')}"
            
            # Send notification
            self.pushover_client.send_message(
                message,
                title="New Food Diary Entry"
            )
            
            logger.info(f"Notification sent for entry from {entry.get('client_name', 'Unknown')}")
            
        except Exception as e:
            logger.error(f"Error sending notification: {str(e)}")

    def run(self):
        """Run the notification service"""
        logger.info("Starting Food Diary Notifier service")
        
        # Open the food diary website for manual login
        self.open_food_diary()
        
        # Schedule the check_new_entries function to run every CHECK_INTERVAL seconds
        schedule.every(config.CHECK_INTERVAL).seconds.do(self.check_new_entries)
        
        # Run immediately on startup
        self.check_new_entries()
        
        # Keep the script running
        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    notifier = FoodDiaryNotifier()
    notifier.run() 