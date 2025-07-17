import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Food Diary Website Settings
FOOD_DIARY_URL = os.getenv('FOOD_DIARY_URL')
API_VERSION = 'v1.0'

# Pushover Notification Settings
PUSHOVER_API_TOKEN = os.getenv('PUSHOVER_API_TOKEN')
PUSHOVER_USER_KEY = os.getenv('PUSHOVER_USER_KEY')

# Application Settings
CHECK_INTERVAL = 300  # Check for new entries every 5 minutes
MAX_RETRIES = 3  # Maximum number of retries for failed requests
RETRY_DELAY = 60  # Delay between retries in seconds

# Authentication Settings
AUTH_TIMEOUT = 300  # Authentication timeout in seconds
REDIRECT_URI = 'http://localhost:8080'  # OAuth redirect URI

# Logging Settings
LOG_LEVEL = 'INFO'
LOG_FILE = 'food_diary_notifier.log' 