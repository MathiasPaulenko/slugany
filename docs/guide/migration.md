# Migration from python-slugify

slugany is designed as a drop-in replacement for `python-slugify` with a simpler, zero-dependency architecture.

## Key Differences

| Aspect | python-slugify | slugany |
|--------|---------------|---------|
| Dependencies | text-unidecode (GPL) | Zero |
| API | Positional + keyword | Keyword-only |
| Multi-language | Limited | Built-in tables (es, pt, de, fr, it) |
| Caching | No | `lru_cache` built-in |
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

## Intentional Difference

slugany uses **keyword-only** arguments. This is by design to improve readability and prevent positional argument errors:

```python
# python-slugify allows positional:
slugify("Hello World", "_")

# slugany requires keyword:
slugify("Hello World", separator="_")
```
