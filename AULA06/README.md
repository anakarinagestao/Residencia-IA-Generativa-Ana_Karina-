# Projeto RAG - Comparação entre Dois Cenários
### Cenário 1: Chargeback | Cenário 2: GymRat

---

# CENÁRIO 1 — CHARGEBACK

## Parte 1 - Identificação dos problemas

### 1.1 Descrição do problema

**Problema:** o analista financeiro de risco perde horas buscando manualmente, um a um, as políticas de chargeback de diferentes gateways de pagamento, para saber como agir em cada disputa (prazo, documentos exigidos, motivo de contestação). Hoje esse processo é manual, com anotações em planilha.

**Usuário:** Analista Financeiro de Risco, técnico em informática cursando administração, atua numa empresa que presta serviço de análise de chargeback para vários bancos/gateways. Nível técnico médio (não é dev, mas entende bem de sistemas). Usa diariamente um sistema de gestão que recebe os alertas de chargeback.

**Informações da consulta:** políticas de chargeback específicas de cada gateway de pagamento (prazos de contestação, códigos de motivo, documentos exigidos para anexar na disputa, regras de resolução).

**Fonte de dados:** documentos internos/oficiais publicados por cada gateway de pagamento (manuais de disputa, políticas de chargeback), que mudam com frequência.

**Por que LLM puro não basta:** essas políticas mudam a cada poucas semanas e variam por gateway; um LLM genérico teria conhecimento desatualizado ou misturaria regras de gateways diferentes, gerando orientação errada sobre prazo ou documento exigido.

**Como seria usado:** assistente integrado dentro do próprio sistema de gestão que ele já usa — ele abre o caso de chargeback e consulta o assistente ali mesmo, sem precisar sair do sistema.

**3 perguntas reais:**

1. "Recebi um chargeback do Stripe, motivo 'produto não recebido', o cliente diz que pagou em 10/07 e nunca chegou o produto. Quantos dias eu tenho pra responder essa contestação e o que preciso enviar como prova de entrega?"
2. "Esse chargeback é de reembolso duplicado. O cliente já foi reembolsado uma vez pelo suporte e agora abriu disputa no PagSeguro pedindo de novo. Que política eu sigo pra contestar isso e evitar pagar duas vezes?"
3. "O valor da disputa é de R$1.200, no Mercado Pago, motivo 'transação não autorizada'. Existe algum valor mínimo que muda o procedimento, ou o processo é igual pra qualquer valor?"

### 1.2 Por que RAG?

**Porque RAG:** busca a política atualizada direto no documento fonte no momento da pergunta, em vez de depender da memória estática do LLM.

**Conhecimento fornecido:** políticas de chargeback de cada gateway de pagamento (prazos, documentos exigidos, motivos de contestação).

**Frequência de mudança:** alta — atualizações a cada poucas semanas/meses, conforme cada gateway revisa suas políticas.

**Documentos privados?** Não são sigilosos por natureza, mas formam uma base curada e específica da empresa/BPO, que precisa manter tudo atualizado e organizado por gateway.

**Problema sem RAG (exemplo):** o LLM poderia confundir as políticas dos gateways ou colocar um prazo genérico. Ex.: pergunta "Qual o prazo dessa contestação?" — sem RAG, o LLM responderia "Você tem 21 dias" (prazo genérico misturado, ignorando que PayPal e Stripe têm prazos diferentes, ou usando versão antiga da política da Stripe).

### 1.3 Limitações - quando RAG não é a resposta

RAG é ideal para perguntas baseadas em texto não-estruturado que exigem contexto e explicação. Não é adequado quando a tarefa envolve:

1. **Banco de dados estruturado + SQL** — contagem/soma exata (quantidade de chargebacks, valores ressarcidos).
2. **Busca por palavra-chave** — localizar termo específico sem entender contexto.
3. **Combinação RAG + SQL** — a solução mais realista: RAG explica políticas/prazos, SQL cuida dos números reais.

**Pergunta que RAG responderia mal e SQL bem:**
- "Quantos chargebacks resolvemos esse mês?"
- "Quantos chargebacks conseguimos ressarcir o valor?"
- "Qual gateway tem mais prazo de contestação?"

**Se a pergunta exigir contar/somar/ordenar info espalhada:** RAG teria duas falhas: retrieval limitado (busca só trechos parecidos, perde dados espalhados) e alucinação na geração (modelo "adivinha" valor plausível em vez de admitir que não sabe).

