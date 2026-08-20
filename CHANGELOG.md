# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.2] - 2026-08-20

### Fixed

- Apply `ruff format` to `slugany/_steps.py` so the CI format check passes.

## [1.0.1] - 2026-08-20

### Fixed

- CLI stdio UTF-8 reconfiguration now uses `getattr` to satisfy mypy and `contextlib.suppress` to keep ruff happy.
- Wrapped the long test list in `test_mixed_case_idempotency_all_styles` to respect the 100-character line length.

## [1.0.0] - 2026-08-20

### Added

- Emoji `text` mode: replaces emojis with textual descriptions via `_EMOJI_TEXT` mapping table (100+ emojis)
- Emoji `keep` mode: preserves emojis in output with `allow_unicode=True` validation
- Greek-to-Latin confusable mappings in `_CONFUSABLES` (α→a, β→b, γ→g, etc.)
- `deconfuse()` public function for standalone Unicode homoglyph replacement
- `deconfuse` exported from `slugany` package (`__all__`)
- `Slugifier` class: stateless slugifier bound to a fixed configuration with `Slugifier.style()` factory
- `Slugifier.__call__` with `TypeError` on non-string input
- `Slugifier.__repr__` for debugging
- `Slugifier.config` read-only property exposing the frozen `SlugConfig`
- CSS-safe slug prefixing for camel, pascal, and train styles
- `_apply_css_safe` pipeline step (before `_apply_case_style`)
- `py.typed` marker (PEP 561) for type checker discovery
- `"Typing :: Typed"` classifier in `pyproject.toml`
- CI coverage enforcement at 100% (`--cov-fail-under=100`)
- Trusted publishing via `pypa/gh-action-pypi-publish@release/v1` with attestations
- Mkdocstrings API documentation with Google-style docstrings (Args, Returns, Raises, Examples)
- Comprehensive guide documentation: migration, performance, contracts
- README with badges (PyPI, CI, coverage, Python versions, License), 3-way comparison table (python-slugify vs unicode-slugify vs slugany)
- FastAPI/Pydantic integration examples in README
- Slugifier builder pattern examples in README
- CLI examples in README
- 478 tests with 100% coverage

### Changed

- `_handle_emoji` now supports three modes: `strip` (remove), `text` (replace with description), `keep` (preserve with `allow_unicode=True`)
- `_EMOJI_RE` regex expanded with additional ranges (U+2300-23FF, U+2B00-2BFF, U+1F000-1F0FF, etc.)
- Pipeline expanded to 18 steps (added `_apply_css_safe` and second `_truncate`/`_trim_separators` pass)
- `_CONFUSABLES` expanded with Greek uppercase and lowercase mappings
- All public function docstrings completed with Google-style Args, Returns, Raises, Examples sections
- README test count badge updated to 478
- Performance documentation updated with pipeline diagram, short-circuit optimization, and Slugifier reuse section
- Migration documentation expanded with full parameter mapping table and intentional differences section
- Contracts documentation expanded with case-insensitive stopwords, CSS-safe output, and multi-character separator contracts

### Fixed

- `_handle_emoji` multi-character emoji matching: iterates over each character in match group for `_EMOJI_TEXT` lookup
- `emoji_mode='keep'` now raises `ValueError` when `allow_unicode=False` instead of silently preserving emojis
- Greek letters αβγ now deconfused to `abg` before NFKD fallback (previously produced empty string)
- Emoji `text` mode correctly replaces emojis with descriptions before transliteration step

## [0.2.0] - 2026-08-20

### Added

- Language auto-detection: `lang='auto'` detects dominant language from Unicode code-point ranges (es, pt, de, fr, it) and selects the appropriate transliteration table
- Optional Pydantic `Slug` type: `Annotated[str, BeforeValidator]` that auto-slugifies string values in Pydantic models; falls back to `str` when pydantic is not installed
- `_LANG_DETECT_RANGES` table in `_tables.py` for language detection

### Fixed

- Pipeline order: `_trim_separators` now runs before `_truncate` to avoid trailing separators after truncation
- `word_boundary` truncation at exact separator position: returns full truncated text instead of losing a word when the boundary falls exactly at a separator
- `SlugConfig.from_kwargs` now rejects `bool` for `max_length` (Python `bool` is a subclass of `int`)
- `is_slug` with empty separator: avoids catastrophic backtracking (ReDoS) by using a simple character-class match
- CLI now catches `ValueError` and `TypeError` from slugify and prints to stderr with exit code 1 instead of an unhandled traceback

## [0.1.0] - 2026-08-19

### Added

