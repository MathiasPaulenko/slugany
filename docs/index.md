# slugany

Slugify multi-idioma, zero dependencias. Alternativa simple a `python-slugify`
sin arrastrar dependencias GPL.

## Instalación

```bash
pip install slugany
```

## Quickstart

```python
from slugany import slugify

slugify("¡Hola Mundo!")        # "hola-mundo"
slugify("Café résumé naïve")   # "cafe-resume-naive"
slugify("Ñandú coração")       # "nandu-coracao"
```

## Por qué slugany

- **Zero deps** — sin GPL, sin text-unidecode
- **Multi-idioma** — tablas propias para es, pt, fr, de, it
- **~200 líneas** — auditable, sin bloat
- **CLI incluido** — `slugany "texto"` desde terminal
- **lru_cache** — resultados cacheados automáticamente
