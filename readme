# Relatório de Análise — Estratégias de Chunking (AULA_04)

**Residência em IA Generativa & RAG — Instituto ECOA / PUC-Rio**
**Autor: Marco Aurélio de Brito**

Neste relatório comparo 10 estratégias de chunking aplicadas a uma base de 12 documentos
(3 artigos em português sobre ética em IA e 9 papers técnicos em inglês sobre LLMs/RAG),
convertidos de PDF para Markdown com Docling e vetorizados com o modelo local
`paraphrase-multilingual-MiniLM-L12-v2` (384 dimensões).

A tabela de dados consolidados abaixo é calculada diretamente de `results/summary.json`
(estatísticas reprodutíveis). A análise das perguntas que segue é a minha interpretação
desses resultados a partir da execução dos experimentos.

## Dados consolidados (12 documentos)

| Teste | Estratégia | Total de chunks | Média (chars) | Mín | Máx |
|------:|------------|----------------:|--------------:|----:|----:|
| 1 | Fixo, 200 caracteres, sem overlap | 7269 | 194.0 | 1 | 200 |
| 2 | Fixo, 500 caracteres, sem overlap | 2971 | 486.9 | 1 | 500 |
| 3 | Fixo, 1000 caracteres, sem overlap | 1491 | 982.0 | 29 | 1000 |
| 4 | Fixo, 2000 caracteres, sem overlap | 748 | 1963.6 | 198 | 2000 |
| 5 | Fixo, 500, overlap 50 (10%) | 3294 | 488.1 | 1 | 500 |
| 6 | Fixo, 500, overlap 200 (40%) | 4938 | 488.5 | 1 | 500 |
| 7 | Por parágrafo | 3996 | 383.9 | 1 | 40445 |
| 8 | Por sentença (grupos de 3) | 3718 | 383.8 | 5 | 24787 |
| 9 | Recursivo (separadores hierárquicos) | 2041 | 735.2 | 1 | 999 |
| 10 | Por seção / heading Markdown | 659 | 2416.9 | 11 | 52313 |

---

## Análise

### 1. Qual estratégia gerou mais chunks?
O **Teste 1 (Fixo, 200 caracteres, sem overlap)**, com **7269 chunks**. Como tem o menor
tamanho de chunk, ele divide o mesmo texto em muito mais pedaços — é o resultado esperado para
o menor alvo de tamanho da base.

### 2. Qual gerou menos chunks?
O **Teste 10 (Por seção / heading Markdown)**, com **659 chunks**. Ele corta o documento apenas
nos cabeçalhos; como boa parte dos documentos tem poucas seções, cada chunk acaba virando uma
seção inteira — poucos pedaços, porém enormes.

### 3. Como o tamanho dos chunks variou?
Nas estratégias de tamanho fixo a variação foi **controlada**: a média acompanhou o alvo
(194.0, 486.9, 982.0 e 1963.6 caracteres para os alvos 200/500/1000/2000) e o máximo respeitou o
limite. Observei que dobrar o tamanho reduz o número de chunks quase pela metade
(7269 → 2971 → 1491 → 748).

Já as estratégias baseadas em estrutura variaram de forma **descontrolada**: máximos de
**40445** (parágrafo), **24787** (sentença) e **52313** (markdown) caracteres, contra mínimos de
1 a 11. Aqui o tamanho depende inteiramente da formatação de cada documento, não de um parâmetro
que eu controle.

### 4. Qual estratégia preservou melhor a estrutura dos documentos?
O **Teste 10 (Markdown por heading)** foi o único a registrar a hierarquia semântica
(título → seção → subseção) nos metadados de cada chunk (`h1`, `h2`, `h3`). Em segundo lugar
coloco o **Recursivo (Teste 9)**, que respeita fronteiras de parágrafo e frase, ainda que sem
registrar a hierarquia explicitamente.

### 5. Como tabelas foram tratadas?
O Docling converteu as tabelas para a **sintaxe de tabela do Markdown** (linhas com `|`,
cabeçalho e linha separadora `|---|`). Na prática o resultado dependeu da complexidade:
**tabelas simples ficaram bem preservadas** — a tabela de resultados GLUE do paper do BERT, por
exemplo, manteve cabeçalho, colunas e valores alinhados e legíveis. Já **tabelas complexas**
(células mescladas ou cabeçalhos em dois níveis) foram **degradadas**: cabeçalhos duplicados e
desalinhados. E há um problema adicional de chunking: quando uma tabela cai no meio de um chunk
de tamanho fixo, ela é **cortada** — parte fica num chunk, parte no seguinte.

### 6. Como imagens foram tratadas?
As imagens **não são extraídas como conteúdo**. O Docling insere um marcador `<!-- image -->` no
lugar da figura, sem OCR do texto interno nem descrição. Confirmei isso nos markdowns (ex.: três
marcadores no *Attention Is All You Need*, correspondentes aos diagramas da arquitetura). Todo o
conteúdo visual (gráficos, diagramas, fórmulas renderizadas como imagem) se perde para a busca
semântica — o embedding de um chunk que contém só `<!-- image -->` não representa nada do que a
figura mostrava.

