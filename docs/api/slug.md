# Slug

`Slug` is an optional Pydantic field type —
`Annotated[str, BeforeValidator(...)]` — that auto-slugifies any string
assigned to the field. It is only available when `pydantic` is installed;
otherwise it falls back to plain `str`.

```python
from pydantic import BaseModel
from slugany import Slug

class Tag(BaseModel):
    name: str
    slug: Slug

tag = Tag(name="Machine Learning", slug="Machine Learning")
assert tag.slug == "machine-learning"
```

::: slugany.Slug
