# slugany

[![CI](https://github.com/MathiasPaulenko/slugany/actions/workflows/ci.yml/badge.svg)](https://github.com/MathiasPaulenko/slugany/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/slugany.svg)](https://pypi.org/project/slugany/)
[![Python](https://img.shields.io/pypi/pyversions/slugany.svg)](https://pypi.org/project/slugany/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://github.com/MathiasPaulenko/slugany)

Multi-language slugify with zero dependencies. A simple, MIT-licensed alternative to `python-slugify`.

## Features

- **Zero deps** — no GPL, no text-unidecode, no UnicodeData beyond the stdlib
- **Multi-language** — built-in tables for Spanish, Portuguese, German, French, and Italian
- **Smart punctuation** — normalizes curly quotes, em-dashes, NBSP, zero-width characters, bullets
- **Case styles** — kebab, snake, camel, pascal, dot, train, filename
- **CLI included** — `slugany "text"` from the terminal with auto-stdin
- **lru_cache** — results cached automatically (maxsize=512)
- **Idempotent** — `slugify(slugify(x)) == slugify(x)` guaranteed
- **Fully typed** — type hints on every public API, `py.typed` marker included
- **~550 lines core** — auditable, no bloat

## Installation

```bash
pip install slugany
```

Requires Python 3.11 or later. No runtime dependencies.

## Quickstart

```python
from slugany import slugify

slugify("¡Hola Mundo!")        # "hola-mundo"
slugify("Café résumé naïve")   # "cafe-resume-naive"
slugify("Ñandú coração")       # "nandu-coracao"
slugify("Über Straße", lang="de")  # "ueber-strasse"
```

## CLI

```bash
slugany "Hello World"
# hello-world

echo "Café" | slugany
# cafe

slugany "hello world" --style camel
# helloWorld

slugany "hello-world-foo" --max-length 10 --word-boundary
# hello-world
```

## Styles

```python
slugify("hello world", style="kebab")    # "hello-world"
slugify("hello world", style="snake")    # "hello_world"
slugify("hello world", style="camel")    # "helloWorld"
slugify("hello world", style="pascal")   # "HelloWorld"
slugify("hello world", style="dot")      # "hello.world"
slugify("hello world", style="train")    # "Hello-World"
slugify("Hello World", style="filename") # "Hello-World"
```

## Languages

```python
slugify("España", lang="es")             # "espana"
slugify("Coração", lang="pt")            # "coracao"
slugify("Über Straße", lang="de")        # "ueber-strasse"
slugify("Cœur", lang="fr")               # "coeur"
slugify("Caffè", lang="it")              # "caffe"
```

## Advanced

```python
# Stopwords
slugify("the quick brown fox", stopwords=["the", "fox"])  # "quick-brown"

# Custom replacements
slugify("hello world", replacements={"hello": "hi"})  # "hi-world"

# Emoji handling
slugify("Hello \U0001f389 World", emoji_mode="strip")  # "hello-world"
slugify("Hello \U0001f389 World", emoji_mode="keep")   # "hello-world"

# CSS-safe (prefix digit-leading slugs)
slugify("123 main st", css_safe=True)  # "s-123-main-st"

# Fallback for empty results
slugify("!!!", fallback="untitled")  # "untitled"

# Unicode preservation
slugify("\u00d1and\u00fa", allow_unicode=True)  # "\u00f1and\u00fa"

# Batch processing
from slugany import slugify_batch
slugify_batch(["Hello World", "Caf\u00e9 R\u00e9sum\u00e9"])  # ["hello-world", "cafe-resume"]

# Validation
from slugany import is_slug
is_slug("hello-world")   # True
is_slug("hello world")   # False
is_slug("hello_world", separator="_")  # True
```

## Migration from python-slugify

slugany is designed as a drop-in replacement with keyword-only arguments:

```python
# python-slugify
from slugify import slugify
slugify("Hello World", "_")

# slugany
from slugany import slugify
slugify("Hello World", separator="_")
```

See the [migration guide](https://mathiaspaulenko.github.io/slugany/guide/migration/) for full details.

## Why slugany?

| Aspect | python-slugify | slugany |
| ------ | -------------- | ------- |
| Dependencies | text-unidecode (GPL) | Zero |
| License | GPL | MIT |
| Multi-language | Limited | Built-in tables (es, pt, de, fr, it) |
| Caching | No | `lru_cache` built-in |
| Core size | ~1000+ lines | ~550 lines |

## Documentation

Full documentation is available at [mathiaspaulenko.github.io/slugany](https://mathiaspaulenko.github.io/slugany/).

- [Basic usage](https://mathiaspaulenko.github.io/slugany/usage/basic/)
- [Styles & presets](https://mathiaspaulenko.github.io/slugany/usage/styles/)
- [Languages](https://mathiaspaulenko.github.io/slugany/usage/languages/)
- [CLI reference](https://mathiaspaulenko.github.io/slugany/usage/cli/)
- [API reference](https://mathiaspaulenko.github.io/slugany/api/slugify/)
- [Contracts & guarantees](https://mathiaspaulenko.github.io/slugany/guide/contracts/)

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before participating in the community.

## License

MIT — see [LICENSE](LICENSE).
