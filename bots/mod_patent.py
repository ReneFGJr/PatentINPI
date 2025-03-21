import database
import os, sys
import re

def get_id(PAT):
    qr = "SELECT id_p FROM rpi_patent_nr WHERE p_nr = '" + PAT + "'"
    rows = database.query(qr)
    if len(rows) == 0:
        print(f"Patente {PAT} não encontrada.")
        sys.exit()
    return rows[0][0]

def clearNPR(nr='BR 20 2017 015440-3 Y1'):
    t = {
        'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8',
        'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8',
        'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8',
        'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8',
        'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8',
        'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8',
        'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8',
        'U1', 'U2', 'U3', 'U4', 'U5', 'U6', 'U7', 'U8',
        'Y1', 'Y2', 'Y3', 'Y4', 'Y5', 'Y6', 'Y7', 'Y8',
        'Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'Z6', 'Z7', 'Z8'
    }

    # Divide a string em partes e verifica se o sufixo final está na lista proibida
    partes = nr.split()
    if partes[-1] in t:
        nr = nr.replace(partes[-1], '')

    # Remove todos os caracteres não numéricos
    nr = nr.replace('\n', '')
    nr = nr.strip()

    if '\n' in nr or '\r' in nr:
        print("OOPS", nr)
        sys.exit()

    if len(nr) > 20:
        print("OPPS", nr)
        sys.exit()

    return nr


def extrair_numeros_patentes(conteudo):
    """
    Extrai todos os números de patentes do conteúdo do arquivo,
    considerando apenas quando (11) está no início da linha.
    """
    rst = re.findall(r'^\((11|21)\)\s+([\w\s-]+)', conteudo, re.MULTILINE)
    return rst


def verificar_e_inserir_patente(numero_patente):
    """
    Verifica se a patente já existe no banco. Se não existir, insere.
    """
    numero_patente = numero_patente.strip()
    qr = "SELECT COUNT(*) FROM rpi_patent_nr WHERE p_nr = '" + numero_patente + "'"
    rows = database.query(qr)
    row = rows[0]
    if row[0] == 0:
        qi = "INSERT INTO rpi_patent_nr (p_nr) VALUES ('" + numero_patente + "')"
        database.insert(qi)
        print(f"Patente {numero_patente} adicionada ao banco.")


def processar_arquivo(file):

    if file.endswith('.txt'):
        with open(file, 'r', encoding='latin-1') as f:
            conteudo = f.read()

        numeros_patentes = extrair_numeros_patentes(conteudo)
        for numero in numeros_patentes:
            numero = clearNPR(numero[1])
            if (len(numero) < 6):
                print("Número de patente inválido:", numero)
                sys.exit()
            else:
                verificar_e_inserir_patente(numero)
                verificar_e_inserir_patente(numero[1])

    print("Processamento concluído.")


if __name__ == '__main__':
    processar_arquivos()
