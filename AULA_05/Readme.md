# Aula 05 — Documents, Metadados e Busca Vetorial com LangChain

Nesta aula, o objetivo foi compreender melhor como o LangChain trabalha com objetos `Document`, como os metadados podem ser utilizados para organizar informações e por que esses dados são importantes em um sistema que realiza busca vetorial, como um RAG.

---

## Exercício 1 — Criando Documents manualmente

### Criando a lista de Documents

Para este exercício, foram criados manualmente cinco objetos `Document`. Cada documento possui duas partes principais:

* `page_content`: armazena o conteúdo textual;
* `metadata`: guarda informações adicionais sobre aquele conteúdo, como arquivo de origem, página, tema e tipo.

```python
from langchain_core.documents import Document

documentos = [
    Document(
        page_content="Embeddings são representações vetoriais densas de texto.",
        metadata={
            "fonte": "arquivo_01.md",
            "pagina": 1,
            "tipo": "teoria",
            "tema": "embeddings",
            "autor": "Marcio"
        }
    ),
    Document(
        page_content="Chunking é o processo de dividir documentos longos em pedaços menores.",
        metadata={
            "fonte": "arquivo_01.md",
            "pagina": 2,
            "tipo": "teoria",
            "tema": "chunking",
            "autor": "Marcio"
        }
    ),
    Document(
        page_content="RAG combina busca de informação com geração de texto por LLMs.",
        metadata={
            "fonte": "arquivo_02.md",
            "pagina": 1,
            "tipo": "teoria",
            "tema": "rag",
            "autor": "Marcio"
        }
    ),
    Document(
        page_content="Tokenização é o processo de dividir texto em unidades menores chamadas tokens.",
        metadata={
            "fonte": "arquivo_02.md",
            "pagina": 3,
            "tipo": "teoria",
            "tema": "tokenizacao",
            "autor": "Marcio"
        }
    ),
    Document(
        page_content="O Recursive Character Text Splitter tenta preservar a estrutura natural do texto.",
        metadata={
            "fonte": "arquivo_01.md",
            "pagina": 4,
            "tipo": "pratica",
            "tema": "chunking",
            "autor": "Marcio"
        }
    ),
]
```

### Exibindo o conteúdo e os metadados

Ao imprimir os documentos, é possível visualizar separadamente o texto armazenado em `page_content` e as informações complementares presentes em `metadata`.

```text
Documento 1:
  page_content: Embeddings são representações vetoriais densas de texto.
  metadata: {'fonte': 'arquivo_01.md', 'pagina': 1, 'tipo': 'teoria', 'tema': 'embeddings', 'autor': 'Marcio'}

Documento 2:
  page_content: Chunking é o processo de dividir documentos longos em pedaços menores.
  metadata: {'fonte': 'arquivo_01.md', 'pagina': 2, 'tipo': 'teoria', 'tema': 'chunking', 'autor': 'Marcio'}

Documento 3:
  page_content: RAG combina busca de informação com geração de texto por LLMs.
  metadata: {'fonte': 'arquivo_02.md', 'pagina': 1, 'tipo': 'teoria', 'tema': 'rag', 'autor': 'Marcio'}

Documento 4:
  page_content: Tokenização é o processo de dividir texto em unidades menores chamadas tokens.
  metadata: {'fonte': 'arquivo_02.md', 'pagina': 3, 'tipo': 'teoria', 'tema': 'tokenizacao', 'autor': 'Marcio'}

Documento 5:
  page_content: O Recursive Character Text Splitter tenta preservar a estrutura natural do texto.
  metadata: {'fonte': 'arquivo_01.md', 'pagina': 4, 'tipo': 'pratica', 'tema': 'chunking', 'autor': 'Marcio'}
```

### Quantidade de documentos

Utilizando `len(documentos)`, foi confirmado que a lista possui cinco objetos:

```python
len(documentos)
```

Resultado:

```text
5
```

---

### Que tipos de dados podem ser armazenados em `metadata`?

Para verificar isso, foram realizados testes utilizando uma lista e também um dicionário aninhado dentro dos metadados.

```python
doc_lista = Document(
    page_content="Teste com lista nos metadados.",
    metadata={
        "tags": ["embeddings", "rag", "chunking"]
    }
)

print(doc_lista.metadata)
```

Resultado:

```text
{'tags': ['embeddings', 'rag', 'chunking']}
```

