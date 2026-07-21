"""
Example credentials file - Copy to credentials.py and fill in your API keys
IMPORTANT: Add credentials.py to .gitignore - Never commit real API keys!
"""

# ============================================================================
# ALPHA VANTAGE
# ============================================================================
# Get free API key from: https://www.alphavantage.co/
ALPHA_VANTAGE_API_KEY = 'your_alpha_vantage_api_key_here'

# ============================================================================
# BROKER CREDENTIALS
# ============================================================================
# For NSE trading, use an authorized broker like:
# - Equity Bank Trading
# - CIC Group
# - SBG Securities
# - etc.

BROKER_API_KEY = 'your_broker_api_key'
BROKER_API_SECRET = 'your_broker_api_secret'
BROKER_ACCOUNT_ID = 'your_account_id'

# ============================================================================
# EMAIL NOTIFICATIONS
# ============================================================================
EMAIL_ADDRESS = 'your_email@gmail.com'
EMAIL_PASSWORD = 'your_app_password'  # Use app-specific password for Gmail
EMAIL_SMTP_SERVER = 'smtp.gmail.com'
EMAIL_SMTP_PORT = 587

# ============================================================================
# SMS NOTIFICATIONS (Twilio)
# ============================================================================
# Get free trial from: https://www.twilio.com/
TWILIO_ACCOUNT_SID = 'your_twilio_account_sid'
TWILIO_AUTH_TOKEN = 'your_twilio_auth_token'
TWILIO_PHONE_NUMBER = '+1234567890'  # Your Twilio phone number
RECIPIENT_PHONE_NUMBER = '+254712345678'  # Your phone number

# ============================================================================
# DATABASE
# ============================================================================
DATABASE_URL = 'sqlite:///nse_trading.db'
# For PostgreSQL: 'postgresql://user:password@localhost/nse_trading'
# For MongoDB: 'mongodb://username:password@localhost:27017/nse_trading'

# ============================================================================
# BACKUP & SECURITY
# ============================================================================
BACKUP_ENCRYPTION_KEY = 'your_encryption_key_here'
