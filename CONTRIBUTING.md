# Contributing to Hybrid BCI Wheelchair

Thank you for your interest in contributing to this project! This document provides guidelines for contributions.

## Ways to Contribute

1. **Bug Reports**: Report issues via GitHub Issues
2. **Feature Requests**: Suggest new features or improvements
3. **Code Contributions**: Submit pull requests with bug fixes or new features
4. **Documentation**: Improve or expand documentation
5. **Testing**: Test on different hardware configurations and report results

## Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
git clone https://github.com/YOUR-USERNAME/hybrid-bci-wheelchair.git
cd hybrid-bci-wheelchair
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows

# Install dependencies with dev tools
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

## Development Guidelines

### Code Style

- Follow **PEP 8** style guide
- Use **type hints** where appropriate
- Write **docstrings** for all public functions and classes
- Keep line length to **100 characters** maximum

Format code with Black:

```bash
black src/ scripts/ tests/
```

Lint with flake8:

```bash
flake8 src/ scripts/ tests/ --max-line-length=100
```

### Testing

- Write tests for all new features
- Ensure existing tests pass
- Aim for >80% code coverage

Run tests:

```bash
pytest tests/ -v
```

Run with coverage:

```bash
pytest tests/ --cov=src/hybrid_bci --cov-report=html
```

### Documentation

- Update README.md if adding new features
- Add docstrings to new functions/classes
- Update API.md for public API changes
- Include usage examples

### Commit Messages

Use clear, descriptive commit messages:

```
feat: Add support for custom motor PWM frequencies
fix: Resolve ultrasonic sensor timeout issue
docs: Update hardware setup guide with voltage divider
test: Add tests for blink detection edge cases
refactor: Simplify motor controller initialization
```

Prefixes:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test additions or modifications
- `refactor`: Code refactoring
- `style`: Formatting, no code change
- `perf`: Performance improvements
- `chore`: Maintenance tasks

## Pull Request Process

1. **Update Tests**: Ensure all tests pass
2. **Update Documentation**: Reflect your changes in docs
3. **Update CHANGELOG**: Add entry describing changes (if applicable)
4. **Create PR**: Submit pull request with clear description
5. **Code Review**: Respond to feedback from maintainers
6. **Merge**: After approval, PR will be merged

### PR Checklist

- [ ] Code follows project style guidelines
- [ ] Tests added/updated and passing
- [ ] Documentation updated
- [ ] No linting errors
- [ ] Commit messages are clear
- [ ] Branch is up to date with master

## Hardware Testing

If you're testing hardware modifications:

1. **Safety First**: Follow all safety guidelines
2. **Document Setup**: Include hardware details in PR
3. **Test Results**: Provide test data or videos
4. **Compatibility**: Note any hardware-specific requirements

## Reporting Issues

When reporting bugs, include:

- **Environment**: OS, Python version, hardware
- **Steps to Reproduce**: Detailed reproduction steps
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Logs/Errors**: Relevant error messages or logs
- **Screenshots**: If applicable

## Feature Requests

For feature requests, describe:

- **Use Case**: Why is this feature needed?
- **Proposed Solution**: How should it work?
- **Alternatives**: Other approaches considered
- **Additional Context**: Any other relevant information

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior

- Harassment or discriminatory language
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information

## Questions?

If you have questions:

- **General Questions**: Open a GitHub Discussion
- **Bug Reports**: Open a GitHub Issue
- **Security Issues**: Contact maintainers directly

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be acknowledged in:
- CONTRIBUTORS.md file (if we create one)
- Release notes for significant contributions
- Project documentation where appropriate

Thank you for contributing to making BCI technology more accessible!