## Parte 2 - Organização dos documentos

**Tipos e volume:** HTML (docs PayPal/Mercado Pago), políticas internas, casos de exemplo reais. Dezenas de documentos, páginas curtas. Atualização a cada 15 dias.

**Estrutura de pastas:**

```
documentos/
├── gateways/
│   ├── paypal/politicas_contestacao/
│   └── mercado_pago/politicas_contestacao/
├── politicas_internas/
├── casos_exemplo/erros_conhecidos/
└── obsoletos/
```

**Definições:** gateways com subpastas próprias facilita busca filtrada; políticas_internas são regras da empresa; casos_exemplo (anonimizados) incluem erros_conhecidos (aprendizado por erro), indexado pelo RAG; obsoletos guarda versões antigas, nunca indexado, só auditoria humana.

**Controle de versão:** estrutura física (documento antigo movido, não copiado, para obsoletos/) + metadado `data_vigencia` (garante priorização do mais recente).

**Filtro de dados sigilosos:** identificados nome de cliente e nº de transação; anonimização automática via regex antes da ingestão (ex.: `[NOME_CLIENTE]`, `[NUM_TRANSACAO]`).

## Parte 3 - Pipeline de ingestão

### 3.1 Extração

- **HTML:** BeautifulSoup4, removendo `<nav>`, `<footer>`, `<script>`, `<style>`, propagandas.
- **PDF com texto selecionável:** pdfplumber ou PyPDF2.
- **PDF escaneado:** OCR via Tesseract (pytesseract).
- **Tabelas:** pdfplumber `extract_tables()` para preservar estrutura linha/coluna (prazos por tipo de transação dependem disso).
- **Imagens:** OCR via Tesseract (prints/comprovantes com valores, datas, status).
- **Multimodal:** áudio fora do escopo por agora; só texto e imagem são tratados.
- **Problemas comuns:** perda de codificação de caracteres (acentos corrompidos) e colapso de tabelas em texto corrido.

### 3.2 Limpeza e normalização

- **Remover:** cabeçalhos/rodapés repetidos, numeração de página, marca d'água, sumário, referências irrelevantes, propagandas.
- **Padronizar:** acentuação/codificação (UTF-8), quebras de linha, espaçamento.
- **Risco de limpar demais:** remover número por engano pode apagar informação crítica (ex.: "30 dias"); limpeza deve ser específica, não genérica.

### 3.3 Frequência de ingestão

- **Políticas/contratos:** mudam raramente; checagem manual a cada 15 dias.
- **Comprovantes/prints:** chegam sem previsibilidade; ingestão em tempo real no momento do envio no chat.
- **Reprocessamento:** só o documento alterado é reprocessado (comparação de data de modificação vs. última ingestão), nunca a base inteira.

## Parte 4 - Metadados

### 4.1 Schema do documento

**Política:**

```json
{
  "document_id": "pol-reembolso-001",
  "title": "Política de Reembolso",
  "document_type": "politica",
  "category": "financeiro",
  "author": "Departamento Jurídico",
  "source": "upload manual - Google Drive",
  "created_at": "2026-01-10"
}
```

**Comprovante:**

```json
{
  "document_id": "comp-4521",
  "title": "Comprovante de Pagamento nº 4521",
  "document_type": "comprovante",
  "category": "financeiro",
  "author": null,
  "source": "sistema de pagamentos - Stripe",
  "created_at": "2026-04-02"
}
```

### 4.2 Schema do chunk

**Política:**

```json
{
  "document_id": "pol-reembolso-001",
  "chunk_id": "pol-reembolso-001-03",
  "page": 2,
  "section": "Prazo para Solicitação de Reembolso",
  "document_type": "politica",
  "text": "O prazo máximo para solicitar reembolso é de 30 dias corridos..."
}
```

**Comprovante:**

```json
{
  "document_id": "comp-4521",
  "chunk_id": "comp-4521-01",
  "page": 1,
  "section": null,
  "document_type": "comprovante",
  "text": "Comprovante de pagamento nº 4521, valor R$ 150,00, gateway Stripe, aprovado em 02/04/2026."
}
```

### 4.3 Perguntas de reflexão

