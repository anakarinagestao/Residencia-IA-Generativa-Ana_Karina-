import re
from langchain_text_splitters import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
    MarkdownHeaderTextSplitter,
)


import nltk
try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab")
from nltk.tokenize import sent_tokenize




def fixo(size, overlap=0):
    """Testes 1-6: CharacterTextSplitter, corte por tamanho fixo."""
    splitter = CharacterTextSplitter(separator="", chunk_size=size, chunk_overlap=overlap)
    return lambda texto: splitter.split_text(texto)


def por_paragrafo(texto):
    """Teste 7: cada parágrafo (bloco separado por linha em branco) vira um chunk."""
    blocos = re.split(r"\n\s*\n", texto)
    return [b.strip() for b in blocos if b.strip()]


def por_sentenca_agrupada(texto, n=3):
    """Teste 8: quebra em sentenças e agrupa de n em n (padrão 3)."""
    sentencas = [s.strip() for s in sent_tokenize(texto, language="portuguese") if s.strip()]
    chunks = []
    for i in range(0, len(sentencas), n):
        grupo = sentencas[i:i + n]
        chunks.append(" ".join(grupo))
    return chunks


def recursivo(size=1000, overlap=100):
    """Teste 9: RecursiveCharacterTextSplitter com separadores hierárquicos explícitos."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", " ", ""],   
    )
    return lambda texto: splitter.split_text(texto)


def por_markdown(texto):
    """Teste 10: MarkdownHeaderTextSplitter, corta por cabeçalhos."""
    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[("#", "h1"), ("##", "h2"), ("###", "h3")]
    )
    docs = splitter.split_text(texto)
    return [d.page_content for d in docs]



ESTRATEGIAS = [
    (1,  "fixed",              fixo(200),                  {"chunk_size": 200,  "chunk_overlap": 0}),
    (2,  "fixed",              fixo(500),                  {"chunk_size": 500,  "chunk_overlap": 0}),
    (3,  "fixed",              fixo(1000),                 {"chunk_size": 1000, "chunk_overlap": 0}),
    (4,  "fixed",              fixo(2000),                 {"chunk_size": 2000, "chunk_overlap": 0}),
    (5,  "fixed_with_overlap", fixo(500, 50),              {"chunk_size": 500,  "chunk_overlap": 50}),
    (6,  "fixed_with_overlap", fixo(500, 200),             {"chunk_size": 500,  "chunk_overlap": 200}),
    (7,  "by_paragraph",       por_paragrafo,              {}),
    (8,  "by_sentence_group3", por_sentenca_agrupada,      {"sentences_per_chunk": 3}),
    (9,  "recursive",          recursivo(1000, 100),       {"chunk_size": 1000, "chunk_overlap": 100}),
    (10, "markdown",           por_markdown,               {}),
]



if __name__ == "__main__":
    texto_teste = """# Introdução

A inteligência artificial transforma a medicina. Os sistemas aprendem com dados. Médicos usam essas ferramentas no dia a dia.

## Autonomia

O paciente tem direito de decidir. A opacidade algorítmica ameaça esse direito. Sistemas devem ser auditáveis.

## Conclusão

A ética precisa acompanhar a tecnologia. Transparência é essencial."""

    for tid, nome, estrategia, config in ESTRATEGIAS:
        chunks = estrategia(texto_teste)
        print(f"\n[Teste {tid}] {nome} {config}")
        print(f"  {len(chunks)} chunks gerados")
        if chunks:
            amostra = " ".join(chunks[0].split())[:90]
            print(f"  1º chunk: {amostra}")
