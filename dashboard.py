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
from market_risk_analysis import MarketRiskAnalyzer

# Page configuration
st.set_page_config(
    page_title="Market Risk Analysis Dashboard",
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
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">📊 Market Risk Analysis Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.header("Portfolio Configuration")
    
    # Portfolio symbols input
    default_symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
    portfolio_symbols = st.sidebar.text_area(
        "Enter Stock Symbols (one per line):",
        value='\n'.join(default_symbols),
        height=150
    ).strip().split('\n')
    
    # Filter out empty symbols
    portfolio_symbols = [symbol.strip().upper() for symbol in portfolio_symbols if symbol.strip()]
    
    # Date range selection
    st.sidebar.subheader("Analysis Period")
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=start_date)
    with col2:
        end_date = st.date_input("End Date", value=end_date)
    
    # Market index selection
    market_index = st.sidebar.selectbox(
        "Market Index:",
        ['^GSPC', '^DJI', '^IXIC', '^RUT'],
        format_func=lambda x: {'^GSPC': 'S&P 500', '^DJI': 'Dow Jones', '^IXIC': 'NASDAQ', '^RUT': 'Russell 2000'}[x]
    )
    
    # Risk-free rate
    risk_free_rate = st.sidebar.slider("Risk-Free Rate (%)", 0.0, 10.0, 2.0, 0.1) / 100
    
    # Run analysis button
    if st.sidebar.button("🚀 Run Analysis", type="primary"):
        with st.spinner("Running market risk analysis..."):
            try:
                # Create analyzer instance
                analyzer = MarketRiskAnalyzer(
                    portfolio_symbols=portfolio_symbols,
                    market_index=market_index,
                    start_date=start_date.strftime('%Y-%m-%d'),
                    end_date=end_date.strftime('%Y-%m-%d')
                )
                
                # Run analysis
                analyzer.fetch_data()
                analyzer.calculate_returns()
                analyzer.calculate_all_metrics()
                
                # Store in session state
                st.session_state.analyzer = analyzer
                st.session_state.analysis_complete = True
                
                st.success("Analysis completed successfully!")
                
            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")
                st.session_state.analysis_complete = False
    
    # Main content
    if st.session_state.get('analysis_complete', False):
        analyzer = st.session_state.analyzer
        
        # Portfolio Overview
        st.header("📈 Portfolio Overview")
        
        # Key metrics in cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_return = sum([analyzer.risk_metrics[symbol]['total_return'] for symbol in portfolio_symbols if symbol in analyzer.risk_metrics]) / len(portfolio_symbols)
            st.metric("Portfolio Return", f"{total_return:.2%}")
        
        with col2:
            avg_volatility = sum([analyzer.risk_metrics[symbol]['volatility'] for symbol in portfolio_symbols if symbol in analyzer.risk_metrics and analyzer.risk_metrics[symbol]['volatility']]) / len(portfolio_symbols)
            st.metric("Avg Volatility", f"{avg_volatility:.2%}")
        
        with col3:
            avg_beta = sum([analyzer.risk_metrics[symbol]['beta'] for symbol in portfolio_symbols if symbol in analyzer.risk_metrics and analyzer.risk_metrics[symbol]['beta']]) / len(portfolio_symbols)
            st.metric("Avg Beta", f"{avg_beta:.3f}")
        
        with col4:
            avg_sharpe = sum([analyzer.risk_metrics[symbol]['sharpe_ratio'] for symbol in portfolio_symbols if symbol in analyzer.risk_metrics and analyzer.risk_metrics[symbol]['sharpe_ratio']]) / len(portfolio_symbols)
            st.metric("Avg Sharpe Ratio", f"{avg_sharpe:.3f}")
        
        # Price Performance Chart
        st.subheader("💰 Price Performance")
        
        # Create price performance chart
        fig_price = go.Figure()
        
        for symbol in portfolio_symbols:
            if symbol in analyzer.data:
                try:
                    # Get the appropriate price column
                    if isinstance(analyzer.data[symbol].columns, pd.MultiIndex):
                        # Multi-level columns
                        if ('Adj Close', symbol) in analyzer.data[symbol].columns:
                            prices = analyzer.data[symbol][('Adj Close', symbol)]
                        elif ('Close', symbol) in analyzer.data[symbol].columns:
                            prices = analyzer.data[symbol][('Close', symbol)]
                        else:
                            continue
                    else:
                        # Single-level columns
                        if 'Adj Close' in analyzer.data[symbol].columns:
                            prices = analyzer.data[symbol]['Adj Close']
                        elif 'Close' in analyzer.data[symbol].columns:
                            prices = analyzer.data[symbol]['Close']
                        else:
                            continue
                    
                    fig_price.add_trace(go.Scatter(
                        x=prices.index,
                        y=prices,
                        mode='lines',
                        name=symbol,
                        line=dict(width=2)
                    ))
                except Exception as e:
                    print(f"Error plotting {symbol}: {e}")
                    continue
        
        fig_price.update_layout(
            title="Stock Price Performance Over Time",
            xaxis_title="Date",
            yaxis_title="Adjusted Close Price ($)",
            hovermode='x unified',
            height=500
        )
        
        st.plotly_chart(fig_price, use_container_width=True)
        
        # Risk Metrics Table
        st.subheader("📊 Risk Metrics Summary")
        
        summary_df = analyzer.generate_summary_report()
        if summary_df is not None:
            # Style the dataframe
            def color_volatility(val):
                if pd.isna(val):
                    return ''
                # Handle both string and numeric values
                try:
                    if isinstance(val, str):
                        val = float(val.replace('%', ''))
                    else:
                        val = float(val)
                    
                    if val > 30:
                        return 'background-color: #ffcdd2'  # Red for high volatility
                    elif val > 20:
                        return 'background-color: #fff3e0'  # Orange for medium volatility
                    else:
                        return 'background-color: #c8e6c9'  # Green for low volatility
                except (ValueError, TypeError):
                    return ''
            
            def color_beta(val):
                if pd.isna(val):
                    return ''
                try:
                    val = float(val)
                    if val > 1.2:
                        return 'background-color: #ffcdd2'  # Red for high beta
                    elif val > 0.8:
                        return 'background-color: #fff3e0'  # Orange for medium beta
                    else:
                        return 'background-color: #c8e6c9'  # Green for low beta
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
                # Add reference line at beta = 1
                fig_beta.add_hline(y=1, line_dash="dash", line_color="red", annotation_text="Market Beta = 1")
                st.plotly_chart(fig_beta, use_container_width=True)
        
        # Returns Distribution
        st.subheader("📈 Returns Distribution")
        
        fig_returns = make_subplots(
            rows=2, cols=2,
            subplot_titles=[f"{symbol} Returns Distribution" for symbol in portfolio_symbols[:4]],
            specs=[[{"type": "histogram"}, {"type": "histogram"}],
                   [{"type": "histogram"}, {"type": "histogram"}]]
        )
        
        for i, symbol in enumerate(portfolio_symbols[:4]):
            if symbol in analyzer.returns:
                row = (i // 2) + 1
                col = (i % 2) + 1
                
                fig_returns.add_trace(
                    go.Histogram(
                        x=analyzer.returns[symbol],
                        name=symbol,
                        nbinsx=30,
                        opacity=0.7
                    ),
                    row=row, col=col
                )
        
        fig_returns.update_layout(height=600, showlegend=False)
        st.plotly_chart(fig_returns, use_container_width=True)
        
        # Correlation Matrix
        st.subheader("🔗 Correlation Matrix")
        
        if len(analyzer.returns) > 1:
            returns_df = pd.DataFrame(analyzer.returns)
            correlation_matrix = returns_df.corr()
            
            fig_corr = px.imshow(
                correlation_matrix,
                title="Returns Correlation Matrix",
                color_continuous_scale='RdBu',
                aspect='auto'
            )
            st.plotly_chart(fig_corr, use_container_width=True)
        
        # Export Section
        st.subheader("💾 Export Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Export to CSV"):
                analyzer.export_data()
                st.success("Data exported successfully! Check your working directory for CSV files.")
        
        with col2:
            if st.button("📈 Export to Excel"):
                # Export to Excel
                with pd.ExcelWriter('portfolio_risk_analysis.xlsx', engine='openpyxl') as writer:
                    summary_df.to_excel(writer, sheet_name='Risk_Summary', index=False)
                    
                    returns_df = pd.DataFrame(analyzer.returns)
                    returns_df.to_excel(writer, sheet_name='Daily_Returns', index=True)
                    
                    price_data = {}
                    for symbol in portfolio_symbols:
                        if symbol in analyzer.data:
                            try:
                                # Get the appropriate price column
                                if isinstance(analyzer.data[symbol].columns, pd.MultiIndex):
                                    # Multi-level columns
                                    if ('Adj Close', symbol) in analyzer.data[symbol].columns:
                                        price_data[symbol] = analyzer.data[symbol][('Adj Close', symbol)]
                                    elif ('Close', symbol) in analyzer.data[symbol].columns:
                                        price_data[symbol] = analyzer.data[symbol][('Close', symbol)]
                                    else:
                                        continue
                                else:
                                    # Single-level columns
                                    if 'Adj Close' in analyzer.data[symbol].columns:
                                        price_data[symbol] = analyzer.data[symbol]['Adj Close']
                                    elif 'Close' in analyzer.data[symbol].columns:
                                        price_data[symbol] = analyzer.data[symbol]['Close']
                                    else:
                                        continue
                            except Exception as e:
                                print(f"Error exporting price data for {symbol}: {e}")
                                continue
                    
                    if price_data:
                        price_df = pd.DataFrame(price_data)
                    else:
                        price_df = pd.DataFrame()
                    price_df.to_excel(writer, sheet_name='Price_Data', index=True)
                
                st.success("Data exported to Excel successfully!")
        
        # Instructions for Power BI
        st.subheader("🚀 Next Steps: Power BI Integration")
        st.markdown("""
        1. **Download the exported CSV/Excel files** from your working directory
        2. **Open Power BI Desktop**
        3. **Import the data** using "Get Data" → "Text/CSV" or "Excel"
        4. **Create visualizations**:
           - Line charts for price performance
           - Bar charts for volatility and beta comparison
           - Tables for risk metrics
           - KPIs for portfolio summary
        5. **Build your dashboard** with filters and slicers
        """)
    
    else:
        # Welcome message when no analysis has been run
        st.info("👈 Use the sidebar to configure your portfolio and click 'Run Analysis' to get started!")
        
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
        
        # Features overview
        st.subheader("✨ Dashboard Features")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **📊 Risk Metrics**
            - Volatility calculation
            - Beta analysis
            - Sharpe ratio
            - Value at Risk (VaR)
            - Maximum drawdown
            """)
        
        with col2:
            st.markdown("""
            **📈 Visualizations**
            - Price performance charts
            - Risk comparison plots
            - Returns distribution
            - Correlation matrix
            """)
        
        with col3:
            st.markdown("""
            **💾 Data Export**
            - CSV format
            - Excel format
            - Power BI ready
            - Tableau compatible
            """)

if __name__ == "__main__":
    main() 