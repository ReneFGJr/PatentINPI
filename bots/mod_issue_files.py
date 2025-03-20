import database, requests
import sys, os
import zipfile

def unzip(limit=100):
    for i in range(limit):
        row = getNextFile(1, 'PZ')
        if not row or row == 0:
            print("Nenhum arquivo para processar.")
            return

        FN = fileName(row)
        ID = row[0]
        type = row[2]

        if os.path.exists(FN):  # Correção aqui
            descompactar_arquivos(FN,type)
            statusUpdate(ID,2)

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
        print(f'   Movendodo para {destino}')

def harvesting(limit=10):
    for i in range(limit):
        id = getNext(0)
    if id == 0:
        return 0
    else:
        register_http(id)
        return id


def directory(directory):
    # Verifica se o diretório existe, se não, cria
    if not os.path.exists(directory):
        os.makedirs(directory)

def fileName(row):
    dir = "../_repository/"
    pasta_tmp = os.path.join(dir, row[2])
    directory(pasta_tmp)

    ############## Arquivo
    save_path = dir + row[2] + "/" + row[1].split("/")[-1]
    return save_path

def statusUpdate(ID,status):

    # Garantir que status seja uma string válida
    qu = f"UPDATE rpi_issue_files SET rf_status = {int(status)} WHERE id_rf = {int(ID)}"
    database.update(qu)

def download(tp = ''):
    row = getNextFile(0,tp)

    if not row or row == 0:
        print("Nenhum arquivo para processar.")
        return
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
    qr = "select count(*) from rpi_issue_files where rf_status = 0"
    row = database.query(qr)
    print(row)
    return row[0][0]


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
