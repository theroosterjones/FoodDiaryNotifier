# Food Diary Notifier

A Python-based notification service that monitors a food diary website for new entries and sends push notifications to your iPhone via Pushover when new entries are detected.

## Features

- 🔄 **Automated Monitoring**: Checks for new food diary entries every 5 minutes
- 📱 **iPhone Notifications**: Sends push notifications via Pushover
- 🌐 **Web Monitoring**: Monitors food diary website for changes
- 📊 **Comprehensive Logging**: Detailed logs for monitoring and debugging
- ⚙️ **Configurable**: Easy to customize check intervals and notification settings

## Prerequisites

- Python 3.7 or higher
- Access to a food diary website
- A Pushover account for iPhone notifications
- Internet connection for website monitoring

## Installation

1. **Clone or download this project**
   ```bash
   git clone <repository-url>
   cd FoodDiaryNotifier
   ```

2. **Install dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Configure environment variables**
   - Copy the `.env` file and fill in your actual values
   - See [Configuration](#configuration) section for details

## Configuration

### 1. Food Diary Website Setup

You need the URL of your food diary website. The program will:
1. Open the website in your browser
2. Let you log in manually
3. Monitor the page for new entries
4. Send notifications when changes are detected

### 2. Website Customization

You may need to customize the `extract_entries()` method in `main.py` to match your website's HTML structure. Look for:
- HTML elements that contain food diary entries
- CSS classes or IDs that identify entry data
- The structure of client names, timestamps, food items, and calories

### 2. Pushover Setup

1. **Create a Pushover account:**
   - Go to [https://pushover.net/](https://pushover.net/) and sign up
   - Download the Pushover app on your iPhone

2. **Get your User Key:**
   - Log into Pushover web interface
   - Your User Key is displayed on the main page
   - Copy this value

3. **Create an Application:**
   - Go to [https://pushover.net/apps](https://pushover.net/apps)
   - Click "Create an Application"
   - Name it "Food Diary Notifier"
   - Copy the API Token

### 3. Environment Variables

Edit the `.env` file with your actual values:

```env
# Food Diary Website Configuration
FOOD_DIARY_URL=https://your-food-diary-website.com

# Pushover Notification Settings
PUSHOVER_API_TOKEN=your_pushover_api_token_here
PUSHOVER_USER_KEY=your_pushover_user_key_here

# Optional: Override default settings
# CHECK_INTERVAL=300  # Check interval in seconds (default: 300 = 5 minutes)
# LOG_LEVEL=INFO      # Logging level (DEBUG, INFO, WARNING, ERROR)
# LOG_FILE=food_diary_notifier.log
```

## Usage

### Starting the Service

```bash
python3 main.py
```

### What Happens When You Start

1. **Website Access**: The app opens your food diary website in the browser
2. **Manual Login**: You log in to the website manually
3. **Content Monitoring**: The program monitors the webpage for changes
4. **Change Detection**: Detects when new entries are added to the page
5. **Notifications**: Sends push notifications to your iPhone for new entries

### Notification Format

Each notification includes:
- Client name
- Timestamp
- Food item
- Calorie count

Example notification:
```
New Food Diary Entry
New food diary entry from John Doe:
Time: 2024-01-15T12:30:00Z
Food: Grilled Chicken Salad
Calories: 350
```

## Configuration Options

### Check Interval
Control how often the service checks for new entries:
```env
CHECK_INTERVAL=300  # 5 minutes (default)
CHECK_INTERVAL=600  # 10 minutes
CHECK_INTERVAL=60   # 1 minute
```

### Logging
Adjust logging verbosity:
```env
LOG_LEVEL=DEBUG    # Most verbose
LOG_LEVEL=INFO     # Default
LOG_LEVEL=WARNING  # Only warnings and errors
LOG_LEVEL=ERROR    # Only errors
```

### Log File
Change where logs are saved:
```env
LOG_FILE=my_custom_log.log
```

## Troubleshooting

### Common Issues

1. **"Website access failed"**
   - Check your `FOOD_DIARY_URL` is correct
   - Ensure the website is accessible and you can log in manually
   - Verify the website structure matches the expected format
   - Check your internet connection

2. **"Pushover notification failed"**
   - Verify your `PUSHOVER_API_TOKEN` and `PUSHOVER_USER_KEY`
   - Check your internet connection
   - Ensure the Pushover app is installed on your iPhone

3. **"API request failed"**
   - Check your access token hasn't expired
   - Verify the API endpoints are correct
   - Check your internet connection

### Logs

Check the log file for detailed information:
```bash
tail -f food_diary_notifier.log
```

### Testing Configuration

Test if your configuration loads correctly:
```bash
python3 -c "import config; print('Configuration loaded successfully!')"
```

## Security Notes

- The `.env` file contains sensitive information - keep it secure
- The OAuth flow uses a local server on port 8080
- Access tokens are stored in memory only
- No persistent storage of sensitive data

## Development

### Project Structure
```
FoodDiaryNotifier/
├── main.py          # Main application logic
├── config.py        # Configuration management
├── requirements.txt  # Python dependencies
├── .env             # Environment variables (create this)
└── README.md        # This file
```

### Dependencies
- `requests==2.31.0` - HTTP requests
- `python-dotenv==1.0.0` - Environment variables
- `pushover.py==0.4` - Pushover notifications
- `schedule==1.2.1` - Task scheduling
- `beautifulsoup4==4.12.2` - HTML parsing

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the logs for error details
3. [Add your contact information or issue tracker] 