### 7. Quais informações foram perdidas durante a conversão PDF → Markdown?
Identifiquei estas perdas: conteúdo das **imagens** (viram marcadores, sem OCR nem descrição);
**numeração de páginas** (o markdown vira texto corrido); formatação de **tabelas complexas**;
**fórmulas matemáticas** (viram texto quebrado ou símbolos soltos nos papers); e artefatos de
**hifenização** de fim de linha, que corrigi parcialmente na limpeza. A presença de chunks de
**1 caractere** (coluna Mín) é um sintoma desses resíduos de conversão.

### 8. O chunking por caracteres fragmentou conceitos ou estruturas importantes?
Sim. O corte por número fixo de caracteres é **cego ao conteúdo** — corta no meio de palavras,
frases e tabelas. O efeito é mais grave no Teste 1 (200 caracteres), onde a fragmentação é
máxima. Chunks fixos maiores (1000, 2000) cortam menos, mas em compensação diluem a relevância,
porque juntam vários assuntos no mesmo chunk.

### 9. O chunking por parágrafo produziu chunks muito grandes?
Sim, em casos extremos. A média ficou moderada (383.9 caracteres), mas o **maior** chunk chegou a
**40445** caracteres — quando um documento tem um parágrafo gigante sem quebra dupla. O tamanho é
**imprevisível** e depende da formatação de origem.

### 10. O chunking por sentença conseguiu preservar melhor o contexto?
Parcialmente. Agrupar 3 sentenças mantém o **fluxo local** entre frases relacionadas (bom para
texto explicativo), mas o tamanho continua **variável** (máximo de **24787** caracteres), porque
a segmentação de sentenças falha com pontuação irregular, abreviações e fórmulas. Preserva
contexto melhor que o corte cego, mas sem garantia nenhuma de tamanho.

### 11. O Recursive Splitter apresentou vantagens?
Sim — na minha avaliação foi a estratégia mais **equilibrada**. Ele divide primeiro por
parágrafo, depois frase, depois palavra, e só corta no caractere em último caso. O resultado
respeita as fronteiras naturais do texto **e** mantém o tamanho sob controle (máximo de 999
caracteres). Combina a previsibilidade do fixo com o respeito à estrutura — é o padrão que eu
recomendaria para RAG.

### 12. O Markdown Splitter conseguiu preservar a estrutura semântica?
Sim quanto à **hierarquia** (foi o único a registrar seção/subseção nos metadados), mas falhou
quanto ao **tamanho**: gerou o maior chunk de toda a análise (**52313** caracteres). Numa base
heterogênea como a minha (papers com poucos headings) isso é crítico — como o modelo local
processa só ~128 tokens (~500 caracteres), num chunk de 52313 caracteres mais de 99% do conteúdo
é ignorado na hora de gerar o embedding. Ou seja: preserva a estrutura, mas produz vetores pouco
representativos.

### 13. Qual estratégia parece mais adequada para um sistema de RAG?
O **Teste 9 (Recursivo)**. Ele oferece o melhor equilíbrio entre respeitar a estrutura e garantir
um teto de tamanho, mantendo os chunks dentro da janela útil do modelo. Em segundo lugar ficaria
o **Teste 5 (Fixo 500 + overlap 10%)**, como baseline simples e previsível.

### 14. Quais estratégias devem ser descartadas?
- **Teste 1 (Fixo 200):** fragmenta demais e corta conceitos.
- **Teste 4 (Fixo 2000):** dilui a relevância e ultrapassa a janela do modelo.
- **Testes 7, 8 e 10 (parágrafo, sentença, markdown):** tamanho descontrolado (máximos de 40445,
  24787 e 52313), inviável de vetorizar de forma representativa. Guardaria o Teste 10 apenas pelo
  valor dos metadados de estrutura, não pela qualidade do embedding.

### 15. Quais estratégias devem ser utilizadas nos próximos experimentos?
Escolheria três, cobrindo os eixos que me interessam:
- **Teste 9 (Recursivo):** estratégia principal para RAG.
- **Teste 5 (Fixo 500 + overlap 50):** baseline de comparação.
- **Teste 6 (Fixo 500 + overlap 200):** para medir se o overlap pesado compensa a redundância
  (gera 4938 chunks contra 2971 do Teste 2, para a mesma cobertura de texto).

As três mantêm o tamanho **dentro da janela do modelo de embedding**, garantindo vetores
representativos — condição que as descartadas não cumprem.

---

## Conclusão geral

Para mim, o trade-off central do chunking é **controle de tamanho vs. respeito à estrutura**.
As estratégias de tamanho fixo garantem previsibilidade, mas ignoram o significado; as
estruturais respeitam o significado, mas perdem o controle do tamanho. O **chunking recursivo**
foi o que melhor conciliou os dois nesta base.

Dois fatores pesaram bastante nos meus resultados: a **heterogeneidade** dos documentos
(PT + EN, artigos + papers) penaliza as estratégias estruturais, que dependem de formatação
consistente; e a **janela curta do modelo local** (~128 tokens) torna qualquer chunk grande
pouco representativo, o que reforça a preferência por um teto de tamanho baixo e controlado.

Respondendo à pergunta central da atividade — *qual estratégia produz a melhor representação
dos documentos para RAG* — a minha conclusão experimental é o **chunking recursivo (Teste 9)**,
por equilibrar preservação de contexto, controle de tamanho e qualidade da representação
vetorial ao mesmo tempo.