- `slugify()` function with keyword-only API and `TypeError` on non-string input
- `slugify_batch()` for batch processing of multiple texts
- `is_slug()` validator with `allow_unicode` support
- `SlugConfig` frozen dataclass with `from_kwargs()` factory and style presets
- Transliteration tables for es, pt, de, fr, it
- Smart punctuation normalization (curly quotes, em-dash, NBSP, zero-width, bullets)
- HTML entity decoding (`&amp;` → `&`)
- Emoji stripping via regex
- Confusable character detection (Cyrillic → Latin)
- Case styles: kebab, snake, camel, pascal, dot, train, filename, url
- Stopwords removal
- Pre/post replacements (dict or iterable of tuples)
- `max_length` with optional `word_boundary` truncation
- `allow_unicode` mode to preserve non-ASCII characters
- `fallback` parameter for empty slug results
- `css_safe` mode to prefix digit-leading slugs
- `emoji_mode` (strip, text, keep)
- `html_entities` and `smart_punctuation` toggles
- `lru_cache` built-in (maxsize=512) with `cache_info()` and `cache_clear()`
- Pipeline architecture with 16 pure-function steps
- CLI with argparse, auto-stdin detection, and batch mode
- `py.typed` marker (PEP 561)
- CI/CD: lint (ruff), typecheck (mypy), test (3.11/3.12/3.13), release, docs
- MkDocs Material documentation with mkdocstrings API reference
- Idempotency, determinism, ASCII output, and no-double-separator contracts
- `SlugConfig` API reference page in documentation
- `CONTRIBUTING.md` with development setup, PR process, and code style guidelines
- `SECURITY.md` with vulnerability reporting policy
- `CODE_OF_CONDUCT.md` based on Contributor Covenant 2.1
- GitHub issue templates (bug report, feature request)
- GitHub pull request template with checklist
- Dependabot configuration for pip and GitHub Actions
- Documentation URL in `pyproject.toml` project URLs
- `__version__` attribute exported from package

### Changed

- `slugify()` and `slugify_batch()` parameters are now properly typed (no more `Any` sentinel pattern) — IDE autocompletion and type checking now work correctly for all 14 keyword arguments
- `slugify_batch()` now accepts explicit keyword arguments instead of `**kwargs: Any`
- `SlugConfig.from_kwargs()` no longer uses `type: ignore` comments — validation constants extracted to module-level `frozenset`s
- `_STYLE_PRESETS` and validation constants moved before `SlugConfig` class definition
- `is_slug()` now raises `TypeError` for non-string `separator` input
- CLI `_build_kwargs` return type changed from `dict[str, object]` to `dict[str, Any]` to eliminate `type: ignore` on `slugify` calls
- `pyproject.toml` description translated to English; license changed to SPDX expression with `license-files`
- README.md and docs/index.md translated from Spanish to English
- `mkdocs.yml` site description translated to English
- Development status classifier updated from Alpha to Beta
- Removed redundant `re.UNICODE` flag from `_UNICODE_ALNUM_RE` (default in Python 3)
- `_CONFIG_DEFAULTS` now computed from dataclass fields instead of hardcoded values (DRY)
- Fixed pipeline step count in documentation (16, not 17)
- Fixed benchmark numbers in performance documentation
- Fixed incorrect emoji_mode examples in README
- README expanded with advanced examples, documentation links, and contributing section
- `docs/index.md` rewritten as a proper landing page with feature list and navigation
- `CONTRIBUTING.md` updated with full dev setup (dev+docs) and Code of Conduct reference
- CI/CD workflows now use pip dependency caching

### Fixed

- Non-ASCII stopwords not transliterated before matching
- css_safe + max_length idempotency (pipeline reorder)
- train + max_length idempotency (double truncate)
- Unicode case boundary splitting for camel/pascal/train styles
- Case boundary splitting: digit-to-lowercase should not split
- Camel/pascal/train idempotency with consecutive uppercase letters
- Missing Cyrillic homoglyphs in _CONFUSABLES (в, к, м, н, т)
- Missing emoji ranges in _EMOJI_RE (U+2300-23FF, U+2B00-2BFF, etc.)
- Replacements double-application (pre/post split by ASCII/non-ASCII keys)
- CSS safe idempotency with camel/pascal/train styles
- Type validation for bool/int/str fields in from_kwargs
- Stopwords matching: non-alphanumeric chars stripped consistently
- Deconfuse skipped when allow_unicode=True
- Emoji mode text/keep preserving emojis through transliteration
- HTML entities, smart punctuation, transliteration interactions

### Removed

- `_verify.py` — redundant sanity-check script duplicated by the test suite
- `docs/changelog.md` — duplicate of root `CHANGELOG.md`; mkdocs now references the original
