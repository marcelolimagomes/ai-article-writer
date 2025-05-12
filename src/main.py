import sys
from langgraph import Graph
from agents.pesquisador_principal import pesquisador_principal
from agents.categorizador import categorizador
from agents.pesquisador_subcategorias import pesquisador_subcategorias
from escritores import escrever_introducao, escrever_secao, escrever_conclusao
from coordenador import coordenador


def main():
    if len(sys.argv) < 2 or not sys.argv[1].strip():
        print("Tema inválido. Forneça um tema válido.")
        sys.exit(1)
    tema = sys.argv[1].strip()

    graph = Graph()
    gp = graph.node("pesquisador_principal", func=pesquisador_principal, input_keys=["tema"])
    gc = graph.node("categorizador", func=categorizador, input_keys=["tema", "pesquisador_principal"])
    gs = graph.map("pesquisador_subcategorias", func=pesquisador_subcategorias, items_key="categorizador")
    gi = graph.node("escrever_introducao", func=escrever_introducao, input_keys=["tema", "pesquisador_principal"])
    gse = graph.map("escrever_secao", func=escrever_secao, items_key="pesquisador_subcategorias")
    gf = graph.node("escrever_conclusao", func=escrever_conclusao, input_keys=["escrever_introducao", "escrever_secao", "pesquisador_principal"])
    coord = graph.node("coordenador", func=coordenador, input_keys=["tema", "escrever_introducao", "escrever_secao", "escrever_conclusao"])

    gp >> gc >> gs
    gs >> gse
    [gi, gse, gf] >> coord

    result = graph.run({"tema": tema})
    print(f"Artigo gerado em PDF: {result['coordenador']}")


if __name__ == "__main__":
    main()
