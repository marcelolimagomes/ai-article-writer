from langchain.tools import DuckDuckGoSearchRun


def pesquisador_subcategorias(subcategoria: str):
    tool = DuckDuckGoSearchRun()
    resultados = tool.run(subcategoria)
    return {"subcategoria": subcategoria, "resultados": resultados}
