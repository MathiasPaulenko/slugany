# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
