from langchain.tools import DuckDuckGoSearchRun


def pesquisador_principal(tema: str):
    search = DuckDuckGoSearchRun()
    raw = search.run(tema)
    # aqui você pode processar raw para extrair url e snippet
    return raw
