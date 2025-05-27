import json, os

def carregarJSON(caminho):
    with open(caminho, "r") as f:
        if(os.path.getsize(caminho) > 0):
            return json.load(f)
        else: return {}

def escreverJSON(caminho, dict):
    with open(caminho, 'w') as f:
        json.dump(dict, f, indent=4)