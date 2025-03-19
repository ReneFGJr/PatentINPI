import database, requests
import sys, os


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

def download():
    row = getNextFile(0)

    ############ Diretorio
    ID = row[0]
    dir = "../_repository/"
    pasta_tmp = os.path.join(dir,row[2])
    directory(pasta_tmp)

    ############## Arquivo
    save_path = dir + row[2] + "/" + row[1].split("/")[-1]

    ############## URL
    file_url = row[1]


    # Baixar o arquivo
    response = requests.get(file_url, stream=True)
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        qu = "update rpi_issue_files set rf_status = 1 where id_rf = " + str(ID)
        database.update(qu)
    else:
        qu = "update rpi_issue_files set rf_status = 500 where id_rf = " + str(
            ID)
        database.update(qu)
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


def getNextFile(status):
    qr = "select * from rpi_issue_files where rf_status = " + str(
        status) + " order by id_rf limit 1"
    row = database.query(qr)
    if len(row) == 0:
        return 0
    else:
        return row[0]


if __name__ == '__main__':
    print("ID", harvesting())
    download()
