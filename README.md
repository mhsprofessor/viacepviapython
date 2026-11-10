# Projeto ViaCEP

Projeto didático em Python para consumir a API pública https://viacep.com.br/

## Estrutura

- api/      -> Camada de comunicacao com a API
- services/ -> Regras de negocio
- utils/    -> Funcoes utilitarias
- data/     -> Pasta para salvar resultados
- main.py   -> Menu principal

## Como executar

    python -m venv venv
    venv\Scripts\activate       # Windows
    source venv/bin/activate    # Linux/Mac

    pip install -r requirements.txt
    python main.py
