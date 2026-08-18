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

## str.translate

Language transliteration uses `str.translate()` with pre-built mapping tables — one of the fastest string transformation methods in Python.

## Pipeline Architecture

The pipeline consists of 17 pure-function steps executed in order. Short-circuit logic skips remaining steps when text becomes empty (except fallback).

## Benchmark

```python
import timeit

timeit.timeit(lambda: slugify("¡Hola Mundo! Café résumé"), number=10000)
# ~0.5s for 10k calls (first call), ~0.01s with cache
```
