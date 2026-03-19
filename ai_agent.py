import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

template = """
Você é o assistente virtual de uma academia.
Dados do Aluno que mandou a mensagem:
- Nome: {nome}
- Objetivo: {objetivo}
- Nível: {nivel_experiencia}
- Mensalidade Ativa: {mensalidade_ativa}

Responda à seguinte mensagem do aluno de forma curta, prestativa e motivadora. 
Se a mensalidade não estiver ativa, lembre-o educadamente de renovar.

Mensagem do aluno: {mensagem}
Sua resposta:
"""

prompt = PromptTemplate.from_template(template)
chain = prompt | llm | StrOutputParser()

def gerar_resposta_ia(aluno_dados: dict, mensagem_recebida: str) -> str:
    return chain.invoke({
        "nome": aluno_dados["nome"],
        "objetivo": aluno_dados["objetivo"],
        "nivel_experiencia": aluno_dados["nivel_experiencia"],
        "mensalidade_ativa": "Sim" if aluno_dados["mensalidade_ativa"] else "Não",
        "mensagem": mensagem_recebida
    })