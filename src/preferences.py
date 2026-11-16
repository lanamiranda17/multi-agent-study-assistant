"""Preferências do usuário e preparação de opções com LLM."""

import json

FOCOS_POSSIVEIS = (
    "conceitual", "comparacao", "aplicacao", "interpretacao",
    "codigo", "resolucao_de_problemas",
)
PROFUNDIDADES = ("basica", "intermediaria", "avancada")
TAMANHOS = ("curta", "media", "detalhada")
NOMES_FOCOS = {
    "conceitual": "Conceitual",
    "comparacao": "Comparação",
    "aplicacao": "Aplicação",
    "interpretacao": "Interpretação",
    "codigo": "Código",
    "resolucao_de_problemas": "Resolução de problemas",
}


def validate_options(options: dict) -> dict:
    """Valida a saída estruturada da análise de conteúdo."""
    if not isinstance(options, dict):
        raise ValueError("A resposta de análise não contém um objeto JSON.")
    topics, focuses = options.get("topicos"), options.get("focos")
    if not isinstance(topics, list) or not isinstance(focuses, list):
        raise ValueError("A resposta deve conter listas 'topicos' e 'focos'.")
    topics = list(dict.fromkeys(t.strip() for t in topics if isinstance(t, str) and t.strip()))
    focuses = list(dict.fromkeys(f for f in focuses if f in FOCOS_POSSIVEIS))
    if not topics:
        raise ValueError("A análise não encontrou tópicos válidos.")
    if not focuses:
        raise ValueError("A análise não sugeriu focos válidos.")
    return {"topicos": topics, "focos": focuses}


def gerar_opcoes(conteudo: str, llm_tutor) -> dict:
    """Usa o Tutor como pré-processamento (não cria terceiro agente)."""
    prompt = f"""Analise o conteúdo estudado abaixo.

CONTEÚDO:
{conteudo}

Identifique:
1. Os principais tópicos estudados que podem ser escolhidos como prioridade.
2. Quais focos de revisão são adequados para esse conteúdo.

Os focos só podem ser escolhidos desta lista:
{list(FOCOS_POSSIVEIS)}

Por exemplo, não selecione 'codigo' se o conteúdo não envolver programação.
Retorne SOMENTE um JSON válido neste formato:
{{"topicos": ["topico 1", "topico 2"], "focos": ["conceitual", "aplicacao"]}}
"""
    resposta = llm_tutor.invoke(prompt)
    raw = resposta.content
    if not isinstance(raw, str):
        raise ValueError("O modelo retornou conteúdo que não é texto.")
    # A resposta deve conter apenas JSON válido, sem markdown ou texto adicional.
    try:
        parsed = json.loads(raw.strip())
    except json.JSONDecodeError as exc:
        raise ValueError("O modelo não retornou JSON válido para as opções.") from exc
    return validate_options(parsed)
