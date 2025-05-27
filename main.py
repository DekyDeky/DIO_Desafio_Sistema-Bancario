from src import login
from src import contas
from utils import limparTela, criarTela

menu_inicial = """[l] Fazer Login
[2] Criar um Usuário
[3] Criar uma Conta Corrente
[4] Entrar como Administrador
[q] Sair

Insira uma opção => """

# <----------- Menu Inicial ----------->
while True:

    limparTela()

    criarTela("Deky Bank", "Bem-vindo")
    opcao = input(menu_inicial).lower()

    if opcao == "1":
        limparTela()
        login.fazerLogin()
    elif opcao == "2":
        limparTela()
        contas.criarUsuario()
    elif opcao == "3":
        limparTela()
        contas.criarContaCorrenteManual()
    elif opcao == "4":
        print("Entrar como Administrador...")
    elif opcao == "q":
        print("\nAté logo!")
        input("Pressione enter para continuar...")       
        break
    else :
       print("\nOperação inválida, por favor selecione novamente a operação desejada.")
       input("Pressione enter para continuar...") 