menu = """

+-----------------------+
|                       |  
|       Deky Bank       |
|       Conta: A1       |
|                       |
+-----------------------+

[d] depositar
[s] Sacar
[e] Extrato
[q] Sair

Insira Letra => """


saldo = 0
extrato_bancario = ""
numero_saques = 0
LIMITE = 500
LIMITE_SAQUES = 3

MSG_NEGATIVO = "Insira um valor positivo!"
MSG_SALDO_INSUF = "Saldo Insuficiente!"
MSG_SALDO_LIMITE = "Valor superior ao Limite de Saque!"
MSG_SALDO_LIMITE_DIARIO = "Total de Saques Diários Atingido!"

def imprimirErro(msgTipo, msgErro):
    print("\n" + f" {msgTipo} não realizado! ".center(50, "="))
    print(f" {msgErro} ".center(50, "="))
    input("Pressione enter para continuar...")

def checarNegativo(input, msgTipo):
    if input < 1:
        imprimirErro(msgTipo, MSG_NEGATIVO)
        return True
    else:
        return False

def montarExtrato(msgTipo, sinal, saldo):
    if msgTipo == "Saque":
        return f"{msgTipo}:\t\t\t {sinal} R$ {saldo:.2f}\n"
    else:
        return f"{msgTipo}:\t\t {sinal} R$ {saldo:.2f}\n"

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

def saque(saldo, extrato, numero_saques):

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

def extrato(saldo, extrato_bancario):
    print("\n" + " Extrato Bancário ".center(50, "="))
    if not extrato_bancario:
        print("Não foram realizadas movimentações.".center(50," "))
    else:
        print(extrato_bancario)
        print(f"Saldo: R$ {saldo:.2f}")
    print("".center(50,"="))
    input("Pressione enter para continuar...")

while True:

    opcao = input(menu).lower()

    if opcao == "d":
        saldo, extrato_bancario = deposito(saldo, extrato_bancario)
    elif opcao == "s":
        saldo, extrato_bancario, numero_saques = saque(saldo, extrato_bancario, numero_saques)
    elif opcao == "e":
        extrato(saldo, extrato_bancario)
    elif opcao == "q":
        print("\nAté logo!")
        input("Pressione enter para continuar...")       
        break
    else:
        print("\nOperação inválida, por favor selecione novamente a operação desejada.")
        input("Pressione enter para continuar...")