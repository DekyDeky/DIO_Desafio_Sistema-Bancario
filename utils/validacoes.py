import os, json
from datetime import datetime

MSG_NEGATIVO = "Insira um valor positivo!"

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
    if extrato == {}:
        return 0
    else:
        ultimaData = datetime.strptime(list(extrato.keys())[-1], "%d/%m/%Y %H:%M:%S")
        if ultimaData.date() < datetime.today().date(): return 0
        else: return saques_diarios