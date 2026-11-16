"""Interface de linha de comando do assistente de estudos multiagente."""

from src.preferences import (
    NOMES_FOCOS, PROFUNDIDADES, TAMANHOS, gerar_opcoes,
)


def escolher_opcao(titulo: str, opcoes: list | tuple, nomes=None, input_fn=input) -> str:
    if not opcoes:
        raise ValueError("Não há opções para selecionar.")
    print(f"\n{titulo}")
    for numero, opcao in enumerate(opcoes, start=1):
        print(f"{numero}. {nomes.get(opcao, opcao) if nomes else opcao}")
    while True:
        resposta = input_fn("Digite o número da opção: ").strip()
        if resposta.isdigit() and 1 <= int(resposta) <= len(opcoes):
            return opcoes[int(resposta) - 1]
        print("Opção inválida. Tente novamente.")


def executar():
    # Importações adiadas para manter o menu testável sem carregar a integração de IA.
    from src.settings import ensure_groq_api_key, create_llms
    from src.graph import build_graph
    from src.review import gerar_revisao

    print("=== Multi-Agent Study Assistant ===")
    conteudo = input("Descreva o conteúdo que você estudou: ").strip()
    while not conteudo:
        print("O conteúdo não pode ficar vazio.")
        conteudo = input("Descreva o conteúdo que você estudou: ").strip()

    ensure_groq_api_key()
    llm_tutor, llm_avaliador = create_llms()
    app = build_graph(llm_tutor, llm_avaliador)

    print("\nAnalisando o conteúdo...")
    opcoes = gerar_opcoes(conteudo, llm_tutor)
    prioridade = escolher_opcao("Qual tópico você quer priorizar?", opcoes["topicos"])
    foco = escolher_opcao("Qual deve ser o foco da revisão?", opcoes["focos"], NOMES_FOCOS)
    profundidade = escolher_opcao("Qual deve ser a profundidade?", PROFUNDIDADES,
                                 {"basica": "Básica", "intermediaria": "Intermediária", "avancada": "Avançada"})
    tamanho = escolher_opcao("Qual deve ser o tamanho?", TAMANHOS,
                            {"curta": "Curta", "media": "Média", "detalhada": "Detalhada"})

    print("\nGerando sua revisão...\n")
    resultado = gerar_revisao(app, conteudo, prioridade, foco, profundidade, tamanho)
    print("\n=== REVISÃO ===\n" + resultado.revisao)
    print("\n=== QUESTÕES ===\n" + resultado.questoes)
    mostrar = input("\nDeseja visualizar o gabarito? [s/N]: ").strip().lower()
    if mostrar in ("s", "sim"):
        print("\n=== GABARITO ===\n" + resultado.gabarito)
    else:
        print("Gabarito não exibido.")


if __name__ == "__main__":
    try:
        executar()
    except (ValueError, RuntimeError) as exc:
        print(f"\nNão foi possível concluir a revisão: {exc}")
        raise SystemExit(1) from exc
    except KeyboardInterrupt:
        print("\nExecução interrompida.")
        raise SystemExit(130)
