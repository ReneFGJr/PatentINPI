import re, sys
import mod_issue_files, mod_patent
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
            metadados(conteudo, ISSUE)
        #mod_issue_files.statusUpdate(IDf, 4)
    else:
        print("O arquivo não existe.", fileName)

def separar_sessoes(texto):
    # Regex para capturar cada sessão iniciando com '(Cd)'
    sessoes = re.split(r'(?=\(Cd\))', texto)

    # Removendo espaços extras e entradas vazias
    sessoes = [s.strip() for s in sessoes if s.strip()]

    return sessoes


def metadados(texto, ISSUE):
    sessoes = separar_sessoes(texto)

    for i, sessao in enumerate(sessoes, 1):
        sessao = sessao.strip()
        if (sessao[0] == '('):
            nrPAT = mod_patent.extrair_numeros_patentes(sessao)
            nrPAT = mod_patent.clearNPR(nrPAT[0][1])
            IDp = mod_patent.get_id(nrPAT)
            print(f"Sessão {i}: {nrPAT} => {IDp}")
            meta = extrair_metadados(sessao)
            for m in meta:
                print(f"{m['codigo']} [{ISSUE}] == {m['valor']}")
                if (m['codigo'] == '73'):
                    mod_patent.update54(IDp, m['valor'])
            print("=" * 50)
            sys.exit()


def extrair_metadados(texto):
    # Expressão regular para capturar campos e seus valores
    padrao = re.compile(r"\((\w{2})\)\s+(.*?)(?=\n\(\w{2}\)|\Z)", re.DOTALL)
    metadados = []

    for match in padrao.finditer(texto):
        codigo = match.group(1)
        valor = match.group(2).strip()
        metadados.append({'codigo': codigo, 'valor': valor})

    return metadados
