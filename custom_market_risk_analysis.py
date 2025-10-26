import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class CustomMarketRiskAnalyzer:
    def __init__(self, portfolio_symbols, market_index='^GSPC', start_date=None, end_date=None):
        """
        Initialize the Custom Market Risk Analyzer
        
        Parameters:
        portfolio_symbols (list): List of stock symbols to analyze
        market_index (str): Market index symbol (default: S&P 500)
        start_date (str): Start date for analysis (format: YYYY-MM-DD)
        end_date (str): End date for analysis (format: YYYY-MM-DD)
        """
        self.portfolio_symbols = portfolio_symbols
        self.market_index = market_index
        self.start_date = start_date
        self.end_date = end_date
        self.data = {}
        self.returns = {}
        self.risk_metrics = {}
        
        # Validate dates
        self._validate_dates()
        
    def _validate_dates(self):
        """Validate the provided dates"""
        try:
            start_dt = datetime.strptime(self.start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(self.end_date, '%Y-%m-%d')
            
            if start_dt >= end_dt:
                raise ValueError("Start date must be before end date")
            
            if end_dt > datetime.now():
                raise ValueError("End date cannot be in the future")
            
            # Check if date range is reasonable
            days_diff = (end_dt - start_dt).days
            if days_diff < 30:
                print(f"Warning: Date range is only {days_diff} days. Consider using at least 30 days for meaningful analysis.")
            elif days_diff > 1825:  # 5 years
                print(f"Warning: Date range is {days_diff} days (over 5 years). This may take longer to process.")
                
        except ValueError as e:
            raise ValueError(f"Invalid date format or range: {e}")
    
    def get_price_column(self, symbol):
        """
        Get the appropriate price column for a symbol
        This ensures consistency between chart and metrics calculations
        """
        if symbol not in self.data:
            return None
            
        data = self.data[symbol]
        
        if isinstance(data.columns, pd.MultiIndex):
            if ('Adj Close', symbol) in data.columns:
                return ('Adj Close', symbol)
            elif ('Close', symbol) in data.columns:
                return ('Close', symbol)
            else:
                return None
        else:
            if 'Adj Close' in data.columns:
                return 'Adj Close'
            elif 'Close' in data.columns:
                return 'Close'
            else:
                return None
    
    def get_price_data(self, symbol):
        """
        Get price data for a symbol using consistent column selection
        """
        price_column = self.get_price_column(symbol)
        if price_column is None:
            return None
        return self.data[symbol][price_column]
    
    def fetch_data(self):
        """Fetch historical price data for portfolio and market index with enhanced error handling"""
        print("Fetching financial data...")
        print(f"Date range: {self.start_date} to {self.end_date}")
        
        successful_downloads = 0
        
        # Fetch market index data
        try:
            print(f"Downloading market index: {self.market_index}")
            market_data = yf.download(
                self.market_index, 
                start=self.start_date, 
                end=self.end_date, 
                progress=False,
                auto_adjust=True,
                prepost=True,
                threads=True
            )
            
            if not market_data.empty and len(market_data) > 5:
                self.data['market'] = market_data
                print(f"SUCCESS: Downloaded market data: {market_data.shape[0]} days")
            else:
                print(f"WARNING: Insufficient market data for {self.market_index}")
                
        except Exception as e:
            print(f"ERROR: Error downloading market data: {e}")
        
        # Fetch portfolio data
        for symbol in self.portfolio_symbols:
            try:
                print(f"Downloading {symbol}...")
                stock_data = yf.download(
                    symbol, 
                    start=self.start_date, 
                    end=self.end_date, 
                    progress=False,
                    auto_adjust=True,
                    prepost=True,
                    threads=True
                )
                
                if not stock_data.empty and len(stock_data) > 5:
                    self.data[symbol] = stock_data
                    successful_downloads += 1
                    print(f"SUCCESS: Downloaded data for {symbol}: {stock_data.shape[0]} days")
                    
                    # Show date range of downloaded data
                    if len(stock_data) > 0:
                        print(f"  Date range: {stock_data.index[0].date()} to {stock_data.index[-1].date()}")
                else:
                    print(f"WARNING: Insufficient data for {symbol} (got {len(stock_data)} days)")
                    
            except Exception as e:
                print(f"ERROR: Error downloading {symbol}: {e}")
                
        print(f"Data fetching completed! Successfully downloaded {successful_downloads}/{len(self.portfolio_symbols)} stocks")
        
        # Check if we have enough data to proceed
        if successful_downloads == 0:
            print("ERROR: No data downloaded! Please check your internet connection and try again.")
            return False
        elif successful_downloads < len(self.portfolio_symbols) // 2:
            print(f"WARNING: Only {successful_downloads} stocks downloaded. Analysis may be limited.")
        
        return True
        
    def calculate_returns(self):
        """Calculate daily returns for all assets with enhanced validation"""
        print("Calculating daily returns...")
        
        successful_calculations = 0
        for symbol, data in self.data.items():
            if not data.empty and len(data) > 5:
                try:
                    # Handle multi-level columns from yfinance
                    if isinstance(data.columns, pd.MultiIndex):
                        if ('Adj Close', symbol) in data.columns:
                            price_column = ('Adj Close', symbol)
                        elif ('Close', symbol) in data.columns:
                            price_column = ('Close', symbol)
                            print(f"WARNING: Using 'Close' instead of 'Adj Close' for {symbol}")
                        else:
                            print(f"ERROR: No price column found for {symbol}, skipping...")
                            continue
                    else:
                        if 'Adj Close' in data.columns:
                            price_column = 'Adj Close'
                        elif 'Close' in data.columns:
                            price_column = 'Close'
                            print(f"WARNING: Using 'Close' instead of 'Adj Close' for {symbol}")
                        else:
                            print(f"ERROR: No price column found for {symbol}, skipping...")
                            continue
                    
                    # Calculate daily returns
                    returns = data[price_column].pct_change().dropna()
                    
                    if len(returns) > 5:
                        self.returns[symbol] = returns
                        successful_calculations += 1
                        print(f"SUCCESS: Calculated returns for {symbol} using {price_column} ({len(returns)} returns)")
                        
                        # Show return statistics
                        print(f"  Mean return: {returns.mean():.4f} ({returns.mean()*100:.2f}%)")
                        print(f"  Std return: {returns.std():.4f} ({returns.std()*100:.2f}%)")
                    else:
                        print(f"WARNING: Insufficient return data for {symbol} ({len(returns)} returns)")
                    
                except Exception as e:
                    print(f"ERROR: Error calculating returns for {symbol}: {e}")
                    continue
            else:
                print(f"WARNING: Skipping {symbol} - no data available")
                
        print(f"Returns calculation completed! Successfully calculated {successful_calculations} returns")
        
        if successful_calculations == 0:
            print("ERROR: No returns calculated! Cannot proceed with analysis.")
            return False
        
        return True
        
    def calculate_volatility(self, symbol, period=252):
        """Calculate annualized volatility"""
        if symbol in self.returns:
            daily_vol = self.returns[symbol].std()
            annual_vol = daily_vol * np.sqrt(period)
            return annual_vol
        return None
        
    def calculate_beta(self, symbol):
        """Calculate beta relative to market"""
        if symbol in self.returns and 'market' in self.returns:
            # Align the returns by date
            stock_returns = self.returns[symbol]
            market_returns = self.returns['market']
            
            # Find common dates
            common_dates = stock_returns.index.intersection(market_returns.index)
            if len(common_dates) > 10:  # Need sufficient overlapping data
                stock_aligned = stock_returns.loc[common_dates]
                market_aligned = market_returns.loc[common_dates]
                
                # Calculate covariance and variance
                covariance = np.cov(stock_aligned, market_aligned)[0, 1]
                market_variance = np.var(market_aligned)
                
                if market_variance != 0:
                    beta = covariance / market_variance
                    return beta
        return None
        
    def calculate_sharpe_ratio(self, symbol, risk_free_rate=0.02, period=252):
        """Calculate Sharpe ratio"""
        if symbol in self.returns:
            excess_returns = self.returns[symbol] - (risk_free_rate / period)
            if excess_returns.std() != 0:
                sharpe = np.sqrt(period) * (excess_returns.mean() / excess_returns.std())
                return sharpe
        return None
        
    def calculate_var(self, symbol, confidence_level=0.05):
        """Calculate Value at Risk (VaR)"""
        if symbol in self.returns:
            var = np.percentile(self.returns[symbol], confidence_level * 100)
            return var
        return None
        
    def calculate_all_metrics(self):
        """Calculate all risk metrics for the portfolio"""
        print("Calculating risk metrics...")
        
        for symbol in self.portfolio_symbols:
            if symbol in self.returns:
                try:
                    # Use consistent method to get price data
                    price_data = self.get_price_data(symbol)
                    if price_data is None:
                        print(f"ERROR: No price data found for {symbol}, skipping metrics...")
                        continue
                    
                    # Calculate all metrics
                    metrics = {
                        'volatility': self.calculate_volatility(symbol),
                        'beta': self.calculate_beta(symbol),
                        'sharpe_ratio': self.calculate_sharpe_ratio(symbol),
                        'var_5%': self.calculate_var(symbol, 0.05),
                        'total_return': (price_data.iloc[-1] / price_data.iloc[0]) - 1,
                        'max_drawdown': self.calculate_max_drawdown(symbol)
                    }
                    
                    print(f"SUCCESS: Calculated metrics for {symbol}")
                    
                except Exception as e:
                    print(f"ERROR: Error calculating metrics for {symbol}: {e}")
                    continue
                self.risk_metrics[symbol] = metrics
                
        print("Risk metrics calculation completed!")
        
    def calculate_max_drawdown(self, symbol):
        """Calculate maximum drawdown"""
        if symbol in self.data:
            try:
                # Get the appropriate price column
                if isinstance(self.data[symbol].columns, pd.MultiIndex):
                    if ('Adj Close', symbol) in self.data[symbol].columns:
                        price_column = ('Adj Close', symbol)
                    elif ('Close', symbol) in self.data[symbol].columns:
                        price_column = ('Close', symbol)
                    else:
                        return None
                else:
                    if 'Adj Close' in self.data[symbol].columns:
                        price_column = 'Adj Close'
                    elif 'Close' in self.data[symbol].columns:
                        price_column = 'Close'
                    else:
                        return None
                
                prices = self.data[symbol][price_column]
                peak = prices.expanding(min_periods=1).max()
                drawdown = (prices - peak) / peak
                return drawdown.min()
            except Exception as e:
                print(f"ERROR: Error calculating max drawdown for {symbol}: {e}")
                return None
        return None
        
    def generate_summary_report(self):
        """Generate a summary report of all metrics"""
        if not self.risk_metrics:
            print("No risk metrics available. Run calculate_all_metrics() first.")
            return None
            
        summary_data = []
        for symbol, metrics in self.risk_metrics.items():
            summary_data.append({
                'Symbol': symbol,
                'Total Return (%)': round(metrics['total_return'] * 100, 2) if metrics['total_return'] is not None else None,
                'Volatility (%)': round(metrics['volatility'] * 100, 2) if metrics['volatility'] is not None else None,
                'Beta': round(metrics['beta'], 3) if metrics['beta'] is not None else None,
                'Sharpe Ratio': round(metrics['sharpe_ratio'], 3) if metrics['sharpe_ratio'] is not None else None,
                'VaR 5% (%)': round(metrics['var_5%'] * 100, 2) if metrics['var_5%'] is not None else None,
                'Max Drawdown (%)': round(metrics['max_drawdown'] * 100, 2) if metrics['max_drawdown'] is not None else None
            })
            
        return pd.DataFrame(summary_data)
        
    def export_data(self, filename='custom_portfolio_risk_data.csv'):
        """Export data to CSV file"""
        if not self.risk_metrics:
            print("No data to export. Run calculate_all_metrics() first.")
            return
            
        # Export risk metrics summary
        summary_df = self.generate_summary_report()
        summary_df.to_csv(filename, index=False)
        print(f"Risk metrics exported to {filename}")
        
        # Export detailed returns data
        returns_df = pd.DataFrame(self.returns)
        returns_filename = filename.replace('.csv', '_returns.csv')
        returns_df.to_csv(returns_filename)
        print(f"Returns data exported to {returns_filename}")
        
        # Export price data
        price_data = {}
        for symbol in self.portfolio_symbols:
            if symbol in self.data:
                try:
                    if isinstance(self.data[symbol].columns, pd.MultiIndex):
                        if ('Adj Close', symbol) in self.data[symbol].columns:
                            price_data[symbol] = self.data[symbol][('Adj Close', symbol)]
                        elif ('Close', symbol) in self.data[symbol].columns:
                            price_data[symbol] = self.data[symbol][('Close', symbol)]
                        else:
                            continue
                    else:
                        if 'Adj Close' in self.data[symbol].columns:
                            price_data[symbol] = self.data[symbol]['Adj Close']
                        elif 'Close' in self.data[symbol].columns:
                            price_data[symbol] = self.data[symbol]['Close']
                        else:
                            continue
                except Exception as e:
                    print(f"ERROR: Error exporting price data for {symbol}: {e}")
                    continue
        
        if price_data:
            price_df = pd.DataFrame(price_data)
            price_filename = filename.replace('.csv', '_prices.csv')
            price_df.to_csv(price_filename)
            print(f"Price data exported to {price_filename}")
        else:
            print("WARNING: No price data available for export")
        
    def run_analysis(self):
        """Run complete analysis pipeline"""
        print("Starting Custom Market Risk Analysis...")
        print("=" * 60)
        print(f"Portfolio: {', '.join(self.portfolio_symbols)}")
        print(f"Market Index: {self.market_index}")
        print(f"Date Range: {self.start_date} to {self.end_date}")
        print("=" * 60)
        
        # Step 1: Fetch data
        if not self.fetch_data():
            print("ERROR: Failed to fetch data. Analysis cannot proceed.")
            return None
        
        # Step 2: Calculate returns
        if not self.calculate_returns():
            print("ERROR: Failed to calculate returns. Analysis cannot proceed.")
            return None
        
        # Step 3: Calculate all metrics
        self.calculate_all_metrics()
        
        print("\nAnalysis Summary:")
        print("=" * 60)
        summary = self.generate_summary_report()
        if summary is not None and not summary.empty:
            print(summary.to_string(index=False))
        else:
            print("ERROR: No metrics could be calculated.")
            
        return summary

def main():
    """Main function to run the analysis"""
    # Define portfolio symbols
    portfolio_symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
    
    # Define date range
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    
    # Create analyzer instance
    analyzer = CustomMarketRiskAnalyzer(
        portfolio_symbols=portfolio_symbols,
        start_date=start_date,
        end_date=end_date
    )
    
    # Run analysis
    summary = analyzer.run_analysis()
    
    # Export data
    analyzer.export_data()
    
    print("\n" + "=" * 60)
    print("Analysis completed! Check the generated CSV files.")
    print("You can now import these files into Power BI or Tableau.")

if __name__ == "__main__":
    main()