Também foi criado um documento contendo um dicionário dentro de outro dicionário:

```python
doc_dict = Document(
    page_content="Teste com dicionário aninhado nos metadados.",
    metadata={
        "info": {
            "autor": "Marcio",
            "ano": 2026
        }
    }
)

print(doc_dict.metadata)
```

Resultado:

```text
{'info': {'autor': 'Marcio', 'ano': 2026}}
```

Nos dois testes, os dados foram aceitos sem apresentar erros. Isso acontece porque, no objeto `Document`, o campo `metadata` funciona como um dicionário (`dict`), permitindo armazenar diferentes estruturas de dados.

No entanto, é importante manter uma organização consistente nos metadados. O LangChain não define, nesse momento, um formato único para essas informações, portanto cabe ao desenvolvedor estabelecer um padrão adequado para o projeto.

> **Ponto de atenção:** o fato de o `Document` aceitar listas ou dicionários aninhados não significa que esses mesmos dados serão aceitos por qualquer banco vetorial. Algumas vector stores podem exigir valores mais simples, como `string`, `int`, `float` ou `bool`. Por isso, antes de indexar os documentos, é importante verificar quais tipos de metadados são suportados pela ferramenta utilizada.

---

### O que acontece se um `Document` for criado sem `metadata`?

O campo `metadata` não é obrigatório. Portanto, é possível criar um documento apenas com o conteúdo textual:

```python
doc_sem_metadata = Document(
    page_content="Documento sem metadados definidos."
)

print(doc_sem_metadata.metadata)
print(type(doc_sem_metadata.metadata))
```

Resultado:

```text
{}
<class 'dict'>
```

Quando nenhum valor é informado, o `Document` cria um dicionário vazio como valor padrão para `metadata`.

---

# Exercício 2 — Projetando um schema de metadados

Neste exercício, foi definido um conjunto de campos para organizar melhor os chunks gerados durante o processamento dos documentos.

A ideia é que os metadados não sirvam apenas para identificar o arquivo de origem, mas também ajudem a entender como o chunk foi criado, onde ele estava localizado no documento e quais características possui.

## Schema definido

| Campo           | Descrição                                                      | Origem            |
| --------------- | -------------------------------------------------------------- | ----------------- |
| `fonte`         | Nome do arquivo `.md` de onde o conteúdo foi obtido            | Obrigatório       |
| `documento_id`  | Identificador utilizado para reconhecer o documento            | Obrigatório       |
| `chunk_index`   | Indica a posição do chunk dentro do documento                  | Obrigatório       |
| `estrategia`    | Estratégia de chunking utilizada na geração do trecho          | Obrigatório       |
| `chunk_size`    | Tamanho configurado para os chunks                             | Obrigatório       |
| `chunk_overlap` | Quantidade de sobreposição configurada entre os chunks         | Obrigatório       |
| `n_caracteres`  | Quantidade real de caracteres presentes no chunk               | Obrigatório       |
| `pagina`        | Página do PDF original relacionada ao conteúdo                 | Campo adicional 1 |
| `heading_secao` | Seção ou título mais próximo do conteúdo, quando disponível    | Campo adicional 2 |
| `contem_tabela` | Indica se foi identificada possível sintaxe de tabela no chunk | Campo adicional 3 |

---

## Justificativa dos campos adicionais

### `pagina`

O campo `pagina` é útil principalmente para rastreabilidade. Em uma aplicação RAG, ele pode permitir que a resposta informe ao usuário a localização original daquela informação.

Por exemplo:

> "A informação foi encontrada na página 5 do documento X."

Esse tipo de dado torna a resposta mais verificável, pois facilita o retorno à fonte original.

### `heading_secao`

Esse campo ajuda a identificar o contexto do trecho recuperado. Além de saber de qual documento a informação veio, é possível saber em qual seção ela estava.

Por exemplo, um chunk pode pertencer às seções:

* Resumo;
* Metodologia;
* Resultados;
* Referências.

Essa informação pode ajudar tanto na organização dos dados quanto na interpretação da relevância do conteúdo recuperado.

### `contem_tabela`

Durante a conversão de documentos de PDF para Markdown, estruturas como tabelas podem não ser preservadas exatamente como estavam no arquivo original.

Por esse motivo, o campo `contem_tabela` foi incluído para indicar que determinado chunk pode conter conteúdo tabular. Isso pode ser útil para aplicar algum tratamento específico ou realizar uma validação antes de utilizar esses dados em uma aplicação.

