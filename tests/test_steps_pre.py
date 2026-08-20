from __future__ import annotations

from slugany._config import SlugConfig
from slugany._steps import (
    _apply_replacements_post,
    _apply_replacements_pre,
    _deconfuse,
    _handle_emoji,
    _html_entities_decode,
    _lowercase,
    _normalize_punctuation,
    _transliterate,
)


class TestNormalizePunctuation:
    def test_curly_quotes(self) -> None:
        result = _normalize_punctuation("Bob\u2019s \u201cquote\u201d", SlugConfig())
        assert result == 'Bob\'s "quote"'

    def test_em_dash(self) -> None:
        assert _normalize_punctuation("a\u2014b", SlugConfig()) == "a-b"

    def test_nbsp(self) -> None:
        assert _normalize_punctuation("a\u00a0b", SlugConfig()) == "a b"

    def test_zero_width(self) -> None:
        assert _normalize_punctuation("a\u200bb", SlugConfig()) == "ab"

    def test_disabled(self) -> None:
        result = _normalize_punctuation("Bob\u2019s", SlugConfig(smart_punctuation=False))
        assert result == "Bob\u2019s"


class TestHtmlEntitiesDecode:
    def test_amp(self) -> None:
        assert _html_entities_decode("Bob&amp;Cafe", SlugConfig()) == "Bob&Cafe"

    def test_numeric(self) -> None:
        assert _html_entities_decode("a&#38;b", SlugConfig()) == "a&b"

    def test_hex(self) -> None:
        assert _html_entities_decode("a&#x26;b", SlugConfig()) == "a&b"

    def test_disabled(self) -> None:
        result = _html_entities_decode("Bob&amp;Cafe", SlugConfig(html_entities=False))
        assert result == "Bob&amp;Cafe"


class TestApplyReplacementsPre:
    def test_basic_non_ascii(self) -> None:
        """Pre-replacements only apply to non-ASCII keys."""
        cfg = SlugConfig.from_kwargs(replacements={"\u00c6": "AE"})
        assert _apply_replacements_pre("\u00c6lfred", cfg) == "AElfred"

    def test_ascii_key_skipped(self) -> None:
        """ASCII keys are not applied in pre-replacements."""
        cfg = SlugConfig.from_kwargs(replacements={"ll": "2"})
        assert _apply_replacements_pre("Hello", cfg) == "Hello"

    def test_empty(self) -> None:
        assert _apply_replacements_pre("Hello", SlugConfig()) == "Hello"

    def test_multiple_non_ascii(self) -> None:
        """Multiple non-ASCII pre-replacements are applied in order."""
        cfg = SlugConfig.from_kwargs(replacements={"\u00c6": "AE", "\u00df": "ss"})
        assert _apply_replacements_pre("\u00c6\u00df", cfg) == "AEss"


class TestHandleEmoji:
    def test_strip(self) -> None:
        assert _handle_emoji("Hello \U0001f389 World", SlugConfig()) == "Hello  World"

    def test_multiple(self) -> None:
        assert _handle_emoji("\U0001f600\U0001f600", SlugConfig()) == ""

    def test_no_emoji(self) -> None:
        assert _handle_emoji("Hello World", SlugConfig()) == "Hello World"

    def test_keep_mode(self) -> None:
        cfg = SlugConfig(emoji_mode="keep", allow_unicode=True)
        assert _handle_emoji("Hello \U0001f389", cfg) == "Hello \U0001f389"

    def test_keep_mode_without_unicode_raises(self) -> None:
        import pytest

        with pytest.raises(ValueError, match="allow_unicode=True"):
            _handle_emoji("Hello \U0001f389", SlugConfig(emoji_mode="keep"))

    def test_text_mode(self) -> None:
        assert (
            _handle_emoji("Hello \U0001f389", SlugConfig(emoji_mode="text")) == "Hello party-popper"
        )


class TestDeconfuse:
    def test_cyrillic(self) -> None:
        assert _deconfuse("\u0441afe", SlugConfig()) == "cafe"

    def test_no_confusables(self) -> None:
        assert _deconfuse("cafe", SlugConfig()) == "cafe"

    def test_skip_with_allow_unicode(self) -> None:
        """Regression: deconfuse must not convert Cyrillic when allow_unicode=True."""
        assert _deconfuse("\u0441afe", SlugConfig(allow_unicode=True)) == "\u0441afe"


