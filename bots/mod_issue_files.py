import database, requests
import sys, os
import zipfile
import mod_patent, mod_issue_files
from pathlib import Path
from colorama import Fore

def checkDIR():
    dir = "../_repository"
    if not os.path.exists(dir):
        os.makedirs(dir)
        print("Criado diretorio ", dir)
    else:
        print("Diretorio ", dir, "existe")

def process(limit = 10):
    for i in range(limit):
        row = getNextFile(2)
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
    print("Processar", ID, link, "TYPE:"+type, IDf, "ISSUE:", ISSUE)
    fileName = "../_repository/_files/PZ/txt/P"+str(ISSUE)+".txt"
    file = Path(fileName)
    ########################################
    if file.exists():
        mod_patent.processar_arquivo(fileName)
        mod_issue_files.statusUpdate(IDf, 3)
    else:
        print("O arquivo não existe.",fileName)

def unzip(limit=100):
    for i in range(limit):
        row = getNextFile(1, 'PZ')

        if not row or row == 0:
            print("Nenhum arquivo para processar.")
            return

        FN = fileName(row)
        ID = row[0]
        type = row[2]

        if os.path.isfile(FN):  # Correção aqui
            #print("Descompactar", FN)
            #sys.exit()
            descompactar_arquivos(FN,type)
            statusUpdate(ID,2)
        else:
            statusUpdate(ID, 0)


def descompactar_arquivos(arquivo,subdir = ''):
    """
    Descompacta os arquivos ZIP da pasta harvesting e organiza os arquivos
    em harvesting/txt/ ou harvesting/xml/ de acordo com o formato.
    """
    pasta_zip = '../_repository/_files/'
    pasta_tmp = os.path.join(pasta_zip, subdir, 'tmp')
    pasta_txt = os.path.join(pasta_zip, subdir, 'txt')
    pasta_xml = os.path.join(pasta_zip, subdir, 'xml')

    # Criando pastas se não existirem
    for pasta in [pasta_tmp, pasta_txt, pasta_xml]:
        os.makedirs(pasta, exist_ok=True)

    try:
        with zipfile.ZipFile(arquivo, 'r') as zip_ref:
            zip_ref.extractall(pasta_tmp)

        # Movendo arquivos para suas respectivas pastas
        for item in os.listdir(pasta_tmp):
            caminho_item = os.path.join(pasta_tmp, item)
            if item.endswith('.txt'):
                mover_arquivo(caminho_item, pasta_txt)
            elif item.endswith('.xml'):
                mover_arquivo(caminho_item, pasta_xml)

    except zipfile.BadZipFile:
        print(f'Erro: {arquivo} não é um arquivo ZIP válido.')


def mover_arquivo(origem, destino_pasta):
    """
    Move um arquivo para a pasta destino, evitando sobrescrever arquivos existentes.
    Se o arquivo já existir, ele será renomeado com um sufixo numérico.
    """
    nome_arquivo = os.path.basename(origem)
    destino = os.path.join(destino_pasta, nome_arquivo)

    # Se já existir, renomeia adicionando um sufixo numérico
    if not os.path.exists(destino):
        os.rename(origem, destino)
        print(f'   Movendo para {destino}')

def harvesting(limit=10):
    for i in range(limit):
        id = getNext(0)
    if id == 0:
        return 0
    else:
        register_http(id)
        return id


def directoryCheck(directory):
    # Verifica se o diretório existe, se não, cria
    if not os.path.exists(directory):
        os.makedirs(directory)

def fileName(row):
    dir = "../_repository/"
    pasta_tmp = os.path.join(dir, row[2])
    directoryCheck(pasta_tmp)

    ############## Arquivo
    save_path = dir + row[2] + "/" + row[1].split("/")[-1]
    return save_path

def statusUpdate(ID,status):

    # Garantir que status seja uma string válida
    qu = f"UPDATE rpi_issue_files SET rf_status = {int(status)} WHERE id_rf = {int(ID)}"
    database.update(qu)

