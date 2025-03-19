import os
import requests
from datetime import datetime, timedelta


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


def coletar_arquivos():
    """
    Percorre as semanas desde o ano 2000 até a semana atual,
    baixando os arquivos de cada semana caso ainda não existam.
    """
    pasta_destino = '../harvesting'
    os.makedirs(pasta_destino, exist_ok=True)

    data_atual = datetime.now()
    data_inicio = datetime(2000, 1, 1)  # Início da coleta no ano 2000

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
    coletar_arquivos()
