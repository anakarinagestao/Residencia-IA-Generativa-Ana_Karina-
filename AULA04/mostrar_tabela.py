import json
import statistics

with open("results/summary.json", encoding="utf-8") as f:
    summary = json.load(f)

# agrega por teste
por_teste = {}
for doc in summary:
    for exp in doc["experiments"]:
        tid = exp["test_id"]
        if tid not in por_teste:
            por_teste[tid] = {"chunks": [], "media": [], "min": [], "max": []}
        por_teste[tid]["chunks"].append(exp["num_chunks"])
        por_teste[tid]["media"].append(exp["avg_chunk_size"])
        por_teste[tid]["min"].append(exp["min_chunk_size"])
        por_teste[tid]["max"].append(exp["max_chunk_size"])

print(f"Documentos analisados: {len(summary)}\n")
print(f"{'Teste':<7}{'Total chunks':<14}{'Media chars':<13}{'Min':<7}{'Max':<7}")
print("-" * 48)

for tid in sorted(por_teste):
    d = por_teste[tid]
    total = sum(d["chunks"])
    media = round(statistics.mean(d["media"]), 1)
    minimo = min(d["min"])
    maximo = max(d["max"])
    print(f"{tid:<7}{total:<14}{media:<13}{minimo:<7}{maximo:<7}")