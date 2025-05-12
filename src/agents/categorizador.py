from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

template = """Liste entre 3 e 5 sub-categorias relevantes para o tema "{tema}"."""
prompt = PromptTemplate(input_variables=["tema"], template=template)
chain = LLMChain(llm=OpenAI(temperature=0.7), prompt=prompt)


def categorizador(tema: str, pesquisador_principal):
    resposta = chain.run(tema=tema)
    # parseie resposta em lista, ex.: split por linhas
    subcats = [line.strip("- ").strip() for line in resposta.splitlines() if line.strip()]
    return subcats
