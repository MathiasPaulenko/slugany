# Contracts

slugany guarantees several invariant contracts, verified by the test suite.

## Idempotency

Applying `slugify()` to a slug produces the same slug:

```python
result = slugify("Hello World!")
assert slugify(result) == result
```

## Determinism

The same input always produces the same output:

```python
assert slugify("Café") == slugify("Café")  # always
```

## No Double Separators

Output never contains consecutive separators, nor leading/trailing separators:

```python
assert "--" not in slugify("Hello  --  World")
assert not slugify("  Hello  ").startswith("-")
assert not slugify("  Hello  ").endswith("-")
```

## ASCII Output

With `allow_unicode=False` (default), output is always pure ASCII:

```python
assert slugify("España", allow_unicode=False).isascii()
```

## No Crash on Empty

Empty strings, whitespace, punctuation-only, and emoji-only inputs produce empty string (or fallback):

```python
assert slugify("") == ""
assert slugify("   ") == ""
assert slugify("!!!") == ""
assert slugify("!!!", fallback="untitled") == "untitled"
```
