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
| `auto` | Auto | Detects the language from characteristic code points |

## Usage

```python
from slugany import slugify

slugify("España", lang="es")           # "espana"
slugify("Coração", lang="pt")          # "coracao"
slugify("Über Straße", lang="de")      # "ueber-strasse"
slugify("Cœur", lang="fr")             # "coeur"
slugify("Caffè", lang="it")            # "caffe"
```

With `lang="auto"` (default), slugany inspects the text for characteristic
characters (ñ/¿/¡ for Spanish, ç/ã/õ for Portuguese, ä/ö/ü/ß for German,
œ/æ for French, à/è/ì/ò/ù for Italian) and picks the table of the most
frequent match. A Spanish dieresis (ü in *güe*/*güi* words like "agüero")
is not treated as a German umlaut. Characters not covered by any table are
handled by NFKD Unicode decomposition plus a default transliteration table
(ß→ss, æ→ae, œ→oe, ø→o, ł→l, etc.).
