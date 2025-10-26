# 📊 Custom Market Risk Analysis Dashboard

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)](https://github.com/yourusername/market-risk-dashboard)

A **Custom Market Risk Analysis Dashboard** with enhanced date handling, robust error management, and real-time data fetching from Yahoo Finance. Built with Python, Streamlit, and Plotly for professional portfolio risk analysis.

## 🚀 Features

### ✨ **Custom Dashboard Features**
- **📅 Smart Date Validation**: Prevents invalid date ranges (minimum 30 days, maximum 5 years)
- **🔗 Connection Testing**: Test Yahoo Finance connectivity before running analysis
- **📊 Real-time Progress**: Live updates during data fetching and calculations
- **🎨 Enhanced UI**: Success/error messages with visual feedback
- **🛡️ Robust Error Handling**: Graceful handling of network issues and data problems
- **💾 Advanced Export**: Multi-sheet Excel exports with comprehensive data

### 📊 **Risk Metrics Calculation**
- **Volatility Analysis**: Annualized volatility for each stock
- **Beta Calculation**: Market sensitivity analysis
- **Sharpe Ratio**: Risk-adjusted return metrics
- **Value at Risk (VaR)**: 5% confidence level risk assessment
- **Maximum Drawdown**: Worst historical decline analysis
- **Total Returns**: Performance measurement over time

### 📈 **Interactive Visualizations**
- **Price Performance Charts**: Time series analysis
- **Risk Comparison Plots**: Volatility and Beta bar charts
- **Returns Distribution**: Histogram analysis
- **Correlation Matrix**: Portfolio diversification insights
- **Real-time Data**: Live market data via Yahoo Finance

### 💾 **Data Export & Integration**
- **CSV Export**: Risk metrics and returns data
- **Excel Export**: Multi-sheet analysis reports
- **Power BI Ready**: Seamless integration
- **Tableau Compatible**: Flexible visualization platform

## 🛠️ Technology Stack

- **Backend**: Python 3.8+
- **Data Processing**: Pandas, NumPy
- **Financial Data**: yfinance (Yahoo Finance API)
- **Web Framework**: Streamlit
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Data Export**: openpyxl (Excel support)

## 📋 Prerequisites

- Python 3.8 or higher
- pip package manager
- Internet connection for live data
- Modern web browser

## 🚀 Quick Start

### 1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/market-risk-dashboard.git
cd market-risk-dashboard
```

### 2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 3. **Run the Custom Dashboard**
```bash
streamlit run custom_dashboard.py
```

**Or use the PowerShell launcher:**
```powershell
.\run_custom_dashboard.ps1
```

### 4. **Access the Dashboard**
Open your browser and navigate to: `http://localhost:8501`

## 📖 Usage Guide

### **Portfolio Configuration**
1. **Enter Stock Symbols**: Add your desired stocks (e.g., AAPL, GOOGL, MSFT)
2. **Select Date Range**: Choose analysis period (default: 1 year)
3. **Choose Market Index**: S&P 500, Dow Jones, NASDAQ, or Russell 2000
4. **Set Risk-Free Rate**: Adjust for Sharpe ratio calculations

### **Running Analysis**
1. **Click "🚀 Run Analysis"** in the sidebar
2. **Wait for Processing** (data fetching and calculations)
3. **Review Results** in the interactive dashboard
4. **Export Data** for external analysis

### **Understanding Metrics**
- **Volatility > 30%**: High risk (Red)
- **Volatility 20-30%**: Medium risk (Orange)  
- **Volatility < 20%**: Low risk (Green)
- **Beta > 1.2**: More volatile than market
- **Beta 0.8-1.2**: Similar to market
- **Beta < 0.8**: Less volatile than market

## 📊 Sample Portfolio Analysis

The dashboard comes pre-configured with a sample portfolio:
- **AAPL** (Apple Inc.)
- **GOOGL** (Alphabet Inc.)
- **MSFT** (Microsoft Corporation)
- **AMZN** (Amazon.com Inc.)
- **TSLA** (Tesla Inc.)

## 🔧 Customization

### **Adding New Risk Metrics**
Edit `market_risk_analysis.py` to add custom calculations:


## 🔍 Troubleshooting

### **Common Issues**

#### **Yahoo Finance Connection Error**
```bash
pip install --upgrade yfinance
```

#### **Missing Dependencies**
```bash
pip install -r requirements.txt
```

#### **Port Already in Use**
```bash
streamlit run dashboard.py --server.port 8502
```

### **Testing Installation**
Run the test script to verify everything works:
```bash
python test_installation.py
```

## 📈 Power BI Integration

1. **Export Data**: Use the dashboard's export buttons
2. **Import to Power BI**: Get Data → Text/CSV or Excel
3. **Create Visualizations**: Build your custom dashboard
4. **Set up Refresh**: Schedule automatic data updates


### **Development Setup**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
python -m pytest

