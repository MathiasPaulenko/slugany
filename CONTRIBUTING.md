# Contributing to slugany

Thank you for your interest in contributing to slugany! This document
outlines the process for contributing to the project.

## Development setup

```bash
git clone https://github.com/MathiasPaulenko/slugany.git
cd slugany
pip install -e ".[dev,docs]"
```

## Running checks

Before submitting a pull request, ensure all checks pass:

```bash
ruff check slugany/ tests/
ruff format --check slugany/ tests/
mypy --strict slugany/
pytest tests/
```

## Pull request process

1. Create a feature branch from `main`.
2. Make your changes with clear, descriptive commit messages.
3. Add or update tests to maintain 100% coverage.
4. Ensure all checks pass (ruff, mypy, pytest).
5. Update the CHANGELOG.md under the `[Unreleased]` section.
6. Open a pull request with a clear description of the changes.

## Code style

- Follow PEP 8, PEP 257, and PEP 484.
- Use `ruff` for linting and formatting.
- Use type hints for all public APIs.
- Keep functions small and focused (single responsibility).
- Write docstrings for all public functions, classes, and methods.

## Testing

- Maintain 100% test coverage.
- Write tests that are readable, deterministic, and independent.
- Use descriptive test method names (`test_<behavior>`).
- Test edge cases: empty input, None, invalid types, boundary conditions.

## Changelog

Follow the [Keep a Changelog](https://keepachangelog.com/) format.
Entries go under `[Unreleased]` until a release is cut.

## License

By contributing, you agree that your contributions will be licensed
under the MIT License.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).
