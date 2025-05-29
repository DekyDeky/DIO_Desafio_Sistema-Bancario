import platform, os, random, string
from datetime import datetime

def limparTela():
    sistema = platform.system()
    if sistema == 'Windows':
        os.system('cls')
    elif sistema == 'Linux':
        os.system('clear')

def criarTela(msg1, msg2):

    print(f"""

    +-----------------------+
    |                       |  
    |{msg1.center(23, " ")}|
    |{msg2.center(23, " ")}|
    |                       |
    +-----------------------+
""")

def pegarHoje():
    hoje = datetime.today()
    return hoje.strftime("%d/%m/%Y %H:%M:%S")

def gerarToken():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))