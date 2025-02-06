import sys

def somaNum(n1,operador,n2):
    if operador == '+':
        return n1 + n2
    return n1 - n2

def analiseLexica(string):
    tokens = []
    numeros = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    operadores = ["+", "-"]
    num_atual = ""
    espaco_entre_numeros = False

    for caracter in string:
        if caracter in numeros:
            if espaco_entre_numeros:
                num_atual += " "
            num_atual += caracter
            espaco_entre_numeros = False

        if caracter == " ":
            espaco_entre_numeros = True
        
        if caracter in operadores:
            if num_atual != "":
                tokens.append(num_atual.strip())
                num_atual = ""
            tokens.append(caracter)
            espaco_entre_numeros = False

    if num_atual != "":
        tokens.append(num_atual.strip())

    return tokens

def analiseSemantica(tokens):

    valida = {
        "numero" : 0,
        "operador" : 0
    }
    operadores = ["-", "+"]
    
    for i in range(len(tokens)):
        if tokens[-1] in operadores:
            return False

        if " " in tokens[i]:
            return False
        elif tokens[i] in operadores:
            valida["operador"] += 1
            valida["numero"] = 0
            if valida["operador"] > 1:
                return False
        elif tokens[i] not in operadores and " " not in tokens[i]:
            valida["numero"] += 1
            valida["operador"] = 0
            if valida["numero"] > 1:
                return False
    return True

def calculator(string):

    string = string.strip()
    tokens = analiseLexica(string)
    # print(tokens)
    # print(analiseSemantica(tokens))
    if not analiseSemantica(tokens):
        raise Exception("Entrada invalida")
    soma = int(tokens[0])

    for i in range(1, len(tokens), 2):
        operador = tokens[i]
        numero = int(tokens[i + 1])

        if operador == "+":
            soma += numero
        elif operador == "-":
            soma -= numero

    return soma

if __name__ == "__main__":
    string = sys.argv[1]
    print(calculator(string))