1. **Filtrar busca:** `document_type` — evita trazer comprovante quando a pergunta é sobre política.
2. **Citar fonte:** `title` + `page` + `section` — ex.: "Fonte: Política de Reembolso, página 2, seção 'Prazo para Solicitação de Reembolso'".
3. **Metadado caro de acrescentar depois:** `page` e `section` — exigiriam reabrir e reprocessar o PDF original inteiro.
4. **Como extrair:** `document_type` manual/sistema no upload; `page` automático via pdfplumber/PyPDF2; `section` via IA/heurística (títulos/negrito); `category` via IA de classificação.

## Parte 5 - Chunking / Splitting

- **Estratégia:** Splitter recursivo (parágrafo → sentença → palavra, se exceder limite).
- **Tamanho:** 500-1000 caracteres.
- **Overlap:** 10-20% (50-100 caracteres em chunks de 500), evitando perder valor/prazo cortado entre chunks.
- **Tipo de divisão:** por parágrafo como unidade preferencial, descendo se exceder o limite.
- **Estratégia por tipo de documento:** políticas longas exigem múltiplos chunks respeitando seções; comprovantes curtos cabem em 1 chunk; transcrições de call center pediriam divisão por turno de fala (não se aplica aqui, mas caso surgisse).

**Consequências de chunk mal dimensionado:**
- **Muito pequenos:** perda de contexto, fragmentação (ex.: "prazo de 30 dias" sem dizer de quê).
- **Muito grandes:** embedding "borrado", mistura de assuntos, desperdício de contexto do LLM.
- **Tabelas/imagens:** tabela mantida completa em 1 chunk; imagem gera legenda descritiva textual indexada.
- **Validação:** teste de retrieval com perguntas reais, revisão manual de amostra, comparação A/B de tamanhos de chunk/overlap.

## Parte 6 - Embeddings

| Item | Detalhe |
|---|---|
| Modelo escolhido | **OpenAI text-embedding-3-small** |
| Dimensão do embedding | 1536 |
| Suporta português? | Sim |
| É multilíngue? | Sim, com foco/melhor performance em inglês |
| Tamanho máximo de entrada | 8.191 tokens |
| É open source? | Não |
| Pode ser executado localmente? | Não, apenas via API OpenAI |
| Possui API? | Sim |
| Custo aproximado | US$ 0,02 por 1M de tokens |

**Por que é adequado:** o cenário lida com documentos institucionais de gateways de pagamento e precisa de alta confiabilidade — erro de prazo gera prejuízo real. Custo-benefício ótimo, bom suporte a português, aceita textos longos (8.191 tokens) e não exige infraestrutura própria (importante, já que o time não tem perfil DevOps).

## Arquitetura Final - Chargeback
(gerando )

**Tabela de decisões:**

| Etapa | Decisão | Justificativa |
|---|---|---|
| Extração | BeautifulSoup4, pdfplumber, Tesseract OCR | Formatos variados (HTML, PDF, imagens) exigem ferramenta própria cada |
| Limpeza | Remoção de ruído + anonimização regex | Documentos institucionais têm ruído repetitivo e dados sensíveis a mascarar |
| Chunking | Recursivo, 500-1000 caracteres, overlap 10-20% | Cláusulas de 1-3 parágrafos; overlap evita cortar prazo/valor no meio |
| Metadados | document_type, gateway, page, section, vigência | Filtra gateway certo e cita fonte exata |
| Embeddings | OpenAI text-embedding-3-small | Baixo custo, alta confiabilidade, sem infraestrutura própria |

**Riscos e limitações:**
- Não resolve perguntas numéricas (precisa SQL complementar).
- Dependência de API externa, sem fallback local.
- Anonimização por regex não é 100% confiável para formatos não previstos.
- OCR pode falhar em prints de baixa qualidade.
- Tabelas muito grandes podem exceder o limite do chunk.

---

# CENÁRIO 2 — GYMRAT

## Parte 1 - Identificação dos problemas

### 1.1 Descrição do problema

**Problema:** participantes dos desafios do GymRat às vezes enviam fotos/registros que não correspondem à proposta real do desafio, sem forma automática de verificar se atendem às regras daquele desafio específico.

**Usuário:** participantes inscritos em desafios de hábitos saudáveis, via app mobile, nível técnico baixo/médio.

**Informação consultada:** regras do desafio em que a pessoa está inscrita.

