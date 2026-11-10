from api.viacep import buscar_endereco


def consultar_por_endereco(uf, cidade, logradouro):
    return buscar_endereco(uf, cidade, logradouro)


def resumo_resultados(resultados):
    if not resultados:
        return "Nenhum resultado encontrado."

    linhas = [f"Total de resultados: {len(resultados)}\n"]
    for i, item in enumerate(resultados, start=1):
        linhas.append(f"[{i}] {item.get('cep', '-')}")
        linhas.append(f"    {item.get('logradouro', '-')}, {item.get('bairro', '-')}")
        linhas.append(f"    {item.get('localidade', '-')}/{item.get('uf', '-')}")
        linhas.append("")
    return "\n".join(linhas)
