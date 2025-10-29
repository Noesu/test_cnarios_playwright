# MUI Automated Testing Framework

A modern, robust test automation framework for testing MUI (Material-UI) components using Python, Playwright, and 
Allure Reports.

## Features

- **Component Testing**: Comprehensive testing for MUI components
- **Cross-browser Support**: Powered by Playwright (to be implemented)
- **Beautiful Reporting**: Allure integration for detailed test reports
- **Page Object Pattern**: Clean, maintainable test structure
- **Parallel Execution**: Support for parallel test runs (to be implemented)
- **Async Support**: Async/await pattern for better performance (to be implemented)

## Prerequisites

- Python 3.13 (framework developed on 3.13, should work on 3.8+ but not fully tested)
- Git

##  Installation

1. **Clone the repository**
```bash
git clone [repository-url]
cd test-cnarios-playwright
```

2. **Install dependencies**
```bash
poetry install
```

3. **Install Playwright browsers**
```bash
poetry run playwright install
```

## Running tests
   
### **Run tests with auto-opened Allure report**
```bash
poetry run pytest tests/
```