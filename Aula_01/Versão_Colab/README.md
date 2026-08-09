<div align="center">

# 🧠 Residência em IA Generativa

### *Jornada de aprendizagem e aplicação prática em Inteligência Artificial Generativa*

[![Status](https://img.shields.io/badge/Status-Em%20andamento-green?style=flat-square)](https://github.com/seu-usuario/Residencia-IA-Generativa-Ana_Karina)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![OpenRouter](https://img.shields.io/badge/API-OpenRouter-purple?style=flat-square)](https://openrouter.ai/)
[![Colab](https://img.shields.io/badge/Ambiente-Google%20Colab-orange?style=flat-square&logo=googlecolab)](https://colab.research.google.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

</div>

---

## 📑 Índice

- [Visão Geral](#-visão-geral)
- [Objetivos](#-objetivos)
- [Arquitetura Técnica](#-arquitetura-técnica)
- [Estrutura do Repositório](#-estrutura-do-repositório)
- [Pré-requisitos](#-pré-requisitos)
- [Como Executar](#-como-executar)
- [Registro de Atividades](#-registro-de-atividades)
- [Competências Desenvolvidas](#-competências-desenvolvidas)
- [Referências](#-referências)
- [Licença](#-licença)

---

## 🔍 Visão Geral

Este repositório documenta minha trajetória na **Residência em IA Generativa**, contendo experimentos práticos, implementações de código e reflexões sobre o uso de modelos de linguagem (LLMs) em cenários reais.

O projeto segue uma abordagem **mão-na-massa**, combinando fundamentos teóricos com aplicações práticas utilizando APIs de modelos de inteligência artificial através do gateway [OpenRouter](https://openrouter.ai/).

---

## 🎯 Objetivos

### Objetivo Geral
Desenvolver competências técnicas e conceituais em IA Generativa, com foco em aplicações práticas e integradas.

### Objetivos Específicos
- ✅ Compreender a arquitetura e funcionamento de LLMs
- ✅ Implementar integrações com APIs de modelos de linguagem
- ✅ Explorar diferentes modelos e suas características
- ✅ Aplicar boas práticas de desenvolvimento e versionamento
- ✅ Documentar aprendizados e experimentos de forma estruturada

---

## 🏗️ Arquitetura Técnica

┌─────────────────┐ ┌──────────────────┐ ┌─────────────────┐ │ │ │ │ │ │ │ Google Colab │─────▶│ OpenRouter │─────▶│ LLM Models │ │ (Execução) │ │ (Gateway API) │ │ (Inferência) │ │ │ │ │ │ │ └─────────────────┘ └──────────────────┘ └─────────────────┘ │ ▼ ┌─────────────────┐ │ │ │ GitHub │ │ (Versionamento) │ │ │ └─────────────────┘




### Stack Tecnológica

| Componente | Tecnologia | Função |
|------------|------------|--------|
| **Linguagem** | Python 3.10+ | Desenvolvimento |
| **Ambiente** | Google Colab | Execução de notebooks |
| **API Gateway** | OpenRouter | Acesso unificado a LLMs |
| **SDK** | OpenAI Python | Cliente da API |
| **Modelo** | Nemotron 3 Ultra 550B | Inferência de linguagem |
| **Versionamento** | Git + GitHub | Controle de código |

---

## 📁 Estrutura do Repositório
Residencia-IA-Generativa-Ana_Karina/ │ ├── Aula01/ │ └── aula01_introducao_ia.ipynb # Primeiro contato com LLMs │ ├── Aula02/ # (Em desenvolvimento) │ ├── assets/ # Imagens e recursos │ ├── README.md # Este arquivo │ └── LICENSE # Licença do projeto




---

## ⚙️ Pré-requisitos

Antes de executar os notebooks, certifique-se de ter:

- [x] Conta no [GitHub](https://github.com/)
- [x] Conta no [Google](https://www.google.com/) (para Colab)
- [x] Conta no [OpenRouter](https://openrouter.ai/)
- [x] Chave de API do OpenRouter configurada

### Configuração da Chave API

1. Acesse [OpenRouter Keys](https://openrouter.ai/keys)
2. Crie uma nova chave de API
3. No Google Colab, vá em: **Ambiente de execução → Atualizar variáveis do ambiente**
4. Adicione: `OPENROUTER_API_KEY` = `sua-chave-aqui`

---

## 🚀 Como Executar

### Passo 1 — Clonar o repositório (opcional)

```bash
git clone https://github.com/seu-usuario/Residencia-IA-Generativa-Ana_Karina.git
cd Residencia-IA-Generativa-Ana_Karina
Passo 2 — Abrir no Google Colab
Acesse o notebook desejado (ex: Aula01/aula01_introducao_ia.ipynb)
Clique no botão "Open in Colab" no topo do arquivo
Ou acesse diretamente: Colab
Passo 3 — Configurar e executar
python


# Célula 1: Configuração
from openai import OpenAI
from google.colab import userdata

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=userdata.get('OPENROUTER_API_KEY')
)

# Célula 2: Chamada da API
response = client.chat.completions.create(
    model="nvidia/nemotron-3-ultra-550b-a55b:free",
    messages=[
        {"role": "user", "content": "write a haiku about ai"}
    ],
)

print(response.choices[0].message.content)
📝 Registro de Atividades
Aula 01 — Introdução aos LLMs via API ✅
Data: Agosto de 2026

Objetivo: Configurar ambiente e realizar primeira chamada a um modelo de linguagem.

Entregas:

✅ Configuração do Google Colab
✅ Criação de chave API no OpenRouter
✅ Integração com SDK OpenAI
✅ Primeira inferência com modelo gratuito
Resultado:

Silent code awakes,
Dreams in patterns, learns, creates,
Mind without a breath.

Modelo utilizado: nvidia/nemotron-3-ultra-550b-a55b:free

Aprendizados:

Funcionamento de APIs de LLMs
Gerenciamento seguro de secrets
Estrutura de requisições chat completions
Formatação de prompts
Aula 02 — [Em desenvolvimento] ⏳
Objetivo: A definir

Status: 🔜 Em breve

💡 Competências Desenvolvidas
Técnicas
Integração com APIs RESTful
Uso de SDKs Python
Manipulação de respostas JSON
Gerenciamento de variáveis de ambiente
Versionamento com Git/GitHub
Conceituais
Arquitetura de LLMs
Prompt engineering básico
Modelos de linguagem e suas aplicações
Boas práticas de segurança com APIs
Transversais
Documentação técnica
Organização de projetos
Resolução de problemas
Aprendizagem contínua
📚 Referências
Documentação Oficial
OpenRouter Documentation
OpenAI Python SDK
Google Colab Guide
GitHub Docs
Modelos Utilizados
NVIDIA Nemotron 3 Ultra
OpenRouter Free Models
📄 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE [blocked] para mais detalhes.

Desenvolvido com 💜 por Ana Karina
Ubá - MG | 2026

GitHub LinkedIn

