"""Grafo fixo: Tutor -> Avaliador -> ferramenta -> Avaliador."""

from langgraph.graph import StateGraph, START, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from src.agents import build_agents
from src.tools import configurar_estrategia_avaliacao


def build_graph(llm_tutor, llm_avaliador):
    tools = [configurar_estrategia_avaliacao]
    tutor, avaliador = build_agents(llm_tutor, llm_avaliador, tools)

    grafo = StateGraph(MessagesState)
    grafo.add_node("tutor", tutor)
    grafo.add_node("avaliador", avaliador)
    grafo.add_node("tools", ToolNode(tools))
    grafo.add_edge(START, "tutor")
    grafo.add_edge("tutor", "avaliador")
    grafo.add_conditional_edges("avaliador", tools_condition)
    grafo.add_edge("tools", "avaliador")
    return grafo.compile()
