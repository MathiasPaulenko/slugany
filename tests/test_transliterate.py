from __future__ import annotations

from slugany import slugify


class TestSpanish:
    def test_n_to_n(self) -> None:
        assert slugify("Espa\u00f1a") == "espana"

    def test_capital_n_to_n(self) -> None:
        assert slugify("ESPA\u00d1A", lowercase=False) == "ESPANA"

    def test_inverted_question_mark_removed(self) -> None:
        assert slugify("\u00bfQu\u00e9 tal?") == "que-tal"

    def test_inverted_exclamation_mark_removed(self) -> None:
        assert slugify("\u00a1Hola!") == "hola"

    def test_full_sentence(self) -> None:
        assert slugify("\u00a1El espa\u00f1ol es f\u00e1cil!") == "el-espanol-es-facil"

    def test_with_lang_es(self) -> None:
        assert slugify("Espa\u00f1a", lang="es") == "espana"


class TestPortuguese:
    def test_cedilha_to_c(self) -> None:
        assert slugify("Cora\u00e7\u00e3o") == "coracao"

    def test_tilde_a_to_a(self) -> None:
        assert slugify("m\u00e3o") == "mao"

    def test_tilde_o_to_o(self) -> None:
        assert slugify("le\u00f5es") == "leoes"

    def test_acentos(self) -> None:
        assert slugify("caf\u00e9") == "cafe"

    def test_with_lang_pt(self) -> None:
        assert slugify("S\u00e3o Paulo", lang="pt") == "sao-paulo"

    def test_full_sentence(self) -> None:
        assert slugify("Acorde\u00e3o do cora\u00e7\u00e3o") == "acordeao-do-coracao"


class TestGerman:
    def test_a_to_ae(self) -> None:
        assert slugify("B\u00e4r", lang="de") == "baer"

    def test_o_to_oe(self) -> None:
        assert slugify("\u00d6l", lang="de") == "oel"

    def test_u_to_ue(self) -> None:
        assert slugify("\u00dcber", lang="de") == "ueber"

    def test_eszett_to_ss(self) -> None:
        assert slugify("Stra\u00dfe", lang="de") == "strasse"

    def test_uppercase(self) -> None:
        assert slugify("\u00c4\u00d6\u00dc", lang="de", lowercase=False) == "AeOeUe"

    def test_full_sentence(self) -> None:
        assert slugify("\u00dcber die Stra\u00dfe", lang="de") == "ueber-die-strasse"

    def test_with_lang_de(self) -> None:
        assert slugify("\u00dcbung", lang="de") == "uebung"


class TestFrench:
    def test_oe_to_oe(self) -> None:
        assert slugify("c\u0153ur", lang="fr") == "coeur"

    def test_ae_to_ae(self) -> None:
        assert slugify("curriculum vit\u00e6", lang="fr") == "curriculum-vitae"

    def test_acentos(self) -> None:
        assert slugify("Caf\u00e9 r\u00e9sum\u00e9", lang="fr") == "cafe-resume"


class TestItalian:
    def test_acentos(self) -> None:
        assert slugify("Caff\u00e8 per favore", lang="it") == "caffe-per-favore"

    def test_uppercase_accent(self) -> None:
        assert slugify("Perch\u00e9", lang="it") == "perche"


class TestAutoDetect:
    def test_auto_detect_spanish(self) -> None:
        assert slugify("España") == "espana"

    def test_auto_detect_portuguese(self) -> None:
        assert slugify("Coração") == "coracao"

    def test_auto_detect_german(self) -> None:
        assert slugify("Übung") == "uebung"

    def test_auto_no_diacritics(self) -> None:
        assert slugify("Hello World") == "hello-world"

    def test_auto_mixed(self) -> None:
        assert "espana" in slugify("España und Übung")


class TestNFKDFallback:
    def test_greek(self) -> None:
        assert slugify("\u03b1\u03b2\u03b3") == "abg"

    def test_cjk(self) -> None:
        assert slugify("\u4f60\u597d") == ""

    def test_mixed(self) -> None:
        assert slugify("Hello \u4f60\u597d World") == "hello-world"
