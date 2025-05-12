import sys
import os
import logging
from typing import List, Dict, TypedDict, Optional
from langchain_community.tools import DuckDuckGoSearchRun, DuckDuckGoSearchResults
from langchain_community.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper
from langchain_openai import ChatOpenAI
from langchain_ollama.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
import markdown
from weasyprint import HTML
import re
import json
import random
from dotenv import load_dotenv


load_dotenv()

# Configuração do logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)


class CustomDuckDuckGoSearchAPIWrapper(DuckDuckGoSearchAPIWrapper):
    def _ddgs_images(
        self, query: str, max_results: Optional[int] = None
    ) -> List[Dict[str, str]]:
        """Run query through DuckDuckGo image search and return results."""
        logging.info(f"Run query through DuckDuckGo image search and return results. Query: {query}")
        from duckduckgo_search import DDGS
        try:
            with DDGS(timeout=30) as ddgs:  # Aumente o timeout para 30 segundos
                ddgs_gen = ddgs.images(
                    query,
                    region=self.region,  # type: ignore[arg-type]
                    safesearch=self.safesearch,
                    max_results=max_results or self.max_results,
                )
                if ddgs_gen:
                    return [r for r in ddgs_gen]
        except Exception as e:
            logger.error(f"Timeout ao buscar imagens para a consulta: {e}")

        return []

# Estado compartilhado para o grafo


class ArticleState(TypedDict):
    topic: str
    main_search_results: List[Dict]
    context_summary: str
    subcategories: List[Dict[str, str]]
    subcategory_results: List[Dict[str, List[Dict]]]
    main_image: str
    # subcategory_images: List[Dict[str, str]]
    introduction: str
    sections: List[str]
    conclusion: str
    markdown_content: str


# Inicialização das ferramentas e modelo de linguagem
search_tool = DuckDuckGoSearchRun()
image_search_tool = DuckDuckGoSearchResults(
    api_wrapper=CustomDuckDuckGoSearchAPIWrapper(),
    output_format="json",
    max_results=1,
    backend="images",
)
llm = None  # ChatOpenAI(model="gpt-4o-mini", temperature=0.7)  # Substitua por Grok se disponível

# Função para validar o tema


def validate_topic(topic: str) -> bool:
    if not topic or topic.strip() == "":
        logger.error("O tema não pode ser vazio.")
        return False
    return True

# Agente 1: Pesquisador Principal


def main_researcher(state: ArticleState) -> ArticleState:
    """Busca conteúdos e uma imagem relacionada ao tema principal."""
    topic = state["topic"]
    logger.info(f"Iniciando pesquisa principal para o tema: {topic}")

    # Busca de conteúdo
    try:
        results = search_tool.run(topic + " tecnologia da informação")
        main_search_results = [{"url": f"result_{i}", "snippet": result} for i, result in enumerate(results.split("\n")[:5])]
        logger.debug(f"Resultados da pesquisa principal: {main_search_results}")
    except Exception as e:
        logger.error(f"Erro na pesquisa principal: {e}")
        main_search_results = []

    # Busca de imagem
    try:
        image_results = json.loads(image_search_tool.run(topic))
        len_results = len(image_results)
        logger.debug(f"Resultados encontrados: {len_results} - {image_results}")
        random.shuffle(image_results)
        main_image = image_results[0]['image'] if len_results > 0 else ""
        logger.debug(f"Imagem principal encontrada: {main_image}")
    except Exception as e:
        logger.error(f"Erro na busca de imagem principal: {e}")
        main_image = ""

    # Gera resumo do contexto
    snippets = "\n".join([res["snippet"] for res in main_search_results])
    prompt = ChatPromptTemplate.from_template(
        "Resuma o tema '{topic}' em 80-120 palavras com base nos resultados de pesquisa:\n{snippets}\n"
        "O resumo deve capturar a essência do tema no contexto de tecnologia da informação."
    )
    try:
        context_summary = llm.invoke(prompt.format(topic=topic, snippets=snippets)).content
        logger.debug(f"Resumo do contexto gerado: {context_summary[:50]}...")
    except Exception as e:
        logger.error(f"Erro na geração do resumo do contexto: {e}")
        context_summary = ""

    return {
        "main_search_results": main_search_results,
        "main_image": main_image,
        "context_summary": context_summary
    }

# Agente 2: Categorizador


