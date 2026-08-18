# slugany

[![CI](https://github.com/MathiasPaulenko/slugany/actions/workflows/ci.yml/badge.svg)](https://github.com/MathiasPaulenko/slugany/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/slugany.svg)](https://pypi.org/project/slugany/)
[![Python](https://img.shields.io/pypi/pyversions/slugany.svg)](https://pypi.org/project/slugany/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://github.com/MathiasPaulenko/slugany)

Slugify multi-idioma, zero dependencias. Alternativa simple a `python-slugify` sin arrastrar dependencias GPL.

## Features

- **Zero deps** — sin GPL, sin text-unidecode, sin UnicodeData más allá de la stdlib
- **Multi-idioma** — tablas propias para español, portugués, alemán, francés e italiano
- **Smart punctuation** — normaliza curly quotes, em-dash, NBSP, zero-width, bullets
- **Case styles** — kebab, snake, camel, pascal, dot, train, filename
- **CLI incluido** — `slugany "texto"` desde terminal con auto-stdin
- **lru_cache** — resultados cacheados automáticamente (maxsize=512)
- **Idempotente** — `slugify(slugify(x)) == slugify(x)` garantizado
- **~550 líneas core** — auditable, sin bloat

## Install

```bash
pip install slugany
```

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
# hello
```

## Styles

```python
slugify("hello world", style="kebab")    # "hello-world"
slugify("hello world", style="snake")    # "hello_world"
slugify("hello world", style="camel")    # "helloWorld"
slugify("hello world", style="pascal")   # "HelloWorld"
slugify("hello world", style="dot")      # "hello.world"
slugify("hello world", style="train")    # "Hello-World"
slugify("hello world", style="filename") # "Hello-World"
```

## Languages

```python
slugify("España", lang="es")             # "espana"
slugify("Coração", lang="pt")            # "coracao"
slugify("Über Straße", lang="de")        # "ueber-strasse"
slugify("Cœur", lang="fr")               # "coeur"
slugify("Caffè", lang="it")              # "caffe"
```

## Migration from python-slugify

slugany is a drop-in replacement with keyword-only arguments:

```python
# python-slugify
from slugify import slugify
slugify("Hello World", "_")

# slugany
from slugany import slugify
slugify("Hello World", separator="_")
```

## Why slugany?

| Aspect | python-slugify | slugany |
| ------ | -------------- | ------- |
| Dependencies | text-unidecode (GPL) | Zero |
| License | GPL | MIT |
| Multi-language | Limited | Built-in tables (es, pt, de, fr, it) |
| Caching | No | `lru_cache` built-in |
| Core size | ~1000+ lines | ~550 lines |

## License

MIT — see [LICENSE](LICENSE).
