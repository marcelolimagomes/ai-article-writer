Sou desenvolvedor de software especializado em inteligência artificial, trabalhando com Python e as bibliotecas LangChain e LangGraph. Estou pesquisando a eficiência de agentes de IA na automação de processos e desejo criar uma aplicação para testar essa eficiência.

**Objetivo**: Desenvolver uma aplicação Python baseada em multi-agentes que automatize a escrita de artigos sobre temas de tecnologia da informação, fornecidos pelo usuário via linha de comando. A aplicação deve usar LangChain e LangGraph para orquestrar os agentes, consolidar o conteúdo em formato Markdown e convertê-lo para PDF.

**Requisitos da Aplicação**:

1. **Entrada do Usuário**: O usuário fornece o tema principal do artigo (e.g., "Inteligência Artificial") via linha de comando. A aplicação deve validar a entrada, rejeitando temas vagos ou inválidos (e.g., strings vazias).
2. **Agentes e Funções**:
   - **Agente 1: Pesquisador Principal**:
     - Função: Buscar conteúdos na internet relacionados ao tema principal.
     - Ferramenta: DuckDuckGo Search (https://python.langchain.com/docs/integrations/tools/ddg/).
     - Entrada: Tema principal.
     - Saída: Lista de resultados (URLs e resumos).
   - **Agente 2: Categorizador**:
     - Função: Derivar o tema principal em até 3-5 sub-categorias relevantes (e.g., para "Inteligência Artificial": "Aprendizado de Máquina", "Redes Neurais", "Ética em IA").
     - Ferramenta: Modelo de linguagem integrado ao LangChain (e.g., Grok ou outro LLM).
     - Entrada: Tema principal e resultados do Pesquisador Principal.
     - Saída: Lista numerada de sub-categorias.
   - **Agente 3: Pesquisador de Sub-categorias**:
     - Função: Buscar conteúdos na internet para cada sub-categoria, processando-as em paralelo para maior eficiência.
     - Ferramenta: DuckDuckGo Search (https://python.langchain.com/docs/integrations/tools/ddg/).
     - Entrada: Lista de sub-categorias.
     - Saída: Lista de pares (sub-categoria, resultados de pesquisa).
   - **Agente 4: Escritor de Introdução**:
     - Função: Escrever uma introdução de 100-150 palavras para o artigo, apresentando o tema principal.
     - Ferramenta: Modelo de linguagem integrado ao LangChain.
     - Entrada: Tema principal e resultados do Pesquisador Principal.
     - Saída: Texto da introdução em Markdown.
   - **Agente 5: Escritor de Seções**:
     - Função: Escrever uma seção de 200-300 palavras para cada sub-categoria, processando-as em paralelo.
     - Ferramenta: Modelo de linguagem integrado ao LangChain.
     - Entrada: Lista de pares (sub-categoria, resultados de pesquisa).
     - Saída: Lista de textos de seções em Markdown.
   - **Agente 6: Escritor de Conclusão**:
     - Função: Escrever uma conclusão de 100-150 palavras, resumindo o artigo.
     - Ferramenta: Modelo de linguagem integrado ao LangChain.
     - Entrada: Introdução, lista de seções e resultados do Pesquisador Principal.
     - Saída: Texto da conclusão em Markdown.
   - **Agente 7: Coordenador**:
     - Função: Consolidar introdução, seções e conclusão em um único arquivo Markdown e convertê-lo para PDF.
     - Ferramenta: Biblioteca `weasyprint` para conversão de Markdown para PDF.
     - Entrada: Introdução, lista de seções e conclusão.
     - Saída: Arquivo Markdown e arquivo PDF.
3. **Fluxo de Execução**:
   - Os agentes operam em sequência, com dependências claras: Pesquisador Principal → Categorizador → Pesquisador de Sub-categorias → Escritores (Introdução, Seções, Conclusão) → Coordenador.
   - As buscas e escrita de seções por sub-categoria devem ser paralelas, usando as capacidades de LangGraph para map-reduce.
   - O estado compartilhado no LangGraph gerencia a passagem de dados entre agentes.
4. **Saída**:
   - Um arquivo Markdown com o artigo completo (título, introdução, seções, conclusão).
   - Um arquivo PDF gerado a partir do Markdown, salvo no mesmo diretório.
5. **Robustez**:
   - Tratar erros, como falhas na pesquisa ou temas inválidos, exibindo mensagens claras ao usuário.
   - Garantir que o artigo tenha conteúdo suficiente (e.g., mínimo de 3 sub-categorias).
6. **Ferramentas e Bibliotecas**:
   - **LangChain**: Para integração com DuckDuckGo Search e modelos de linguagem.
   - **LangGraph**: Para orquestração dos agentes e gerenciamento do estado.
   - **DuckDuckGo Search**: Para buscas na internet.
   - **Weasyprint**: Para conversão de Markdown para PDF.
   - **Modelo de Linguagem**: Um LLM integrado ao LangChain (e.g., Grok, via API da xAI, ou outro).

**Código Fonte**:

- Escrever o código em Python, usando LangChain e LangGraph.
- Incluir comentários explicando a função de cada agente e o fluxo do LangGraph.
- Estruturar o código em módulos (e.g., agentes, ferramentas, coordenador) para maior clareza.

**Exemplo de Uso**:

```bash
python artigo.py "Inteligência Artificial"
```

Saída: Arquivo `artigo_inteligencia_artificial.md` e `artigo_inteligencia_artificial.pdf` no diretório atual.