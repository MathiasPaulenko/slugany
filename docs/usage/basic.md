# Basic Usage

## slugify()

The `slugify()` function converts any text into a URL-friendly slug.

```python
from slugany import slugify

slugify("Hello World")           # "hello-world"
slugify("¡Hola Mundo!")          # "hola-mundo"
slugify("Café résumé")           # "cafe-resume"
```

## Parameters

All parameters are keyword-only:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `separator` | `str` | `"-"` | Word separator |
| `lowercase` | `bool` | `True` | Lowercase output |
| `max_length` | `int` | `0` | Max slug length (0 = unlimited) |
| `word_boundary` | `bool` | `False` | Truncate at word boundary |
| `stopwords` | `Iterable[str]` | `None` | Words to remove |
| `allow_unicode` | `bool` | `False` | Preserve Unicode |
| `replacements` | `Mapping[str, str] \| Iterable[tuple[str, str]]` | `None` | Custom replacements applied before and after pipeline |
| `style` | `str` | `None` | Style preset |
| `lang` | `str` | `"auto"` | Language for transliteration |
| `fallback` | `str` | `""` | Fallback for empty slugs |
| `emoji_mode` | `str` | `"strip"` | Emoji handling |
| `css_safe` | `bool` | `False` | CSS-safe prefix |
| `html_entities` | `bool` | `True` | Decode HTML entities |
| `smart_punctuation` | `bool` | `True` | Normalize smart punctuation |

## Advanced examples

### Stopwords

```python
slugify("the quick brown fox", stopwords=["the", "fox"])
# "quick-brown"
```

### Custom replacements

```python
slugify("hello world", replacements={"hello": "hi"})
# "hi-world"
```

### Fallback for empty slugs

```python
slugify("!!!", fallback="untitled")
# "untitled"
```

### CSS-safe output

```python
slugify("123 main st", css_safe=True)
# "s-123-main-st"
```

### Unicode preservation

```python
slugify("Ñandú", allow_unicode=True)
# "ñandú"
```

### Batch processing

```python
from slugany import slugify_batch

slugify_batch(["Hello World", "Café Résumé"])
# ["hello-world", "cafe-resume"]
```

### Validation

```python
from slugany import is_slug

is_slug("hello-world")              # True
is_slug("hello world")              # False
is_slug("hello_world", separator="_")  # True
```
