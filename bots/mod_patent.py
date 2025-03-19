import database
import os, sys
import re


def extrair_numeros_patentes(conteudo):
    """
    Extrai todos os números de patentes do conteúdo do arquivo,
    considerando apenas quando (11) está no início da linha.
    """
    return re.findall(r'^\(11\)\s+([\w\s-]+)', conteudo, re.MULTILINE)


def verificar_e_inserir_patente(numero_patente):
    """
    Verifica se a patente já existe no banco. Se não existir, insere.
    """
    qr = "SELECT COUNT(*) FROM rpi_patent_nr WHERE p_nr = '"+numero_patente+"'"
    rows = database.query(qr)
    row = rows[0]
    if row[0] == 0:
        qi = "INSERT INTO rpi_patent_nr (p_nr) VALUES ('"+numero_patente+"')"
        database.insert(qi)
        print(f"Patente {numero_patente} adicionada ao banco.")


def processar_arquivos():
    """
    Percorre todos os arquivos na pasta harvesting/txt,
    extrai os números de patentes e insere no banco de dados.
    """
    pasta_txt = '../harvesting/txt'

    if not os.path.exists(pasta_txt):
        print("Pasta de textos não encontrada.")
        return

    for arquivo in os.listdir(pasta_txt):
        caminho_arquivo = os.path.join(pasta_txt, arquivo)
        print("############### Arquivo ###########",arquivo)

        if arquivo.endswith('.txt'):
            with open(caminho_arquivo, 'r', encoding='latin-1') as f:
                conteudo = f.read()

            numeros_patentes = extrair_numeros_patentes(conteudo)
            for numero in numeros_patentes:
                verificar_e_inserir_patente(numero.strip())


    print("Processamento concluído.")


if __name__ == '__main__':
    processar_arquivos()
