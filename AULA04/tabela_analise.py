import json
import statistics
from pathlib import Path

# tabela de referência: descrição, vantagem, limitação e uso de cada teste
# (a análise qualitativa; os números vêm do summary.json)
DESCRICAO = {
    1:  ("Fixo, 200 caracteres, sem overlap", "Máxima fragmentação",
         "Trechos pequenos e específicos", "Corta palavras e perde contexto",
         "Busca por informações muito pontuais"),
    2:  ("Fixo, 500 caracteres, sem overlap", "Fragmentação moderada",
         "Equilíbrio entre tamanho e quantidade", "Ainda pode cortar unidades semânticas",
         "Baseline simples e previsível"),
    3:  ("Fixo, 1000 caracteres, sem overlap", "Mais contexto por chunk",
         "Preserva explicações mais longas", "Pode misturar assuntos diferentes",
         "Textos com argumentos extensos"),
    4:  ("Fixo, 2000 caracteres, sem overlap", "Pouca fragmentação",
         "Grande quantidade de contexto", "Dilui a relevância semântica",
         "Resumo e modelos com contexto amplo"),
    5:  ("Fixo, 500, overlap 50 (10%)", "Overlap leve",
         "Preserva fronteiras com pouca redundância", "Aumenta moderadamente o processamento",
         "Busca semântica com chunks fixos"),
    6:  ("Fixo, 500, overlap 200 (40%)", "Overlap pesado",
         "Reduz a perda nas fronteiras", "Grande redundância e maior custo",
         "Informações críticas atravessando fronteiras"),
    7:  ("Por parágrafo", "Preserva parágrafos",
         "Mantém unidades naturais do texto", "Tamanhos muito variáveis",
         "Documentos com parágrafos bem estruturados"),
    8:  ("Por sentença, agrupando 3", "Agrupa três sentenças",
         "Preserva o fluxo entre frases relacionadas", "Tamanho variável e segmentação sensível",
         "Textos narrativos ou explicativos"),
    9:  ("Recursivo, separadores hierárquicos", "Separação hierárquica",
         "Equilibra estrutura e limite de tamanho", "Pode criar chunks pequenos por artefatos",
         "Estratégia geral para RAG"),
    10: ("Por seção/heading Markdown", "Preserva seções semânticas",
         "Mantém títulos e conteúdos relacionados", "Seções podem ficar extensas demais",
         "Markdown e documentação estruturada"),
}


def carregar_summary(caminho="results/summary.json"):
    return json.loads(Path(caminho).read_text(encoding="utf-8"))


def agregar_por_teste(summary):
    """Junta as estatísticas de todos os documentos, por test_id."""
    # acumula por teste: soma de chunks, e todas as médias/min/max
    por_teste = {}
    for doc in summary:
        for exp in doc["experiments"]:
            tid = exp["test_id"]
            if tid not in por_teste:
                por_teste[tid] = {"num_chunks": [], "avg": [], "min": [], "max": []}
            por_teste[tid]["num_chunks"].append(exp["num_chunks"])
            por_teste[tid]["avg"].append(exp["avg_chunk_size"])
            por_teste[tid]["min"].append(exp["min_chunk_size"])
            por_teste[tid]["max"].append(exp["max_chunk_size"])
    return por_teste


def montar_tabela(por_teste):
    linhas = []
    for tid in sorted(por_teste):
        d = por_teste[tid]
        desc = DESCRICAO[tid]
        linhas.append({
            "teste": tid,
            "estrategia": desc[0],
            "total_chunks": sum(d["num_chunks"]),
            "media_chunks_por_doc": round(statistics.mean(d["num_chunks"]), 1),
            "media_caracteres": round(statistics.mean(d["avg"]), 2),
            "min_caracteres": min(d["min"]),
            "max_caracteres": max(d["max"]),
            "efeito": desc[1],
            "vantagem": desc[2],
            "limitacao": desc[3],
            "quando_usar": desc[4],
        })
    return linhas


def imprimir(linhas):
    print(f"\n{'Teste':<6}{'Estratégia':<38}{'Total':<8}{'Méd/doc':<9}{'Méd chars':<11}{'Min':<6}{'Max':<7}")
    print("-" * 85)
    for l in linhas:
        print(f"{l['teste']:<6}{l['estrategia']:<38}{l['total_chunks']:<8}"
              f"{l['media_chunks_por_doc']:<9}{l['media_caracteres']:<11}"
              f"{l['min_caracteres']:<6}{l['max_caracteres']:<7}")


if __name__ == "__main__":
    summary = carregar_summary()
    por_teste = agregar_por_teste(summary)
    linhas = montar_tabela(por_teste)

    print(f"Documentos analisados: {len(summary)}")
    imprimir(linhas)

    # salva a tabela em JSON para reuso
    saida = Path("results/tabela_analise.json")
    saida.write_text(json.dumps(linhas, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nTabela salva em {saida}")