**Origem:** organizador cria o texto de regras dentro do app ao lançar cada novo desafio.

**Por que LLM puro não basta:** regras específicas por desafio, atualizadas/criadas toda semana — o LLM "chutaria" resposta genérica.

**Como é usado:** via chat/assistente dentro do app mobile.

**3 perguntas reais:**

1. "Eu fiz as atividades certas? Registrei do jeito que o desafio pede?"
2. "Essa foto que eu mandei serve pra esse desafio ou eu preciso mandar outra coisa?"
3. "Quais são as regras do desafio que eu me inscrevi essa semana?"

### 1.2 Por que RAG?

Regras atualizadas semanalmente e específicas por desafio; LLM nunca teve acesso a esse conteúdo em treinamento. Conhecimento fornecido: texto das regras cadastradas pelo organizador. Frequência: semanal. Documento privado/específico: sim, mesmo sem ser "PDF corporativo".

**Exemplo de resposta errada sem RAG:** pergunta "quais são as regras dessa semana?" → LLM inventa "beber 2L de água e caminhar 30 minutos" quando a regra real é "20 minutos de alongamento + foto".

### 1.3 Limitações - quando RAG não é a resposta

- **Busca por palavra-chave:** localizar desafio pelo nome exato.
- **SQL:** contagem de desafios completados, check-ins, participantes.
- **Regras determinísticas:** status de prazo (sim/não fixo baseado em data).

**Pergunta que RAG responde mal e SQL bem:** "Quantos desafios já completei?", "quantos check-ins consegui?", "quanto preciso pra ganhar o desafio?"

**Sem RAG apropriado:** resposta aproximada, podendo alucinar número.

## Parte 2 - Organização dos documentos

**Tipo:** texto simples digitado no app. Volume: dezenas de desafios ativos. Tamanho: 4-5 parágrafos. Frequência: nova entrada semanal.

**Estrutura de pastas:**

```
documentos/
├── desafios_ativos/
│   ├── desafio_hidratacao_semana34/
│   └── desafio_alongamento_semana35/
├── desafios_encerrados/
│   └── desafio_caminhada_semana30/
└── regras_gerais/
    └── termos_gerais_gymrat.txt
```

**Justificativa:** separar ativos/encerrados evita responder com regra vencida; cada desafio tem registro próprio; regras_gerais evita confundir regra específica com geral.

**Documento fora da base:** desafios encerrados, controlados via metadado `status` + filtro obrigatório.

**Versionamento:** cada desafio semanal é documento novo, nunca sobrescreve o anterior.

## Parte 3 - Pipeline de ingestão

### 3.1 Extração

Texto já digital, direto do banco de dados — sem OCR nem parsing de PDF. Problema possível: erros de formatação ao copiar/colar (tratado na limpeza).

### 3.2 Limpeza e normalização

Remove espaços duplicados, quebras de linha estranhas, caracteres invisíveis. Padroniza UTF-8 e espaçamento entre parágrafos. Risco: limpeza agressiva pode juntar duas regras distintas.

### 3.3 Frequência de ingestão

Pipeline roda sob demanda, a cada novo desafio publicado. Reprocessamento seletivo: só o documento editado é reprocessado (via `document_id` único).

## Parte 4 - Metadados

### 4.1 Metadados do documento

```json
{
  "document_id": "desafio_hidratacao_semana34",
  "title": "Desafio de Hidratação - Semana 34",
  "author": "nome_do_organizador",
  "source": "app_gymrat",
  "document_type": "regras_desafio",
  "created_at": "2026-08-17",
  "updated_at": "2026-08-20",
  "status": "ativo",
  "data_inicio": "2026-08-17",
  "data_fim": "2026-08-24",
  "category": "hidratacao"
}
```

### 4.2 Metadados do chunk

```json
{
  "document_id": "desafio_hidratacao_semana34",
  "chunk_id": "desafio_hidratacao_semana34-02",
  "paragrafo": 2,
  "status": "ativo",
  "document_type": "regras_desafio",
  "text": "..."
}
```

**Respondendo:**

1. **Filtrar busca:** `status` + `data_fim` — evita trazer regra de desafio encerrado.
2. **Citar fonte:** `title` + `data_inicio`/`data_fim` — ex.: "Fonte: Desafio de Hidratação - Semana 34 (17/08 a 24/08)".
3. **Metadado caro de acrescentar depois:** `status` — exigiria reindexar toda a base.
4. **Como extrair:** maioria já existe estruturada no banco relacional do app, copiada direto para o metadado vetorial.

