import socket

def db():
    hostname = socket.gethostname()
    if (hostname == 'DESKTOP-M0Q0TD7'):
        config = {
            'user': 'root',
            'password': '',
            'host': 'localhost',
            'database': 'brapci_patent',
            'charset': 'utf8'
        }
    elif (hostname == 'DESKTOP-1KULHVO'):
        config = {
            'user': 'root',
            'password': '',
            'host': 'localhost',
            'database': 'brapci_patent',
            'charset': 'utf8'
        }
    else:
        config = {
            'user': 'root',
            'password': '',
            'host': '127.0.0.1',
            'database': 'brapci_patent',
            'charset': 'utf8'
        }
    return config

def codec():
    return True
