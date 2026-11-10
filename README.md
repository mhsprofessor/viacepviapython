# Projeto ViaCEP

Projeto didático em Python para consulta de CEPs e endereços brasileiros utilizando a API pública [ViaCEP](https://viacep.com.br/).

O programa roda em linha de comando (CLI), com menu interativo, e permite consultar um CEP, vários CEPs de uma vez ou buscar CEPs a partir de um endereço (UF/Cidade/Logradouro). O resultado pode ser exportado para arquivos JSON, CSV ou TXT.

## Funcionalidades

- **Consulta por CEP**: informa um CEP e recebe logradouro, complemento, bairro, cidade, UF, código IBGE e DDD
- **Consulta em lote**: consulta vários CEPs de uma vez (separados por vírgula), exibindo sucesso ou erro de cada um
- **Consulta reversa (por endereço)**: busca os CEPs a partir de UF, cidade e logradouro
- **Exportação de resultados**: salva o último resultado consultado em JSON, CSV ou TXT na pasta `data/`
- **Listagem de arquivos**: mostra os arquivos já salvos
- **Tratamento de erros**: CEP com tamanho inválido, CEP não encontrado, tempo de conexão esgotado, falha de rede e erros HTTP

## Estrutura do projeto

```
viacep_projeto/
├── api/
│   └── viacep.py          # Camada de comunicação com a API (biblioteca requests)
├── services/
│   ├── busca_cep.py       # Consultas por CEP (individual e em lote) e resumo dos dados
│   ├── busca_endereco.py  # Consulta por UF/Cidade/Logradouro e resumo dos resultados
│   └── validador.py       # Validações de CEP e UF
├── utils/
│   ├── arquivo.py         # Leitura e gravação de arquivos (JSON, CSV, TXT) na pasta data/
│   └── formatador.py      # Formatação de CEP (00000-000), endereço completo e separadores
├── data/                  # Resultados exportados (ignorada pelo Git, exceto .gitkeep)
├── main.py                # Menu principal (ponto de entrada do programa)
├── requirements.txt       # Dependências do projeto
├── .gitignore
└── README.md
```

### Arquitetura em camadas

| Camada     | Papel                                                                 |
|------------|-----------------------------------------------------------------------|
| `api/`     | Única camada que conversa com a internet (requisições HTTP e erros)   |
| `services/`| Regras de negócio: orquestra consultas e monta os resumos exibidos    |
| `utils/`   | Funções auxiliares: manipulação de arquivos e formatação de textos    |
| `main.py`  | Interface com o usuário: menu, entrada de dados e exibição de resultados |

## Como obter o projeto

O código-fonte está disponível no GitHub: <https://github.com/mhsprofessor/viacepviapython>

### Opção 1 — Clonar com Git

```
git clone https://github.com/mhsprofessor/viacepviapython.git
cd viacepviapython
```

### Opção 2 — Baixar o ZIP

1. Acesse a página do repositório no GitHub
2. Clique em **Code** → **Download ZIP**
3. Extraia o arquivo em uma pasta de sua preferência
4. Abra um terminal dentro da pasta extraída

## Como executar

### Pré-requisitos

- Python 3.8 ou superior
- Conexão com a internet (necessária para consultar a API do ViaCEP)

### Passo a passo

1. Crie e ative um ambiente virtual:

   ```
   python -m venv venv
   venv\Scripts\activate       # Windows
   source venv/bin/activate    # Linux/Mac
   ```

2. Instale as dependências:

   ```
   pip install -r requirements.txt
   ```

3. Execute o programa:

   ```
   python main.py
   ```

## Menu principal

| Opção | Descrição                                          |
|-------|----------------------------------------------------|
| 1     | Consultar um CEP                                   |
| 2     | Consultar vários CEPs (separados por vírgula)      |
| 3     | Consultar endereço por UF/Cidade/Logradouro        |
| 4     | Salvar o último resultado em JSON (`data/resultado.json`) |
| 5     | Salvar o último resultado em CSV (`data/resultado.csv`)   |
| 6     | Salvar o último resultado em TXT (`data/resultado.txt`)   |
| 7     | Listar arquivos salvos na pasta `data/`            |
| 8     | Sair                                               |

> As opções 4, 5 e 6 exigem que uma consulta (opções 1 a 3) tenha sido feita antes na mesma execução.

## Endpoints utilizados

| Operação            | Endpoint                                          |
|---------------------|---------------------------------------------------|
| Busca por CEP       | `GET https://viacep.com.br/ws/{cep}/json/`        |
| Busca por endereço  | `GET https://viacep.com.br/ws/{uf}/{cidade}/{logradouro}/json/` |

## Erros tratados

A camada `api/viacep.py` converte falhas na exceção personalizada `ViaCEPError`, exibida de forma amigável no menu:

- CEP que não contém 8 dígitos
- CEP inexistente (a API retorna `erro: true`)
- UF com tamanho inválido ou campos de cidade/logradouro vazios
- Tempo de conexão esgotado (timeout de 10 segundos)
- Falha de conexão com a internet
- Erros HTTP (4xx/5xx)

## Sugestões de melhorias

Ideias para evoluir o projeto, incluindo algumas voltadas à análise de dados:

1. **Base histórica de consultas** — hoje as exportações (`resultado.csv`, `resultado.json`) sobrescrevem o arquivo anterior. Gravar cada consulta de forma acumulativa (CSV incremental ou banco SQLite), com data e hora, montaria uma base histórica pronta para análise.

2. **Análise exploratória com pandas** — carregar os dados salvos com `pandas` e gerar estatísticas das consultas: endereços por UF, cidade e bairro, bairros e DDDs mais frequentes, comparação entre regiões etc.

3. **Visualização de dados** — criar gráficos de barras por UF/cidade com `matplotlib` ou montar um dashboard interativo com `Streamlit`, podendo incluir um mapa da distribuição das consultas pelo Brasil com `plotly`.

4. **Testes automatizados** — adicionar testes com `pytest`, simulando as respostas da API com `unittest.mock`, para validar entradas, mensagens de erro e formatação sem depender de internet.

5. **Cache de consultas** — guardar em memória (ou com `requests-cache`) os CEPs já consultados na sessão, evitando requisições repetidas ao ViaCEP e tornando o programa mais rápido.
