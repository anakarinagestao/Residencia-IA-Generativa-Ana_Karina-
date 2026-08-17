import json
import numpy as np
from pathlib import Path
from embed_local import gerar_embedding

RESULTS = Path("results")


def cosseno(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def carregar_chunks(test_id):
    """Lê todos os chunks+embeddings de um teste, de TODOS os documentos, do cache."""
    registros = []
    for pasta_doc in RESULTS.iterdir():
        if not pasta_doc.is_dir():
            continue
        arquivo = pasta_doc / f"test_{test_id:02d}" / "chunks_embeddings.json"
        if arquivo.exists():
            registros.extend(json.loads(arquivo.read_text(encoding="utf-8")))
    return registros


def buscar(pergunta, test_id, top=3):
    registros = carregar_chunks(test_id)
    if not registros:
        print(f"Nenhum chunk encontrado para o teste {test_id}.")
        return

    # embedda SÓ a pergunta (os trechos já vêm prontos do cache)
    v_pergunta = gerar_embedding([pergunta])[0]

    resultados = []
    for r in registros:
        score = cosseno(v_pergunta, r["embedding"])
        resultados.append((score, r))
    resultados.sort(key=lambda x: x[0], reverse=True)

    print(f"\nPERGUNTA: {pergunta}")
    print(f"ESTRATÉGIA: teste {test_id}  |  {len(registros)} chunks no cache\n")
    for i, (score, r) in enumerate(resultados[:top], start=1):
        preview = " ".join(r["text"].split())[:220]
        print(f"[{i}] score={score:.4f}  |  {r['document_name']}")
        print(f"    {preview}\n")


if __name__ == "__main__":
    pergunta = "O que é 'Autonomia e opacidade algorítmica'?"
    for tid in [1, 9, 10]:   # fixo pequeno vs recursivo vs markdown
        buscar(pergunta, test_id=tid)