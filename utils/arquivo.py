import csv
import json
import os


PASTA_DATA = "data"


def garantir_pasta():
    if not os.path.exists(PASTA_DATA):
        os.makedirs(PASTA_DATA)


def salvar_json(nome_arquivo, dados):
    garantir_pasta()
    caminho = os.path.join(PASTA_DATA, nome_arquivo)
    try:
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)
        return caminho
    except Exception as e:
        raise IOError(f"Erro ao salvar JSON: {e}")


def ler_json(nome_arquivo):
    caminho = os.path.join(PASTA_DATA, nome_arquivo)
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo '{nome_arquivo}' nao encontrado.")
    except json.JSONDecodeError:
        raise ValueError(f"Arquivo '{nome_arquivo}' nao e um JSON valido.")


def salvar_csv(nome_arquivo, lista_dicionarios):
    garantir_pasta()
    caminho = os.path.join(PASTA_DATA, nome_arquivo)

    if not lista_dicionarios:
        raise ValueError("Lista vazia: nada para salvar.")

    try:
        campos = list(lista_dicionarios[0].keys())
        with open(caminho, "w", newline="", encoding="utf-8") as f:
            escritor = csv.DictWriter(f, fieldnames=campos)
            escritor.writeheader()
            for item in lista_dicionarios:
                escritor.writerow(item)
        return caminho
    except Exception as e:
        raise IOError(f"Erro ao salvar CSV: {e}")


def salvar_txt(nome_arquivo, texto):
    garantir_pasta()
    caminho = os.path.join(PASTA_DATA, nome_arquivo)
    try:
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(texto)
        return caminho
    except Exception as e:
        raise IOError(f"Erro ao salvar TXT: {e}")


def listar_arquivos():
    garantir_pasta()
    return [a for a in os.listdir(PASTA_DATA) if a != ".gitkeep"]
