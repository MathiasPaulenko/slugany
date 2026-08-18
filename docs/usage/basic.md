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
| `replacements` | `Mapping` | `None` | Custom replacements |
| `style` | `str` | `None` | Style preset |
| `lang` | `str` | `"auto"` | Language for transliteration |
| `fallback` | `str` | `""` | Fallback for empty slugs |
| `emoji_mode` | `str` | `"strip"` | Emoji handling |
| `css_safe` | `bool` | `False` | CSS-safe prefix |
| `html_entities` | `bool` | `True` | Decode HTML entities |
| `smart_punctuation` | `bool` | `True` | Normalize smart punctuation |
