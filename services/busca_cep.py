from api.viacep import buscar_cep
from utils.formatador import formatar_endereco_completo


def consultar_por_cep(cep):
    return buscar_cep(cep)


def consultar_varios_ceps(lista_ceps):
    resultados = []
    for cep in lista_ceps:
        try:
            dados = buscar_cep(cep)
            resultados.append({"cep": cep, "sucesso": True, "dados": dados})
        except Exception as e:
            resultados.append({"cep": cep, "sucesso": False, "erro": str(e)})
    return resultados


def resumo_cep(dados):
    linhas = []
    linhas.append(f"CEP:         {dados.get('cep', '-')}")
    linhas.append(f"Logradouro:  {dados.get('logradouro', '-')}")
    linhas.append(f"Complemento: {dados.get('complemento', '-')}")
    linhas.append(f"Bairro:      {dados.get('bairro', '-')}")
    linhas.append(f"Cidade:      {dados.get('localidade', '-')}")
    linhas.append(f"UF:          {dados.get('uf', '-')}")
    linhas.append(f"IBGE:        {dados.get('ibge', '-')}")
    linhas.append(f"DDD:         {dados.get('ddd', '-')}")
    return "\n".join(linhas)


def endereco_formatado(dados):
    return formatar_endereco_completo(dados)
