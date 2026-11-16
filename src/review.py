"""Chamada do grafo e separação dos resultados textuais."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReviewResult:
    revisao: str
    questoes: str
    gabarito: str


def extrair_questoes_gabarito(texto: str) -> tuple[str, str]:
    """Exige os blocos produzidos pelo Avaliador."""
    start_questions, end_questions = "<QUESTOES>", "</QUESTOES>"
    start_answers, end_answers = "<GABARITO>", "</GABARITO>"
    if any(texto.count(tag) != 1 for tag in
           (start_questions, end_questions, start_answers, end_answers)):
        raise ValueError("O Avaliador não retornou os blocos esperados.")
    a = texto.index(start_questions) + len(start_questions)
    b = texto.index(end_questions)
    c = texto.index(start_answers) + len(start_answers)
    d = texto.index(end_answers)
    if not (a <= b < c <= d):
        raise ValueError("Os blocos do Avaliador estão fora de ordem.")
    questoes, gabarito = texto[a:b].strip(), texto[c:d].strip()
    if not questoes or not gabarito:
        raise ValueError("As questões ou o gabarito estão vazios.")
    return questoes, gabarito


def gerar_revisao(app, conteudo: str, prioridade: str, foco: str,
                  profundidade: str, tamanho_revisao: str) -> ReviewResult:
    from langchain_core.messages import HumanMessage, AIMessage

    mensagem = (
        f"Conteúdo estudado: {conteudo}\n"
        f"Prioridade: {prioridade}\n"
        f"Foco: {foco}\n"
        f"Profundidade: {profundidade}\n"
        f"Tamanho da revisão: {tamanho_revisao}"
    )
    # Estado criado do zero para cada pedido: não há memória persistente.
    resultado = app.invoke({"messages": [HumanMessage(content=mensagem)]},
                          config={"recursion_limit": 10})
    respostas = [m.content for m in resultado["messages"]
                 if isinstance(m, AIMessage) and isinstance(m.content, str) and m.content]
    if len(respostas) < 2:
        raise ValueError("Os agentes não retornaram revisão e avaliação.")
    questoes, gabarito = extrair_questoes_gabarito(respostas[-1])
    return ReviewResult(revisao=respostas[0], questoes=questoes, gabarito=gabarito)
