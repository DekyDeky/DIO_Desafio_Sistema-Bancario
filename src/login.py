from utils import resetarSaquesDiarios, criarTela, limparTela, checarCPFExistente, imprimirErro
from src import carregarJSON, escreverJSON
from src import CONTASCORRENTS_DIR, NUM_AGENCIA, USUARIOS_DIR
from src import funcionalidades

MENU_PRINCIPAL = """[d] depositar
[s] Sacar
[e] Extrato
[t] Transferência
[q] Sair

Insira Letra => """

def menuPrincipal(Usuario, contaAtual, numConta):

    saldo = contaAtual["Saldo"]
    extrato_bancario = contaAtual["Extrato"]
    numero_saques = resetarSaquesDiarios(contaAtual["Extrato"], contaAtual["Saques_Diarios"])
    totalTransferencias = 0
    
    while True:
        limparTela()

        criarTela("Deky Bank", Usuario)
        opcao = input(MENU_PRINCIPAL).lower()

        if opcao == "d":
            limparTela()
            saldo, extrato_bancario = funcionalidades.deposito(saldo, extrato_bancario)
        elif opcao == "s":
            limparTela()
            saldo, extrato_bancario, numero_saques = funcionalidades.saque(saldo=saldo, extrato=extrato_bancario, numero_saques=numero_saques)
        elif opcao == "e":
            limparTela()
            funcionalidades.extrato(saldo, extrato_bancario=extrato_bancario)
        elif opcao == "t":
            limparTela()
            saldo, extrato_bancario, totalTransferencias = funcionalidades.transferencia(saldo, extrato_bancario, totalTransferencias, numConta)
        elif opcao == "q":
            print("\nAté logo!")
            input("Pressione enter para continuar...")       
            return saldo, extrato_bancario, numero_saques, totalTransferencias
        else:
            print("\nOperação inválida, por favor selecione novamente a operação desejada.")
            input("Pressione enter para continuar...")

def fazerLogin():
    criarTela("Deky Bank", "Login")
    CPF = input("Insira seu CPF: ")

    if not (checarCPFExistente(CPF, True, False, "Login")):
        return

    contasCorrentesSessao = []
    numContasCorren = []
    numContas = 0
    stringMenu = ""

    contasCorrentes = carregarJSON(CONTASCORRENTS_DIR)
    
    for chave in contasCorrentes:
        if contasCorrentes[chave]["CPF"] == CPF:
            contasCorrentesSessao.append(contasCorrentes[chave])
            numContasCorren.append(chave)
            numContas += 1
            chaveAtual = chave
            stringMenu += f"[{numContas}] {NUM_AGENCIA} - {chave}\n"

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
        numContaAtual = numContasCorren[int(SelecaoAtual)-1]
    elif len(contasCorrentesSessao) == 1:
        contaAtual = contasCorrentesSessao[0]
        numContaAtual = numContasCorren[0]

    usuarioAtual = carregarJSON(USUARIOS_DIR)[CPF]

    resultadoSaldo, resultadoExtrato, resultadoNumero_Saques, totalTransferencias = menuPrincipal(usuarioAtual["nome"], contaAtual, numContaAtual)

    contaAtual["Saldo"] = resultadoSaldo
    contaAtual["Extrato"] = resultadoExtrato
    contaAtual["Saques_Diarios"] = resultadoNumero_Saques
    contaAtual["Transf_Diarias"] = totalTransferencias

    contasCorrentes[chaveAtual] = contaAtual

    escreverJSON(CONTASCORRENTS_DIR, contasCorrentes)