#!/usr/bin/env python3
"""
Test script to verify Market Risk Analysis Dashboard installation
Run this script to check if all dependencies are properly installed
"""

import sys
import importlib

def test_imports():
    """Test if all required packages can be imported"""
    required_packages = [
        'pandas',
        'numpy',
        'yfinance',
        'matplotlib',
        'seaborn',
        'streamlit',
        'plotly',
        'openpyxl',
        'scipy'
    ]
    
    print("🔍 Testing package imports...")
    print("=" * 50)
    
    failed_imports = []
    
    for package in required_packages:
        try:
            module = importlib.import_module(package)
            version = getattr(module, '__version__', 'Unknown')
            print(f"✓ {package:<15} - Version: {version}")
        except ImportError as e:
            print(f"✗ {package:<15} - FAILED: {e}")
            failed_imports.append(package)
    
    print("=" * 50)
    
    if failed_imports:
        print(f"\n❌ {len(failed_imports)} package(s) failed to import:")
        for package in failed_imports:
            print(f"   - {package}")
        print("\n💡 Solution: Run 'pip install -r requirements.txt'")
        return False
    else:
        print("\n✅ All packages imported successfully!")
        return True

def test_yfinance_connection():
    """Test if yfinance can connect to Yahoo Finance"""
    print("\n🌐 Testing Yahoo Finance connection...")
    print("=" * 50)
    
    try:
        import yfinance as yf
        import datetime
        
        # Use dynamic dates - last 10 days to ensure we get trading days
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=10)
        
        print(f"Testing data download from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}...")
        
        # Try with SPY first (more reliable than individual stocks)
        data = yf.download('SPY', start=start_date, end=end_date, progress=False)
        
        if not data.empty and len(data) > 0:
            print("✅ Successfully downloaded data from Yahoo Finance")
            print(f"   Downloaded {len(data)} rows of data")
            return True
        else:
            print("❌ No data received from Yahoo Finance")
            return False
            
    except Exception as e:
        print(f"❌ Failed to connect to Yahoo Finance: {e}")
        return False

def test_python_version():
    """Check Python version compatibility"""
    print("\n🐍 Checking Python version...")
    print("=" * 50)
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("✅ Python version is compatible (3.8+)")
        return True
    else:
        print("❌ Python version 3.8+ is required")
        return False

def test_file_access():
    """Test if required files are accessible"""
    print("\n📁 Testing file access...")
    print("=" * 50)
    
    required_files = [
        'market_risk_analysis.py',
        'dashboard.py',
        'requirements.txt',
        'config.py'
    ]
    
    missing_files = []
    
    for filename in required_files:
        try:
            with open(filename, 'r') as f:
                print(f"✅ {filename} - Accessible")
        except FileNotFoundError:
            print(f"❌ {filename} - NOT FOUND")
            missing_files.append(filename)
    
    if missing_files:
        print(f"\n❌ {len(missing_files)} file(s) missing:")
        for filename in missing_files:
            print(f"   - {filename}")
        return False
    else:
        print("\n✅ All required files are accessible!")
        return True

def main():
    """Run all tests"""
    print("🚀 Market Risk Analysis Dashboard - Installation Test")
    print("=" * 60)
    
    tests = [
        ("Python Version", test_python_version),
        ("File Access", test_file_access),
        ("Package Imports", test_imports),
        ("Yahoo Finance Connection", test_yfinance_connection)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} {status}")
    
    print("=" * 60)
    print(f"Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your system is ready to run the dashboard.")
        print("\nTo start the dashboard, run:")
        print("   streamlit run dashboard.py")
        print("\nOr use the provided batch files:")
        print("   run_dashboard.bat (Windows)")
        print("   run_dashboard.ps1 (PowerShell)")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please fix the issues above.")
        print("\nCommon solutions:")
        print("1. Install missing packages: pip install -r requirements.txt")
        print("2. Check internet connection for Yahoo Finance test")
        print("3. Ensure all files are in the same directory")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 