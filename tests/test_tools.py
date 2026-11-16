import unittest

from src.strategy import obter_estrategia


class TestStrategy(unittest.TestCase):
    def test_intermediate(self):
        result = obter_estrategia("intermediaria", "comparacao")
        self.assertEqual((result["multipla_escolha"], result["abertas"]), (3, 2))
        self.assertEqual(result["dificuldade"], "media")

    def test_invalid(self):
        self.assertIn("erro", obter_estrategia("xyz", "codigo"))
        self.assertIn("erro", obter_estrategia("basica", "xyz"))


if __name__ == "__main__":
    unittest.main()
