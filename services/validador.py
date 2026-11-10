def limpar_cep(cep):
    return "".join(filter(str.isdigit, cep))


def cep_valido(cep):
    return len(limpar_cep(cep)) == 8


def uf_valida(uf):
    return isinstance(uf, str) and len(uf.strip()) == 2
