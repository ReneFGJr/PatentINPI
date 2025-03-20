import database
import os, sys
import re

def clearNPR(nr):
    t = {'B1','B8','C8','F1','Y1','Y8'}
    nr = nr.replace(' B1','')
    nr = nr.replace(' B1', '')
    nr = nr.replace(' B1', '')
    return re.sub(r'\D', '', nr)

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
    numero_patente = numero_patente.strip()
    qr = "SELECT COUNT(*) FROM rpi_patent_nr WHERE p_nr = '"+numero_patente+"'"
    print(qr)
    rows = database.query(qr)
    row = rows[0]
    if row[0] == 0:
        qi = "INSERT INTO rpi_patent_nr (p_nr) VALUES ('"+numero_patente+"')"
        database.insert(qi)
        print(f"Patente {numero_patente} adicionada ao banco.")


def processar_arquivo(file):

    if file.endswith('.txt'):
        with open(file, 'r', encoding='latin-1') as f:
            conteudo = f.read()

        numeros_patentes = extrair_numeros_patentes(conteudo)
        for numero in numeros_patentes:
            numero = numero.replace('\n','').strip()
            verificar_e_inserir_patente(numero)

    print("Processamento concluído.")


if __name__ == '__main__':
    processar_arquivos()
