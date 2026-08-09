📋 README Profissional (Versão Compacta)
markdown


<div align="center">

# 🧠 Residência em IA Generativa

### Experimentos práticos com modelos de linguagem

[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)](https://www.python.org/)
[![OpenRouter](https://img.shields.io/badge/API-OpenRouter-purple?style=flat-square)](https://openrouter.ai/)
[![Status](https://img.shields.io/badge/Status-Em%20andamento-green?style=flat-square)]()

</div>

---

## 📖 Sobre

Repositório dedicado aos experimentos práticos da **Residência em IA Generativa**, documentando aprendizados e implementações com modelos de linguagem (LLMs) através da API do OpenRouter.

---

## 📁 Estrutura
├── Aula01/ │ └── aula01_introducao_ia.ipynb # Primeiro contato com LLMs ├── Aula02/ # (Em breve) └── README.md




---

## 🚀 Como executar

### 1. Configurar ambiente

- Crie uma conta no [OpenRouter](https://openrouter.ai/)
- Gere sua chave de API em [openrouter.ai/keys](https://openrouter.ai/keys)
- No Google Colab, adicione a secret: `OPENROUTER_API_KEY`

### 2. Executar notebook

```python
from openai import OpenAI
from google.colab import userdata

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=userdata.get('OPENROUTER_API_KEY')
)

response = client.chat.completions.create(
    model="nvidia/nemotron-3-ultra-550b-a55b:free",
    messages=[{"role": "user", "content": "write a haiku about ai"}]
)

print(response.choices[0].message.content)

## 📝 Atividades

01	Introdução aos LLMs via API	✅ Concluído
02	Em desenvolvimento	⏳ Próxima


## 🛠️ Stack

Python — Linguagem principal
Google Colab — Ambiente de execução
OpenRouter — Gateway para LLMs
OpenAI SDK — Cliente da API
Ana Karina | Rj  | 2026
