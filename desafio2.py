import os, json, platform
from datetime import datetime

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

numAgencia = "0001"

MSG_NEGATIVO = "Insira um valor positivo!"
MSG_SALDO_INSUF = "Saldo Insuficiente!"
MSG_SALDO_LIMITE = "Valor superior ao Limite de Saque!"
MSG_SALDO_LIMITE_DIARIO = "Total de Saques Diários Atingido!"

LIMITE = 500
LIMITE_SAQUES = 10

CONTASCORRENTS_DIR = './db/contasCorrentes.json'
USUARIOS_DIR = './db/usuarios.json'

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

def checarCPFExistente(CPF, mostrarMsg, cadastrado, msgErro):
    with open('./db/usuarios.json') as usuarios:
        if(os.path.getsize('./db/usuarios.json') == 0):
            return False
        
        contasDict = json.load(usuarios)

        for chave in contasDict.keys():
            if CPF == chave:
                if mostrarMsg and cadastrado:
                    imprimirErro(msgErro, "CPF já cadastrado!")
                return True
   
    if mostrarMsg and not cadastrado:
        imprimirErro(msgErro, "CPF não cadastrado!")
    return False    

def resetarSaquesDiarios(extrato, saques_diarios):
    ultimaData = datetime.strptime(list(extrato.keys())[-1], "%d/%m/%Y %H:%M:%S")
    if ultimaData.date() < datetime.today().date(): return 0
    else: return saques_diarios

# <----------- Funções para JSON ----------->
def carregarJSON(caminho):
    with open(caminho, "r") as f:
        if(os.path.getsize(caminho) > 0):
            return json.load(f)
        else: return {}

def escreverJSON(caminho, dict):
    with open(caminho, 'w') as f:
        json.dump(dict, f, indent=4)

# <----------- Funções para Montar Strings ----------->
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

# <----------- Funções de funcionalidades ----------->
def deposito(saldo, extrato):

    valor = float(input("\nInsira o valor à se depositar: "))
    
    if checarNegativo(valor, "Depósito"):
        return saldo, extrato

    saldo += valor
    extrato.update({pegarHoje() : {"Deposito" : f"+{saldo}"} })
    print("\n" + "Extrato realizado com sucesso!".center(50, "="))
    print(f" Novo Saldo: R$ {saldo: .2f} ".center(50, "="))
    input("Pressione enter para continuar...")

    return saldo, extrato

