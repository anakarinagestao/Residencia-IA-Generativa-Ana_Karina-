"""
Adiciona contagem de tokens e overlap real às estatísticas, lendo o CACHE.
Não recalcula embeddings — só lê os textos já salvos e conta tokens.
Rode de dentro de AULA_04:  python adicionar_tokens.py
"""
import json
import statistics
from pathlib import Path
import tiktoken

RESULTS = Path("results")
enc = tiktoken.get_encoding("cl100k_base")


def contar_tokens(texto):
    return len(enc.encode(texto))


def overlap_real(textos):
    """Estima o % médio de sobreposição entre chunks vizinhos.
    Mede quantos caracteres do fim de um chunk aparecem no começo do próximo."""
    if len(textos) < 2:
        return 0.0
    sobreposicoes = []
    for i in range(len(textos) - 1):
        a, b = textos[i], textos[i + 1]
        # procura o maior sufixo de 'a' que é prefixo de 'b'
        maior = 0
        limite = min(len(a), len(b))
        for tam in range(limite, 0, -1):
            if a[-tam:] == b[:tam]:
                maior = tam
                break
        pct = (maior / len(a) * 100) if a else 0
        sobreposicoes.append(pct)
    return round(statistics.mean(sobreposicoes), 2)


def processar():
    summary_atualizado = []

    for pasta_doc in sorted(RESULTS.iterdir()):
        if not pasta_doc.is_dir():
            continue

        experimentos = []
        for pasta_teste in sorted(pasta_doc.glob("test_*")):
            arquivo = pasta_teste / "chunks_embeddings.json"
            if not arquivo.exists():
                continue

            registros = json.loads(arquivo.read_text(encoding="utf-8"))
            textos = [r["text"] for r in registros]

            # conta tokens de cada chunk e adiciona ao registro
            tokens_por_chunk = []
            for r in registros:
                t = contar_tokens(r["text"])
                r["tokens"] = t
                tokens_por_chunk.append(t)

            # regrava o JSON com o campo tokens incluído
            arquivo.write_text(
                json.dumps(registros, ensure_ascii=False, indent=2), encoding="utf-8"
            )

            tamanhos = [len(t) for t in textos]
            experimentos.append({
                "test_id": registros[0]["test_id"],
                "strategy": registros[0]["strategy"],
                "chunk_size": registros[0].get("chunk_size"),
                "chunk_overlap": registros[0].get("chunk_overlap"),
                "num_chunks": len(textos),
                "avg_chunk_size": round(statistics.mean(tamanhos), 2),
                "min_chunk_size": min(tamanhos),
                "max_chunk_size": max(tamanhos),
                "avg_tokens": round(statistics.mean(tokens_por_chunk), 2),
                "min_tokens": min(tokens_por_chunk),
                "max_tokens": max(tokens_por_chunk),
                "overlap_real_pct": overlap_real(textos),
                "embedding_dimension": len(registros[0]["embedding"]),
            })
            print(f"  {pasta_doc.name} / test_{experimentos[-1]['test_id']:02d}: "
                  f"média {experimentos[-1]['avg_tokens']} tokens, "
                  f"overlap real {experimentos[-1]['overlap_real_pct']}%")

        summary_atualizado.append({
            "document": pasta_doc.name + ".pdf",
            "document_id": f"doc{len(summary_atualizado)+1:02d}",
            "experiments": experimentos,
        })

    (RESULTS / "summary.json").write_text(
        json.dumps(summary_atualizado, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\nConcluído. {len(summary_atualizado)} documentos atualizados com tokens e overlap real.")


if __name__ == "__main__":
    processar()