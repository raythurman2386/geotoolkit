# Contributing to GeoToolKit

First off, thank you for considering contributing to GeoToolKit! It's people like you that make GeoToolKit such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* Use a clear and descriptive title
* Describe the exact steps which reproduce the problem
* Provide specific examples to demonstrate the steps
* Describe the behavior you observed after following the steps
* Explain which behavior you expected to see instead and why
* Include screenshots if possible
* Include your environment details:
    * OS version
    * Python version
    * GeoToolKit version
    * GDAL version
    * Other relevant package versions

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* A clear and descriptive title
* A detailed description of the proposed functionality
* Explain why this enhancement would be useful
* List any additional dependencies that might be required
* Include mockups or examples if applicable

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code follows the existing style
6. Issue that pull request!

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/raythurman2386/geotoolkit.git
cd geotoolkit
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install development dependencies:
```bash
pip install -e ".[dev,docs]"
```

4. Install pre-commit hooks:
```bash
pre-commit install
```

## Development Process

1. Create a new branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and commit:
```bash
git add .
git commit -m "Description of your changes"
```

3. Push to your fork:
```bash
git push origin feature/your-feature-name
```

4. Create a Pull Request

## Testing

Run the test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=geotoolkit tests/
```

## Documentation

Build the documentation:
```bash
cd docs
make html
```

## Style Guide

* Follow PEP 8 guidelines
* Use type hints
* Write docstrings in Google format
* Keep line length to 88 characters (Black default)
* Sort imports using isort

## Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

## Additional Notes

### Documentation Style

* Use clear, concise language
* Include code examples
* Document both successful and error cases
* Include type hints in examples
* Provide real-world use cases

### Version Control Workflow

1. Feature Development
    * Create feature branch
    * Develop and test
    * Submit PR

2. Bug Fixes
    * Create bug fix branch
    * Fix and test
    * Submit PR

3. Documentation
    * Create docs branch
    * Update documentation
    * Submit PR

## Questions?

Feel free to contact the project maintainers if you have any questions or need help getting started.