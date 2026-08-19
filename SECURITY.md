# Security policy

## Supported versions

The latest released version of slugany receives security fixes.

## Reporting a vulnerability

If you discover a security vulnerability, please report it responsibly:

1. **Do not** open a public GitHub issue.
2. Email the maintainer at `mathias.paulenko@outlook.com` with a
   description of the vulnerability and steps to reproduce.
3. You will receive an acknowledgment within 48 hours.

## Security considerations

slugany is a pure-Python library with zero runtime dependencies. It does
not:

- Read or write files
- Make network requests
- Execute arbitrary code
- Use `eval` or `exec`
- Deserialize untrusted data

All input is treated as text and processed through a deterministic
pipeline of string transformations.
