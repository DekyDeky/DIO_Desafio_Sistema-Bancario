from src import LIMITE_SAQUES, MSG_SALDO_LIMITE_DIARIO, MSG_SALDO_INSUF, MSG_SALDO_LIMITE, LIMITE, LIMITE_TRANSFERENCIA, NUM_AGENCIA, CONTASCORRENTS_DIR
from src import carregarJSON
from utils import imprimirErro, pegarHoje
from utils import checarNegativo

def deposito(saldo, extrato, token):

    valor = float(input("\nInsira o valor à se depositar: "))
    
    if checarNegativo(valor, "Depósito"):
        return saldo, extrato

    saldo += valor
    extrato.update({pegarHoje() : {"Sessao" : token, "Deposito" : f"+{saldo}"} })
    print("\n" + "Extrato realizado com sucesso!".center(50, "="))
    print(f" Novo Saldo: R$ {saldo: .2f} ".center(50, "="))
    input("Pressione enter para continuar...")

    return saldo, extrato

def saque(*, saldo, extrato, numero_saques, token):

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
    extrato.update({pegarHoje() : { "Sessao" : token, "Saque" : f"-{valor}"}})
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
        for chave, valor in extrato_bancario.items():
            for move, quant in valor.items():
                if move == "Transferencia":
                    print(f"-> {chave} | {move} : R$ {quant['valor']} | {quant['remetente']} -> {quant['destinatario']}")
                elif move == "Deposito" or move == "Saque":
                    print(f"-> {chave} | {move} : R$ {quant}")
            
        print(f"Saldo: R$ {saldo:.2f}")
    print("".center(50,"="))
    input("Pressione enter para continuar...")

def transferencia(saldo, extrato_bancario, totalTransferencias, numConta, token):
    
    checarLimite = totalTransferencias > LIMITE_TRANSFERENCIA
    if checarLimite:
        imprimirErro("Transferência", "Limite de Transferências diárias atingido!")
        return saldo, extrato_bancario, totalTransferencias

    agenciaTransf = input("Insira o número de Agência da conta: ")

    if agenciaTransf != NUM_AGENCIA:
        imprimirErro("Transferência", "Agência Desconhecida!")
        return saldo, extrato_bancario, totalTransferencias

    contaTransf = input("Insira o número da conta que deseja transferir: ")

    contasCorrentes = carregarJSON(CONTASCORRENTS_DIR)

    if not str(contaTransf) in list(contasCorrentes.keys()):
        imprimirErro("Transferência", "Conta não encontrada!")
        return saldo, extrato_bancario, totalTransferencias

    if contaTransf == numConta:
        imprimirErro("Transferência", "Não é possível transferir para si mesmo!")
        return saldo, extrato_bancario, totalTransferencias

    valor = float(input("Insira o valor a ser transferido: "))
    
    checarSaldo = valor > saldo
    if(checarNegativo(valor, "transferência")):
        return saldo, extrato_bancario, totalTransferencias
    
    if checarSaldo:
        imprimirErro("Saque", MSG_SALDO_INSUF)
        return saldo, extrato, totalTransferencias
    
    print(f"\n Deseja fazer uma transferência de {valor:.2f} para a conta {NUM_AGENCIA} - {contaTransf}?")

    while True:
        resposta = input("[s] Sim \n[n] Não \n=>").lower()

        if resposta == 'n': 
            imprimirErro("Transferência", "Transferência cancelada")
            return saldo, extrato_bancario, totalTransferencias
        elif resposta == 's':
            saldo -= valor
            extrato_bancario.update({pegarHoje() : { 
               "Transferencia" : {   
                    "valor" : valor, 
                    "remetente" : numConta,
                    "destinatario" : contaTransf,
                    "sessao" : token
                   }}}) 
            totalTransferencias += 1

            print("\n" + "Transferência realizada com sucesso!".center(50, "="))
            print(f" Novo Saldo: R$ {saldo:.2f} ".center(50, "="))
            input("Pressione enter para continuar...")

            return saldo, extrato_bancario, totalTransferencias
        
        else:
            print("\n Insira um valor válido! \n")   