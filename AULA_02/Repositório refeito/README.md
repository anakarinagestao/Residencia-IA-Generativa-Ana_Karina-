# 📚 Aula 2 — Conversão Inteligente de PDFs com Docling

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://www.python.org/)
[![Docling](https://img.shields.io/badge/Docling-2.x-green)](https://github.com/DS4SD/docling)
[![Status](https://img.shields.io/badge/Status-Concluído-brightgreen)]()
[![Google Colab](https://img.shields.io/badge/Google_Colab-Notebook-orange?logo=googlecolab)](https://colab.research.google.com/)

> Projeto desenvolvido durante a **Residência em IA Generativa** — pipeline completo de conversão de artigos acadêmicos em formatos estruturados com extração automatizada de metadados.

---

## 🎯 Objetivos

- Converter artigos científicos em **PDF** para **Markdown** (leitura humana) e **JSON** (processamento computacional)
- Extrair metadados automaticamente: **título, autores e ano de publicação**
- Criar um pipeline reprodutível e documentado, pronto para uso em pesquisas futuras

---

## 📄 Artigos processados

| # | Artigo | Título | Autores | Ano |
|---|--------|--------|---------|:---:|
| 1 | `bioetica_e_ia` | Entre o algoritmo e o Juramento de Hipócrates: bioética na era da inteligência artificial | Juracy Barbosa dos Santos, Guilhermina Rego, Rui Nunes | 2026 |
| 2 | `escrita_academica_ia` | Escrita acadêmica ética, responsável e humana com inteligência artificial | Rafael Cardoso Sampaio | 2025 |
| 3 | `twitter_algoritmo` | O caso Twitter/X: algoritmo, espaço público e ultraliberalismo digital | Ettore S. Batalha, Jefferson R. da Silva, Bruno D. V. E. Velásquez | 2025 |

---


---

## 🛠️ Tecnologias

| Tecnologia | Função |
|------------|--------|
| **Python 3.10+** | Linguagem principal |
| **Docling** | Biblioteca IBM para parsing e conversão de documentos |
| **Google Colab** | Ambiente de execução em nuvem |
| **JSON** | Formato estruturado de saída para processamento |
| **Markdown** | Formato de saída para leitura humana |
| **Regex** | Extração de padrões textuais (ano, metadados) |

---

## 🚀 Como executar

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/Residencia-IA-Generativa-Ana_Karina.git
cd Residencia-IA-Generativa-Ana_Karina/aula_2

2. Instale as dependências

pip install -r requirements.txt

3. Execute o notebook
Abra o arquivo notebook/aula_2_conversao_docling.ipynb no Google Colab ou Jupyter e execute todas as células.

Conversão PDF → Markdown
Arquivos .md preservam a estrutura do documento (títulos, parágrafos, tabelas), ideais para leitura e análise humana.

Conversão PDF → JSON
Arquivos .json com etiquetas estruturais (section_header, text, page_header, footnote), permitindo processamento computacional e extração de dados.

Extração de metadados
Cada artigo gera um arquivo _metadados.json com:

json


{
  "arquivo_original": "bioetica_e_ia (3).pdf",
  "titulo": "Entre o algoritmo e o Juramento de Hipócrates...",
  "autores": ["Juracy Barbosa dos Santos", "Guilhermina Rego", "Rui Nunes"],
  "ano_edicao": 2026
}

🧠 Principais aprendizados
Estrutura de PDFs: Documentos acadêmicos raramente possuem metadados embutidos — é preciso extraí-los da estrutura textual
Docling: A biblioteca organiza o conteúdo com etiquetas semânticas, facilitando a navegação programática
Estratégia de extração: Usar a estrutura do JSON (label) é mais confiável que expressões regulares no texto bruto
Pipeline reprodutível: Separar dados brutos, processados e metadados garante rastreabilidade
👩‍💻 Autora
Ana Karina
Residência em IA Generativa — 2026

📅 Agosto de 2026





