# 🤝 Contributing to Market Risk Analysis Dashboard

Thank you for your interest in contributing to our project! This document provides guidelines and information for contributors.

## 🚀 Quick Start

1. **Fork the repository**
2. **Clone your fork**: `git clone https://github.com/yourusername/market-risk-dashboard.git`
3. **Create a branch**: `git checkout -b feature/amazing-feature`
4. **Make your changes**
5. **Test your changes**: `python test_installation.py`
6. **Commit**: `git commit -m 'Add amazing feature'`
7. **Push**: `git push origin feature/amazing-feature`
8. **Open a Pull Request**

## 📋 Development Setup

### Prerequisites
- Python 3.8+
- Git
- pip

### Local Development Environment
```bash
# Clone the repository
git clone https://github.com/yourusername/market-risk-dashboard.git
cd market-risk-dashboard

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8 pre-commit

# Install pre-commit hooks
pre-commit install
```

## 🧪 Testing

### Run Tests
```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=./ --cov-report=html

# Run specific test file
python -m pytest test_installation.py

# Run with verbose output
python -m pytest -v
```

### Test Installation
```bash
python test_installation.py
```

### Test Dashboard
```bash
streamlit run dashboard.py
```

## 🔧 Code Quality

### Code Formatting
We use **Black** for code formatting:
```bash
# Format all Python files
black .

# Check formatting without changing files
black --check --diff .
```

### Linting
We use **flake8** for linting:
```bash
# Run linter
flake8 .

# Run with specific rules
flake8 . --max-line-length=127 --ignore=E203,W503
```

### Pre-commit Hooks
Pre-commit hooks automatically run formatting and linting on commit:
```bash
# Install pre-commit hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## 📝 Code Style Guidelines

### Python Code
- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions under 50 lines
- Use type hints where appropriate

### Example
```python
def calculate_volatility(returns: pd.Series, period: int = 252) -> float:
    """
    Calculate annualized volatility.
    
    Args:
        returns: Daily returns series
        period: Number of trading days in a year
        
    Returns:
        Annualized volatility as float
    """
    daily_vol = returns.std()
    annual_vol = daily_vol * np.sqrt(period)
    return annual_vol
```

### Documentation
- Update README.md for new features
- Add docstrings to new functions
- Include examples in documentation
- Update requirements.txt for new dependencies

## 🎯 Areas for Contribution

### High Priority
- **Bug fixes**: Fix reported issues
- **Performance improvements**: Optimize calculations
- **Error handling**: Improve robustness
- **Testing**: Add more test coverage

### Medium Priority
- **New risk metrics**: Add additional financial ratios
- **UI improvements**: Enhance dashboard appearance
- **Data sources**: Add alternative data providers
- **Export formats**: Support more file types

### Low Priority
- **Documentation**: Improve guides and examples
- **Code refactoring**: Clean up existing code
- **Examples**: Add sample portfolios and use cases

## 🐛 Reporting Issues

### Before Reporting
1. Check existing issues for duplicates
2. Search documentation for solutions
3. Test with the latest version

### Issue Template
```markdown
**Description**
Brief description of the issue

**Steps to Reproduce**
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., Windows 10, macOS 12]
- Python: [e.g., 3.9.7]
- Version: [e.g., 1.0.0]

**Additional Information**
Any other context, logs, or screenshots
```

## 🔄 Pull Request Process

### Before Submitting
1. **Test thoroughly**: Ensure all tests pass
2. **Update documentation**: Update README, docstrings
3. **Check formatting**: Run Black and flake8
4. **Test dashboard**: Verify dashboard works correctly

### PR Template
```markdown
**Description**
Brief description of changes

**Type of Change**
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

**Testing**
- [ ] All tests pass
- [ ] Dashboard works correctly
- [ ] No new warnings

**Screenshots**
If applicable, add screenshots

**Checklist**
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
```

### Review Process
1. **Automated checks** must pass
2. **Code review** by maintainers
3. **Testing** on different environments
4. **Documentation** review
5. **Final approval** and merge

## 🏷️ Versioning

We use [Semantic Versioning](https://semver.org/):
- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

## 📞 Getting Help

### Communication Channels
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and general discussion
- **Pull Requests**: Code contributions

### Resources
- [Python Documentation](https://docs.python.org/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Financial Risk Management](https://www.investopedia.com/)

## 🎉 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to Market Risk Analysis Dashboard! 🚀📊** 