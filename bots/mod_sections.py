import re, sys
import mod_issue_files
from pathlib import Path
from colorama import Fore

def process(limit = 10):
    for i in range(limit):
        row = mod_issue_files.getNextFile(3)
        if row != []:
            type = row[2]
            ############### Tipos de Processamento
            if (type == 'PZ'):
                processar_PZ(row)


############################################## Processar Patentes
def processar_PZ(line):
    IDf = line[0]
    link = line[1]
    type = line[2]
    ID = line[3]
    ISSUE = line[4]
    print("Processar", ID, link, "TYPE:" + type, IDf, "ISSUE:", ISSUE)
    fileName = "../_repository/_files/PZ/txt/P" + str(ISSUE) + ".txt"
    file = Path(fileName)
    ########################################
    if file.exists():
        with open(fileName, 'r', encoding='latin-1') as f:
            conteudo = f.read()
            metadados(conteudo)
        #mod_issue_files.statusUpdate(IDf, 4)
    else:
        print("O arquivo não existe.", fileName)

def separar_sessoes(texto):
    # Regex para capturar cada sessão iniciando com '(Cd)'
    sessoes = re.split(r'(?=\(Cd\))', texto)

    # Removendo espaços extras e entradas vazias
    sessoes = [s.strip() for s in sessoes if s.strip()]

    return sessoes

def metadados(texto):
    sessoes = separar_sessoes(texto)
    for i, sessao in enumerate(sessoes, 1):
        print(f"Sessão {i}:")
        print(sessao)
        print("-" * 50)
        if (sessao[0] == '('):
            sys.exit()
