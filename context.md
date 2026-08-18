# slugany — Context

## What

Slugify multi-idioma, zero dependencias. Alternativa simple a `python-slugify` sin arrastrar dependencias GPL.

```python
from slugany import slugify

slugify("¡Hola Mundo!")  # "hola-mundo"
slugify("Café résumé naïve")  # "cafe-resume-naive"
slugify("Ñandú coração")  # "nandu-coracao"
```

## Why

`python-slugify` (8.0.4, ~1.4M downloads/month) es el estándar pero arrastra `text-unidecode` (GPL) como dependencia obligatoria. Muchos proyectos comerciales no pueden usar deps GPL. `slugany` resuelve eso: transliteración built-in, zero deps, licencia MIT.

## Stack

- Python >=3.11
- hatchling (build backend)
- Zero runtime dependencies
- Dev: pytest, ruff, mypy --strict

## Scope

~200 líneas de código. Una función principal `slugify()` con API limpia.

### Features

- Transliteración Unicode → ASCII sin dependencias externas
- Soporte multi-idioma: español, portugués, francés, alemán, italiano
- Separador configurable (default: `-`)
- Lowercase por defecto (configurable)
- Max length opcional con word boundary
- Stopwords opcional
- HTML entities decoding
- Type hints completos
- CLI incluida

### Non-goals (v1)

- Soporte para CJK (chino, japonés, coreano) — usar unidecode si se necesita
- Unique slug generation (manejo de colisiones en DB)
- Async API

## Competitors

| Paquete | Version | Downloads/mes | Deps | License | Ult. update | Status |
|---------|---------|---------------|------|---------|-------------|--------|
| python-slugify | 8.0.4 | ~1.4M | text-unidecode (GPL) | MIT | Feb 2024 | Activo, dominante |
| unicode-slugify | 0.1.5 | ~200K | six + unidecode | BSD | Oct 2021 | Estancado |
| awesome-slugify | 1.6.5 | ~50K | unidecode | GPLv3 | Jun 2015 | Abandonado |
| slugify | 0.0.1 | ~10K | none | Unknown | Dec 2010 | Abandonado |
| slugsmith | 0.1.0 | new | none | MIT | Mar 2026 | Nuevo, similar |

## Differentiators

1. **Zero dependencias, sin GPL** — argumento principal vs python-slugify
2. **Transliteración built-in** — tablas propias para idiomas latinos (es, pt, fr, de, it)
3. **API simple** — python-slugify tiene 15 parámetros; slugany ofrece presets (`style="url"`, `style="filename"`)
4. **Drop-in compatible** — `from slugany import slugify` como reemplazo directo
5. **~200 líneas** — auditable, sin bloat
6. **Python 3.11+** — moderno, type hints, sin legacy Python 2

## API design (preliminary)

```python
def slugify(
    text: str,
    *,
    separator: str = "-",
    lowercase: bool = True,
    max_length: int = 0,
    word_boundary: bool = False,
    stopwords: tuple[str, ...] = (),
    allow_unicode: bool = False,
    replacements: dict[str, str] | None = None,
) -> str: ...
```

### Presets

```python
slugify(text, style="url")        # separator="-", lowercase=True, max_length=200
slugify(text, style="filename")   # separator="_", lowercase=False, max_length=255
```

## CLI

```bash
slugany "¡Hola Mundo!"           # hola-mundo
echo "Café résumé" | slugany     # cafe-resume
```

## Package structure

```
slugany/
├── slugany/
│   ├── __init__.py          # Public API: slugify
│   ├── slugify.py           # Main slugify function
│   ├── transliterate.py     # Unicode → ASCII tables
│   ├── presets.py           # URL/filename presets
│   └── cli.py               # CLI entry point
├── tests/
│   ├── test_slugify.py
│   ├── test_transliterate.py
│   ├── test_presets.py
│   └── test_cli.py
├── pyproject.toml
├── README.md
├── LICENSE                  # MIT
└── .gitignore
```

## pyproject.toml (preliminary)

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "slugany"
version = "0.1.0"
description = "Slugify multi-idioma, zero deps. Alternativa simple a python-slugify sin GPL."
readme = "README.md"
license = "MIT"
requires-python = ">=3.11"
authors = [{ name = "Mathias Paulenko", email = "mathias.paulenko@outlook.com" }]
keywords = ["slugify", "slug", "unicode", "transliteration", "i18n"]
classifiers = [
    "Development Status :: 4 - Beta",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Topic :: Text Processing",
]

[project.scripts]
slugany = "slugany.cli:main"

[tool.hatch.version]
path = "slugany/__init__.py"

[tool.ruff]
target-version = "py311"
line-length = 100

[tool.mypy]
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
```

## Roadmap

- **v0.1.0** — Core: slugify(), transliteration tables (es, pt, fr, de, it), CLI, tests
- **v0.2.0** — Presets (url, filename), HTML entities, stopwords, replacements
- **v1.0.0** — Docs, CI/CD, PyPI publish, 100% coverage

## License

MIT — sin GPL, sin problemas de licencia comercial.

## Links

- GitHub: https://github.com/MathiasPaulenko/slugany
- Local: D:\Codigo\slugany
- PyPI: (pending)
- Brainstorming: D:\Codigo\brainstorming\ideas\libraries\README.md (row: slugany)
