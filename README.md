# 🤖 AI Article Writer - Gerador Automático de Artigos com Agentes de IA

![Agentes de IA](https://img.shields.io/badge/AI-Agents-blue) ![Python](https://img.shields.io/badge/Python-3.8+-green) ![LangChain](https://img.shields.io/badge/LangChain-Framework-orange) ![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-purple)

## 📋 Sobre o Projeto

O **AI Article Writer** é uma aplicação inovadora que utiliza múltiplos agentes de Inteligência Artificial para criar artigos completos sobre tecnologia da informação de forma totalmente automatizada. O principal objetivo é gerar conteúdo de alta qualidade que possa ser facilmente publicado em redes sociais como **LinkedIn** e **Twitter**.

### 🎯 Objetivo Principal

Implementar agentes de Inteligência Artificial especializados para:
- ✍️ Escrever artigos técnicos de forma autônoma
- 🔍 Pesquisar informações atualizadas na internet
- 📱 Gerar conteúdo otimizado para redes sociais
- 🤝 Facilitar o compartilhamento de conhecimento técnico

## 🏗️ Arquitetura do Sistema

O projeto utiliza uma arquitetura multi-agente baseada em **LangChain** e **LangGraph**, onde cada agente tem uma responsabilidade específica:

### 🤖 Agentes Implementados

1. **🔍 Pesquisador Principal**
   - Busca informações gerais sobre o tema
   - Utiliza DuckDuckGo Search para coleta de dados
   - Gera resumo contextual do tema

2. **📂 Categorizador**
   - Deriva o tema em 5-7 sub-categorias relevantes
   - Cria descrições detalhadas para cada categoria
   - Garante cobertura abrangente do assunto

3. **🔎 Pesquisador de Sub-categorias**
   - Busca conteúdos específicos para cada sub-categoria
   - Processa pesquisas em paralelo para eficiência
   - Coleta dados especializados

4. **✏️ Escritor de Introdução**
   - Cria introdução envolvente de 150-200 palavras
   - Contextualiza o tema e apresenta as sub-categorias
   - Inclui emojis para engajamento

5. **📝 Escritor de Seções**
   - Desenvolve seções de 250-350 palavras por sub-categoria
   - Mantém consistência técnica e tom profissional
   - Conecta conteúdo ao contexto geral

6. **🏁 Escritor de Conclusão**
   - Sintetiza os pontos principais do artigo
   - Gera hashtags para redes sociais
   - Finaliza com call-to-action

7. **🎛️ Coordenador**
   - Consolida todo o conteúdo em Markdown
   - Converte para PDF automaticamente
   - Gerencia versionamento de arquivos

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+** - Linguagem principal
- **LangChain** - Framework para integração com LLMs
- **LangGraph** - Orquestração de agentes multi-agent
- **OpenAI GPT-4** - Modelo de linguagem principal
- **Ollama** - Alternativa para modelos locais
- **DuckDuckGo Search** - Ferramenta de busca
- **WeasyPrint** - Conversão Markdown para PDF
- **Markdown** - Formato de saída

## 🚀 Instalação e Configuração

### Pré-requisitos

```bash
# Python 3.8 ou superior
python --version

# Git para clonar o repositório
git --version
```

### 1. Clone o Repositório

```bash
git clone https://github.com/marcelolimagomes/ai-article-writer.git
cd ai-article-writer
```

### 2. Instale as Dependências

```bash
# Crie um ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt
```

### 3. Configure as Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Para usar OpenAI
OPENAI_API_KEY=sua_chave_openai_aqui

# Para usar Ollama (opcional)
OLLAMA_HOST=http://localhost:11434
```

### 4. Instale o Ollama (Opcional)

Se preferir usar modelos locais:

```bash
# Instale o Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Baixe um modelo (exemplo)
ollama pull gemma2:9b
```

## 💻 Como Usar

### Uso Básico

```bash
# Com OpenAI
python src/artigo.py openai "Inteligência Artificial"

# Com Ollama
python src/artigo.py ollama "Blockchain"
```

### Exemplos de Temas

```bash
# Temas de exemplo que funcionam bem
python src/artigo.py openai "Machine Learning"
python src/artigo.py openai "Desenvolvimento de Software"
python src/artigo.py openai "Segurança da Informação"
python src/artigo.py openai "Cloud Computing"
python src/artigo.py openai "Internet das Coisas"
```

### Saída Gerada

O sistema gera automaticamente:
- `artigo_tema.md` - Arquivo Markdown formatado
- `artigo_tema.pdf` - Versão PDF para compartilhamento
- Versionamento automático (`_v1`, `_v2`, etc.)

## 📁 Estrutura do Projeto

```
ai-article-writer/
├── src/
│   ├── artigo.py              # Script principal
│   ├── agents/                # Agentes individuais
│   │   ├── pesquisador_principal.py
│   │   ├── categorizador.py
│   │   └── pesquisador_subcategorias.py
│   ├── escritores.py          # Agentes de escrita
│   └── coordenador.py         # Coordenador final
├── articles/                  # Artigos gerados
├── nb/                        # Notebooks de teste
├── requirements.txt           # Dependências
├── .env.example              # Exemplo de configuração
└── README.md                 # Este arquivo
```

## 📊 Artigos Exemplo

O projeto já gerou diversos artigos sobre:
- 🤖 Criando Agentes de IA com LangChain e LangGraph
- 🔗 Implementação do Protocolo MCP
- 🛠️ Soluções Open Source com Ollama
- 📱 Desenvolvimento de Aplicações Móveis com IA
- 🔒 Segurança em Sistemas de IA

## 🎯 Casos de Uso

### Para Profissionais de TI
- 📝 Criação rápida de conteúdo técnico
- 📈 Geração de posts para LinkedIn
- 🎓 Material educativo sobre tecnologias

### Para Criadores de Conteúdo
- 🚀 Automatização de pesquisa e escrita
- 📱 Conteúdo otimizado para redes sociais
- ⏰ Economia de tempo na produção

### Para Estudantes
- 📚 Aprendizado sobre arquiteturas multi-agente
- 🔧 Prática com LangChain e LangGraph
- 💡 Exemplos reais de IA aplicada

## 🤝 Como Contribuir

Sua contribuição é muito bem-vinda! Existem várias formas de colaborar:

### 🐛 Reportar Bugs
- Abra uma issue descrevendo o problema
- Inclua logs e informações do ambiente
- Forneça passos para reproduzir

### 💡 Sugerir Melhorias
- Novas funcionalidades de agentes
- Melhorias na qualidade do texto
- Otimizações de performance
- Novos formatos de saída

### 🔧 Desenvolver
1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

### 📋 Ideas para Futuras Implementações
- [ ] Interface web para uso mais fácil
- [ ] Suporte a mais modelos LLM
- [ ] Integração direta com redes sociais
- [ ] Sistema de templates personalizáveis
- [ ] Análise de SEO e otimização
- [ ] Geração de imagens com IA
- [ ] Suporte a múltiplos idiomas

## 🔧 Configurações Avançadas

### Personalizando Prompts
Você pode modificar os prompts dos agentes editando o arquivo `src/artigo.py` nas funções de cada agente.

### Ajustando Parâmetros
- **Temperature**: Controla criatividade (0.1-1.0)
- **Max Results**: Número de resultados de pesquisa
- **Word Count**: Tamanho das seções

### Modelos Suportados
- **OpenAI**: gpt-4, gpt-3.5-turbo, gpt-4o-mini
- **Ollama**: llama2, gemma2, mistral, etc.

## 📈 Roadmap

### Versão 2.0
- [ ] Interface web intuitiva
- [ ] Dashboard de métricas
- [ ] Sistema de templates
- [ ] Integração com CMS

### Versão 3.0
- [ ] Agentes especializados por área
- [ ] Sistema de aprendizado contínuo
- [ ] API REST para integração
- [ ] Marketplace de agentes

## 🚨 Troubleshooting

### Problemas Comuns

**Erro de API Key**
```bash
Error: Invalid API key
```
Solução: Verifique se a `OPENAI_API_KEY` está configurada corretamente no `.env`

**Timeout na Pesquisa**
```bash
Timeout ao buscar informações
```
Solução: Verifique sua conexão com a internet e tente novamente

**Erro de Conversão PDF**
```bash
Erro na conversão para PDF
```
Solução: Instale `weasyprint` corretamente: `pip install weasyprint`

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🌟 Agradecimentos

Agradecimentos especiais à comunidade open source e aos projetos que tornaram isso possível:
- [LangChain](https://langchain.com/) - Framework para LLMs
- [LangGraph](https://langchain-ai.github.io/langgraph/) - Orquestração multi-agente
- [OpenAI](https://openai.com/) - Modelos de linguagem
- [Ollama](https://ollama.ai/) - Modelos locais

## 📞 Contato e Conexões

### 👨‍💻 Sobre o Autor
**Marcelo Lima Gomes** - Desenvolvedor especializado em IA e soluções inovadoras

### 🔗 Conecte-se Comigo
- **GitHub**: [github.com/marcelolimagomes](https://github.com/marcelolimagomes)
- **LinkedIn**: [linkedin.com/in/marcelolimagomes](https://linkedin.com/in/marcelolimagomes)

### 💬 Vamos Colaborar!
Estou sempre aberto a:
- 🤝 Novas colaborações
- 💡 Discussões sobre IA e tecnologia
- 🚀 Projetos inovadores
- 📚 Compartilhamento de conhecimento

**Conecte-se comigo no LinkedIn e vamos construir o futuro da IA juntos!** 🚀

---

⭐ **Se este projeto foi útil para você, considere dar uma estrela no GitHub!** ⭐

📢 **Compartilhe nas redes sociais e ajude a comunidade a crescer!**

#IA #InteligenciaArtificial #Python #LangChain #AutomacaoDeConteudo #TecnologiaDaInformacao
