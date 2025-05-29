from src import carregarJSON, escreverJSON
from src import NUM_AGENCIA
from utils import criarTela
from utils import checarCPFExistente

def criarContaCorrente(CPF):
    contaCorr = {"Agencia" : NUM_AGENCIA, "CPF" : CPF, "Saldo" : 0, "Extrato" : {}, "Saques_Diarios" : 0, "Transf_Diarias" : 0}
    dictJson = carregarJSON('./db/contasCorrentes.json')

    if dictJson == {}:
        numContaCorr = 1
    else:
        numContaCorr = int(list(dictJson.keys())[-1]) + 1

    while True:

        print(f"Deseja criar a conta corrente {numContaCorr} na Agência {NUM_AGENCIA} no CPF: {CPF}?")
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