---

## Exemplos utilizando chunks reais

Para testar o schema, foram utilizados dois chunks provenientes de documentos diferentes. Os dois foram gerados anteriormente na Aula 04 utilizando a estratégia **Recursive Character Text Splitter**, correspondente ao Teste 9.

O objetivo foi verificar se a mesma estrutura de metadados poderia ser utilizada de forma consistente para documentos diferentes.

### Exemplo 1 — `bioetica_e_ia.md`

```json
{
  "fonte": "bioetica_e_ia.md",
  "documento_id": "bioetica_e_ia",
  "chunk_index": 0,
  "estrategia": "recursive",
  "chunk_size": 500,
  "chunk_overlap": 50,
  "n_caracteres": 405,
  "pagina": null,
  "heading_secao": null,
  "contem_tabela": true
}
```

### Exemplo 2 — `twitter_algoritmo.md`

```json
{
  "fonte": "twitter_algoritmo.md",
  "documento_id": "twitter_algoritmo",
  "chunk_index": 0,
  "estrategia": "recursive",
  "chunk_size": 500,
  "chunk_overlap": 50,
  "n_caracteres": 465,
  "pagina": null,
  "heading_secao": null,
  "contem_tabela": false
}
```

### Sobre os campos `pagina` e `heading_secao`

Nos dois exemplos, esses campos possuem o valor `null`.

Isso acontece porque o processo utilizado anteriormente para converter o PDF em Markdown, através do `pymupdf4llm`, não manteve no texto uma referência direta ao número da página original.

Além disso, a estratégia **Recursive Character Text Splitter** utilizada nesses exemplos não adiciona automaticamente informações sobre títulos ou headings. Esse comportamento é diferente, por exemplo, do **Markdown Header Text Splitter**, que consegue trabalhar preservando a estrutura de cabeçalhos.

Portanto, o valor `null` nesses campos representa uma limitação das informações disponíveis no pipeline utilizado para gerar esses chunks, e não um problema no schema criado.

### Sobre o campo `contem_tabela`

A identificação desse campo foi feita utilizando uma regra simples:

```python
"|" in texto
```

Ou seja, se o caractere `|` estiver presente no texto, o campo pode ser marcado como `true`.

Esse método funciona apenas como uma heurística e pode gerar falsos positivos. No primeiro exemplo, por exemplo, o valor `true` não representa necessariamente a existência de uma tabela. O caractere `|` pode estar sendo utilizado apenas como um separador visual no conteúdo.

Por isso, para uma aplicação real, seria interessante utilizar uma estratégia mais precisa para identificar estruturas tabulares.

---

## Perguntas finais

### Qual campo seria mais útil para citar a fonte na resposta final de um sistema RAG?

Para uma identificação básica, a combinação de `fonte` com `chunk_index` já permite localizar a origem de um trecho.

Por exemplo:

> "Informação recuperada do documento `bioetica_e_ia.md`, no chunk 3."

Entretanto, se o objetivo for apresentar uma referência mais clara para o usuário, o campo `pagina` seria especialmente útil. Dessa forma, seria possível informar algo como:

> "A informação foi encontrada na página 5 do documento X."

No pipeline utilizado até o momento, essa informação ainda não está disponível para todos os chunks, mas seria uma melhoria importante para aumentar a rastreabilidade das respostas.

### Por que o `chunk_index` é importante quando um trecho é recuperado incompleto?

O `chunk_index` permite saber exatamente em qual posição determinado trecho está dentro de um documento.

Isso é importante porque, dependendo da estratégia de chunking, uma explicação pode acabar dividida entre dois ou mais chunks. Se o sistema recuperar apenas o chunk de índice `5`, por exemplo, talvez ele contenha somente uma parte da explicação.

Nesse caso, é possível utilizar o `documento_id` junto com o `chunk_index` para localizar os trechos próximos, como os chunks `4` e `6`, e recuperar mais contexto antes de gerar a resposta.

Dessa forma, o sistema não fica limitado apenas ao trecho inicialmente encontrado e pode considerar informações anteriores ou posteriores para construir uma resposta mais completa.

Essa ideia de recuperar conteúdo ao redor do trecho encontrado é uma forma de **expansão de contexto**, utilizada em estratégias mais robustas de recuperação de informações em sistemas RAG.
