import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class MarketRiskAnalyzer:
    def __init__(self, portfolio_symbols, market_index='^GSPC', start_date=None, end_date=None):
        """
        Initialize the Market Risk Analyzer
        
        Parameters:
        portfolio_symbols (list): List of stock symbols to analyze
        market_index (str): Market index symbol (default: S&P 500)
        start_date (str): Start date for analysis (default: 1 year ago)
        end_date (str): End date for analysis (default: today)
        """
        self.portfolio_symbols = portfolio_symbols
        self.market_index = market_index
        self.start_date = start_date or (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        self.end_date = end_date or datetime.now().strftime('%Y-%m-%d')
        self.data = {}
        self.returns = {}
        self.risk_metrics = {}
        
    def fetch_data(self):
        """Fetch historical price data for portfolio and market index"""
        print("Fetching financial data...")
        
        # Fetch market index data
        market_data = yf.download(self.market_index, start=self.start_date, end=self.end_date)
        self.data['market'] = market_data
        
        # Fetch portfolio data
        for symbol in self.portfolio_symbols:
            try:
                stock_data = yf.download(symbol, start=self.start_date, end=self.end_date)
                self.data[symbol] = stock_data
                
                if not stock_data.empty:
                    print(f"✓ Downloaded data for {symbol}")
                    print(f"  Columns: {list(stock_data.columns)}")
                    print(f"  Shape: {stock_data.shape}")
                    print(f"  Date range: {stock_data.index[0]} to {stock_data.index[-1]}")
                else:
                    print(f"⚠️  Downloaded empty data for {symbol}")
                    
            except Exception as e:
                print(f"✗ Error downloading {symbol}: {e}")
                
        print("Data fetching completed!")
        
    def calculate_returns(self):
        """Calculate daily returns for all assets"""
        print("Calculating daily returns...")
        
        for symbol, data in self.data.items():
            if not data.empty:
                try:
                    # Handle multi-level columns from yfinance
                    if isinstance(data.columns, pd.MultiIndex):
                        # Multi-level columns: ('Close', 'AAPL'), ('High', 'AAPL'), etc.
                        if ('Adj Close', symbol) in data.columns:
                            price_column = ('Adj Close', symbol)
                        elif ('Close', symbol) in data.columns:
                            price_column = ('Close', symbol)
                            print(f"⚠️  Using 'Close' instead of 'Adj Close' for {symbol}")
                        else:
                            print(f"❌ No price column found for {symbol}, skipping...")
                            continue
                    else:
                        # Single-level columns: 'Close', 'High', 'Low', etc.
                        if 'Adj Close' in data.columns:
                            price_column = 'Adj Close'
                        elif 'Close' in data.columns:
                            price_column = 'Close'
                            print(f"⚠️  Using 'Close' instead of 'Adj Close' for {symbol}")
                        else:
                            print(f"❌ No price column found for {symbol}, skipping...")
                            continue
                    
                    # Calculate daily returns using available price column
                    returns = data[price_column].pct_change().dropna()
                    self.returns[symbol] = returns
                    print(f"✓ Calculated returns for {symbol} using {price_column}")
                    
                except Exception as e:
                    print(f"❌ Error calculating returns for {symbol}: {e}")
                    continue
                
        print("Returns calculation completed!")
        
    def calculate_volatility(self, symbol, period=252):
        """
        Calculate annualized volatility
        
        Parameters:
        symbol (str): Stock symbol
        period (int): Number of trading days in a year (default: 252)
        
        Returns:
        float: Annualized volatility
        """
        if symbol in self.returns:
            daily_vol = self.returns[symbol].std()
            annual_vol = daily_vol * np.sqrt(period)
            return annual_vol
        return None
        
    def calculate_beta(self, symbol):
        """
        Calculate beta relative to market
        
        Parameters:
        symbol (str): Stock symbol
        
        Returns:
        float: Beta value
        """
        if symbol in self.returns and 'market' in self.returns:
            # Calculate covariance and variance
            covariance = np.cov(self.returns[symbol], self.returns['market'])[0, 1]
            market_variance = np.var(self.returns['market'])
            
            if market_variance != 0:
                beta = covariance / market_variance
                return beta
        return None
        
    def calculate_sharpe_ratio(self, symbol, risk_free_rate=0.02, period=252):
        """
        Calculate Sharpe ratio
        
        Parameters:
        symbol (str): Stock symbol
        risk_free_rate (float): Risk-free rate (default: 2%)
        period (int): Number of trading days in a year
        
        Returns:
        float: Sharpe ratio
        """
        if symbol in self.returns:
            excess_returns = self.returns[symbol] - (risk_free_rate / period)
            sharpe = np.sqrt(period) * (excess_returns.mean() / excess_returns.std())
            return sharpe
        return None
        
    def calculate_var(self, symbol, confidence_level=0.05):
        """
        Calculate Value at Risk (VaR)
        
        Parameters:
        symbol (str): Stock symbol
        confidence_level (float): Confidence level (default: 5%)
        
        Returns:
        float: VaR value
        """
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
                    # Get the appropriate price column
                    if isinstance(self.data[symbol].columns, pd.MultiIndex):
                        # Multi-level columns
                        if ('Adj Close', symbol) in self.data[symbol].columns:
                            price_column = ('Adj Close', symbol)
                        elif ('Close', symbol) in self.data[symbol].columns:
                            price_column = ('Close', symbol)
                        else:
                            print(f"❌ No price column found for {symbol}, skipping metrics...")
                            continue
                    else:
                        # Single-level columns
                        if 'Adj Close' in self.data[symbol].columns:
                            price_column = 'Adj Close'
                        elif 'Close' in self.data[symbol].columns:
                            price_column = 'Close'
                        else:
                            print(f"❌ No price column found for {symbol}, skipping metrics...")
                            continue
                    
                    metrics = {
                        'volatility': self.calculate_volatility(symbol),
                        'beta': self.calculate_beta(symbol),
                        'sharpe_ratio': self.calculate_sharpe_ratio(symbol),
                        'var_5%': self.calculate_var(symbol, 0.05),
                        'total_return': (self.data[symbol][price_column].iloc[-1] / self.data[symbol][price_column].iloc[0]) - 1,
                        'max_drawdown': self.calculate_max_drawdown(symbol)
                    }
                except Exception as e:
                    print(f"❌ Error calculating metrics for {symbol}: {e}")
                    continue
                self.risk_metrics[symbol] = metrics
                
        print("Risk metrics calculation completed!")
        
    def calculate_max_drawdown(self, symbol):
        """Calculate maximum drawdown"""
        if symbol in self.data:
            try:
                # Get the appropriate price column
                if isinstance(self.data[symbol].columns, pd.MultiIndex):
                    # Multi-level columns
                    if ('Adj Close', symbol) in self.data[symbol].columns:
                        price_column = ('Adj Close', symbol)
                    elif ('Close', symbol) in self.data[symbol].columns:
                        price_column = ('Close', symbol)
                    else:
                        return None
                else:
                    # Single-level columns
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
                print(f"❌ Error calculating max drawdown for {symbol}: {e}")
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
                'Total Return (%)': round(metrics['total_return'] * 100, 2),
                'Volatility (%)': round(metrics['volatility'] * 100, 2) if metrics['volatility'] else None,
                'Beta': round(metrics['beta'], 3) if metrics['beta'] else None,
                'Sharpe Ratio': round(metrics['sharpe_ratio'], 3) if metrics['sharpe_ratio'] else None,
                'VaR 5% (%)': round(metrics['var_5%'] * 100, 2) if metrics['var_5%'] else None,
                'Max Drawdown (%)': round(metrics['max_drawdown'] * 100, 2) if metrics['max_drawdown'] else None
            })
            
        return pd.DataFrame(summary_data)
        
    def export_data(self, filename='portfolio_risk_data.csv'):
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
                    # Get the appropriate price column
                    if isinstance(self.data[symbol].columns, pd.MultiIndex):
                        # Multi-level columns
                        if ('Adj Close', symbol) in self.data[symbol].columns:
                            price_column = ('Adj Close', symbol)
                        elif ('Close', symbol) in self.data[symbol].columns:
                            price_column = ('Close', symbol)
                        else:
                            continue
                    else:
                        # Single-level columns
                        if 'Adj Close' in self.data[symbol].columns:
                            price_column = 'Adj Close'
                        elif 'Close' in self.data[symbol].columns:
                            price_column = 'Close'
                        else:
                            continue
                    
                    price_data[symbol] = self.data[symbol][price_column]
                except Exception as e:
                    print(f"❌ Error exporting price data for {symbol}: {e}")
                    continue
        
        if price_data:
            price_df = pd.DataFrame(price_data)
            price_filename = filename.replace('.csv', '_prices.csv')
            price_df.to_csv(price_filename)
            print(f"Price data exported to {price_filename}")
        else:
            print("⚠️  No price data available for export")
        
    def run_analysis(self):
        """Run complete analysis pipeline"""
        print("Starting Market Risk Analysis...")
        print("=" * 50)
        
        self.fetch_data()
        self.calculate_returns()
        self.calculate_all_metrics()
        
        print("\nAnalysis Summary:")
        print("=" * 50)
        summary = self.generate_summary_report()
        if summary is not None:
            print(summary.to_string(index=False))
            
        return summary

def main():
    """Main function to run the analysis"""
    # Define portfolio symbols (you can modify this list)
    portfolio_symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
    
    # Create analyzer instance
    analyzer = MarketRiskAnalyzer(portfolio_symbols)
    
    # Run analysis
    summary = analyzer.run_analysis()
    
    # Export data
    analyzer.export_data()
    
    print("\n" + "=" * 50)
    print("Analysis completed! Check the generated CSV files.")
    print("You can now import these files into Power BI or Tableau.")

if __name__ == "__main__":
    main() 