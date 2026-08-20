from __future__ import annotations

import pytest

from slugany import deconfuse, slugify
from slugany._tables import _CONFUSABLES


class TestConfusables:
    def test_cyrillic(self) -> None:
        assert "саfe".translate(_CONFUSABLES) == "cafe"

    def test_greek(self) -> None:
        assert "αβγ".translate(_CONFUSABLES) == "abg"

    def test_mixed(self) -> None:
        assert "саfeα".translate(_CONFUSABLES) == "cafea"

    def test_deconfuse_public(self) -> None:
        assert deconfuse("саfe") == "cafe"
        assert deconfuse("αβγ") == "abg"

    def test_auto_deconfuse_in_slugify(self) -> None:
        assert slugify("саfe") == "cafe"

    def test_deconfuse_non_string(self) -> None:
        """Regression: deconfuse must raise TypeError for non-string input."""
        with pytest.raises(TypeError, match="text must be a string"):
            deconfuse(None)  # type: ignore[arg-type]
        with pytest.raises(TypeError, match="text must be a string"):
            deconfuse(123)  # type: ignore[arg-type]
