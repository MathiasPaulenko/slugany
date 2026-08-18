# Languages

slugany supports multi-language transliteration with built-in tables.

## Supported Languages

| Code | Language | Examples |
|------|----------|---------|
| `es` | Spanish | ñ→n, ¿→removed, ¡→removed |
| `pt` | Portuguese | ç→c, ã→a, õ→o |
| `de` | German | ä→ae, ö→oe, ü→ue, ß→ss |
| `fr` | French | œ→oe, æ→ae, à→a |
| `it` | Italian | è→e, à→a, ì→i |
| `auto` | Auto | NFKD decomposition fallback |

## Usage

```python
from slugany import slugify

slugify("España", lang="es")           # "espana"
slugify("Coração", lang="pt")          # "coracao"
slugify("Über Straße", lang="de")      # "ueber-strasse"
slugify("Cœur", lang="fr")             # "coeur"
slugify("Caffè", lang="it")            # "caffe"
```

When `lang="auto"` (default), slugany uses NFKD Unicode decomposition as a fallback for characters not in any language table.
