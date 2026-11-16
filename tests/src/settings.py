"""Configuração de acesso ao modelo de linguagem."""

import os
from getpass import getpass

MODEL_NAME = "openai/gpt-oss-20b"


def ensure_groq_api_key() -> None:
    """Solicita a chave em ambiente interativo quando ainda não configurada."""
    if not os.getenv("GROQ_API_KEY"):
        key = getpass("Groq API Key: ").strip()
        if not key:
            raise ValueError("É necessário informar GROQ_API_KEY para usar os agentes.")
        os.environ["GROQ_API_KEY"] = key


def create_llms():
    from langchain_groq import ChatGroq

    return (
        ChatGroq(model=MODEL_NAME, temperature=0.2),
        ChatGroq(model=MODEL_NAME, temperature=0.4),
    )
