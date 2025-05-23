import datetime

menu_inicial = """[l] Fazer Login
[2] Criar um Usuário
[3] Criar uma Conta Corrente
[4] Entrar como Administrador
[q] Sair

Insira uma opção => """

menu_principal = """[d] depositar
[s] Sacar
[e] Extrato
[q] Sair

Insira Letra => """

saldo = 0
extrato_bancario = ""
numero_saques = 0
LIMITE = 500
LIMITE_SAQUES = 3

numAgencia = "0001"

MSG_NEGATIVO = "Insira um valor positivo!"
MSG_SALDO_INSUF = "Saldo Insuficiente!"
MSG_SALDO_LIMITE = "Valor superior ao Limite de Saque!"
MSG_SALDO_LIMITE_DIARIO = "Total de Saques Diários Atingido!"

contas_secao = dict()
contasCorrente_secao = dict()

# <----------- Funções para checagem ----------->
def imprimirErro(msgTipo, msgErro):
    print("\n" + f" {msgTipo} não realizado(a)! ".center(50, "="))
    print(f" {msgErro} ".center(50, "="))
    input("Pressione enter para continuar...")

def checarNegativo(input, msgTipo):
    if input < 1:
        imprimirErro(msgTipo, MSG_NEGATIVO)
        return True
    else:
        return False

def checarCPFExistente(CPF, mostrarMsg, msgErro):
    CPFsRegistrados = list(contas_secao.keys())

    for chave in CPFsRegistrados:
        if CPF == chave:
            if mostrarMsg == True:
                imprimirErro(msgErro, "CPF já cadastrado!")
            return True
        
    return False

# <----------- Funções para Montar Strings ----------->
def montarExtrato(msgTipo, sinal, saldo):
    if msgTipo == "Saque":
        return f"{msgTipo}:\t\t\t {sinal} R$ {saldo:.2f}\n"
    else:
        return f"{msgTipo}:\t\t {sinal} R$ {saldo:.2f}\n"

def criarTela(msg1, msg2):

    print(f"""

    +-----------------------+
    |                       |  
    |{msg1.center(23, " ")}|
    |{msg2.center(23, " ")}|
    |                       |
    +-----------------------+
""")

# <----------- Funções de funcionalidades ----------->
def deposito(saldo, extrato):

    valor = float(input("\nInsira o valor à se depositar: "))
    
    if checarNegativo(valor, "Depósito"):
        return saldo, extrato

    saldo += valor
    extrato += montarExtrato("Depósito", "+", valor)
    print("\n" + "Extrato realizado com sucesso!".center(50, "="))
    print(f" Novo Saldo: R$ {saldo: .2f} ".center(50, "="))
    input("Pressione enter para continuar...")

    return saldo, extrato

def saque(saldo=saldo, extrato=extrato_bancario, numero_saques=numero_saques):

    checarLimiteSaques = numero_saques >= LIMITE_SAQUES

    if checarLimiteSaques:
        imprimirErro("Saque", MSG_SALDO_LIMITE_DIARIO)
        return saldo, extrato, numero_saques

    print(f" Regras de Saque ".center(50, "="))
    print("""
 - O valor sacado não deve ser superior ao seu saldo.
 - O valor sacado não deve ser superior a R$ 500,00.
 - Só é possível sacar 3 vezes por dia.
    """)
    print("".center(50, "="))
    print(f"\nVocê fez {numero_saques} Saques!\n")

    valor = float(input("\nInsira o valor à se sacar: "))

    checarSaldo = valor > saldo
    checarLimiteSaque = valor > LIMITE

    if checarNegativo(valor, "Saque"):
        return saldo, extrato, numero_saques
    
    if checarSaldo:
        imprimirErro("Saque", MSG_SALDO_INSUF)
        return saldo, extrato, numero_saques
    
    if checarLimiteSaque:
        imprimirErro("Saque", MSG_SALDO_LIMITE)
        return saldo, extrato, numero_saques
        
    
    saldo -= valor
    extrato += montarExtrato("Saque", "-", valor)
    numero_saques += 1

    print("\n" + "Saque realizado com sucesso!".center(50, "="))
    print(f" Novo Saldo: R$ {saldo:.2f} ".center(50, "="))
    input("Pressione enter para continuar...")

    return saldo, extrato, numero_saques

