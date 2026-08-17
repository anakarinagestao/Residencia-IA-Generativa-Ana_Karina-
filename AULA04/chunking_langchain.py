import os
import re
import glob
import requests
import numpy as np
from dotenv import load_dotenv
from langchain_text_splitters import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
    MarkdownHeaderTextSplitter,
)

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")


def gerar_embedding(textos, model="openai/text-embedding-3-small", lote=100):
    vetores = []
    for i in range(0, len(textos), lote):
        pedaco = textos[i:i + lote]
        resposta = requests.post(
            "https://openrouter.ai/api/v1/embeddings",
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
            json={"model": model, "input": pedaco},
        )
        resposta.raise_for_status()
        vetores.extend(item["embedding"] for item in resposta.json()["data"])
    return vetores


def cosseno(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

LIMITE_SEGURO = 8000  # ~limite de caracteres que a API de embedding aceita por trecho


def maior_trecho(trechos):
    """Retorna o tamanho (em caracteres) do maior trecho da lista."""
    return max(len(t) for t in trechos)


def limpar_texto(texto):
    """Junta palavras quebradas por hífen de fim de linha (herança do PDF)."""
    return re.sub(r"(\w+)\s+-\s*(\w+)", r"\1\2", texto)


def carregar_texto(pasta="../documentos/markdown"): 
    caminhos = glob.glob(os.path.join(pasta, "*.md"))
    if not caminhos:
        raise FileNotFoundError(f"Nenhum .md em {pasta}. Rode de dentro de AULA_04.")
    partes = []
    for caminho in caminhos:
        with open(caminho, encoding="utf-8") as f:
            partes.append(f.read())
    return "\n\n".join(partes)


def fixo(size, overlap=0):
    """CharacterTextSplitter: corte por tamanho, sem respeitar estrutura."""
    splitter = CharacterTextSplitter(
        separator="", chunk_size=size, chunk_overlap=overlap
    )
    return lambda texto: splitter.split_text(texto)


def recursivo(size, overlap=0):
    """RecursiveCharacterTextSplitter: tenta parágrafo→frase→palavra antes de cortar."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=size, chunk_overlap=overlap
    )
    return lambda texto: splitter.split_text(texto)


def por_secao(texto):
    """MarkdownHeaderTextSplitter: corta nos cabeçalhos do markdown."""
    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[("#", "h1"), ("##", "h2"), ("###", "h3")]
    )
    docs = splitter.split_text(texto)
    return [d.page_content for d in docs]


ESTRATEGIAS = [
    ("1  Fixo 200, sem overlap",        fixo(200)),
    ("2  Fixo 500, sem overlap",        fixo(500)),
    ("3  Fixo 1000, sem overlap",       fixo(1000)),
    ("4  Fixo 2000, sem overlap",       fixo(2000)),
    ("5  Fixo 500, overlap 50 (10%)",   fixo(500, 50)),
    ("6  Fixo 500, overlap 200 (40%)",  fixo(500, 200)),
    ("7  Recursivo 500, overlap 50",    recursivo(500, 50)),
    ("8  Recursivo 1000, overlap 100",  recursivo(1000, 100)),
    ("9  Recursivo 500, overlap 100",   recursivo(500, 100)),
    ("10 Por secao (Markdown headers)", por_secao),
]


query = "O que é 'Autonomia e opacidade algorítmica'?"
texto = limpar_texto(carregar_texto())

print(f"QUERY: {query}\n")

for nome, estrategia in ESTRATEGIAS:
    trechos = estrategia(texto)

    if not trechos:
        print("=" * 78)
        print(f"{nome}  —  (nenhum trecho gerado)")
        print("=" * 78, "\n")
        continue

    # checa se algum trecho passa do limite da API antes de tentar embeddar
    maior = maior_trecho(trechos)
    if maior > LIMITE_SEGURO:
        print("=" * 78)
        print(f"{nome}  —  {len(trechos)} trechos")
        print("=" * 78)
        print(f"  [ESTRATÉGIA INADEQUADA PARA ESTA BASE]")
        print(f"  O maior trecho tem {maior} caracteres, acima do limite de {LIMITE_SEGURO}")
        print(f"  aceito pela API de embedding. O chunking por seção não controla o")
        print(f"  tamanho do trecho: documentos longos sem subtítulos (ex.: papers")
        print(f"  técnicos) viram um único chunk gigante. Em uma base heterogênea,")
        print(f"  prefira tamanho fixo ou recursivo, que garantem um teto de tamanho.\n")
        continue

    vetores = gerar_embedding([query] + trechos)
    v_query, v_trechos = vetores[0], vetores[1:]
    scores = sorted(
        ((cosseno(v_query, v), t) for v, t in zip(v_trechos, trechos)),
        key=lambda x: x[0], reverse=True,
    )[:3]

    print("=" * 78)
    print(f"{nome}  —  {len(trechos)} trechos")
    print("=" * 78)
    for score, trecho in scores:
        preview = " ".join(trecho.split())[:180]
        print(f"  score={score:.4f}  {preview}")
    print()