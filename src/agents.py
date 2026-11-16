"""Responsabilidades independentes dos dois agentes."""

from langchain_core.messages import SystemMessage

TUTOR_INSTRUCTIONS = """Você é um tutor responsável por produzir uma revisão do conteúdo estudado.
Produza uma revisão, não uma aula para aprender o conteúdo do zero.
Respeite o tamanho solicitado:
- curta: no máximo 120 palavras, até 3 tópicos, sem tabelas ou exemplos extensos;
- media: entre 200 e 300 palavras, podendo incluir um exemplo curto;
- detalhada: até 500 palavras, com explicações e exemplos quando úteis.
Dê maior atenção ao tópico indicado como prioridade.
Não crie questões; sua função é apenas realizar a revisão.
"""

AVALIADOR_INSTRUCTIONS = """Você é um avaliador responsável por criar questões de revisão
com base na revisão produzida pelo Tutor e nas preferências do usuário.
Antes de gerar as questões, use a ferramenta disponível para definir a estratégia.
Siga a estratégia retornada quanto à quantidade e aos tipos de questões,
nível de dificuldade e abordagem. Dê maior atenção à prioridade indicada.
Gere questões de múltipla escolha e abertas; não refaça a revisão.
Gere as respostas, mas não as revele junto das questões.
A resposta final deve usar obrigatoriamente estes delimitadores:
<QUESTOES>
Questões para o estudante, sem respostas nem gabarito.
</QUESTOES>
<GABARITO>
Respostas corretas das questões e respostas esperadas das abertas.
</GABARITO>
"""


def build_agents(llm_tutor, llm_avaliador, tools):
    """Cria os nós com dependências explícitas, sem variáveis globais de modelo."""
    avaliador_com_ferramentas = llm_avaliador.bind_tools(tools)

    def tutor(state):
        response = llm_tutor.invoke([SystemMessage(content=TUTOR_INSTRUCTIONS)] + state["messages"])
        return {"messages": [response]}

    def avaliador(state):
        response = avaliador_com_ferramentas.invoke(
            [SystemMessage(content=AVALIADOR_INSTRUCTIONS)] + state["messages"]
        )
        return {"messages": [response]}

    return tutor, avaliador
