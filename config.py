# Configuration file for Market Risk Analysis Dashboard
# Modify these settings to customize your analysis

# Default portfolio symbols
DEFAULT_PORTFOLIO = [
    'AAPL',    # Apple Inc.
    'GOOGL',   # Alphabet Inc. (Google)
    'MSFT',    # Microsoft Corporation
    'AMZN',    # Amazon.com Inc.
    'TSLA',    # Tesla Inc.
    'NVDA',    # NVIDIA Corporation
    'META',    # Meta Platforms Inc.
    'BRK-B',   # Berkshire Hathaway Inc.
    'JPM',     # JPMorgan Chase & Co.
    'V'        # Visa Inc.
]

# Market indices for comparison
MARKET_INDICES = {
    '^GSPC': 'S&P 500',
    '^DJI': 'Dow Jones Industrial Average',
    '^IXIC': 'NASDAQ Composite',
    '^RUT': 'Russell 2000',
    '^VIX': 'CBOE Volatility Index'
}

# Default analysis period (in days)
DEFAULT_ANALYSIS_PERIOD = 365  # 1 year

# Risk-free rate (annual)
DEFAULT_RISK_FREE_RATE = 0.02  # 2%

# Volatility calculation period (trading days in a year)
TRADING_DAYS_PER_YEAR = 252

# Value at Risk confidence level
VAR_CONFIDENCE_LEVEL = 0.05  # 5%

# Maximum number of stocks to analyze simultaneously
MAX_PORTFOLIO_SIZE = 20

# Data refresh settings
DATA_REFRESH_INTERVAL = 300  # 5 minutes (in seconds)

# Chart customization
CHART_COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'success': '#2ca02c',
    'warning': '#ff7f0e',
    'danger': '#d62728',
    'info': '#17a2b8'
}

# Export settings
EXPORT_FORMATS = ['csv', 'excel']
DEFAULT_EXPORT_FILENAME = 'portfolio_risk_analysis'

# Performance settings
ENABLE_CACHING = True
CACHE_TTL = 3600  # 1 hour (in seconds)

# Risk thresholds for color coding
RISK_THRESHOLDS = {
    'volatility': {
        'low': 0.20,      # < 20%
        'medium': 0.30,   # 20-30%
        'high': 0.30      # > 30%
    },
    'beta': {
        'low': 0.8,       # < 0.8
        'medium': 1.2,    # 0.8-1.2
        'high': 1.2       # > 1.2
    },
    'sharpe_ratio': {
        'low': 0.5,       # < 0.5
        'medium': 1.0,    # 0.5-1.0
        'high': 1.0       # > 1.0
    }
}

# Dashboard layout settings
DASHBOARD_CONFIG = {
    'page_title': 'Market Risk Analysis Dashboard',
    'page_icon': '📊',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded',
    'menu_items': {
        'Get Help': 'https://github.com/your-repo/issues',
        'Report a bug': 'https://github.com/your-repo/issues',
        'About': 'Market Risk Analysis Dashboard v1.0'
    }
}

# Email alerts (if implemented)
EMAIL_ALERTS = {
    'enabled': False,
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'your-email@gmail.com',
    'recipient_emails': []
}

# Logging settings
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'market_risk_analysis.log'
}

# Custom risk metrics (add your own calculations here)
CUSTOM_METRICS = {
    'enabled': False,
    'metrics': [
        # 'calculate_sortino_ratio',
        # 'calculate_treynor_ratio',
        # 'calculate_information_ratio'
    ]
}

# Data source settings
DATA_SOURCES = {
    'primary': 'yfinance',
    'fallback': None,
    'cache_enabled': True,
    'request_timeout': 30
}

# Portfolio optimization settings
OPTIMIZATION = {
    'enabled': False,
    'method': 'sharpe',  # 'sharpe', 'min_variance', 'max_return'
    'constraints': {
        'min_weight': 0.0,
        'max_weight': 1.0,
        'target_return': None
    }
} 