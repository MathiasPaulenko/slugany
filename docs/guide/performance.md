# Performance

slugany is designed for speed with zero dependencies.

## lru_cache

`slugify()` uses `functools.lru_cache(maxsize=512)` internally. Repeated calls with the same input and configuration return instantly from cache.

```python
from slugany import slugify

slugify("Hello World")  # cache miss
slugify("Hello World")  # cache hit — instant

slugify.cache_info()    # CacheInfo(hits=1, misses=1, maxsize=512, currsize=1)
slugify.cache_clear()   # clear cache
```

The cache key is `(text, config)` where `config` is a frozen `SlugConfig` instance. Frozen dataclasses are hashable, making them ideal cache keys.

### Cache sizing

The default `maxsize=512` balances memory and hit rate for typical workloads. For batch processing of unique strings, the cache provides less benefit but does not hurt performance. Clear the cache between batches if memory is a concern:

```python
slugify.cache_clear()
```

## str.translate vs regex

Language transliteration uses `str.translate()` with pre-built mapping tables — one of the fastest string transformation methods in Python.

| Method | Speed | Use case |
|--------|-------|----------|
| `str.translate()` | Fastest | Character-to-string mapping (transliteration, deconfusion) |
| `re.sub()` | Fast | Pattern-based replacement (emoji, separators) |
| Manual loop | Slowest | Avoided entirely |

All transliteration tables (`_DEFAULT_TABLE`, `_ES_TABLE`, `_DE_TABLE`, etc.) are pre-built `dict[int, str]` at module load time, so `str.translate()` pays no construction cost at runtime.

## Pipeline Architecture

The pipeline consists of 18 pure-function steps executed in order. Each step takes `(text, config)` and returns transformed text:

```text
html_entities_decode → normalize_punctuation → replacements_pre → handle_emoji
→ deconfuse → transliterate → lowercase → replacements_post → remove_stopwords
→ replace_non_alphanumeric → collapse_separators → trim_separators → truncate
→ fallback → css_safe → case_style → truncate → trim_separators
```

### Short-circuit optimization

When `text` becomes empty, all steps are skipped except `_apply_fallback`:

```python
def _run_pipeline(text: str, config: SlugConfig) -> str:
    for step in _STEPS:
        if not text and step is not _apply_fallback:
            continue
        text = step(text, config)
    return text
```

This avoids unnecessary work on inputs that reduce to empty early (e.g., punctuation-only or emoji-only strings).

### Pure functions

Every step is a pure function — no side effects, no global state. This makes the pipeline:

- **Thread-safe**: no locks needed.
- **Cacheable**: `lru_cache` works correctly because outputs depend only on inputs.
- **Testable**: each step can be tested in isolation.

## Slugifier reuse

For high-throughput scenarios, `Slugifier` avoids repeated `SlugConfig.from_kwargs()` validation on every call:

```python
from slugany import Slugifier

s = Slugifier.style("camel", max_length=20)

for text in large_corpus:
    slug = s(text)  # config validation happens once, not per call
```

The `Slugifier` stores a frozen `SlugConfig` and calls `_run_pipeline` directly, bypassing the `slugify()` wrapper's config construction and validation.

## Benchmark

```python
import timeit

timeit.timeit(lambda: slugify("¡Hola Mundo! Café résumé"), number=10000)
# ~0.6s for 10k calls (no cache), ~0.1s with cache
```

### Slugifier vs slugify

```python
import timeit

s = Slugifier.style("kebab")
timeit.timeit(lambda: s("¡Hola Mundo! Café résumé"), number=10000)
# ~0.4s for 10k calls — faster than slugify() due to skipped validation
```
