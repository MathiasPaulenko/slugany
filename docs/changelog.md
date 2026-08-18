# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- Replacements now stored as `tuple` instead of `frozenset` to preserve insertion order — chained replacements like `[('a', 'b'), ('b', 'c')]` are now deterministic
- `_apply_case_style` now filters empty words to prevent trailing separators when truncation produces partial words (e.g. `slugify('hello-world-foo', style='train', max_length=6)` no longer produces `'Hello-'`)
- Pipeline reordered: `_truncate` now runs before `_trim_separators` so truncation can't reintroduce trailing separators
- `_trim_separators` now trims partial trailing/leading separators after truncation with multi-character separators (e.g. `separator='--'` with `max_length=5` no longer produces `'æu-'`)
- Default transliteration table added for NFKD-resistant characters: `ß`→`ss`, `Æ`→`AE`, `æ`→`ae`, `Œ`→`OE`, `œ`→`oe`, `Ð`→`D`, `ð`→`d`, `Þ`→`TH`, `þ`→`th` — these are now transliterated for all languages, not just when a specific `lang` is selected

### Added

- `SlugConfig` API reference page in documentation

## [0.1.0] - 2026-08-18

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
- Pipeline architecture with 17 pure-function steps
- CLI with argparse, auto-stdin detection, and batch mode
- `py.typed` marker (PEP 561)
- CI/CD: lint (ruff), typecheck (mypy), test (3.11/3.12/3.13), release, docs
- MkDocs Material documentation with mkdocstrings API reference
- Idempotency, determinism, ASCII output, and no-double-separator contracts
