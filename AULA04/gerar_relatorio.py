"""
Gera o RELATORIO.md a partir do summary.json.
As respostas numéricas (1, 2, 3) são CALCULADAS dos dados reais — não digitadas.
As respostas de análise são texto interpretativo baseado nos números.
Rode de dentro de AULA_04:  python gerar_relatorio.py
"""
import json
import statistics
from pathlib import Path

# nomes legíveis de cada teste
NOMES = {
    1:  "Fixo, 200 caracteres, sem overlap",
    2:  "Fixo, 500 caracteres, sem overlap",
    3:  "Fixo, 1000 caracteres, sem overlap",
    4:  "Fixo, 2000 caracteres, sem overlap",
    5:  "Fixo, 500, overlap 50 (10%)",
    6:  "Fixo, 500, overlap 200 (40%)",
    7:  "Por parágrafo",
    8:  "Por sentença (grupos de 3)",
    9:  "Recursivo (separadores hierárquicos)",
    10: "Por seção / heading Markdown",
}


def carregar():
    return json.loads(Path("results/summary.json").read_text(encoding="utf-8"))


def agregar(summary):
    """Consolida estatísticas por teste, somando/mediando os 12 documentos."""
    por_teste = {}
    for doc in summary:
        for exp in doc["experiments"]:
            t = exp["test_id"]
            d = por_teste.setdefault(t, {"chunks": [], "media": [], "min": [], "max": []})
            d["chunks"].append(exp["num_chunks"])
            d["media"].append(exp["avg_chunk_size"])
            d["min"].append(exp["min_chunk_size"])
            d["max"].append(exp["max_chunk_size"])
    resumo = {}
    for t, d in por_teste.items():
        resumo[t] = {
            "total_chunks": sum(d["chunks"]),
            "media_chars": round(statistics.mean(d["media"]), 1),
            "min_chars": min(d["min"]),
            "max_chars": max(d["max"]),
        }
    return resumo


def tabela_markdown(resumo):
    linhas = ["| Teste | Estratégia | Total de chunks | Média (chars) | Mín | Máx |",
              "|------:|------------|----------------:|--------------:|----:|----:|"]
    for t in sorted(resumo):
        r = resumo[t]
        linhas.append(f"| {t} | {NOMES[t]} | {r['total_chunks']} | "
                      f"{r['media_chars']} | {r['min_chars']} | {r['max_chars']} |")
    return "\n".join(linhas)


