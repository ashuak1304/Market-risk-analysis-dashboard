import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
import warnings
warnings.filterwarnings('ignore')

# Import our custom analyzer
from custom_market_risk_analysis import CustomMarketRiskAnalyzer

# Page configuration
st.set_page_config(
    page_title="Custom Market Risk Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .risk-high { color: #d62728; }
    .risk-medium { color: #ff7f0e; }
    .risk-low { color: #2ca02c; }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def validate_date_range(start_date, end_date):
    """Validate the date range"""
    if start_date >= end_date:
        return False, "Start date must be before end date"
    
    if end_date > datetime.now().date():
        return False, "End date cannot be in the future"
    
    # Check if date range is too short (less than 30 days)
    if (end_date - start_date).days < 30:
        return False, "Date range should be at least 30 days for meaningful analysis"
    
    # Check if date range is too long (more than 5 years)
    if (end_date - start_date).days > 1825:  # 5 years
        return False, "Date range should not exceed 5 years"
    
    return True, "Valid date range"

def test_yfinance_connection():
    """Test yfinance connection with a simple download"""
    try:
        # Test with a simple download
        test_data = yf.download("AAPL", period="5d", progress=False)
        if not test_data.empty:
            return True, "Connection successful"
        else:
            return False, "No data returned from Yahoo Finance"
    except Exception as e:
        return False, f"Connection failed: {str(e)}"

def main():
    # Header
    st.markdown('<h1 class="main-header">📊 Custom Market Risk Analysis Dashboard</h1>', unsafe_allow_html=True)
    
    # Test connection first
    st.subheader("🔗 Connection Test")
    if st.button("Test Yahoo Finance Connection"):
        with st.spinner("Testing connection..."):
            success, message = test_yfinance_connection()
            if success:
                st.success(f"✅ {message}")
            else:
                st.error(f"❌ {message}")
    
    # Sidebar
    st.sidebar.header("📋 Portfolio Configuration")
    
    # Portfolio symbols input
    default_symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
    portfolio_symbols = st.sidebar.text_area(
        "Enter Stock Symbols (one per line):",
        value='\n'.join(default_symbols),
        height=150,
        help="Enter stock symbols one per line. Examples: AAPL, GOOGL, MSFT"
    ).strip().split('\n')
    
    # Filter out empty symbols
    portfolio_symbols = [symbol.strip().upper() for symbol in portfolio_symbols if symbol.strip()]
    
    # Date range selection with validation
    st.sidebar.subheader("📅 Analysis Period")
    
    # Default dates
    end_date_default = datetime.now().date()
    start_date_default = end_date_default - timedelta(days=365)
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date", 
            value=start_date_default,
            max_value=datetime.now().date(),
            help="Select the start date for analysis"
        )
    with col2:
        end_date = st.date_input(
            "End Date", 
            value=end_date_default,
            max_value=datetime.now().date(),
            help="Select the end date for analysis"
        )
    
    # Date validation
    is_valid, validation_message = validate_date_range(start_date, end_date)
    if not is_valid:
        st.sidebar.error(f"⚠️ {validation_message}")
    else:
        st.sidebar.success(f"✅ {validation_message}")
    
    # Market index selection
    market_index = st.sidebar.selectbox(
        "Market Index:",
        ['^GSPC', '^DJI', '^IXIC', '^RUT'],
        format_func=lambda x: {
            '^GSPC': 'S&P 500', 
            '^DJI': 'Dow Jones', 
            '^IXIC': 'NASDAQ', 
            '^RUT': 'Russell 2000'
        }[x],
        help="Select the market index for beta calculation"
    )
    
    # Risk-free rate
    risk_free_rate = st.sidebar.slider(
        "Risk-Free Rate (%)", 
        0.0, 10.0, 2.0, 0.1,
        help="Risk-free rate for Sharpe ratio calculation"
    ) / 100
    
    # Display selected configuration
    st.sidebar.subheader("📊 Selected Configuration")
    st.sidebar.write(f"**Stocks:** {', '.join(portfolio_symbols)}")
    st.sidebar.write(f"**Period:** {start_date} to {end_date}")
    st.sidebar.write(f"**Market Index:** {market_index}")
    st.sidebar.write(f"**Risk-Free Rate:** {risk_free_rate:.1%}")
    
    # Run analysis button
    if st.sidebar.button("🚀 Run Analysis", type="primary", disabled=not is_valid):
        if not portfolio_symbols:
            st.error("Please enter at least one stock symbol")
        else:
            with st.spinner("Running market risk analysis..."):
                try:
                    # Create analyzer instance
                    analyzer = CustomMarketRiskAnalyzer(
                        portfolio_symbols=portfolio_symbols,
                        market_index=market_index,
                        start_date=start_date.strftime('%Y-%m-%d'),
                        end_date=end_date.strftime('%Y-%m-%d')
                    )
                    
                    # Run analysis with better error handling
                    st.info("📡 Fetching data from Yahoo Finance...")
                    success = analyzer.fetch_data()
                    
                    if success:
                        st.info("📊 Calculating returns...")
                        success = analyzer.calculate_returns()
                        
                        if success:
                            st.info("⚡ Calculating risk metrics...")
                            analyzer.calculate_all_metrics()
                            
                            # Store in session state
                            st.session_state.analyzer = analyzer
                            st.session_state.analysis_complete = True
                            st.session_state.analysis_date_range = f"{start_date} to {end_date}"
                            
                            st.success("✅ Analysis completed successfully!")
                        else:
                            st.error("❌ Failed to calculate returns. Please check your data.")
                            st.session_state.analysis_complete = False
                    else:
                        st.error("❌ Failed to fetch data. Please check your internet connection and try again.")
                        st.session_state.analysis_complete = False
                        
                except Exception as e:
                    st.error(f"❌ Error during analysis: {str(e)}")
                    st.session_state.analysis_complete = False
    
    # Main content
    if st.session_state.get('analysis_complete', False):
        analyzer = st.session_state.analyzer
        
        # Analysis Summary Header
        st.header("📈 Analysis Results")
        st.markdown(f"""
        <div class="success-box">
            <h4>✅ Analysis Completed Successfully</h4>
            <p><strong>Date Range:</strong> {st.session_state.get('analysis_date_range', 'N/A')}</p>
            <p><strong>Stocks Analyzed:</strong> {', '.join(portfolio_symbols)}</p>
            <p><strong>Market Index:</strong> {market_index}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Portfolio Overview Metrics
        st.subheader("📊 Portfolio Overview")
        
        # Create 4 columns for key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_return = sum([analyzer.risk_metrics[symbol]['total_return'] 
                              for symbol in portfolio_symbols 
                              if symbol in analyzer.risk_metrics]) / len(portfolio_symbols)
            st.metric("Portfolio Return", f"{total_return:.2%}")
        
        with col2:
            avg_volatility = sum([analyzer.risk_metrics[symbol]['volatility'] 
                                for symbol in portfolio_symbols 
                                if symbol in analyzer.risk_metrics 
                                and analyzer.risk_metrics[symbol]['volatility']]) / len(portfolio_symbols)
            st.metric("Avg Volatility", f"{avg_volatility:.2%}")
        
        with col3:
            avg_beta = sum([analyzer.risk_metrics[symbol]['beta'] 
                          for symbol in portfolio_symbols 
                          if symbol in analyzer.risk_metrics 
                          and analyzer.risk_metrics[symbol]['beta']]) / len(portfolio_symbols)
            st.metric("Avg Beta", f"{avg_beta:.3f}")
        
        with col4:
            avg_sharpe = sum([analyzer.risk_metrics[symbol]['sharpe_ratio'] 
                            for symbol in portfolio_symbols 
                            if symbol in analyzer.risk_metrics 
                            and analyzer.risk_metrics[symbol]['sharpe_ratio']]) / len(portfolio_symbols)
            st.metric("Avg Sharpe Ratio", f"{avg_sharpe:.3f}")
        
        # Price Performance Chart
        st.subheader("💰 Price Performance")
        
        # Add debugging information
        with st.expander("🔍 Debug Information"):
            st.write("**Data Consistency Check:**")
            for symbol in portfolio_symbols:
                if symbol in analyzer.data and symbol in analyzer.risk_metrics:
                    # Use the consistent method to get price data
                    prices = analyzer.get_price_data(symbol)
                    if prices is None:
                        st.write(f"**{symbol}:** No price data available")
                        continue
                    
                    price_column = analyzer.get_price_column(symbol)
                    manual_return = (prices.iloc[-1] / prices.iloc[0]) - 1
                    stored_return = analyzer.risk_metrics[symbol]['total_return']
                    
                    st.write(f"**{symbol}:**")
                    st.write(f"- Price column: {price_column}")
                    st.write(f"- First price: ${prices.iloc[0]:.2f}")
                    st.write(f"- Last price: ${prices.iloc[-1]:.2f}")
                    st.write(f"- Manual calculation: {manual_return:.2%}")
                    st.write(f"- Stored metric: {stored_return:.2%}")
                    st.write(f"- Match: {'✓' if abs(manual_return - stored_return) < 0.001 else '✗'}")
        
        fig_price = go.Figure()
        
        for symbol in portfolio_symbols:
            if symbol in analyzer.data:
                try:
                    # Use the consistent method to get price data
                    prices = analyzer.get_price_data(symbol)
                    if prices is None:
                        st.warning(f"No price data available for {symbol}")
                        continue
                    
                    fig_price.add_trace(go.Scatter(
                        x=prices.index,
                        y=prices,
                        mode='lines',
                        name=symbol,
                        line=dict(width=2)
                    ))
                except Exception as e:
                    st.warning(f"Could not plot {symbol}: {e}")
                    continue
        
        fig_price.update_layout(
            title=f"Stock Price Performance ({start_date} to {end_date})",
            xaxis_title="Date",
            yaxis_title="Adjusted Close Price ($)",
            hovermode='x unified',
            height=500
        )
        
        st.plotly_chart(fig_price, use_container_width=True)
        
        # Risk Metrics Table
        st.subheader("📊 Risk Metrics Summary")
        
        summary_df = analyzer.generate_summary_report()
        if summary_df is not None and not summary_df.empty:
            # Color coding functions for risk levels
            def color_volatility(val):
                if pd.isna(val):
                    return ''
                try:
                    if isinstance(val, str):
                        val = float(val.replace('%', ''))
                    else:
                        val = float(val)
                    
                    if val > 30:
                        return 'background-color: #ffcdd2'  # Red
                    elif val > 20:
                        return 'background-color: #fff3e0'  # Orange
                    else:
                        return 'background-color: #c8e6c9'  # Green
                except (ValueError, TypeError):
                    return ''
            
            def color_beta(val):
                if pd.isna(val):
                    return ''
                try:
                    val = float(val)
                    if val > 1.2:
                        return 'background-color: #ffcdd2'  # Red
                    elif val > 0.8:
                        return 'background-color: #fff3e0'  # Orange
                    else:
                        return 'background-color: #c8e6c9'  # Green
                except (ValueError, TypeError):
                    return ''
            
            styled_df = summary_df.style.applymap(color_volatility, subset=['Volatility (%)']).applymap(color_beta, subset=['Beta'])
            st.dataframe(styled_df, use_container_width=True)
        
        # Risk Analysis Charts
        st.subheader("🎯 Risk Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Volatility Comparison
            volatility_data = []
            symbols = []
            for symbol in portfolio_symbols:
                if symbol in analyzer.risk_metrics and analyzer.risk_metrics[symbol]['volatility']:
                    volatility_data.append(analyzer.risk_metrics[symbol]['volatility'] * 100)
                    symbols.append(symbol)
            
            if volatility_data:
                fig_vol = px.bar(
                    x=symbols,
                    y=volatility_data,
                    title="Annualized Volatility by Stock",
                    labels={'x': 'Stock Symbol', 'y': 'Volatility (%)'},
                    color=volatility_data,
                    color_continuous_scale='RdYlGn_r'
                )
                st.plotly_chart(fig_vol, use_container_width=True)
        
        with col2:
            # Beta Comparison
            beta_data = []
            symbols = []
            for symbol in portfolio_symbols:
                if symbol in analyzer.risk_metrics and analyzer.risk_metrics[symbol]['beta']:
                    beta_data.append(analyzer.risk_metrics[symbol]['beta'])
                    symbols.append(symbol)
            
            if beta_data:
                fig_beta = px.bar(
                    x=symbols,
                    y=beta_data,
                    title="Beta by Stock (vs Market)",
                    labels={'x': 'Stock Symbol', 'y': 'Beta'},
                    color=beta_data,
                    color_continuous_scale='RdYlGn'
                )
                fig_beta.add_hline(y=1, line_dash="dash", line_color="red", annotation_text="Market Beta = 1")
                st.plotly_chart(fig_beta, use_container_width=True)
        
        # Export Section
        st.subheader("💾 Export Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Export to CSV"):
                analyzer.export_data()
                st.success("Data exported successfully! Check your working directory for CSV files.")
        
        with col2:
            if st.button("📈 Export to Excel"):
                try:
                    with pd.ExcelWriter('custom_portfolio_analysis.xlsx', engine='openpyxl') as writer:
                        summary_df.to_excel(writer, sheet_name='Risk_Summary', index=False)
                        
                        returns_df = pd.DataFrame(analyzer.returns)
                        returns_df.to_excel(writer, sheet_name='Daily_Returns', index=True)
                        
                        # Export price data
                        price_data = {}
                        for symbol in portfolio_symbols:
                            if symbol in analyzer.data:
                                try:
                                    if isinstance(analyzer.data[symbol].columns, pd.MultiIndex):
                                        if ('Adj Close', symbol) in analyzer.data[symbol].columns:
                                            price_data[symbol] = analyzer.data[symbol][('Adj Close', symbol)]
                                        elif ('Close', symbol) in analyzer.data[symbol].columns:
                                            price_data[symbol] = analyzer.data[symbol][('Close', symbol)]
                                        else:
                                            continue
                                    else:
                                        if 'Adj Close' in analyzer.data[symbol].columns:
                                            price_data[symbol] = analyzer.data[symbol]['Adj Close']
                                        elif 'Close' in analyzer.data[symbol].columns:
                                            price_data[symbol] = analyzer.data[symbol]['Close']
                                        else:
                                            continue
                                except Exception as e:
                                    st.warning(f"Could not export price data for {symbol}: {e}")
                                    continue
                        
                        if price_data:
                            price_df = pd.DataFrame(price_data)
                            price_df.to_excel(writer, sheet_name='Price_Data', index=True)
                    
                    st.success("Data exported to Excel successfully!")
                except Exception as e:
                    st.error(f"Error exporting to Excel: {e}")
    
    else:
        # Welcome message when no analysis has been run
        st.info("👈 Use the sidebar to configure your portfolio and click 'Run Analysis' to get started!")
        
        # Instructions
        st.subheader("📋 How to Use This Dashboard")
        st.markdown("""
        1. **Enter Stock Symbols**: Add the stocks you want to analyze (one per line)
        2. **Select Date Range**: Choose your analysis period (minimum 30 days, maximum 5 years)
        3. **Choose Market Index**: Select the benchmark for beta calculation
        4. **Set Risk-Free Rate**: Adjust for Sharpe ratio calculations
        5. **Click Run Analysis**: The dashboard will fetch data and calculate metrics
        
        **Note**: Make sure you have a stable internet connection for data fetching.
        """)
        
        # Sample portfolio example
        st.subheader("📋 Sample Portfolio")
        st.markdown("""
        The dashboard will analyze stocks like:
        - **AAPL** (Apple Inc.)
        - **GOOGL** (Alphabet Inc.)
        - **MSFT** (Microsoft Corporation)
        - **AMZN** (Amazon.com Inc.)
        - **TSLA** (Tesla Inc.)
        
        You can modify this list in the sidebar to analyze any stocks you're interested in!
        """)

if __name__ == "__main__":
    main()
