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

    def test_cyrillic_case_consistency(self) -> None:
        """Regression: lowercase Cyrillic must map to lowercase Latin."""
        assert slugify("в", lowercase=False) == "b"
        assert slugify("к", lowercase=False) == "k"
        assert slugify("м", lowercase=False) == "m"
        assert slugify("н", lowercase=False) == "h"
        assert slugify("т", lowercase=False) == "t"
        assert slugify("ВКМНТ", lowercase=False) == "BKMHT"

    def test_greek_visual_mappings(self) -> None:
        """Regression: Greek must map to visually identical Latin letters."""
        assert slugify("ΗΡΧ", lowercase=False) == "HPX"
        assert slugify("ηρχ", lowercase=False) == "npx"
        assert slugify("νω", lowercase=False) == "vw"
