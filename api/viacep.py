import requests


BASE_URL = "https://viacep.com.br/ws"
TIMEOUT = 10


class ViaCEPError(Exception):
    pass


def buscar_cep(cep):
    cep_limpo = "".join(filter(str.isdigit, cep))

    if len(cep_limpo) != 8:
        raise ViaCEPError("CEP deve conter 8 digitos.")

    url = f"{BASE_URL}/{cep_limpo}/json/"

    try:
        resposta = requests.get(url, timeout=TIMEOUT)
        resposta.raise_for_status()
    except requests.exceptions.Timeout:
        raise ViaCEPError("Tempo de conexao esgotado.")
    except requests.exceptions.ConnectionError:
        raise ViaCEPError("Falha na conexao com a internet.")
    except requests.exceptions.HTTPError as e:
        raise ViaCEPError(f"Erro HTTP: {e}")

    dados = resposta.json()

    if "erro" in dados and dados["erro"]:
        raise ViaCEPError(f"CEP '{cep}' nao encontrado.")

    return dados


def buscar_endereco(uf, cidade, logradouro):
    if not uf or len(uf) != 2:
        raise ViaCEPError("UF deve ter 2 letras.")

    if not cidade or not logradouro:
        raise ViaCEPError("Cidade e logradouro sao obrigatorios.")

    cidade_encoded = cidade.replace(" ", "%20")
    logradouro_encoded = logradouro.replace(" ", "%20")
    url = f"{BASE_URL}/{uf}/{cidade_encoded}/{logradouro_encoded}/json/"

    try:
        resposta = requests.get(url, timeout=TIMEOUT)
        resposta.raise_for_status()
    except requests.exceptions.Timeout:
        raise ViaCEPError("Tempo de conexao esgotado.")
    except requests.exceptions.ConnectionError:
        raise ViaCEPError("Falha na conexao com a internet.")
    except requests.exceptions.HTTPError as e:
        raise ViaCEPError(f"Erro HTTP: {e}")

    dados = resposta.json()

    if not dados:
        raise ViaCEPError("Nenhum endereco encontrado.")

    return dados
