# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-08-18

### Added

- `slugify()` function with keyword-only API
- Transliteration tables for es, pt, fr, de, it
- Smart punctuation normalization (curly quotes, em-dash, NBSP, zero-width)
- Empty-slug fallback parameter
- Case styles: kebab, snake, camel, pascal, dot, train
- CLI with auto-stdin detection
- `is_slug()` validator
- `lru_cache` built-in (maxsize=512)
- `slugify_batch()` for batch processing
- Idempotency, determinism, and no-double-separator contracts
- `SlugConfig` frozen dataclass
- Pipeline architecture with 16 pure-function steps
