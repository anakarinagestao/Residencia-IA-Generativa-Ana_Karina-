# 🧠 Aula 3 — Embeddings e Busca Semântica

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://www.python.org/)
[![Sentence Transformers](https://img.shields.io/badge/Sentence--Transformers-2.x-green)](https://www.sbert.net/)
[![Status](https://img.shields.io/badge/Status-Concluído-brightgreen)]()

> Projeto desenvolvido durante a **Residência em IA Generativa da PUC Rio (Turma 2026)** — implementação de distância euclidiana, distância de cosseno e busca semântica em documentos.

---

## 🎯 Objetivos

- Entender o conceito de **embeddings** como representações vetoriais de texto
- Implementar funções de **distância euclidiana** e **distância de cosseno** do zero
- Construir um sistema de **busca semântica** que encontra trechos relevantes pelo significado (não por palavras-chave)
- Comparar diferentes estratégias de divisão de texto (linhas vs. parágrafos)

---

## 📄 Dados utilizados

Documentos `.md` gerados na Aula 2 (artigos acadêmicos sobre bioética, IA e Twitter/X).

---

## 🛠️ Tecnologias

| Tecnologia | Função |
|------------|--------|
| **Python 3.10+** | Linguagem principal |
| **Sentence Transformers** | Geração de embeddings (modelo all-MiniLM-L6-v2) |
| **NumPy** | Operações vetoriais |

---

## 🧠 Principais aprendizados

1. **Embeddings** transformam palavras/textos em vetores onde significados parecidos = vetores próximos
2. **Distância de Cosseno** é mais usada que Euclidiana para comparar embeddings (captura melhor a semântica)
3. **Busca Semântica** substitui busca por palavra-chave com muito mais precisão
4. **Tamanho do trecho** afeta a qualidade: linhas são precisas, parágrafos são contextuais

---

## 👩‍💻 Autora

**Ana Karina** — PUC Rio 2026
