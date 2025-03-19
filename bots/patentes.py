from colorama import Fore
import socket, os, sys

def logo():
    versao = '0.25.03.19'
    print(" "+Fore.YELLOW)
    print("██████╗  █████╗ ████████╗███████╗███╗   ██╗████████╗███████╗███████╗")
    print("██╔══██╗██╔══██╗╚══██╔══╝██╔════╝████╗  ██║╚══██╔══╝██╔════╝██╔════╝")
    print("██████╔╝███████║   ██║   █████╗  ██╔██╗ ██║   ██║   █████╗  ███████╗")
    print("██╔═══╝ ██╔══██║   ██║   ██╔══╝  ██║╚██╗██║   ██║   ██╔══╝  ╚════██║")
    print("██║     ██║  ██║   ██║   ███████╗██║ ╚████║   ██║   ███████╗███████║")
    print("╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚══════╝"+Fore.WHITE)
    print("Base de dados de patentes do INPI - BOTs - Versão",versao)
    print(" ")

def auto():
    print("Sem parâmetros, use")
    print(Fore.YELLOW+"   python patentes.py help"+Fore.WHITE)
    print(" ")

if __name__ == '__main__':
    logo()

    hostname = socket.gethostname()
    if (hostname == 'DESKTOP-M0Q0TD7'):
        diretorio = os.getcwd()
    else:
        diretorio = '/data/Brapci3.1/bots/ROBOTi'

    print("Diretório", diretorio)
    os.chdir(diretorio)

    if (len(sys.argv) > 1):
        parm = sys.argv
        run(parm)
    else:
        auto()
