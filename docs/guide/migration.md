# Migration from python-slugify

slugany is designed as a drop-in replacement for `python-slugify` with a simpler, zero-dependency architecture.

## Key Differences

| Aspect | python-slugify | slugany |
|--------|---------------|---------|
| Dependencies | text-unidecode (GPL) | Zero |
| API | Positional + keyword | Keyword-only |
| Multi-language | Limited | Built-in tables (es, pt, de, fr, it) |
| Caching | No | `lru_cache` built-in |
| Smart punctuation | No | Built-in (smart quotes, dashes, zero-width) |
| Emoji support | No | `strip`, `text`, `keep` modes |
| CSS-safe | No | Built-in `css_safe` option |
| Style presets | No | `kebab`, `snake`, `camel`, `pascal`, `dot`, `train`, `filename`, `url` |
| Confusables | Limited | Cyrillic + Greek homoglyph deconfusion |
| License | GPL | MIT |

## Basic Migration

```python
# python-slugify
from slugify import slugify
slugify("Hello World")

# slugany
from slugany import slugify
slugify("Hello World")
```

## Parameter Mapping

| python-slugify | slugany | Notes |
|---------------|---------|-------|
| `separator` | `separator` | Same |
| `lowercase` | `lowercase` | Same |
| `max_length` | `max_length` | Same |
| `word_boundary` | `word_boundary` | Same |
| `stopwords` | `stopwords` | Same |
| `replacements` | `replacements` | Same |
| `allow_unicode` | `allow_unicode` | Same |
| `regex_pattern` | — | Not supported; use `replacements` instead |
| — | `style` | New: case style presets |
| — | `lang` | New: language transliteration |
| — | `fallback` | New: fallback for empty slugs |
| — | `emoji_mode` | New: emoji handling |
| — | `css_safe` | New: CSS-safe prefix |
| — | `html_entities` | New: HTML entity decoding |
| — | `smart_punctuation` | New: smart punctuation normalization |

## Intentional Differences

### Keyword-only arguments

slugany uses **keyword-only** arguments. This is by design to improve readability and prevent positional argument errors:

```python
# python-slugify allows positional:
slugify("Hello World", "_")

# slugany requires keyword:
slugify("Hello World", separator="_")
```

### Smart punctuation normalization

slugany normalizes smart quotes, dashes, and zero-width characters by default. Disable with `smart_punctuation=False`:

```python
# python-slugify: smart quotes preserved as-is
# slugany: smart quotes normalized to ASCII
slugify("Bob's café")  # -> "bob-s-cafe"
```

### Zero dependencies

slugany has zero runtime dependencies. No `text-unidecode`, no `unidecode`, no regex libraries. All transliteration tables are built-in.

### Slugifier class

slugany introduces `Slugifier`, a reusable slugifier bound to a fixed configuration:

```python
from slugany import Slugifier

s = Slugifier.style("camel", max_length=20)
s("Hello World")       # -> "helloWorld"
s("Another Example")   # -> "anotherExample"
```

### deconfuse() utility

slugany exposes `deconfuse()` as a standalone utility for replacing confusable Unicode characters:

```python
from slugany import deconfuse
deconfuse("саfe")  # -> "cafe" (Cyrillic s -> Latin c)
deconfuse("αβγ")   # -> "abg" (Greek -> Latin)
```
