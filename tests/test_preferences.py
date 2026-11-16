import unittest
from src.preferences import validate_options
from main import escolher_opcao


class TestPreferences(unittest.TestCase):
    def test_valid_options(self):
        got = validate_options({"topicos": ["Grafos", "Grafos", "Busca"],
                                "focos": ["aplicacao", "codigo", "invalido"]})
        self.assertEqual(got, {"topicos": ["Grafos", "Busca"],
                               "focos": ["aplicacao", "codigo"]})

    def test_empty_options(self):
        with self.assertRaises(ValueError):
            validate_options({"topicos": [], "focos": ["codigo"]})

    def test_choose_option(self):
        self.assertEqual(escolher_opcao("Escolha", ["a", "b"],
                                       input_fn=lambda _: "2"), "b")


if __name__ == "__main__":
    unittest.main()