def categorizer(state: ArticleState) -> ArticleState:
    """Deriva o tema principal em 5-7 sub-categorias com descrições."""
    topic = state["topic"]
    context_summary = state["context_summary"]
    main_results = state["main_search_results"]
    snippets = "\n".join([res["snippet"] for res in main_results])

    prompt = ChatPromptTemplate.from_template(
        "Com base no tema '{topic}', no resumo do contexto:\n{context_summary}\n"
        "e nos resultados de pesquisa:\n{snippets}\n"
        "Gere uma lista de 5 a 7 sub-categorias relevantes para um artigo sobre tecnologia da informação. "
        "Para cada sub-categoria, forneça uma breve descrição (50-80 palavras). "
        "Retorne em formato Markdown, como:\n1. Sub-categoria: Descrição\n"
    )
    logger.info(f"Gerando sub-categorias para o tema: {topic}")
    try:
        response = llm.invoke(prompt.format(topic=topic, context_summary=context_summary, snippets=snippets)).content
        subcategories = []
        for line in response.split("\n"):
            if line.strip() and line.startswith(tuple(f"{i}." for i in range(1, 6))):
                name, desc = line.split(":", 1)
                subcategories.append({"name": name.strip()[2:].strip(), "description": desc.strip()})
        if len(subcategories) < 3:
            logger.error("Menos de 3 sub-categorias geradas.")
            return {"subcategories": []}
        logger.debug(f"Sub-categorias geradas: {[sub['name'] for sub in subcategories]}")
        return {"subcategories": subcategories[:5]}
    except Exception as e:
        logger.error(f"Erro na categorização: {e}")
        return {"subcategories": []}

# Agente 3: Pesquisador de Sub-categorias


def subcategory_researcher(state: ArticleState) -> ArticleState:
    """Busca conteúdos e imagens para cada sub-categoria."""
    subcategories = state["subcategories"]
    subcategory_results = []
    # subcategory_images = []

    logger.info("Iniciando pesquisa para sub-categorias")
    for subcategory in subcategories:
        subcategory_name = subcategory["name"]
        try:
            # Busca de conteúdo
            results = search_tool.run(subcategory_name + " tecnologia da informação")
            subcategory_results.append({
                "subcategory": subcategory_name,
                "results": [{"url": f"result_{i}", "snippet": result} for i, result in enumerate(results.split("\n")[:5])]
            })
            logger.debug(f"Resultados para sub-categoria {subcategory_name}: {subcategory_results[-1]['results']}")
        except Exception as e:
            logger.error(f"Erro na pesquisa da sub-categoria {subcategory_name}: {e}")
            subcategory_results.append({"subcategory": subcategory_name, "results": []})

        # try:
        #     # Busca de imagem
        #     image_results = json.loads(image_search_tool.run(subcategory_name))
        #     len_results = len(image_results)
        #     random.shuffle(image_results)
        #     image_url = image_results[0]['image'] if len_results > 0 else ""
        #     subcategory_images.append({"subcategory": subcategory_name, "image": image_url})
        #     logger.debug(f"Imagem para sub-categoria {subcategory_name}: {image_url}")
        # except Exception as e:
        #     logger.error(f"Erro na pesquisa das imagens para sub-categoria {subcategory_name}: {e}")
        #     subcategory_images.append({"subcategory": subcategory_name, "image": ""})

    return {
        "subcategory_results": subcategory_results,
        # "subcategory_images": subcategory_images
    }

# Agente 4: Escritor de Introdução


def introduction_writer(state: ArticleState) -> ArticleState:
    """Escreve a introdução do artigo em Markdown, alinhada ao contexto e sub-categorias."""
    topic = state["topic"]
    context_summary = state["context_summary"]
    main_results = state["main_search_results"]
    subcategories = state["subcategories"]
    snippets = "\n".join([res["snippet"] for res in main_results])
    subcat_list = "\n".join([f"- {sub['name']}: {sub['description']}" for sub in subcategories])

    prompt = ChatPromptTemplate.from_template(
        "Escreva uma introdução de 150 a 200 palavras para um artigo sobre '{topic}' no contexto de tecnologia da informação. "
        "Use o resumo do contexto:\n{context_summary}\n"
        "e os resultados de pesquisa:\n{snippets}\n"
        "A introdução deve apresentar o tema, sua relevância e mencionar as sub-categorias a seguir:\n{subcat_list}\n"
        "Utilize emojis para tornar o texto mais envolvente.\n"
        "Formate em Markdown, começando com '## Introdução'."
    )
    logger.info(f"Escrevendo introdução para o tema: {topic}")
    try:
        introduction = llm.invoke(prompt.format(
            topic=topic, context_summary=context_summary, snippets=snippets, subcat_list=subcat_list
        )).content
        logger.debug(f"Introdução gerada: {introduction[:50]}...")
        return {"introduction": introduction}
    except Exception as e:
        logger.error(f"Erro na escrita da introdução: {e}")
        return {"introduction": "## Introdução\nErro ao gerar conteúdo."}