## Parte 5 - Chunking / Splitting

- **Estratégia:** divisão por parágrafo (cada parágrafo = 1 regra = 1 chunk).
- **Tamanho:** curto, 1 parágrafo.
- **Overlap:** não seria utilizado — pesquisas mostram que não traz ganho de qualidade e aumenta custo de indexação sem necessidade em textos curtos.
- **Splitter recursivo:** não necessário, pois o texto já é curto.
- **Estratégia por tipo de documento:** não necessária, há só um tipo de documento.

**Consequências:**
- **Muito pequenos (por frase):** risco de quebrar regra no meio.
- **Muito grandes (desafio inteiro):** traz regras irrelevantes, dilui resposta.
- **Tabela/imagem:** não se aplica, só texto puro.
- **Validação:** testar as 3 perguntas reais e verificar se o chunk recuperado contém exatamente a regra pedida.

## Parte 6 - Embeddings

| Item | Detalhe |
|---|---|
| Modelo escolhido | **BGE-M3 (BAAI)** |
| Dimensão do embedding | 1024 |
| Suporta português? | Sim |
| É multilíngue? | Sim, 100+ idiomas treinados de forma equilibrada |
| Tamanho máximo de entrada | 8.192 tokens |
| É open source? | Sim (Apache-2.0) |
| Pode ser executado localmente? | Sim, GPU de porte médio (ou CPU, mais lento) |
| Possui API? | Sim, via Hugging Face Inference API (free tier) ou local |
| Custo aproximado | Gratuito |

**Por que é adequado:** volume baixo (dezenas de desafios), textos curtos, sem custo — essencial para bolsista usar só ferramentas gratuitas. Performance equivalente/superior ao `text-embedding-3-small` em benchmarks multilíngues (MTEB ~65,1), com bom suporte a português.

**Respondendo (comum aos dois cenários):**
- **Alternativa descartada (Chargeback):** BGE-M3 foi considerado, mas descartado por exigir infraestrutura própria de GPU, pior custo-benefício que a API para baixo volume.
- **Alternativa descartada (GymRat):** text-embedding-3-small foi considerado, mas descartado por gerar custo recorrente sem necessidade.
- **Dados sigilosos mudam a escolha local vs. API?** No Chargeback, comprovantes contêm dados sensíveis, mas já são anonimizados via regex antes do embedding, permitindo manter a API. Sem essa anonimização, a escolha mudaria para modelo local.
- **Relação entre tamanho máximo de entrada e chunking:** em ambos os cenários, os chunks (500-1000 caracteres no Chargeback; parágrafo curto no GymRat) estão muito abaixo do limite de tokens dos modelos escolhidos (8.191/8.192 tokens), evitando qualquer risco de truncamento.

## Arquitetura Final - GymRat

gerando

**Tabela de decisões:**

| Etapa | Decisão | Justificativa |
|---|---|---|
| Extração | Nenhuma ferramenta especial | Texto já digital do banco de dados do app |
| Limpeza | Remoção de espaços/caracteres invisíveis | Ruído de formatação, sem risco de perda de conteúdo |
| Chunking | Por parágrafo, sem overlap | Cada parágrafo já é uma regra completa e independente |
| Metadados | status, data_inicio, data_fim, category | Evita misturar regra encerrada com a ativa da semana |
| Embeddings | BGE-M3 | Gratuito, open-source, atende bem o português, volume baixo |

**Riscos e limitações:**
- Não resolve perguntas de contagem (precisa SQL complementar).
- BGE-M3 local exige GPU para boa velocidade; em CPU pode ficar lento com crescimento de volume.
- Falta de padronização do texto do organizador (cada um escreve diferente).
- Não valida a foto do check-in em si (fora do escopo do RAG textual).

---

# Comparação entre os dois cenários

## Pontos onde as decisões foram diferentes