def extrato(saldo, extrato_bancario=extrato_bancario):
    print("\n" + " Extrato Bancário ".center(50, "="))
    if not extrato_bancario:
        print("Não foram realizadas movimentações.".center(50," "))
    else:
        print(extrato_bancario)
        print(f"Saldo: R$ {saldo:.2f}")
    print("".center(50,"="))
    input("Pressione enter para continuar...")

# <----------- Funções de Criação de Conta ----------->
def criarUsuario():
    criarTela("Registrar", "Usuário")

    nome = input("Insira seu nome completo: ").title()
    dataNascimento = input("Insira sua data de nascimento (DD/MM/AAAA): ")
    dataNascimentoFormat = datetime.datetime.strptime(dataNascimento, "%d/%m/%Y")
    CPF = input("Insira seu CPF (apenas números): ")

    if(checarCPFExistente(CPF, True, "Cadastro de Usuário")):
        return

    logradouro = input("Insira sua Rua/Logradouro: ")
    bairro = input("Insira seu Bairro: ")
    cidade = input("Insira sua Cidade: ")
    estado = input("Insira a Sigla do seu Estado: ")

    endereco = f"{logradouro}, {bairro}, {cidade}/{estado}"

    contas_secao[CPF] = {
        "nome": nome,
        "dataNascimento": dataNascimentoFormat.date(),
        "endereco": endereco
    }

    print(f"""
          
    Nome: {nome}
    Data de Nascimento: {dataNascimento}
    CPF: {CPF}
    Endereço: {endereco}

    """)
    
    input("Pressione enter para continuar...")  

def criarContaCorrente():
    criarTela("Registrar", "Conta Corrente")
    CPF = input("Insira o CPF da conta: ")

    if not (checarCPFExistente(CPF, False, "Cadastro da Conta Corrente")):
        return

    contaCorr = {"Agencia" : numAgencia, "CPF" : CPF}

    if contasCorrente_secao == {}:
        numContaCorr = 1
    else:
        numContaCorr = list(contasCorrente_secao.keys())[-1] + 1

    while True:

        print(f"Deseja criar a conta corrente {numContaCorr} na Agência {numAgencia} no CPF: {CPF}?")
        print("[s] Sim\n[n] Não\n")
        resposta = input("==>").lower()

        if resposta == "s":
            contasCorrente_secao[numContaCorr] = contaCorr
            print("\nConta Corrente criada com sucesso!")
            input("Pressione enter para continuar...")
            return
        elif resposta == "n":
            print("Retornado ao menu...")
            input("Pressione enter para continuar...")
            return
        else:
            print("Insira uma letra válida!\n\n")

#def menuPrincipal():
#    while True:
#
#        criarTela("Deky Bank", "Conta: A1")
#        opcao = input(menu_principal).lower()
#
#        if opcao == "d":
#            saldo, extrato_bancario = deposito(saldo, extrato_bancario)
#        elif opcao == "s":
#            saldo, extrato_bancario, numero_saques = saque(saldo, extrato_bancario, numero_saques)
#        elif opcao == "e":
#            extrato(saldo, extrato_bancario)
#        elif opcao == "q":
#            print("\nAté logo!")
#            input("Pressione enter para continuar...")       
#            break
#        else:
#            print("\nOperação inválida, por favor selecione novamente a operação desejada.")
#            input("Pressione enter para continuar...")

while True:

    criarTela("Deky Bank", "Bem-vindo")
    opcao = input(menu_inicial).lower()

    if opcao == "1":
        print("Fazer Login...")
    elif opcao == "2":
        criarUsuario()
    elif opcao == "3":
        criarContaCorrente()
    elif opcao == "4":
        print("Entrar como Administrador...")
    elif opcao == "q":
        print("\nAté logo!")
        input("Pressione enter para continuar...")       
        break
    else :
       print("\nOperação inválida, por favor selecione novamente a operação desejada.")
       input("Pressione enter para continuar...") 





