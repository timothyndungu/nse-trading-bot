"""
NSE Trading Bot - Configuration Settings
Controls all bot parameters and constants
"""

import os
from datetime import time

# ============================================================================
# MARKET SETTINGS
# ============================================================================

# NSE Trading hours
NSE_MARKET_OPEN = time(9, 30)
NSE_MARKET_CLOSE = time(15, 0)
NSE_TIMEZONE = 'Africa/Nairobi'

# NSE listed stocks (main board)
NSE_STOCKS = [
    'ABCKENYA', 'ACCESSKENYA', 'AIRKENYA', 'ARM', 'BAMBURI', 'BANK', 'BARCLAYS',
    'BATU', 'BRITISH', 'CARBACID', 'CENTUM', 'CERTIFICATES', 'CIC', 'CITYOAK',
    'CMC', 'COCOASHUN', 'COOPERATIVE', 'CRAFTSILK', 'CROWN', 'CYTONN', 'DIAMOND',
    'DRDP', 'DTK', 'EABL', 'EAPCO', 'EASTAFRICASTANDARD', 'EASYTEL', 'EGERTON',
    'ELDFP', 'ELDP', 'ELKENYA', 'EQUITY', 'ETHANOL', 'EVERREADY', 'EXCHANGE',
    'FINBANK', 'FIRESTONE', 'FKL', 'FLOATKENYA', 'FOCUS', 'FORD', 'FORTIS',
    'GAPLIMITED', 'GEOTHERMAL', 'GHCL', 'GLAXOSMITHKLINE', 'GLOBAL', 'GOLF',
    'GROWTHPOINT', 'GUARANTY', 'GUINNESS', 'HARDEL', 'HEAT', 'HIGHLANDS',
    'HILTON', 'HISTEEL', 'HLFP', 'HLDP', 'HOME', 'HOMEPOINT', 'HPC',
    'HOSTELS', 'HOUSING', 'HUDCO', 'HURLINGHAM', 'IBRACO', 'ICDC', 'IDCKENYA',
    'IDELIMITED', 'INAMAGRO', 'INCA', 'INDOKENYA', 'INFINITY', 'INITIATIVE',
    'INSIGHT', 'INSUREPLUS', 'IPCN', 'IRIS', 'ITEMS', 'JACKPOT', 'JAMII',
    'JAMBIMOTORS', 'JATCO', 'JAVALIMITED', 'JDS', 'JETLIMITED', 'JITUME',
    'JUBILEE', 'JUHUDI', 'JUVELNL', 'KAL', 'KALYALIMITED', 'KAMNAN', 'KAPLAHY',
    'KARBANKS', 'KAUL', 'KAVI', 'KBLIMITED', 'KCBGROUP', 'KCC', 'KCOLIMITED',
    'KDPLIMITED', 'KENATCO', 'KENACASA', 'KENCORE', 'KENGEN', 'KENGS', 'KENOL',
    'KENSALT', 'KENUTILITIES', 'KENYLIMITED', 'KERUTILITIES', 'KGHM', 'KHL',
    'KIAMBILIMITED', 'KIBWEZI', 'KICOHOLDINGS', 'KIDELIMITED', 'KILINDINI',
    'KILI', 'KINETIC', 'KINGFISHER', 'KINGTEX', 'KIPG', 'KIPROPERTY', 'KIRLIMITED',
    'KISII', 'KITEGAS', 'KITLIMITED', 'KITUI', 'KITUIGROUP', 'KLA', 'KLINSAVE',
    'KMIKENYA', 'KNFC', 'KNGGOLD', 'KNGLIMITED', 'KNHC', 'KNSPICE', 'KNWATERLIMITED',
    'KOIL', 'KOLIMITED', 'KONAGAS', 'KONZA', 'KOREAN', 'KORUNA', 'KOSARSLIMITED',
    'KOSTER', 'KOTARPLC', 'KOTIKESJA', 'KOTILEAP', 'KOTIMEYER', 'KOTIMIL',
    'KOTIMLIMITED', 'KOTIMOTORS', 'KOTINA', 'KOTINETWORKSLTD', 'KOTINVESTMENT',
    'KOTIPES', 'KOTIRUNWAY', 'KOTISANA', 'KOTISANSA', 'KOTISHELL', 'KOTISMALLBIZ',
    'KOTITECHKENYA', 'KOTIWATCHTOWER', 'KOTIXPRE', 'KOTKPL', 'KOTPHARMA',
    'KOTSCANDLE', 'KOTSHIPPING', 'KOTSPEECH', 'KOTTAX', 'KOTTRUCKERS', 'KOTVCC',
    'KOTVEHICLES', 'KOTVISION', 'KOTVISIONKENYA', 'KOTZANZIBAR', 'KPLIMITED',
    'KPMG', 'KRBL', 'KREATIVEHOTELS', 'KREDIT', 'KRENTEL', 'KREPLC', 'KREST',
    'KRISTAINVESTMENTS', 'KRMOTORS', 'KRONOPLC', 'KRPLC', 'KRYPTON', 'KSE',
    'KSHAKTIGROUP', 'KSLIMITED', 'KSPHARMA', 'KSWEB', 'KTKENYA', 'KTLIMITED',
    'KTPLC', 'KUBEENERGY', 'KUFAI', 'KUGEL', 'KUHLE', 'KUKUKENYA', 'KULIMITED',
    'KUMUD', 'KUNAALIMITED', 'KUNASYSTEMS', 'KUNAUNVESTMENTS', 'KUNDASYSTEMS',
    'KUNDUINDUSTRIES', 'KUNDUKENYA', 'KUNDUMEATS', 'KUNDALIMITED', 'KUNDISYSTEMS',
    'KUNDUL', 'KUNDZUINVESTMENTS', 'KUNEMI', 'KUNETECH', 'KUNEUIKENYA', 'KUNGULE',
    'KUNILIMITED', 'KUNINJAGROUP', 'KUNION', 'KUNISTUDIOS', 'KUNISYSTEMS',
    'KUNITHUM', 'KUNITIMP', 'KUNITURF', 'KUNIZAMULIMITED', 'KUNKAI', 'KUNKALAS',
    'KUNKALI', 'KUNKAMLIMITED', 'KUNKAMI', 'KUNKAMIS', 'KUNKAMS', 'KUNKANETTED',
    'KUNKANISYSTEMS', 'KUNKAPHARMA', 'KUNKAPOLY', 'KUNKATECH', 'KUNKATOY',
    'KUNKATRADERS', 'KUNKAVENTURE', 'KUNKAWIRE', 'KUNKAXIMUM', 'KUNKAZM',
    'KUNKCAREERS', 'KUNKCARPET', 'KUNKCATERING', 'KUNKCAVIAR', 'KUNKCLASSIC',
    'KUNKCLEAR', 'KUNKCLEAN', 'KUNKCLICK', 'KUNKCLOUD', 'KUNKCLUSTER', 'KUNKCOAL',
    'KUNKCOAST', 'KUNKCOBALT', 'KUNKCOCKTAIL', 'KUNKCODE', 'KUNKCODEX', 'KUNKCO',
    'KUNKCOFFEE', 'KUNKCOIL', 'KUNKCOIN', 'KUNKCOKE', 'KUNKCOLLAB', 'KUNKCOLOR',
    'KUNKCOLOSS', 'KUNKCOLUMN', 'KUNKCOMBAT', 'KUNKCOMFORT', 'KUNKCOMICS',
    'KUNKCOMING', 'KUNKCOMMIT', 'KUNKCOMMON', 'KUNKCOMPANY', 'KUNKCOMPLEX',
    'KUNKCOMPLY', 'KUNKCOMPORT', 'KUNKCOMPOSE', 'KUNKCOMPOUND', 'KUNKCOMPREHEND',
    'KUNKCOMPRESS', 'KUNKCOMPRISE', 'KUNKCOMPROMISE', 'KUNKCOMPUTE', 'KUNKCOMRADE',
    'KUNKCONCEAL', 'KUNKCONCEDE', 'KUNKCONCEIT', 'KUNKCONCENT', 'KUNKCONCENT'
]