| Aspecto | Chargeback | GymRat | Por quê |
|---|---|---|---|
| Extração | Múltiplas ferramentas (BS4, pdfplumber, OCR) | Nenhuma ferramenta especial | Chargeback recebe formatos variados; GymRat só texto digital puro |
| Chunking | Recursivo, 500-1000 caracteres, com overlap | Por parágrafo, sem overlap | Cláusulas longas exigem margem de segurança; regras curtas já são unidades completas |
| Anonimização | Sim (regex) | Não se aplica | Chargeback lida com dados de clientes reais; GymRat só tem regra de desafio |
| Embedding | OpenAI text-embedding-3-small (pago) | BGE-M3 (gratuito) | Empresa pode absorver custo baixo pela confiabilidade; bolsista precisa de gratuito |
| Frequência de ingestão | Duas velocidades (política 15 dias / comprovante tempo real) | Uma velocidade (sob demanda) | Chargeback tem dois tipos de documento com dinâmicas diferentes; GymRat só um tipo |

## Pontos onde as decisões foram iguais

- **Pipeline geral** (extração → limpeza → metadados → chunking → embedding → banco vetorial) idêntico — sinal de **boa prática geral**, esqueleto padrão de qualquer RAG.
- **Reprocessamento seletivo** (só o documento alterado, não a base inteira) — também boa prática, evita custo desnecessário.
- **Metadado de status/vigência para filtrar busca** — necessidade real em qualquer conteúdo que muda com o tempo, não repetição sem pensar.
- **RAG não resolve contagem/soma** (Parte 1.3) — limitação estrutural do próprio RAG, não do cenário.

## Se eu tivesse que construir apenas um dos dois

Escolheria o **Chargeback** — representa um problema de negócio real e mensurável, com base de documentos mais rica e desafiadora tecnicamente (múltiplos formatos, dados sensíveis, políticas por gateway), exercitando mais competências do pipeline completo (OCR, extração de tabela, anonimização, decisão custo vs. hospedagem) do que o GymRat.

---

# Referências

- OpenAI API Docs — text-embedding-3-large/small: https://developers.openai.com/api/docs/models/text-embedding-3-large
- Ergini, "BGE-M3 vs OpenAI Embeddings: Which Should You Use?" (ago/2026): https://ergini.com/blog/bge-m3-vs-openai-embeddings
- CodeLint.Dev, "Embedding Models 2025 — MTEB, Dimensions & Pricing": https://codelint.dev/ai-tools/embedding-guide
- Markaicode, "Pick the Right Embedding Model: OpenAI vs. BGE-M3" (fev/2026): https://markaicode.com/vs/pick-the-right-embedding-model-openai-vs-bge-m3/
- Bennani, S. & Moslonka, C., "A Systematic Analysis of Chunking Strategies for Reliable Question Answering", arXiv, 2026.
- Jurafsky, D. & Martin, J., "Speech and Language Processing", capítulo sobre pré-processamento de texto: https://web.stanford.edu/~jurafsky/slp3/
- Python Docs, "Unicode HOWTO": https://docs.python.org/3/howto/unicode.html
- LangChain Documentation, "Overview": https://docs.langchain.com/oss/python/langchain/overview
- LangChain Documentation, "Text Splitters": https://python.langchain.com/docs/how_to/#text-splitters
- Pinecone Learning Center, "Chunking Strategies for LLM Applications": https://www.pinecone.io/learn/chunking-strategies/
- Kleppmann, M., "Designing Data-Intensive Applications", capítulo 2 (desnormalização em bancos de dados)
- Lewis, P. et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks", Meta AI, 2020: https://arxiv.org/abs/2005.11401

---

# Como usei IA para me apoiar nessa atividade

Criei  a **Claudinha** (assistente baseada em IA, modelo Claude/Anthropic) como mentora ao longo de toda a construção dos dois cenários de RAG (Chargeback e GymRat). A ferramenta foi usada para:

- **Estruturar o raciocínio** de cada parte do desafio (diagnóstico do problema, organização de documentos, pipeline de ingestão, metadados, chunking e embeddings), sempre respondendo primeiro antes de validar ou complementar.
- **Montar diagramas e tabelas de decisão** de forma organizada, sintetizando as escolhas feitas ao longo da conversa.

**Como avaliei e verifiquei as respostas da IA:**
- Toda informação técnica veio acompanhada de **fonte/link específico**, conferido antes de aceitar como verdadeira.
- Comparei dados de mais de uma fonte na mesma pesquisa para reduzir risco de informação desatualizada.
- Revisei criticamente as justificativas, sempre conectando com as características específicas de cada cenário, em vez de aceitar recomendações genéricas.
