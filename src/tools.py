"""Ferramenta explícita para definir estratégia da avaliação."""

from langchain_core.tools import tool
from src.strategy import obter_estrategia

@tool
def configurar_estrategia_avaliacao(profundidade: str, foco: str) -> dict:
    """Define obrigatoriamente a estratégia antes de gerar questões.

    A profundidade determina quantidade de questões e dificuldade;
    o foco determina a abordagem. A prioridade orienta os temas,
    não a estrutura da avaliação.
    """
    return obter_estrategia(profundidade, foco)
