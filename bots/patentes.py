from colorama import Fore
import socket, os, sys
import mod_issue_files, mod_rpi

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

################################################################################ RUN
def run(parm):
    if parm[1] == 'help':
        help()
    elif parm[1] == 'issue':
        if len(parm) > 2:
            print("Issue", parm[2])
            ################################################### Limit
            limit = 10  # Valor padrão
            if len(parm) > 3:
                try:
                    limit = int(parm[4])
                except ValueError:
                    print(
                        f"Erro: '{parm[4]}' não é um número válido. Usando limite padrão (10)."
                    )

            if parm[2] in ['files', 'download']:
                for i in range(limit):
                    if len(parm) > 3:
                        mod_issue_files.download(parm[3])
                    else:
                        mod_issue_files.download()

            elif parm[2] == 'recheck':
                mod_rpi.recheck()

        else:
            mod_issue_files.harvesting()
    else:
        auto()

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
