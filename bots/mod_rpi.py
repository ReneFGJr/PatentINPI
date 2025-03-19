import requests
import database
from bs4 import BeautifulSoup
import re

def register(nrRPI,status):
    qr = "select * from rpi_issue where rpi_nr = " + str(nrRPI)
    rows = database.query(qr)

    if len(rows) == 0:
        qi = "insert into rpi_issue (rpi_nr, rpi_status) values (" + str(nrRPI) + "," + str(status) + ")"
        database.insert(qi)


def get_latest_rpi_number():
    url = "https://revistas.inpi.gov.br/rpi/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Procurando por padrões numéricos na página
        numbers = []
        for text in soup.stripped_strings:
            match = re.search(r'\b\d{4}\b', text)
            if match:
                numbers.append(int(match.group()))

        if numbers:
            return max(numbers)  # Retorna o maior número encontrado

        return 0
    else:
        return -1

def check_new_issue():
    nrRPI = get_latest_rpi_number()
    while(nrRPI > 1200):
        qr = "select * from rpi_issue where rpi_nr = " + str(nrRPI)
        rows = database.query(qr)
        if len(rows) == 0:
            print(nrRPI,"off")
            url = "https://revistas.inpi.gov.br/txt/P"+str(nrRPI)+".zip"
            if check_url_exists(url):
                register(nrRPI, 0)
            else:
                register(nrRPI, '404')
        nrRPI -= 1

def check_url_exists(url):
    response = requests.head(url)
    return response.status_code == 200

if __name__ == '__main__':
    check_new_issue()