# Agente 5: Escritor de Seções


def section_writer(state: ArticleState) -> ArticleState:
    """Escreve seções para cada sub-categoria em Markdown, alinhadas ao contexto."""
    subcategory_results = state["subcategory_results"]
    context_summary = state["context_summary"]
    sections = []

    prompt = ChatPromptTemplate.from_template(
        "Escreva uma seção de 250 a 350 palavras sobre '{subcategory}' no contexto de tecnologia da informação. "
        "Use o resumo do contexto do artigo:\n{context_summary}\n"
        "e os resultados de pesquisa:\n{snippets}\n"
        "A seção deve conectar o tema ao contexto geral do artigo e ser informativa, com tom profissional. Utilize emojis para tornar o texto mais envolvente. "
        "Formate em Markdown, começando com '## {subcategory}'. "
    )

    logger.info("Escrevendo seções para sub-categorias")
    for subcat in subcategory_results:
        subcategory = subcat["subcategory"]
        snippets = "\n".join([res["snippet"] for res in subcat["results"]])
        try:
            section = llm.invoke(prompt.format(
                subcategory=subcategory, context_summary=context_summary, snippets=snippets
            )).content
            sections.append(section)
            logger.debug(f"Seção gerada para {subcategory}: {section[:50]}...")
        except Exception as e:
            logger.error(f"Erro na escrita da seção {subcategory}: {e}")
            sections.append(f"## {subcategory}\nErro ao gerar conteúdo.")

    return {"sections": sections}

# Agente 6: Escritor de Conclusão


def conclusion_writer(state: ArticleState) -> ArticleState:
    """Escreve a conclusão do artigo em Markdown, sintetizando o contexto e seções."""
    topic = state["topic"]
    context_summary = state["context_summary"]
    introduction = state["introduction"]
    sections = state["sections"]

    prompt = ChatPromptTemplate.from_template(
        "Escreva uma conclusão de 150 a 200 palavras para um artigo sobre '{topic}' no contexto de tecnologia da informação. "
        "Use o resumo do contexto:\n{context_summary}\n"
        "Considere a introdução:\n{introduction}\n"
        "e as seções:\n{sections}\n"
        "A conclusão deve resumir os pontos principais, destacar a importância do tema e conectar as seções ao contexto geral. Utilize emojis para tornar o texto mais envolvente. "
        "Formate em Markdown, começando com '## Conclusão'."
        "Gere hashtags para publicação do conteúdo em redes sociais no final do texto com base no tema e no conteúdo do artigo. "
    )
    logger.info(f"Escrevendo conclusão para o tema: {topic}")
    try:
        conclusion = llm.invoke(prompt.format(
            topic=topic, context_summary=context_summary, introduction=introduction, sections="\n".join(sections)
        )).content
        logger.debug(f"Conclusão gerada: {conclusion[:50]}...")
        return {"conclusion": conclusion}
    except Exception as e:
        logger.error(f"Erro na escrita da conclusão: {e}")
        return {"conclusion": "## Conclusão\nErro ao gerar conteúdo."}

# Agente 7: Coordenador


