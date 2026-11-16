import unittest
from src.review import extrair_questoes_gabarito


class TestParsing(unittest.TestCase):
    def test_extract(self):
        self.assertEqual(
            extrair_questoes_gabarito("<QUESTOES>1. Q?</QUESTOES><GABARITO>1. A</GABARITO>"),
            ("1. Q?", "1. A"),
        )

    def test_missing_delimiters(self):
        with self.assertRaises(ValueError):
            extrair_questoes_gabarito("sem estrutura")


if __name__ == "__main__":
    unittest.main()
