import re
import json
import statistics
from pathlib import Path

from embed_local import gerar_embedding, EMBEDDING_MODEL
from estrategias import ESTRATEGIAS
from langchain_text_splitters import MarkdownHeaderTextSplitter


def limpar_texto(texto):
    """Junta palavras quebradas por hífen de fim de linha (herança do PDF)."""
    return re.sub(r"(\w+)\s+-\s*(\w+)", r"\1\2", texto)


def chunks_com_metadata(test_id, estrategia_fn, texto):
    """Retorna lista de (texto_do_chunk, metadata).
    Só o teste 10 carrega metadata de heading; os demais vêm vazios."""
    if test_id == 10:
        splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[("#", "h1"), ("##", "h2"), ("###", "h3")]
        )
        docs = splitter.split_text(texto)
        return [(d.page_content, dict(d.metadata)) for d in docs]
    chunks = estrategia_fn(texto)
    return [(c, {}) for c in chunks]


def processar_documento(caminho_md, doc_id, pasta_resultados):
    nome = Path(caminho_md).stem
    texto = limpar_texto(Path(caminho_md).read_text(encoding="utf-8"))
    experimentos = []

    for test_id, strategy, estrategia_fn, config in ESTRATEGIAS:
        pares = chunks_com_metadata(test_id, estrategia_fn, texto)
        textos = [t for t, _ in pares]

        if not textos:
            print(f"  [teste {test_id:02d}] {strategy}: nenhum chunk — pulado")
            continue

        pasta_teste = pasta_resultados / nome / f"test_{test_id:02d}"
        arquivo = pasta_teste / "chunks_embeddings.json"

        if arquivo.exists():
            registros_existentes = json.loads(arquivo.read_text(encoding="utf-8"))
            tamanhos = [len(r["text"]) for r in registros_existentes]
            experimentos.append({
                "test_id": test_id, "strategy": strategy,
                "chunk_size": config.get("chunk_size"),
                "chunk_overlap": config.get("chunk_overlap"),
                "num_chunks": len(registros_existentes),
                "avg_chunk_size": round(statistics.mean(tamanhos), 2),
                "min_chunk_size": min(tamanhos), "max_chunk_size": max(tamanhos),
                "embedding_dimension": len(registros_existentes[0]["embedding"]),
            })
            print(f"  [teste {test_id:02d}] {strategy}: {len(registros_existentes)} chunks — CACHE")
            continue

        vetores = gerar_embedding(textos)

        registros = []
        for i, ((txt, meta), vec) in enumerate(zip(pares, vetores), start=1):
            registros.append({
                "chunk_id": f"{doc_id}_test{test_id:02d}_chunk{i:03d}",
                "document_id": doc_id,
                "document_name": nome + ".pdf",
                "test_id": test_id,
                "strategy": strategy,
                "chunk_size": config.get("chunk_size"),
                "chunk_overlap": config.get("chunk_overlap"),
                "text": txt,
                "embedding": [round(float(x), 6) for x in vec],
                "metadata": meta,
            })

        pasta_teste.mkdir(parents=True, exist_ok=True)
        arquivo.write_text(
            json.dumps(registros, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        tamanhos = [len(t) for t in textos]
        experimentos.append({
            "test_id": test_id, "strategy": strategy,
            "chunk_size": config.get("chunk_size"),
            "chunk_overlap": config.get("chunk_overlap"),
            "num_chunks": len(textos),
            "avg_chunk_size": round(statistics.mean(tamanhos), 2),
            "min_chunk_size": min(tamanhos), "max_chunk_size": max(tamanhos),
            "embedding_dimension": len(vetores[0]),
        })
        print(f"  [teste {test_id:02d}] {strategy}: {len(textos)} chunks, "
              f"média {round(statistics.mean(tamanhos), 2)} chars")

    return {"document": nome + ".pdf", "document_id": doc_id, "experiments": experimentos}


if __name__ == "__main__":
    PASTA_MD = Path("../documentos/markdown")
    PASTA_RESULTS = Path("results")

    print(f"Modelo de embedding: {EMBEDDING_MODEL}\n")

    # todos os 12 documentos, numerados
    docs = sorted(PASTA_MD.glob("*.md"))
    documentos = [(d.name, f"doc{i:02d}") for i, d in enumerate(docs, start=1)]

    todos_resumos = []
    for nome_arquivo, doc_id in documentos:
        doc = PASTA_MD / nome_arquivo
        print(f"Processando: {doc.name}  ({doc_id})")
        resumo = processar_documento(doc, doc_id, PASTA_RESULTS)
        todos_resumos.append(resumo)
        print()

    summary_path = PASTA_RESULTS / "summary.json"
    summary_path.write_text(
        json.dumps(todos_resumos, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Concluído. {len(todos_resumos)} documentos processados.")