class TestTransliterate:
    def test_es(self) -> None:
        assert _transliterate("Espa\u00f1a", SlugConfig(lang="es")) == "Espana"

    def test_de(self) -> None:
        assert _transliterate("\u00dcbung", SlugConfig(lang="de")) == "Uebung"

    def test_pt(self) -> None:
        assert _transliterate("Cora\u00e7\u00e3o", SlugConfig(lang="pt")) == "Coracao"

    def test_allow_unicode(self) -> None:
        assert _transliterate("Espa\u00f1a", SlugConfig(allow_unicode=True)) == "Espa\u00f1a"

    def test_nfkd(self) -> None:
        assert _transliterate("caf\u00e9", SlugConfig()) == "cafe"

    def test_default_table_ss(self) -> None:
        assert _transliterate("Stra\u00dfe", SlugConfig()) == "Strasse"

    def test_default_table_oe(self) -> None:
        assert _transliterate("C\u0153ur", SlugConfig()) == "Coeur"

    def test_default_table_ae(self) -> None:
        assert _transliterate("\u00c6lfred", SlugConfig()) == "AElfred"

    def test_default_table_thorn(self) -> None:
        assert _transliterate("\u00feorn", SlugConfig()) == "thorn"

    def test_default_table_eth(self) -> None:
        assert _transliterate("\u00f0e", SlugConfig()) == "de"

    def test_default_table_oslash(self) -> None:
        """Regression: ø/Ø must transliterate to o/O."""
        assert _transliterate("\u00f8re", SlugConfig()) == "ore"
        assert _transliterate("\u00d8re", SlugConfig()) == "Ore"

    def test_default_table_stroke_d(self) -> None:
        """Regression: đ/Đ must transliterate to d/D."""
        assert _transliterate("\u0111ai", SlugConfig()) == "dai"
        assert _transliterate("\u0110ai", SlugConfig()) == "Dai"

    def test_default_table_stroke_l(self) -> None:
        """Regression: ł/Ł must transliterate to l/L."""
        assert _transliterate("\u0142odz", SlugConfig()) == "lodz"
        assert _transliterate("\u0141odz", SlugConfig()) == "Lodz"

    def test_default_table_stroke_h(self) -> None:
        """Regression: ħ/Ħ must transliterate to h/H."""
        assert _transliterate("\u0127a", SlugConfig()) == "ha"
        assert _transliterate("\u0126a", SlugConfig()) == "Ha"

    def test_default_table_dotless_i(self) -> None:
        """Regression: ı (dotless i) must transliterate to i."""
        assert _transliterate("beyo\u011flu", SlugConfig()) == "beyoglu"

    def test_default_table_eng(self) -> None:
        """Regression: ŋ/Ŋ must transliterate to n/N."""
        assert _transliterate("\u014b", SlugConfig()) == "n"
        assert _transliterate("\u014a", SlugConfig()) == "N"

    def test_default_table_kra(self) -> None:
        """Regression: ĸ must transliterate to k."""
        assert _transliterate("\u0138", SlugConfig()) == "k"

    def test_default_table_t_stroke(self) -> None:
        """Regression: Ŧ/ŧ must transliterate to T/t."""
        assert _transliterate("\u0166ana", SlugConfig()) == "Tana"
        assert _transliterate("\u0167ana", SlugConfig()) == "tana"

    def test_default_table_g_stroke(self) -> None:
        """Regression: Ǥ/ǥ must transliterate to G/g."""
        assert _transliterate("\u01e4ulu", SlugConfig()) == "Gulu"
        assert _transliterate("\u01e5ulu", SlugConfig()) == "gulu"

    def test_default_table_ae_acute(self) -> None:
        """Regression: Ǽ/ǽ must transliterate to AE/ae.

        NFKD decomposes to Æ+acute which is non-ASCII.
        """
        assert _transliterate("\u01fcre", SlugConfig()) == "AEre"
        assert _transliterate("\u01fdre", SlugConfig()) == "aere"

    def test_default_table_o_stroke_acute(self) -> None:
        """Regression: Ǿ/ǿ must transliterate to O/o.

        NFKD decomposes to Ø+acute which is non-ASCII.
        """
        assert _transliterate("\u01fere", SlugConfig()) == "Ore"
        assert _transliterate("\u01ffre", SlugConfig()) == "ore"

    def test_default_table_ou(self) -> None:
        """Regression: Ȣ/ȣ must transliterate to OU/ou."""
        assert _transliterate("\u0222", SlugConfig()) == "OU"
        assert _transliterate("\u0223", SlugConfig()) == "ou"

    def test_default_table_dotless_j(self) -> None:
        """Regression: ȷ (dotless j) must transliterate to j."""
        assert _transliterate("\u0237", SlugConfig()) == "j"

    def test_default_table_turned_e(self) -> None:
        """Regression: ǝ (turned e) must transliterate to e."""
        assert _transliterate("\u01dd", SlugConfig()) == "e"

    def test_de_lang_overrides_default(self) -> None:
        assert _transliterate("Stra\u00dfe", SlugConfig(lang="de")) == "Strasse"

    def test_emoji_keep_preserves_emoji(self) -> None:
        """Regression: transliterate must preserve emoji when emoji_mode='keep'."""
        cfg = SlugConfig(emoji_mode="keep", allow_unicode=True)
        assert _transliterate("Hello\U0001f389World", cfg) == "Hello\U0001f389World"

    def test_emoji_text_preserves_emoji(self) -> None:
        """Regression: transliterate must handle text mode (emoji already replaced)."""
        cfg = SlugConfig(emoji_mode="text")
        assert _transliterate("Hello party-popperWorld", cfg) == "Hello party-popperWorld"

    def test_emoji_strip_removes_emoji(self) -> None:
        """emoji_mode='strip' removes emoji before transliterate (via _handle_emoji)."""
        cfg = SlugConfig(emoji_mode="strip")
        assert _transliterate("Hello  World", cfg) == "Hello  World"


class TestApplyReplacementsPost:
    def test_basic(self) -> None:
        cfg = SlugConfig.from_kwargs(replacements={"ll": "2"})
        assert _apply_replacements_post("hello", cfg) == "he2o"

    def test_empty(self) -> None:
        assert _apply_replacements_post("hello", SlugConfig()) == "hello"

    def test_non_ascii_key_skipped(self) -> None:
        """Post-replacements only apply to ASCII keys."""
        cfg = SlugConfig.from_kwargs(replacements={"\u00c6": "AE"})
        assert _apply_replacements_post("\u00c6lfred", cfg) == "\u00c6lfred"


class TestLowercase:
    def test_true(self) -> None:
        assert _lowercase("Hello", SlugConfig()) == "hello"

    def test_false(self) -> None:
        assert _lowercase("Hello", SlugConfig(lowercase=False)) == "Hello"
