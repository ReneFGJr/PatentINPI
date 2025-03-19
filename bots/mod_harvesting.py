import os
import requests
from datetime import datetime, timedelta
import zipfile


def calcular_numero_semana(data):
    """
    Calcula o número da semana no formato Pxxxx baseado na data fornecida.
    O número da semana começa na primeira semana do ano.
    """
    ano_inicio = datetime(data.year, 1, 1)
    semana_num = (data - ano_inicio).days // 7 + 1
    return f'P{data.year % 100:02d}{semana_num:02d}'


def baixar_arquivo(url, destino):
    """
    Baixa um arquivo da URL especificada e salva no destino.
    Se ocorrer erro na requisição, ignora.
    """
    try:
        resposta = requests.get(url, stream=True)
        resposta.raise_for_status()
        with open(destino, 'wb') as arquivo:
            for chunk in resposta.iter_content(chunk_size=8192):
                arquivo.write(chunk)
        print(f'{destino} baixado com sucesso.')
    except requests.exceptions.RequestException as e:
        print(f'Erro ao baixar {url}: {e}')


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
        print(f'Movido {nome_arquivo} para {destino}')

def descompactar_arquivos():
    """
    Descompacta os arquivos ZIP da pasta harvesting e organiza os arquivos
    em harvesting/txt/ ou harvesting/xml/ de acordo com o formato.
    """
    pasta_zip = '../harvesting'
    pasta_tmp = os.path.join(pasta_zip, 'tmp')
    pasta_txt = os.path.join(pasta_zip, 'txt')
    pasta_xml = os.path.join(pasta_zip, 'xml')

    # Criando pastas se não existirem
    for pasta in [pasta_tmp, pasta_txt, pasta_xml]:
        os.makedirs(pasta, exist_ok=True)

    # Percorre os arquivos ZIP na pasta principal
    for arquivo in os.listdir(pasta_zip):
        if arquivo.endswith('.zip'):
            caminho_zip = os.path.join(pasta_zip, arquivo)
            try:
                with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
                    zip_ref.extractall(pasta_tmp)
                    print(f'{arquivo} extraído para {pasta_tmp}')

                # Movendo arquivos para suas respectivas pastas
                for item in os.listdir(pasta_tmp):
                    caminho_item = os.path.join(pasta_tmp, item)
                    if item.endswith('.txt'):
                        mover_arquivo(caminho_item, pasta_txt)
                    elif item.endswith('.xml'):
                        mover_arquivo(caminho_item, pasta_xml)

            except zipfile.BadZipFile:
                print(f'Erro: {arquivo} não é um arquivo ZIP válido.')

def coletar_arquivos():
    """
    Percorre as semanas desde o ano 2000 até a semana atual,
    baixando os arquivos de cada semana caso ainda não existam.
    """
    pasta_destino = '../harvesting'
    os.makedirs(pasta_destino, exist_ok=True)

    data_atual = datetime.now()
    data_inicio = datetime(2020, 1, 1)  # Início da coleta no ano 2000

    while data_inicio <= data_atual:
        numero_semana = calcular_numero_semana(data_inicio)
        url = f'http://revistas.inpi.gov.br/txt/{numero_semana}.zip'
        caminho_arquivo = os.path.join(pasta_destino, f'{numero_semana}.zip')

        if not os.path.exists(caminho_arquivo):
            baixar_arquivo(url, caminho_arquivo)
        else:
            print(f'{caminho_arquivo} já existe. Pulando download.')

        data_inicio += timedelta(weeks=1)


if __name__ == '__main__':
    descompactar_arquivos()
    coletar_arquivos()