def saque(*, saldo, extrato, numero_saques):

    checarLimiteSaques = numero_saques >= LIMITE_SAQUES

    if checarLimiteSaques:
        imprimirErro("Saque", MSG_SALDO_LIMITE_DIARIO)
        return saldo, extrato, numero_saques

    print(f" Regras de Saque ".center(50, "="))
    print("""
 - O valor sacado não deve ser superior ao seu saldo.
 - O valor sacado não deve ser superior a R$ 500,00.
 - Só é possível sacar 10 vezes por dia.
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
    extrato.update({pegarHoje() : { "Saque" : f"-{valor}"}})
    #extrato += montarExtrato("Saque", "-", valor)
    numero_saques += 1

    print("\n" + "Saque realizado com sucesso!".center(50, "="))
    print(f" Novo Saldo: R$ {saldo:.2f} ".center(50, "="))
    input("Pressione enter para continuar...")

    return saldo, extrato, numero_saques

def extrato(saldo, /, *, extrato_bancario):
    print("\n" + " Extrato Bancário ".center(50, "="))
    if not extrato_bancario:
        print("Não foram realizadas movimentações.".center(50," "))
    else:
        #print(extrato_bancario)
        for chave, valor in extrato_bancario.items():
            for move, quant in valor.items():
                print(f"-> {chave} | {move} : {quant}")
            
        print(f"Saldo: R$ {saldo:.2f}")
    print("".center(50,"="))
    input("Pressione enter para continuar...")

# <----------- Funções de Conta ----------->
def criarContaCorrente(CPF):
    contaCorr = {"Agencia" : numAgencia, "CPF" : CPF, "Saldo" : 0, "Extrato" : {}, "Saques_Diarios" : 0}
    dictJson = carregarJSON('./db/contasCorrentes.json')

    if dictJson == {}:
        numContaCorr = 1
    else:
        numContaCorr = int(list(dictJson.keys())[-1]) + 1

    while True:

        print(f"Deseja criar a conta corrente {numContaCorr} na Agência {numAgencia} no CPF: {CPF}?")
        print("[s] Sim\n[n] Não\n")
        resposta = input("==>").lower()

        if resposta == "s":
            dictJson[numContaCorr] = contaCorr
            escreverJSON('./db/contasCorrentes.json', dictJson)
            print("\nConta Corrente criada com sucesso!")
            input("Pressione enter para continuar...")
            break
        elif resposta == "n":
            print("Criação da conta corrente cancelada!")
            input("Pressione enter para continuar...")
            break
        else:
            print("Insira uma letra válida!\n\n")

def criarContaCorrenteManual():
    criarTela("Registrar", "Conta Corrente")
    CPF = input("Insira o CPF da conta: ")

    if not (checarCPFExistente(CPF, True, False, "Cadastro da Conta Corrente")):
        return

    criarContaCorrente(CPF)

def criarUsuario():
    criarTela("Registrar", "Usuário")

    nome = input("Insira seu nome completo: ").title()
    dataNascimento = input("Insira sua data de nascimento (DD/MM/AAAA): ")
    CPF = input("Insira seu CPF (apenas números): ")

    if(checarCPFExistente(CPF, True, True, "Cadastro de Usuário")):
        return

    logradouro = input("Insira sua Rua/Logradouro: ")
    bairro = input("Insira seu Bairro: ")
    cidade = input("Insira sua Cidade: ")
    estado = input("Insira a Sigla do seu Estado: ")

    endereco = f"{logradouro}, {bairro}, {cidade}/{estado}"

    print(f"""
          
    Nome: {nome}
    Data de Nascimento: {dataNascimento}
    CPF: {CPF}
    Endereço: {endereco}

    """)

    print("Deseja criar este usuário?")
    print("[s] Sim\n[n] Não\n")
    resposta = input("==>").lower()

    while True:
        if resposta == 'n':
            print("Retornado ao menu...")
            input("Pressione enter para continuar...")
            return
        elif resposta == 's':
            jsonDict = carregarJSON('./db/usuarios.json')

            jsonDict[CPF] = {
                                "nome": nome,
                                "dataNascimento": dataNascimento,
                                "endereco": endereco
                            }

            escreverJSON('./db/usuarios.json', jsonDict) 

            print("\nUsuário criado com sucesso!")

            criarContaCorrente(CPF)
            
            return
        else:
            print("Insira uma letra válida!\n\n") 

def menuPrincipal(Usuario, contaAtual):

    saldo = contaAtual["Saldo"]
    extrato_bancario = contaAtual["Extrato"]
    numero_saques = resetarSaquesDiarios(contaAtual["Extrato"], contaAtual["Saques_Diarios"])
    
    while True:

        limparTela()

        criarTela("Deky Bank", Usuario)
        opcao = input(menu_principal).lower()

        if opcao == "d":
            limparTela()
            saldo, extrato_bancario = deposito(saldo, extrato_bancario)
        elif opcao == "s":
            limparTela()
            saldo, extrato_bancario, numero_saques = saque(saldo=saldo, extrato=extrato_bancario, numero_saques=numero_saques)
        elif opcao == "e":
            limparTela()
            extrato(saldo, extrato_bancario=extrato_bancario)
        elif opcao == "q":
            print("\nAté logo!")
            input("Pressione enter para continuar...")       
            return saldo, extrato_bancario, numero_saques
        else:
            print("\nOperação inválida, por favor selecione novamente a operação desejada.")
            input("Pressione enter para continuar...")

def fazerLogin():
    criarTela("Deky Bank", "Login")
    CPF = input("Insira seu CPF: ")

    if not (checarCPFExistente(CPF, True, False, "Login")):
        return

    contasCorrentesSessao = []
    numContas = 0
    stringMenu = ""

    contasCorrentes = carregarJSON(CONTASCORRENTS_DIR)
    
    for chave in contasCorrentes:
        if contasCorrentes[chave]["CPF"] == CPF:
            contasCorrentesSessao.append(contasCorrentes[chave])
            numContas += 1
            chaveAtual = chave
            stringMenu += f"[{numContas}] {numAgencia} - {chave}\n"

    if contasCorrentes == {}:
        imprimirErro("Login", "O usuário não possui Conta Corrente")
        return
    
    print(f"Logando em {CPF}...")
    input("Pressione enter para continuar...") 

    limparTela()

    if len(contasCorrentesSessao) > 1:
        criarTela("Deky Bank", "Contas Correntes")
        print(stringMenu)
        SelecaoAtual = input("Selecione uma conta corrente: ")
        contaAtual = contasCorrentesSessao[int(SelecaoAtual)-1]
    elif len(contasCorrentesSessao) == 1:
        contaAtual = contasCorrentesSessao[0]

    usuarioAtual = carregarJSON(USUARIOS_DIR)[CPF]

    resultadoSaldo, resultadoExtrato, resultadoNumero_Saques = menuPrincipal(usuarioAtual["nome"], contaAtual)

    contaAtual["Saldo"] = resultadoSaldo
    contaAtual["Extrato"] = resultadoExtrato
    contaAtual["Saques_Diarios"] = resultadoNumero_Saques

    contasCorrentes[chaveAtual] = contaAtual

    escreverJSON(CONTASCORRENTS_DIR, contasCorrentes)


# <----------- Menu Inicial ----------->
while True:

    limparTela()

    criarTela("Deky Bank", "Bem-vindo")
    opcao = input(menu_inicial).lower()

    if opcao == "1":
        limparTela()
        fazerLogin()
    elif opcao == "2":
        limparTela()
        criarUsuario()
    elif opcao == "3":
        limparTela()
        criarContaCorrenteManual()
    elif opcao == "4":
        print("Entrar como Administrador...")
    elif opcao == "q":
        print("\nAté logo!")
        input("Pressione enter para continuar...")       
        break
    else :
       print("\nOperação inválida, por favor selecione novamente a operação desejada.")
       input("Pressione enter para continuar...") 