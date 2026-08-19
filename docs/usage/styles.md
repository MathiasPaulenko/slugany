# Styles & Presets

## Style Presets

slugany includes built-in style presets:

| Preset | Separator | Lowercase | Style |
|--------|-----------|-----------|-------|
| `url` | `-` | `True` | — |
| `filename` | `-` | `False` | — |
| `kebab` | `-` | `True` | — |
| `snake` | `_` | `True` | — |
| `camel` | `-` | `True` | `camel` |
| `pascal` | `-` | `False` | `pascal` |
| `dot` | `.` | `True` | — |
| `train` | `-` | `False` | `train` |

## Usage

```python
from slugany import slugify

slugify("hello world", style="kebab")    # "hello-world"
slugify("hello world", style="snake")    # "hello_world"
slugify("hello world", style="camel")    # "helloWorld"
slugify("hello world", style="pascal")   # "HelloWorld"
slugify("hello world", style="dot")      # "hello.world"
slugify("hello world", style="train")    # "Hello-World"
slugify("Hello World", style="filename") # "Hello-World"
```
