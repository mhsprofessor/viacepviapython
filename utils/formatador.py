def formatar_cep(cep):
    cep = "".join(filter(str.isdigit, cep))
    if len(cep) != 8:
        return cep
    return f"{cep[:5]}-{cep[5:]}"


def formatar_endereco_completo(dados):
    logradouro = dados.get("logradouro", "")
    numero = dados.get("numero", "")
    complemento = dados.get("complemento", "")
    bairro = dados.get("bairro", "")
    cidade = dados.get("localidade", "")
    uf = dados.get("uf", "")
    cep = dados.get("cep", "")

    partes = [logradouro]
    if numero:
        partes.append(numero)
    if complemento:
        partes.append(complemento)
    if bairro:
        partes.append(bairro)
    if cidade or uf:
        partes.append(f"{cidade}/{uf}")
    if cep:
        partes.append(f"CEP {cep}")

    return " - ".join(p for p in partes if p)


def linha_separadora(tamanho=50, caractere="-"):
    return caractere * tamanho