def coordinator(state: ArticleState) -> ArticleState:
    """Consolida o conteúdo em Markdown com imagens e converte para PDF."""
    topic = state["topic"]
    introduction = state["introduction"]
    sections = state["sections"]
    conclusion = state["conclusion"]
    main_image = state["main_image"]
    # subcategory_images = state["subcategory_images"]

    # Consolida o conteúdo em Markdown
    markdown_content = f"# Artigo: {topic}\n\n"
    if main_image:
        markdown_content += f"![{topic}]({main_image})\n\n"
    markdown_content += f"{introduction}\n\n"

    # for section, subcat_image in zip(sections, subcategory_images):
    #     if subcat_image["image"]:
    #         markdown_content += f"![{subcat_image['subcategory']}]({subcat_image['image']})\n\n"
    #     markdown_content += f"{section}\n\n"

    for section in sections:
        markdown_content += f"{section}\n\n"

    markdown_content += conclusion

    # Salva o arquivo Markdown com versionamento
    dir_name = os.path.dirname('./articles/')
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    safe_filename = re.sub(r'[^\w\s-]', '', topic.lower().replace(' ', '_'))
    base_name = f"artigo_{safe_filename}"
    counter = 1
    md_filename = os.path.join(dir_name, f"{base_name}.md")
    while os.path.exists(md_filename):
        md_filename = os.path.join(dir_name, f"{base_name}_v{counter}.md")
        counter += 1
    markdown_file = md_filename

    try:
        with open(markdown_file, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        logger.info(f"Arquivo Markdown gerado: {markdown_file}")
    except Exception as e:
        logger.error(f"Erro ao salvar arquivo Markdown: {e}")

    # Converte para PDF com versionamento
    counter = 1

    pdf_filename = os.path.join(dir_name, f"{base_name}.pdf")

    while os.path.exists(pdf_filename):
        pdf_filename = os.path.join(dir_name, f"{base_name}_v{counter}.pdf")
        counter += 1
    pdf_file = pdf_filename

    try:
        html_content = markdown.markdown(markdown_content)
        HTML(string=html_content).write_pdf(pdf_file)
        logger.info(f"Arquivo PDF gerado: {pdf_file}")
    except Exception as e:
        logger.error(f"Erro na conversão para PDF: {e}")

    return {"markdown_content": markdown_content}


def setup_agents():
    # Definição do grafo
    workflow = StateGraph(ArticleState)

    # Adiciona nós para cada agente
    workflow.add_node("main_researcher", main_researcher)
    workflow.add_node("categorizer", categorizer)
    workflow.add_node("subcategory_researcher", subcategory_researcher)
    workflow.add_node("introduction_writer", introduction_writer)
    workflow.add_node("section_writer", section_writer)
    workflow.add_node("conclusion_writer", conclusion_writer)
    workflow.add_node("coordinator", coordinator)

    # Define as transições
    workflow.set_entry_point("main_researcher")
    workflow.add_edge("main_researcher", "categorizer")
    workflow.add_edge("categorizer", "subcategory_researcher")
    workflow.add_edge("subcategory_researcher", "introduction_writer")
    workflow.add_edge("introduction_writer", "section_writer")
    workflow.add_edge("section_writer", "conclusion_writer")
    workflow.add_edge("conclusion_writer", "coordinator")
    workflow.add_edge("coordinator", END)

    # Compila o grafo
    app = workflow.compile()
    return app

# Função principal


def main():
    if len(sys.argv) != 3:
        logger.error("Uso incorreto. Exemplo: python artigo.py <openai|ollama> <tema>")
        sys.exit(1)

    logger.info("Iniciando o gerador de artigos. Parâmetros recebidos: \n1:[%s]\n2:[%s]", sys.argv[1], sys.argv[2])

    llm_name = sys.argv[1]
    global llm
    if llm_name == "openai":
        logger.info("Usando modelo de linguagem OpenAI.")
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    elif llm_name == "ollama":
        logger.info("Usando modelo de linguagem Ollama.")
        llm = ChatOllama(model="gemma3:12b", temperature=0.7)
    else:
        logger.error("Modelo de linguagem inválido. Use 'openai' ou 'ollama'.")
        sys.exit(1)

    topic = sys.argv[2]
    if not validate_topic(topic):
        sys.exit(1)

    logger.info(f"Iniciando geração do artigo para o tema: {topic}")
    # Executa o grafo
    initial_state = {
        "topic": topic,
        "main_search_results": [],
        "context_summary": "",
        "subcategories": [],
        "subcategory_results": [],
        "main_image": "",
        # "subcategory_images": [],
        "introduction": "",
        "sections": [],
        "conclusion": "",
        "markdown_content": ""
    }
    try:
        app = setup_agents()
        result = app.invoke(initial_state)
        if not result["markdown_content"]:
            logger.error("Nenhum conteúdo gerado.")
    except Exception as e:
        logger.error(f"Erro na execução do grafo: {e}")


if __name__ == "__main__":
    main()
