from __future__ import annotations

_PUNCTUATION_TABLE: dict[int, str | int | None] = str.maketrans(
    {
        # Curly quotes
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        # Dashes
        "\u2013": "-",
        "\u2014": "-",
        "\u2212": "-",
        # Spaces
        "\u00a0": " ",
        "\u2002": " ",
        "\u2003": " ",
        "\u2004": " ",
        "\u2005": " ",
        "\u2006": " ",
        "\u2007": " ",
        "\u2008": " ",
        "\u2009": " ",
        "\u200a": " ",
        "\u202f": " ",
        "\u205f": " ",
        "\u3000": " ",
        # Zero-width characters
        "\u200b": "",
        "\u200c": "",
        "\u200d": "",
        "\ufeff": "",
        # Bullet
        "\u2022": "-",
    }  # type: ignore[arg-type]
)

_ES_TABLE: dict[int, str] = {
    ord("ñ"): "n",
    ord("Ñ"): "N",
    ord("¿"): "",
    ord("¡"): "",
}

_PT_TABLE: dict[int, str] = {
    ord("ç"): "c",
    ord("Ç"): "C",
    ord("ã"): "a",
    ord("Ã"): "A",
    ord("õ"): "o",
    ord("Õ"): "O",
    ord("á"): "a",
    ord("Á"): "A",
    ord("é"): "e",
    ord("É"): "E",
    ord("í"): "i",
    ord("Í"): "I",
    ord("ó"): "o",
    ord("Ó"): "O",
    ord("ú"): "u",
    ord("Ú"): "U",
    ord("â"): "a",
    ord("Â"): "A",
    ord("ê"): "e",
    ord("Ê"): "E",
    ord("ô"): "o",
    ord("Ô"): "O",
}

_DE_TABLE: dict[int, str] = {
    ord("ä"): "ae",
    ord("ö"): "oe",
    ord("ü"): "ue",
    ord("Ä"): "Ae",
    ord("Ö"): "Oe",
    ord("Ü"): "Ue",
    ord("ß"): "ss",
}

_FR_IT_TABLE: dict[int, str] = {
    ord("œ"): "oe",
    ord("Œ"): "OE",
    ord("æ"): "ae",
    ord("Æ"): "AE",
    ord("à"): "a",
    ord("À"): "A",
    ord("è"): "e",
    ord("È"): "E",
    ord("ì"): "i",
    ord("Ì"): "I",
    ord("ò"): "o",
    ord("Ò"): "O",
    ord("ù"): "u",
    ord("Ù"): "U",
}

_LANGUAGE_TABLES: dict[str, dict[int, str]] = {
    "es": _ES_TABLE,
    "pt": _PT_TABLE,
    "de": _DE_TABLE,
    "fr": _FR_IT_TABLE,
    "it": _FR_IT_TABLE,
}

_CONFUSABLES: dict[int, str] = {
    ord("а"): "a",
    ord("А"): "A",
    ord("е"): "e",
    ord("Е"): "E",
    ord("о"): "o",
    ord("О"): "O",
    ord("р"): "p",
    ord("Р"): "P",
    ord("с"): "c",
    ord("С"): "C",
    ord("х"): "x",
    ord("Х"): "X",
    ord("у"): "y",
    ord("У"): "Y",
    ord("і"): "i",
    ord("І"): "I",
    ord("ј"): "j",
    ord("Ј"): "J",
    ord("ѕ"): "s",
    ord("Ѕ"): "S",
}
