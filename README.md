# Residência em Tecnologias de IA Generativa - Aula 01

**Autor:** Ana Karina 

## Propósito

Este repositório foi criado para registrar meu aprendizado durante a Residência em Tecnologias de IA Generativa.

Aqui serão armazenados os códigos, exercícios, projetos e anotações desenvolvidos ao longo das aulas, servindo como registro da minha evolução na área de Inteligência Artificial.

---

## Introdução à IA - Aula 01

Este projeto contém o código inicial para interagir com a API da OpenAI utilizando Python.

Para garantir a eficiência de recursos e o isolamento das dependências, recomendamos fortemente o uso de um Ambiente Virtual Python (Virtual Environment ou venv).

## 🚀 Passo a Passo para Configuração e Execução

### 1. Criar o Ambiente Virtual (venv)

No Linux/macOS

```bash
python3 -m venv venv
```

No Windows

```bash
python -m venv venv
```

### 2. Ativar o Ambiente Virtual

No Linux/macOS

```bash
source venv/bin/activate
```

No Windows

```bash
venv\Scripts\activate
```

### 3. Instalar as Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar as Variáveis de Ambiente

Crie um arquivo `.env` contendo:

```text
OPENAI_API_KEY=sua_chave_de_api_aqui
OPENAI_MODEL=gpt-4o-mini
```

### 5. Executar o projeto

```bash
cd AULA_01
python hello_llm.py
```

### Encerrar o ambiente virtual

```bash
deactivate
```