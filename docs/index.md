# slugany

Multi-language slugify with zero dependencies. A simple, MIT-licensed alternative
to `python-slugify` without GPL dependencies.

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

## Next steps

- [Basic usage](usage/basic.md)
- [Styles & presets](usage/styles.md)
- [Languages](usage/languages.md)
- [CLI reference](usage/cli.md)
- [API reference](api/slugify.md)
- [Migration from python-slugify](guide/migration.md)
- [Contracts & guarantees](guide/contracts.md)