# ============================================================================
# TRADING PARAMETERS
# ============================================================================

# Initial capital
INITIAL_CAPITAL = 1000000  # 1 Million KES

# Position sizing
MAX_POSITION_SIZE = 0.1  # Max 10% per stock
MIN_POSITION_SIZE = 0.01  # Min 1% per stock
POSITION_SIZING_METHOD = 'fixed_fractional'  # or 'kelly', 'equal_weight'

# Risk management
MAX_DAILY_LOSS = 0.05  # Stop if lose 5% in a day
MAX_PORTFOLIO_DRAWDOWN = 0.20  # Stop if portfolio drawdown > 20%
RISK_PER_TRADE = 0.02  # Risk 2% per trade
MAX_POSITIONS = 10  # Max concurrent positions

# Order execution
MIN_ORDER_VALUE = 50000  # Minimum KES per order
SLIPPAGE = 0.001  # 0.1% estimated slippage
COMMISSION = 0.001  # 0.1% commission per trade

# ============================================================================
# TECHNICAL INDICATORS
# ============================================================================

# RSI (Relative Strength Index)
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

# MACD (Moving Average Convergence Divergence)
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

# Bollinger Bands
BB_PERIOD = 20
BB_STD_DEV = 2

# Moving Averages
SMA_SHORT = 20
SMA_MEDIUM = 50
SMA_LONG = 200

