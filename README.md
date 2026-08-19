# slugany

[![CI](https://github.com/MathiasPaulenko/slugany/actions/workflows/ci.yml/badge.svg)](https://github.com/MathiasPaulenko/slugany/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/slugany.svg)](https://pypi.org/project/slugany/)
[![Python](https://img.shields.io/pypi/pyversions/slugany.svg)](https://pypi.org/project/slugany/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://github.com/MathiasPaulenko/slugany)
[![Tests](https://img.shields.io/badge/tests-381%20passed-blue.svg)](https://github.com/MathiasPaulenko/slugany/actions/workflows/ci.yml)
[![mypy](https://img.shields.io/badge/mypy-strict%20%E2%9C%93-blue.svg)](https://github.com/MathiasPaulenko/slugany)
[![ruff](https://img.shields.io/badge/ruff-clean%20%E2%9C%93-blue.svg)](https://github.com/MathiasPaulenko/slugany)

A multi-language slugify library with zero runtime dependencies. MIT-licensed, fully typed, and audited for idempotency — a clean alternative to `python-slugify` with no GPL baggage.

> **381 tests · 100% coverage · `mypy --strict` clean · `ruff` clean · 13,800+ randomized idempotency checks passed**

## Why slugany?

`python-slugify` is the de facto standard, but it drags in `text-unidecode` (GPL) and over 1,000 lines of code. `slugany` was built from scratch to be:

| | python-slugify | slugany |
| --- | --- | --- |
| **Runtime deps** | `text-unidecode` (GPL) | **Zero** |
| **License** | GPL | **MIT** |
| **Languages** | Limited | **Built-in: es, pt, de, fr, it** |
| **Caching** | No | **`lru_cache` built-in (512)** |
| **Typing** | Partial | **Fully typed, `py.typed` marker** |
| **Core size** | ~1,000+ lines | **~550 lines** |
| **Idempotency** | Not guaranteed | **Guaranteed & tested** |
| **CLI** | Separate package | **Built-in** |

## Features

- **Zero runtime deps** — only the Python standard library
- **Multi-language transliteration** — Spanish, Portuguese, German, French, Italian
- **8 case styles** — kebab, snake, camel, pascal, dot, train, filename, url
- **Smart punctuation** — normalizes curly quotes, em-dashes, NBSP, zero-width chars, bullets
- **HTML entity decoding** — `&amp;` → `&` before processing
- **Emoji handling** — strip, keep, or convert to text
- **Confusable detection** — Cyrillic homoglyphs → Latin equivalents
- **Stopwords removal** — filter out common words per language
- **Custom replacements** — pre- and post-pipeline string substitution
- **CSS-safe slugs** — prefix digit-leading slugs with `s-`
- **Max length with word boundaries** — truncate without breaking words
- **Unicode preservation** — `allow_unicode=True` keeps non-ASCII chars
- **Fallback for empty slugs** — never get an empty string
- **Built-in `lru_cache`** — results cached automatically (maxsize=512)
- **CLI with stdin support** — pipe text directly: `echo "text" | slugany`
- **Idempotent** — `slugify(slugify(x)) == slugify(x)`, guaranteed and tested
- **Fully typed** — type hints on every public API, `py.typed` marker (PEP 561)
- **~550 lines core** — auditable, no bloat

## Installation

```bash
pip install slugany
```

Requires Python 3.11+. No runtime dependencies.

## Quickstart

```python
from slugany import slugify

slugify("¡Hola Mundo!")            # "hola-mundo"
slugify("Café résumé naïve")       # "cafe-resume-naive"
slugify("Ñandú coração")           # "nandu-coracao"
slugify("Über Straße", lang="de")  # "ueber-strasse"
slugify("Hello 🎉 World")          # "hello-world"
```

## CLI

```bash
# Basic usage
slugany "Hello World"
# hello-world

# Pipe from stdin
echo "Café" | slugany
# cafe

# Case styles
slugany "hello world" --style camel
# helloWorld

slugany "hello world" --style train
# Hello-World

# Truncation with word boundary
slugany "hello-world-foo-bar" --max-length 10 --word-boundary
# hello-world

# Batch mode (one slug per line)
slugany --batch < input.txt

# CSS-safe slugs
slugany "123 main st" --css-safe
# s-123-main-st
```

## Case Styles

```python
slugify("hello world", style="kebab")     # "hello-world"
slugify("hello world", style="snake")     # "hello_world"
slugify("hello world", style="camel")     # "helloWorld"
slugify("hello world", style="pascal")    # "HelloWorld"
slugify("hello world", style="dot")       # "hello.world"
slugify("hello world", style="train")     # "Hello-World"
slugify("hello world", style="filename")  # "Hello-World"
slugify("hello world", style="url")       # "hello-world"
```

## Languages

Built-in transliteration tables for five languages:

```python
slugify("España", lang="es")          # "espana"
slugify("Coração", lang="pt")         # "coracao"
slugify("Über Straße", lang="de")     # "ueber-strasse"
slugify("Cœur", lang="fr")            # "coeur"
slugify("Caffè", lang="it")           # "caffe"
```

## Advanced

```python
from slugany import slugify, slugify_batch, is_slug

# Stopwords — remove common words
slugify("the quick brown fox", stopwords=["the", "fox"])  # "quick-brown"

# Custom replacements — substitute before and after transliteration
slugify("hello world", replacements={"hello": "hi"})  # "hi-world"
slugify("Straße", replacements={"ß": "ss"})           # "strass"

# Emoji handling
slugify("Hello 🎉 World", emoji_mode="strip")  # "hello-world"
slugify("Hello 🎉 World", emoji_mode="keep")   # "hello-world"

# CSS-safe — prefix digit-leading slugs for CSS class names
slugify("123 main st", css_safe=True)  # "s-123-main-st"

# Fallback — never get an empty string
slugify("!!!", fallback="untitled")  # "untitled"

# Unicode preservation — keep non-ASCII characters
slugify("Ñandú", allow_unicode=True)  # "ñandú"

# Max length with word boundary — truncate without breaking words
slugify("hello world foo bar", max_length=15, word_boundary=True)  # "hello-world"

# Batch processing
slugify_batch(["Hello World", "Café Résumé"])  # ["hello-world", "cafe-resume"]

# Validation
is_slug("hello-world")              # True
is_slug("hello world")              # False
is_slug("hello_world", separator="_")  # True
is_slug("hello-wörld", allow_unicode=True)  # True

# Cache inspection
from slugany import slugify
slugify.cache_info()   # CacheInfo(hits=0, misses=1, maxsize=512, currsize=1)
slugify.cache_clear()  # Clear the cache
```

## Migration from python-slugify

slugany is designed as a drop-in replacement. The main difference is that all arguments are keyword-only:

```python
# python-slugify
from slugify import slugify
slugify("Hello World", "_")
slugify("Hello World", separator="_", stopwords=["the"])

# slugany
from slugany import slugify
slugify("Hello World", separator="_")
slugify("Hello World", separator="_", stopwords=["the"])
```

See the [migration guide](https://mathiaspaulenko.github.io/slugany/guide/migration/) for full details.

## Documentation

Full documentation at **[mathiaspaulenko.github.io/slugany](https://mathiaspaulenko.github.io/slugany/)**

- [Basic usage](https://mathiaspaulenko.github.io/slugany/usage/basic/)
- [Styles & presets](https://mathiaspaulenko.github.io/slugany/usage/styles/)
- [Languages](https://mathiaspaulenko.github.io/slugany/usage/languages/)
- [CLI reference](https://mathiaspaulenko.github.io/slugany/usage/cli/)
- [API reference](https://mathiaspaulenko.github.io/slugany/api/slugify/)
- [Contracts & guarantees](https://mathiaspaulenko.github.io/slugany/guide/contracts/)
- [Performance](https://mathiaspaulenko.github.io/slugany/guide/performance/)

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, PR process, and code style guidelines.

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before participating.

## License

MIT — see [LICENSE](LICENSE).
