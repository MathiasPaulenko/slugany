# Contracts

slugany guarantees several invariant contracts, verified by the test suite.

## Idempotency

Applying `slugify()` to a slug produces the same slug:

```python
result = slugify("Hello World!")
assert slugify(result) == result
```

This holds for all style presets:

```python
for style in ("kebab", "snake", "camel", "pascal", "train", "dot", "filename", "url"):
    result = slugify("hello world", style=style)
    assert slugify(result, style=style) == result
```

## Determinism

The same input always produces the same output:

```python
assert slugify("Café") == slugify("Café")  # always
```

No random behavior, no time-dependent logic, no global mutable state.

## No Double Separators

Output never contains consecutive separators, nor leading/trailing separators:

```python
assert "--" not in slugify("Hello  --  World")
assert not slugify("  Hello  ").startswith("-")
assert not slugify("  Hello  ").endswith("-")
```

This also holds for multi-character separators:

```python
assert slugify("hello   world", separator="--") == "hello--world"
assert slugify("--hello--", separator="--") == "hello"
```

## ASCII Output

With `allow_unicode=False` (default), output is always pure ASCII:

```python
assert slugify("España", allow_unicode=False).isascii()
```

All non-ASCII characters are transliterated or stripped. Confusable homoglyphs (Cyrillic, Greek) are converted to their Latin equivalents.

## Fallback

Empty strings, whitespace, punctuation-only, and emoji-only inputs produce empty string (or fallback):

```python
assert slugify("") == ""
assert slugify("   ") == ""
assert slugify("!!!") == ""
assert slugify("!!!", fallback="untitled") == "untitled"
```

The fallback is returned as-is — it should be a valid slug to maintain idempotency:

```python
assert slugify("!!!", fallback="untitled") == "untitled"
assert slugify("untitled") == "untitled"
```

## Case-Insensitive Stopwords

Stopwords are matched case-insensitively regardless of the `lowercase` setting:

```python
assert slugify("The Hello World", stopwords=["the"]) == "hello-world"
assert slugify("THE HELLO WORLD", stopwords=["the"]) == "hello-world"
```

Stopwords containing non-alphanumeric characters are normalized before matching:

```python
assert slugify("hello-world foo", stopwords=["hello-world"]) == "foo"
assert slugify("hello_world foo", stopwords=["hello_world"]) == "foo"
```

Non-ASCII stopwords are transliterated to match the deconfused text:

```python
assert slugify("café hello", stopwords=["café"]) == "hello"
assert slugify("ä hello", stopwords=["ä"], lang="de") == "hello"
```

## CSS-Safe Output

When `css_safe=True`, slugs starting with a digit are prefixed to produce valid CSS identifiers:

```python
assert slugify("2024 recap", css_safe=True) == "s-2024-recap"
assert slugify("hello world", css_safe=True) == "hello-world"
```

The prefix adapts to the active style preset:

```python
assert slugify("123 hello", css_safe=True, style="camel") == "s123Hello"
assert slugify("123 hello", css_safe=True, style="pascal") == "S123Hello"
assert slugify("123 hello", css_safe=True, style="train") == "S-123-Hello"
```