# ATR (Average True Range)
ATR_PERIOD = 14

# ============================================================================
# ML MODEL PARAMETERS
# ============================================================================

# LSTM Model
LSTM_UNITS = 128
LSTM_DROPOUT = 0.2
LSTM_LOOK_BACK = 60  # Past 60 days
LSTM_FORECAST_HORIZON = 5  # Predict 5 days ahead
LSTM_EPOCHS = 100
LSTM_BATCH_SIZE = 32

# XGBoost Model
XGBOOST_MAX_DEPTH = 5
XGBOOST_LEARNING_RATE = 0.1
XGBOOST_N_ESTIMATORS = 100

# Data normalization
NORMALIZATION_METHOD = 'minmax'  # or 'standard'
TRAIN_TEST_SPLIT = 0.8
VALIDATION_SPLIT = 0.1

# ============================================================================
# BACKTESTING PARAMETERS
# ============================================================================

BACKTEST_START_DATE = '2022-01-01'
BACKTEST_END_DATE = '2024-01-01'
BACKTEST_FREQUENCY = '1D'  # Daily bars

# ============================================================================
# DATA COLLECTION
# ============================================================================

# API Configuration
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', '')
YAHOO_FINANCE_ENABLED = True  # yfinance doesn't require API key
NSE_SCRAPE_ENABLED = True

# Data update frequency
DATA_UPDATE_INTERVAL = 300  # Update every 5 minutes (seconds)
HISTORICAL_DATA_YEARS = 3  # Download 3 years of historical data

# ============================================================================
# BROKER INTEGRATION
# ============================================================================

# Broker API Configuration
BROKER_NAME = 'DEMO'  # Change to actual broker
BROKER_API_KEY = os.getenv('BROKER_API_KEY', '')
BROKER_API_SECRET = os.getenv('BROKER_API_SECRET', '')
PAPER_TRADING = True  # Start with paper trading

# ============================================================================
# MONITORING & LOGGING
# ============================================================================

LOG_LEVEL = 'INFO'
LOG_FILE = 'logs/trading_bot.log'
LOG_MAX_BYTES = 10485760  # 10MB
LOG_BACKUP_COUNT = 5

# Performance tracking
PERFORMANCE_LOG_FILE = 'logs/performance.json'
TRADES_LOG_FILE = 'logs/trades.csv'

# ============================================================================
# DASHBOARD
# ============================================================================

DASHBOARD_HOST = '0.0.0.0'
DASHBOARD_PORT = 5000
DASHBOARD_DEBUG = True
DASHBOARD_REFRESH_INTERVAL = 5000  # milliseconds

# ============================================================================
# NOTIFICATIONS
# ============================================================================

EMAIL_NOTIFICATIONS = False
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS', '')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')

SMS_NOTIFICATIONS = False
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER', '')

# ============================================================================
# STRATEGY SELECTION
# ============================================================================

# Active strategies
ACTIVE_STRATEGIES = [
    'momentum',
    'mean_reversion',
    'trend_following'
]

# Strategy weights (if using ensemble)
STRATEGY_WEIGHTS = {
    'momentum': 0.4,
    'mean_reversion': 0.3,
    'trend_following': 0.3
}

# ============================================================================
# DEVELOPMENT
# ============================================================================

DEBUG_MODE = False
VERBOSE_LOGGING = True
SAVE_MODEL_CHECKPOINTS = True
CHECKPOINT_DIR = 'models/checkpoints'
