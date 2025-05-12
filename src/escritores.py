from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Introdução
intro_tmpl = PromptTemplate(input_variables=["tema"], template="Escreva uma introdução de 100-150 palavras para o tema \"{tema}\" em Markdown.")
intro_chain = LLMChain(llm=OpenAI(temperature=0.7), prompt=intro_tmpl)


def escrever_introducao(tema: str, pesquisador_principal):
    return intro_chain.run(tema=tema)


# Seção por sub-categoria
secao_tmpl = PromptTemplate(input_variables=["subcategoria", "resultados"], template="""
Escreva uma seção de 200-300 palavras em Markdown sobre "{subcategoria}", usando estes pontos de pesquisa:
{resultados}
""")
secao_chain = LLMChain(llm=OpenAI(temperature=0.7), prompt=secao_tmpl)


def escrever_secao(item):
    return secao_chain.run(subcategoria=item["subcategoria"], resultados=item["resultados"])


# Conclusão
concl_tmpl = PromptTemplate(input_variables=["introducao", "secoes"], template="""
Com base na introdução e nas seções abaixo, escreva uma conclusão de 100-150 palavras em Markdown:
Introdução:
{introducao}

Seções:
{secoes}
""")
concl_chain = LLMChain(llm=OpenAI(temperature=0.7), prompt=concl_tmpl)


def escrever_conclusao(escrever_introducao, escrever_secao, pesquisador_principal):
    secoes = "\n\n".join(escrever_secao)
    return concl_chain.run(introducao=escrever_introducao, secoes=secoes)
