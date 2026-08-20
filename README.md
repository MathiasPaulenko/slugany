# slugany

[![CI](https://github.com/MathiasPaulenko/slugany/actions/workflows/ci.yml/badge.svg)](https://github.com/MathiasPaulenko/slugany/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/slugany.svg)](https://pypi.org/project/slugany/)
[![Python](https://img.shields.io/pypi/pyversions/slugany.svg)](https://pypi.org/project/slugany/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://github.com/MathiasPaulenko/slugany)
[![Tests](https://img.shields.io/badge/tests-478%20passed-blue.svg)](https://github.com/MathiasPaulenko/slugany/actions/workflows/ci.yml)
[![mypy](https://img.shields.io/badge/mypy-strict%20%E2%9C%93-blue.svg)](https://github.com/MathiasPaulenko/slugany)
[![ruff](https://img.shields.io/badge/ruff-clean%20%E2%9C%93-blue.svg)](https://github.com/MathiasPaulenko/slugany)

A multi-language slugify library with zero runtime dependencies. MIT-licensed, fully typed, and audited for idempotency — a clean alternative to `python-slugify` with no GPL baggage.

> **478 tests · 100% coverage · `mypy --strict` clean · `ruff` clean · 13,800+ randomized idempotency checks passed**

## Why slugany?

`python-slugify` is the de facto standard, but it drags in `text-unidecode` (GPL) and over 1,000 lines of code. `slugany` was built from scratch to be:

| | python-slugify | unicode-slugify | slugany |
| --- | --- | --- | --- |
| **Runtime deps** | `text-unidecode` (GPL) | `unidecode` (GPL) | **Zero** |
| **License** | GPL | GPL | **MIT** |
| **Languages** | Limited | Limited | **Built-in: es, pt, de, fr, it** |
| **Caching** | No | No | **`lru_cache` built-in (512)** |
| **Typing** | Partial | Partial | **Fully typed, `py.typed` marker** |
| **Core size** | ~1,000+ lines | ~800 lines | **~550 lines** |
| **Idempotency** | Not guaranteed | Not guaranteed | **Guaranteed & tested** |
| **CLI** | Separate package | No | **Built-in** |
| **Style presets** | No | No | **8 built-in** |
| **Emoji handling** | No | No | **strip, text, keep** |
| **Confusables** | No | No | **Cyrillic + Greek** |
| **CSS-safe** | No | No | **Built-in** |
| **Smart punctuation** | No | No | **Built-in** |
| **HTML entities** | No | No | **Built-in** |
| **Fallback** | No | No | **Built-in** |

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
slugify("Hello 🎉 World", emoji_mode="text")   # "helloparty-popperworld"
slugify("Hello 🎉 World", emoji_mode="keep", allow_unicode=True)  # "hello-🎉-world"

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

## Slugifier — Reusable Builder Pattern

For high-throughput scenarios, create a `Slugifier` once and reuse it. Config validation happens once, not per call:

```python
from slugany import Slugifier

# Create once
s = Slugifier.style("camel", max_length=20, stopwords=["the", "a"])

# Reuse
s("The Quick Brown Fox")   # "quickBrownFox"
s("A Lazy Dog")            # "lazyDog"
s("Hello World")           # "helloWorld"

# Inspect config
s.config  # SlugConfig(style='camel', max_length=20, ...)
```

## FastAPI / Pydantic Integration

Use slugany with Pydantic for automatic slug generation in API models:

```python
from pydantic import BaseModel, field_validator
from slugany import slugify

class Article(BaseModel):
    title: str
    slug: str

    @field_validator("slug", mode="before")
    @classmethod
    def generate_slug(cls, v: str, info) -> str:
        if not v and info.data.get("title"):
            return slugify(info.data["title"], style="kebab")
        return slugify(v, style="kebab") if v else ""

article = Article(title="Hello World!", slug="")
print(article.slug)  # "hello-world"
```

### Slug type with Annotated

```python
from typing import Annotated
from pydantic import BaseModel, StringConstraints
from slugany import slugify, is_slug

Slug = Annotated[str, StringConstraints(pattern=r"^[a-z0-9]+(-[a-z0-9]+)*$")]

class Tag(BaseModel):
    name: str
    slug: Slug

    @field_validator("slug", mode="before")
    @classmethod
    def auto_slug(cls, v: str, info) -> str:
        return slugify(v or info.data.get("name", ""))

tag = Tag(name="Machine Learning", slug="")
print(tag.slug)  # "machine-learning"
```

### FastAPI query parameter

```python
from fastapi import FastAPI, Query
from slugany import slugify

app = FastAPI()

@app.get("/search")
async def search(q: str = Query(..., min_length=1)):
    slug = slugify(q, fallback="all")
    return {"query": q, "slug": slug}
```

## deconfuse — Standalone Utility

Replace confusable Unicode homoglyphs with Latin equivalents:

```python
from slugany import deconfuse

deconfuse("саfe")   # "cafe" — Cyrillic s → Latin c
deconfuse("αβγ")    # "abg"  — Greek → Latin
deconfuse("Hello")  # "Hello" — no change
```

`slugify()` applies deconfusion automatically. Use `deconfuse()` standalone when you need the raw replacement without full slugification.

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

### From unicode-slugify

```python
# unicode-slugify
from slugify import slugify
slugify("Hello World")

# slugany — same result, zero deps
from slugany import slugify
slugify("Hello World")  # "hello-world"
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
