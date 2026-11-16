"""Regras determinísticas para a estratégia de avaliação."""

ABORDAGENS = {
    "conceitual": "Priorizar definições, características, relações entre conceitos e compreensão teórica.",
    "comparacao": "Priorizar diferenças, semelhanças, vantagens, desvantagens e comparação entre conceitos.",
    "aplicacao": "Priorizar situações práticas em que o estudante precise aplicar o conteúdo estudado.",
    "interpretacao": "Priorizar análise e interpretação de exemplos, situações, resultados ou informações apresentadas.",
    "codigo": "Priorizar leitura, interpretação, correção e produção de pequenos trechos de código.",
    "resolucao_de_problemas": "Priorizar problemas que exijam raciocínio e combinação dos conceitos estudados para chegar a uma solução.",
}


def obter_estrategia(profundidade: str, foco: str) -> dict:
    """Parte determinística da ferramenta, testável sem LLM."""
    parametros = {
        "basica": (4, 1, "baixa"),
        "intermediaria": (3, 2, "media"),
        "avancada": (2, 3, "alta"),
    }
    valores = parametros.get(profundidade.lower())
    if valores is None:
        return {"erro": "Profundidade inválida"}
    abordagem = ABORDAGENS.get(foco.lower())
    if abordagem is None:
        return {"erro": "Foco inválido"}
    multipla_escolha, abertas, dificuldade = valores
    return {
        "multipla_escolha": multipla_escolha,
        "abertas": abertas,
        "dificuldade": dificuldade,
        "abordagem": abordagem,
    }