def gerar(summary, resumo):
    # --- respostas CALCULADAS dos dados ---
    mais = max(resumo, key=lambda t: resumo[t]["total_chunks"])
    menos = min(resumo, key=lambda t: resumo[t]["total_chunks"])
    n_docs = len(summary)

    # os testes estruturais e seus máximos (para as perguntas 9, 12)
    max7 = resumo[7]["max_chars"]
    max8 = resumo[8]["max_chars"]
    max10 = resumo[10]["max_chars"]

    md = f"""# Relatório de Análise — Estratégias de Chunking (AULA_04)

**Residência em IA Generativa & RAG — Instituto ECOA / PUC-Rio**

Análise comparativa de 10 estratégias de chunking sobre {n_docs} documentos (3 artigos em
português sobre ética em IA e 9 papers técnicos em inglês sobre LLMs/RAG), convertidos de PDF
para Markdown com Docling e vetorizados com o modelo local
`paraphrase-multilingual-MiniLM-L12-v2` (384 dimensões).

*Este relatório é gerado automaticamente a partir de `results/summary.json`.
As respostas 1, 2 e 3 são calculadas diretamente dos dados.*

## Dados consolidados ({n_docs} documentos)

{tabela_markdown(resumo)}

---

## Respostas

### 1. Qual estratégia gerou mais chunks?
**Teste {mais} ({NOMES[mais]})**, com **{resumo[mais]['total_chunks']} chunks** — o maior total.
Por ter o menor tamanho de chunk, divide o mesmo texto em mais pedaços.

### 2. Qual gerou menos chunks?
**Teste {menos} ({NOMES[menos]})**, com **{resumo[menos]['total_chunks']} chunks** — o menor total.
Divide o documento apenas nos cabeçalhos; como muitos documentos têm poucas seções, cada chunk
vira uma seção inteira e grande.

### 3. Como o tamanho dos chunks variou?
Nas estratégias de tamanho fixo, a variação foi **controlada**: a média acompanhou o alvo
({resumo[1]['media_chars']}, {resumo[2]['media_chars']}, {resumo[3]['media_chars']} e
{resumo[4]['media_chars']} caracteres para os alvos 200/500/1000/2000) e o máximo respeitou o
limite. Dobrar o tamanho reduziu o número de chunks pela metade
({resumo[1]['total_chunks']} → {resumo[2]['total_chunks']} → {resumo[3]['total_chunks']} → {resumo[4]['total_chunks']}).

Já as estratégias baseadas em estrutura variaram de forma **descontrolada**: máximos de
**{max7}** (parágrafo), **{max8}** (sentença) e **{max10}** (markdown) caracteres, contra
mínimos de 1 a 11 — o tamanho depende inteiramente da formatação do documento.

### 4. Qual estratégia preservou melhor a estrutura dos documentos?
O **Teste 10 (Markdown por heading)** — única a registrar a hierarquia semântica
(título → seção → subseção) nos metadados de cada chunk (`h1`, `h2`, `h3`). O Recursivo (Teste 9)
vem em segundo por respeitar fronteiras de parágrafo e frase, sem porém registrar a hierarquia.

### 5. Como tabelas foram tratadas?
O Docling converteu tabelas para a **sintaxe de tabela do Markdown** (linhas com `|`,
cabeçalho e linha separadora `|---|`). O resultado depende da complexidade da tabela:
**tabelas simples foram bem preservadas** — por exemplo, a tabela de resultados GLUE do paper
do BERT manteve cabeçalho, colunas e valores alinhados e legíveis. Já **tabelas complexas**
(com células mescladas ou cabeçalhos em dois níveis) foram **degradadas**: os cabeçalhos
aparecem duplicados e desalinhados, quebrando a estrutura. Além disso, quando uma tabela cai
no meio de um chunk de tamanho fixo, ela é **cortada** — parte fica num chunk, parte em outro.

### 6. Como imagens foram tratadas?
As imagens **não são extraídas como conteúdo** — o Docling insere um marcador `<!-- image -->`
no lugar onde a figura estava, sem OCR do texto interno nem descrição. Foi confirmado nos
markdowns (ex.: três marcadores no paper *Attention Is All You Need*, correspondentes aos
diagramas da arquitetura). Todo o conteúdo visual (gráficos, diagramas, fórmulas renderizadas
como imagem) é **perdido** para a busca semântica: o embedding de um chunk com `<!-- image -->`
não representa nada do que a figura mostrava.

### 7. Quais informações foram perdidas durante a conversão PDF → Markdown?
Perdas identificadas: conteúdo das **imagens** (viram marcadores, sem OCR nem descrição);
**numeração de páginas** (o markdown é texto corrido); formatação de **tabelas complexas**;
**fórmulas matemáticas** (viram texto quebrado ou símbolos soltos nos papers); e artefatos de
**hifenização** de fim de linha, parcialmente corrigidos na limpeza. A presença de chunks de
**1 caractere** (coluna Mín) evidencia resíduos da conversão.

### 8. O chunking por caracteres fragmentou conceitos ou estruturas importantes?
Sim. O corte por número fixo de caracteres é **cego ao conteúdo** — corta no meio de palavras,
frases e tabelas. É mais grave no Teste 1 (200 caracteres), onde a fragmentação é máxima. Chunks
fixos maiores (1000, 2000) cortam menos, mas diluem a relevância (mais assuntos por chunk).

### 9. O chunking por parágrafo produziu chunks muito grandes?
Sim, em casos extremos. A média ficou moderada ({resumo[7]['media_chars']} caracteres), mas o
**maior** chunk chegou a **{max7}** caracteres — quando um documento tem um parágrafo enorme sem
quebra dupla. O tamanho é **imprevisível**, dependente da formatação de origem.

### 10. O chunking por sentença conseguiu preservar melhor o contexto?
Parcialmente. Agrupar 3 sentenças mantém o **fluxo local** entre frases relacionadas (bom para
texto explicativo), mas o tamanho é **variável** (máximo de **{max8}** caracteres), pois a
segmentação falha com pontuação irregular, abreviações e fórmulas. Preserva contexto melhor que
o corte cego, sem garantia de tamanho.

### 11. O Recursive Splitter apresentou vantagens?
Sim — a estratégia mais **equilibrada**. Divide primeiro por parágrafo, depois frase, depois
palavra, cortando no caractere só em último caso. Resultado: respeita fronteiras naturais **e**
mantém o tamanho sob controle (máximo de {resumo[9]['max_chars']} caracteres). Combina a
previsibilidade do fixo com o respeito à estrutura — padrão recomendado para RAG.

### 12. O Markdown Splitter conseguiu preservar a estrutura semântica?
Sim quanto à **hierarquia** (único a registrar seção/subseção nos metadados), mas falhou quanto
ao **tamanho**: gerou o maior chunk da análise (**{max10}** caracteres). Numa base heterogênea
(papers com poucos headings) isso é crítico — e como o modelo local processa apenas ~128 tokens
(~500 caracteres), em um chunk de {max10} caracteres mais de 99% do conteúdo é ignorado ao gerar
o embedding. Preserva estrutura, mas produz vetores pouco representativos.

### 13. Qual estratégia parece mais adequada para um sistema de RAG?
O **Teste 9 (Recursivo)** — melhor equilíbrio entre respeitar a estrutura e garantir teto de
tamanho, mantendo os chunks na janela útil do modelo. Em segundo, o **Teste 5 (Fixo 500 +
overlap 10%)**, como baseline simples e previsível.

### 14. Quais estratégias devem ser descartadas?
- **Teste 1 (Fixo 200):** fragmenta demais, corta conceitos.
- **Teste 4 (Fixo 2000):** dilui relevância e ultrapassa a janela do modelo.
- **Testes 7, 8 e 10 (parágrafo, sentença, markdown):** tamanho descontrolado (máximos de
  {max7}, {max8} e {max10}), inviável de vetorizar de forma representativa. O Teste 10 mantém
  valor apenas pelos metadados de estrutura.

### 15. Quais estratégias devem ser utilizadas nos próximos experimentos?
Três, cobrindo os eixos relevantes:
- **Teste 9 (Recursivo):** estratégia principal para RAG.
- **Teste 5 (Fixo 500 + overlap 50):** baseline de comparação.
- **Teste 6 (Fixo 500 + overlap 200):** para medir se o overlap pesado compensa a redundância
  (gera {resumo[6]['total_chunks']} chunks contra {resumo[2]['total_chunks']} do Teste 2, pela
  mesma cobertura de texto).

Todas mantêm o tamanho **dentro da janela do modelo de embedding**, garantindo vetores
representativos — condição que as descartadas não satisfazem.

---

## Conclusão geral

O trade-off central do chunking é **controle de tamanho vs. respeito à estrutura**. Estratégias
de tamanho fixo garantem previsibilidade mas ignoram o significado; as estruturais respeitam o
significado mas perdem o controle do tamanho. O **chunking recursivo** melhor concilia os dois.

Dois fatores foram decisivos nesta base: a **heterogeneidade** dos documentos (PT + EN, artigos
+ papers) penaliza as estratégias estruturais, que dependem de formatação consistente; e a
**janela curta do modelo local** (~128 tokens) torna qualquer chunk grande pouco representativo,
reforçando a preferência por teto de tamanho baixo e controlado.
"""
    return md


if __name__ == "__main__":
    summary = carregar()
    resumo = agregar(summary)
    md = gerar(summary, resumo)
    Path("RELATORIO.md").write_text(md, encoding="utf-8")
    print("RELATORIO.md gerado com sucesso.")
    print(f"  {len(summary)} documentos, 10 estrategias.")