def download(tp = ''):
    dir = "../_repository"
    directoryCheck(dir)

    row = getNextFile(0,tp)

    if not row or row == 0:
        print(Fore.YELLOW+"Nenhum arquivo para processar."+Fore.WHITE)
        return -1

    ############ Diretorio
    ID = row[0]
    save_path = fileName(row)

    ############## URL
    file_url = row[1]

    # Baixar o arquivo
    response = requests.get(file_url, stream=True)
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        statusUpdate(ID,1)
    else:
        statusUpdate(ID, 500)
    print("   download", save_path)
    return 1

def register(nrRPI, status, type, file):
    qr = "select * from rpi_issue_files where rf_url = '" + file + "'"
    rows = database.query(qr)

    if len(rows) == 0:
        qi = "insert into rpi_issue_files (rf_issue, rf_status, rf_url, rf_tipo) values (" + str(
            nrRPI) + "," + str(status) + ",'" + file + "','" + type + "')"
        database.insert(qi)


def register_http(nrRPI):
    urls = [
        ('PZ', f'https://revistas.inpi.gov.br/txt/P{nrRPI}.zip'),
        ('CZ', f'https://revistas.inpi.gov.br/txt/CT{nrRPI}.zip'),
        ('PC', f'https://revistas.inpi.gov.br/txt/PC{nrRPI}.zip'),
        ('PDC', f'https://revistas.inpi.gov.br/pdf/Comunicados{nrRPI}.pdf'),
        ('PDD', f'https://revistas.inpi.gov.br/pdf/Desenhos_Industriais{nrRPI}.pdf'),
        ('PDM', f'https://revistas.inpi.gov.br/pdf/Marcas{nrRPI}.pdf'),
        ('PPC', f'https://revistas.inpi.gov.br/pdf/Programa_de_computador{nrRPI}.pdf'),
        ('PTP', f'https://revistas.inpi.gov.br/pdf/Topografia_de_circuto_Integrado{nrRPI}.pdf')
    ]

    status = 0

    for tipo, url in urls:
        qr = "SELECT * FROM rpi_issue_files WHERE rf_url = '"+url+"'"
        rows = database.query(qr)

        if not rows:
            print("Registrar", url)
            register(nrRPI, status, tipo, url)

    ############ Update
    qr = "update rpi_issue set rpi_status = 1 where rpi_nr = " + str(nrRPI)
    database.update(qr)

def getNext(status):
    qr = "select rpi_nr from rpi_issue where rpi_status = " + str(
        status) + " order by rpi_nr desc limit 1"
    row = database.query(qr)
    if len(row) == 0:
        return 0
    else:
        return row[0][0]

def resume():
    qr = "select count(*), rf_status, rf_tipo from rpi_issue_files group by rf_tipo, rf_status order by rf_tipo, rf_status"
    row = database.query(qr)
    status = {0: 'Pendente', 1: 'Baixado', 2: 'Descompactado',3:'Pre-Processado',4:'Processado Metadados I', 5:'Processado Metadados II'}
    type = {'PZ': 'Patente ZIP', 'CZ': 'Certificado ZIP', 'PC': 'Patente Completa', 'PDC': 'Comunicado',
            'PDD': 'Desenho', 'PDM': 'Marca', 'PPC': 'Programa de Computador', 'PTP': 'Topografia de Circuito Integrado'}
    tp = ''
    for i in row:
        if tp != i[2]:
            tp = i[2]
            print("=============== Tipo", type[tp],tp)
        print(status[i[1]], i[0])



def getNextFile(status,type=''):
    compl = ''
    if type != '':
        compl = " and rf_tipo = '"+type+"' "
    qr = "select * from rpi_issue_files where rf_status = " + str(
        status) + " "+ compl +"order by id_rf limit 1"
    row = database.query(qr)
    if len(row) == 0:
        return 0
    else:
        return row[0]


if __name__ == '__main__':
    harvesting()
    download()
