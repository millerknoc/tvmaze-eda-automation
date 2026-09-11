import csv

import requests


def buscar_notas_em_lote(lista_series):
    # Lista vazia para guardar os resultados antes de salvar
    resultados_finais = []

    print("Iniciando a busca...\n")

    for nome_serie in lista_series:
        print(f"Pesquisando: {nome_serie}...")
        url = f"https://api.tvmaze.com/singlesearch/shows?q={nome_serie}"
        resposta = requests.get(url)

        if resposta.status_code == 200:
            dados = resposta.json()
            titulo = dados.get("name", "Desconhecido")

            estreia = dados.get("premiered", "")
            ano = estreia[:4] if estreia else "Desconhecido"

            nota = dados.get("rating", {}).get("average", "Sem nota")

            rede = dados.get("network")
            web = dados.get("webChannel")
            status = dados.get("status", "Desconhecido")
            duracao_media = dados.get("averageRuntime", "Desconhecido")
            idioma = dados.get("language", "Desconhecido")

            pais = "Desconhecido"
            if rede and rede.get("country"):
                pais = rede["country"].get("name", "Desconhecido")
            elif web and web.get("country"):
                pais = web["country"].get("name", "Desconhecido")

            generos_lista = dados.get("genres", [])
            generos = ", ".join(generos_lista) if generos_lista else "Sem gênero"

            imdb_id = dados.get("externals", {}).get("imdb", "Sem ID")
            link_imdb = (
                f"https://www.imdb.com/title/{imdb_id}/"
                if imdb_id != "Sem ID"
                else "Sem link"
            )

            onde_assistir = (
                rede["name"] if rede else (web["name"] if web else "Desconhecido")
            )

            if isinstance(nota, (int, float)) and nota >= 8.0:
                resultados_finais.append(
                    [titulo, ano, nota, onde_assistir, status, generos, link_imdb]
                )
                print(f"  -> {titulo} aprovada! (Nota: {nota})")
            else:
                print(f"  -> {titulo} ignorada. (Nota: {nota})")

            # Adiciona os dados dessa série na nossa lista de resultados
            resultados_finais.append([titulo, ano, nota, onde_assistir])
        else:
            print(f"  -> Erro ou não encontrada: {nome_serie}")

    # Parte 2: Salvar tudo em um arquivo CSV
    nome_arquivo = "tabela_series.csv"

    # Abre o arquivo para escrita ('w'), garantindo a formatação correta de caracteres (utf-8)
    with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)

        # Escreve o cabeçalho da tabela
        escritor.writerow(
            [
                "Série",
                "Ano",
                "Nota TVMaze",
                "Streaming/Canal",
                "Status",
                "Gêneros",
                "Link IMDB",
            ]
        )

        # Escreve todas as linhas de dados de uma vez
        escritor.writerows(resultados_finais)

    print("-" * 30)
    print(f"Sucesso! Resultados salvos no arquivo: {nome_arquivo}")
    print("-" * 30)


# Abre o arquivo de texto no modo de leitura ('r')
with open("series.txt", "r", encoding="utf-8") as arquivo_texto:
    # Lê todo o arquivo e quebra as linhas em uma lista do Python
    minhas_series = arquivo_texto.read().splitlines()

# Remove possíveis linhas em branco que você tenha deixado sem querer no final do .txt
minhas_series = [serie for serie in minhas_series if serie.strip()]

# Roda a função com a lista que acabou de ser lida do arquivo
buscar_notas_em_lote(minhas_series)
