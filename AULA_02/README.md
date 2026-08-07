# Introdução à IA - Aula 02
Este projeto contém o código para conversão de documentos PDF em Markdown utilizando a biblioteca Docling, além da extração de metadados estruturados (título, autores e ano) utilizando Structured Outputs via API.

## Passo a Passo para Configuração e Execução

### 1. Ativar o Ambiente Virtual
No Linux/macOS

source venv/bin/activate

No Windows

venv\Scripts\activate


### 2. Instalar o Docling

pip install docling


Documentação oficial: https://docling-project.github.io/docling/getting_started/installation/

### 3. Converter os PDFs para Markdown
Os arquivos PDF originais (bioética e IA, escrita acadêmica, algoritmo do Twitter) foram convertidos para Markdown utilizando o Docling, preservando títulos, parágrafos e estrutura do documento.

### 4. Extrair Metadados com Structured Outputs
Para cada arquivo `.md` gerado, foi utilizada uma chamada de API (via OpenRouter, modelo `openai/gpt-oss-20b:free`) com Structured Outputs para extrair:
- **Título** do trabalho
- **Autores** (lista)
- **Ano** de publicação

O resultado é salvo em um arquivo `.json` correspondente, no formato:

{
"titulo": "Título do trabalho",
"autores": ["Autor 1", "Autor 2"],
"ano": 2024
}


## Arquivos desta pasta
| Arquivo | Descrição |
|---|---|
| `Aula_02.ipynb` | Notebook completo com todo o processo (conversão + extração de metadados) |
| `bioetica_e_ia.md` / `.json` | Conversão e metadados do artigo sobre bioética e IA |
| `escrita_academica_ia.md` / `.json` | Conversão e metadados do artigo sobre escrita acadêmica |
| `twitter_algoritmo.md` / `.json` | Conversão e metadados do artigo sobre algoritmo do Twitter |

## Como sair do Ambiente Virtual?

deactivate
