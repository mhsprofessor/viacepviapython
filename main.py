from api.viacep import ViaCEPError
from services.busca_cep import (
    consultar_por_cep,
    consultar_varios_ceps,
    resumo_cep,
    endereco_formatado,
)
from services.busca_endereco import (
    consultar_por_endereco,
    resumo_resultados,
)
from utils.formatador import linha_separadora
from utils.arquivo import (
    salvar_json,
    salvar_csv,
    salvar_txt,
    listar_arquivos,
)


def limpar_tela():
    print("\n" * 50)


def aguardar():
    input("\nTecle ENTER para continuar...")


def exibir_menu():
    limpar_tela()
    print("===== PROJETO VIACEP - MENU =====")
    print("1 - Consultar um CEP")
    print("2 - Consultar varios CEPs")
    print("3 - Consultar endereco por UF/Cidade/Logradouro")
    print("4 - Salvar ultimo resultado em JSON")
    print("5 - Salvar ultimo resultado em CSV")
    print("6 - Salvar ultimo resultado em TXT")
    print("7 - Listar arquivos salvos")
    print("8 - Sair")
    print()

    entrada = input("Informe sua opcao: ")
    try:
        return int(entrada)
    except ValueError:
        return -1


def opcao_1(estado):
    print("\n===== CONSULTAR CEP =====")
    cep = input("Informe o CEP (ex: 01001000): ").strip()

    try:
        dados = consultar_por_cep(cep)
        print(linha_separadora())
        print(resumo_cep(dados))
        print(linha_separadora())
        print("Endereco formatado:")
        print(endereco_formatado(dados))
        estado["ultimo"] = dados
        estado["tipo"] = "cep"
    except ViaCEPError as e:
        print(f"Erro ViaCEP: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")


def opcao_2(estado):
    print("\n===== CONSULTAR VARIOS CEPS =====")
    entrada = input("Informe os CEPs separados por virgula: ")
    lista = [c.strip() for c in entrada.split(",") if c.strip()]

    if not lista:
        print("Nenhum CEP informado.")
        return

    resultados = consultar_varios_ceps(lista)

    print(linha_separadora())
    for r in resultados:
        if r["sucesso"]:
            d = r["dados"]
            print(f"[OK] {r['cep']} -> {d.get('localidade', '-')}/{d.get('uf', '-')}")
        else:
            print(f"[ERRO] {r['cep']} -> {r['erro']}")
    print(linha_separadora())

    estado["ultimo"] = resultados
    estado["tipo"] = "lista_ceps"


def opcao_3(estado):
    print("\n===== CONSULTAR POR ENDERECO =====")
    uf = input("UF (ex: SP): ").strip()
    cidade = input("Cidade (ex: Sao Paulo): ").strip()
    logradouro = input("Logradouro (ex: Avenida Paulista): ").strip()

    try:
        resultados = consultar_por_endereco(uf, cidade, logradouro)
        print(linha_separadora())
        print(resumo_resultados(resultados))
        print(linha_separadora())
        estado["ultimo"] = resultados
        estado["tipo"] = "lista_enderecos"
    except ViaCEPError as e:
        print(f"Erro ViaCEP: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")


def opcao_4(estado):
    print("\n===== SALVAR EM JSON =====")
    if "ultimo" not in estado:
        print("Nenhum resultado para salvar. Faca uma consulta antes.")
        return

    try:
        caminho = salvar_json("resultado.json", estado["ultimo"])
        print(f"Salvo em: {caminho}")
    except Exception as e:
        print(f"Erro: {e}")


def opcao_5(estado):
    print("\n===== SALVAR EM CSV =====")
    if "ultimo" not in estado:
        print("Nenhum resultado para salvar. Faca uma consulta antes.")
        return

    ultimo = estado["ultimo"]

    if isinstance(ultimo, dict):
        lista = [ultimo]
    elif isinstance(ultimo, list):
        lista = []
        for item in ultimo:
            if isinstance(item, dict) and item.get("sucesso"):
                lista.append(item["dados"])
            elif isinstance(item, dict) and "cep" in item:
                lista.append(item)
    else:
        print("Formato nao suportado para CSV.")
        return

    if not lista:
        print("Nada para salvar em CSV.")
        return

    try:
        caminho = salvar_csv("resultado.csv", lista)
        print(f"Salvo em: {caminho}")
    except Exception as e:
        print(f"Erro: {e}")


def opcao_6(estado):
    print("\n===== SALVAR EM TXT =====")
    if "ultimo" not in estado:
        print("Nenhum resultado para salvar. Faca uma consulta antes.")
        return

    ultimo = estado["ultimo"]
    tipo = estado.get("tipo", "")

    try:
        if tipo == "cep":
            texto = resumo_cep(ultimo) + "\n\n" + endereco_formatado(ultimo)
        elif tipo == "lista_ceps":
            linhas = []
            for r in ultimo:
                if r["sucesso"]:
                    linhas.append(resumo_cep(r["dados"]))
                    linhas.append(linha_separadora(40, "="))
            texto = "\n".join(linhas)
        elif tipo == "lista_enderecos":
            texto = resumo_resultados(ultimo)
        else:
            texto = str(ultimo)

        caminho = salvar_txt("resultado.txt", texto)
        print(f"Salvo em: {caminho}")
    except Exception as e:
        print(f"Erro: {e}")


def opcao_7():
    print("\n===== ARQUIVOS SALVOS =====")
    try:
        arquivos = listar_arquivos()
        if not arquivos:
            print("Nenhum arquivo salvo em 'data/'.")
            return
        for a in arquivos:
            print(f"  - {a}")
    except Exception as e:
        print(f"Erro: {e}")


def main():
    estado = {}

    while True:
        opcao = exibir_menu()

        if opcao == 1:
            opcao_1(estado)
            aguardar()
        elif opcao == 2:
            opcao_2(estado)
            aguardar()
        elif opcao == 3:
            opcao_3(estado)
            aguardar()
        elif opcao == 4:
            opcao_4(estado)
            aguardar()
        elif opcao == 5:
            opcao_5(estado)
            aguardar()
        elif opcao == 6:
            opcao_6(estado)
            aguardar()
        elif opcao == 7:
            opcao_7()
            aguardar()
        elif opcao == 8:
            print("\nEncerrando...")
            break
        else:
            print("\nOpcao invalida!")
            aguardar()


if __name__ == "__main__":
    main()
