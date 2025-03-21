from colorama import Fore
import socket, os, sys
import mod_issue_files, mod_rpi, mod_sections

def logo():
    versao = '0.25.03.19'
    print(" "+Fore.YELLOW)
    print("██████╗  █████╗ ████████╗███████╗███╗   ██╗████████╗███████╗")
    print("██╔══██╗██╔══██╗╚══██╔══╝██╔════╝████╗  ██║╚══██╔══╝██╔════╝")
    print("██████╔╝███████║   ██║   █████╗  ██╔██╗ ██║   ██║   █████╗  ")
    print("██╔═══╝ ██╔══██║   ██║   ██╔══╝  ██║╚██╗██║   ██║   ██╔══╝  ")
    print("██║     ██║  ██║   ██║   ███████╗██║ ╚████║   ██║   ███████╗ " + Fore.YELLOW + "Lab BR" + Fore.YELLOW)
    print("╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝ " + Fore.YELLOW + "══════" + Fore.WHITE)
    print("Base de dados de patentes do INPI - BOTs - Versão",versao)
    print(" ")

def auto():
    print("Sem parâmetros, use")
    print(Fore.YELLOW+"   python patentes.py help"+Fore.WHITE)
    print(" ")
    fcn = [{'cmd':'checkSystem','desc':'Verificar diretórios'},
           {'cmd':'resume','desc':'Retomar download'},
           {'cmd':'issue','desc':'Processar arquivos'},
           {'cmd':'issue files','desc':'Baixar arquivos'},
           {'cmd':'issue download','desc':'Baixar arquivos'},
           {'cmd':'issue recheck','desc':'Revisar arquivos'},
           {'cmd':'issue unzip','desc':'Descompactar arquivos'}]
    for i in fcn:
        print(i['cmd'] + " - " + i['desc'])

################################################################################ RUN
def run(parm):
    if parm[1] == 'help':
        help()
    elif parm[1] == 'checkSystem':
        mod_issue_files.checkDIR()
    elif parm[1] == 'resume':
        mod_issue_files.resume()
    elif parm[1] == 'issue':
        if len(parm) > 2:
            print("Issue", parm[2])
            ################################################### Limit
            limit = 10  # Valor padrão
            if len(parm) > 4:
                try:
                    limit = int(parm[4])
                except ValueError:
                    print(
                        f"Erro: '{parm[4]}' não é um número válido. Usando limite padrão (10)."
                    )

            if parm[2] in ['files', 'download']:
                loop = 1
                for i in range(limit):
                    if loop == 1:
                        if len(parm) > 3:
                            loop = mod_issue_files.download(parm[3])
                        else:
                            loop = mod_issue_files.download('')
            elif parm[2] == 'process':
                mod_issue_files.process()
            elif parm[2] == 'metadata':
                mod_sections.process()
            elif parm[2] == 'recheck':
                mod_rpi.recheck()
            elif parm[2] == 'unzip':
                mod_issue_files.unzip()
            else:
                print("Comando não encontrado.")
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
        diretorio = '/data/PatentINPI/bots/'

    print("Diretório", diretorio)
    os.chdir(diretorio)

    if (len(sys.argv) > 1):
        parm = sys.argv
        run(parm)
    else:
        auto()
