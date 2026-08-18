# CLI

slugany includes a command-line interface.

## Basic Usage

```bash
slugany "Hello World"
# Output: hello-world
```

## Options

| Flag | Description |
|------|-------------|
| `-s, --separator` | Word separator |
| `--style` | Style preset |
| `--lang` | Language for transliteration |
| `--max-length` | Maximum slug length |
| `--word-boundary` | Truncate at word boundary |
| `--lowercase / --no-lowercase` | Control case |
| `--allow-unicode` | Preserve Unicode characters |
| `--fallback` | Fallback for empty slugs |
| `--emoji-mode` | Emoji handling (strip/text/keep) |
| `--css-safe` | CSS-safe prefix |
| `--batch` | Read stdin line by line |

## Stdin

If no text argument is provided and stdin is piped, slugany reads from stdin:

```bash
echo "Café" | slugany
# Output: cafe
```

## Batch

```bash
echo -e "Hello World\nCafé" | slugany --batch
# Output:
# hello-world
# cafe
```
