def rail_fence(texto, linhas):
    """
    Criptografa uma mesagem desejada, utilizando transposição por Rail Fence.

    Parâmetros:
    - texto: a mensagem original.
    - linhas: em quantas linhas a mensagem será dividida.

    Retorna:
    - ciphertext: a mensagem cifrada.
    """

    lista = ["" for _ in range(linhas)] 
    texto = texto.replace(" ", "").upper()
    ciphertext = ""
    counter = 0
    ida_volta = True

    for letra in texto:
        lista[counter] += letra 
        
        counter, ida_volta = ida_ou_volta(counter, linhas, ida_volta)

    for linha in lista:
        ciphertext += linha

    return ciphertext    


def ida_ou_volta(counter, linhas, ida_volta):
    """
    Define se a contagem de letras está indo ou voltando.

    Parâmetros:
    - counter: index da lista.
    - linhas: quantidade de rails.
    - ida_volta: True se está indo, False se está voltando.

    Retorna:
    - counter: o próximo index da lista.
    - ida_volta: se está indo ou voltando.
    """

    # Diagonal avançando.
    if ida_volta:
        counter += 1
    # Diagonal retornando.    
    else:    
        counter -= 1

    # Ao chegar na base volta uma linha
    if counter == linhas:
        counter -= 2
        ida_volta = False 
    # Ao chegar no teto volta uma linha      
    if counter == -1:
        counter += 2
        ida_volta = True    

    return counter, ida_volta


def quebra_cifra(texto, max_linhas:int):
    """
    Decifra uma mensagem criptografada por Rail Fence.

    Parâmetros:
    - texto: a mensagem cifrada.
    - max_linhas: máximo de linhas consideradas para decifrar.

    Retorna:
    - Uma lista com as possíveis mensagens e seus respectivos rails.
    """


    possiveis_mensagens = []

    if len(texto) < max_linhas:
        max_linhas = len(texto)

    for linha in range(2, max_linhas):
        lista = tamanho_linhas(texto, linha)
        ciphertext = separa_texto(texto, lista)
        plaintext = decifra_rail(ciphertext, linha)
        possiveis_mensagens.append((linha, plaintext))

    return possiveis_mensagens


def tamanho_linhas(texto, linhas):
    """
    Descobre quantas letras tem em cada linha cifrada.

    Parâmetros:
    - texto: o texto cifrado.
    - linhas: quantidade de rails.

    Retorna:
    - lista: cada item da lista é um número que aponta quantas letras ela possui.
    """

    lista = [0 for _ in range(linhas)] 
    texto = texto.replace(" ", "")
    counter = 0
    ida_volta = True

    for letra in texto:
        lista[counter] += 1
        
        counter, ida_volta = ida_ou_volta(counter, linhas, ida_volta)   

    return lista


def separa_texto(texto, lista):
    """
    Divide o texto em uma lista com quantidade de letras diferentes pra cada index.

    Parâmetros:
    - texto: a mensagem cifrada.
    - lista: aponta qual a quantidade de letra pra cada index.

    Retorna:
    - texto_separado: uma lista com letras em cada item.
    """

    texto_separado = ["" for _ in range(len(lista))]
    counter = 0
    idx = 0

    for letra in texto:
        if lista and (counter == lista[0]):
            counter = 0
            idx += 1
            del lista[0]

        texto_separado[idx] += letra
        counter += 1

    return texto_separado


def decifra_rail(texto_separado, linhas):
    """
    Decifra um ciphertext à partir da quantidade de rails usada pra criptografar.

    Parâmetros:
    - texto_separado: o texto cifrado separado em linhas.
    - linhas: a quantidade de rails.

    Retorna:
    - plaintext: a mensagem original
    """

    tamanho_texto = sum(len(t) for t in texto_separado)
    plaintext = ""
    counter = 0
    ida_volta = True 

    for letra in range(tamanho_texto):
        letra, texto_separado[counter] = pop(texto_separado[counter])
        plaintext += letra
        
        counter, ida_volta = ida_ou_volta(counter, linhas, ida_volta)

    return plaintext        


def pop(string):
    """
    Remove e retorna o primeiro caractere de uma string.

    Parâmetros:
    - string: a string a ser manipulada

    Retorna:
    - primeiro_caractere: primeiro caractere da string 
    - nova_string: string sem o primeiro item
    """

    if string:
        primeiro_caractere = string[0]
        nova_string = string[1:]
        return primeiro_caractere, nova_string
    else:
        return '', string
    



def main():
    """
    Função principal que coleta entradas do usuário e chama as funções do programa.
    """

    while True:
        # Menu
        print("==============================================================================================================")
        print("Digite (1) para criptografar uma mensagem com a técnica Rail Fence.")
        print("Digite (2) para descriptografar uma mensagem.")
        print("Digite (3) para encerrar.")
        opcao = int(input("Escolha uma das opções acima: "))
        
        match opcao:
            # Criptografar mensagem.
            case 1:
                print("==============================================================================================================")
                mensagem = input("Digite a mensagem: ")
                linhas = int(input("Digite a quantidade de linhas: "))
                ciphertext = rail_fence(mensagem, linhas)
                print(f"A mensagem criptografada é: {ciphertext}")
                input("Digite (0) para voltar ao menu: ")
            
            # Descriptograr mensagem.
            case 2:
                print("==============================================================================================================")
                ciphertext = input("Digite o texto cifrado: ")
                max_rails = int(input("Digite o máximo de Rails que serão testadas; "))
                print("As possíveis mensagens originais são: ")
                print(*quebra_cifra(ciphertext, max_rails + 1), sep="\n|\n")
                input("Digite (0) para voltar ao menu: ")
            
            # Encerrar programa.
            case 3:
                print("==============================================================================================================")
                print("Programa encerrado =)")
                break

            # Caso de resposta inválida.    
            case _:
                print("==============================================================================================================")
                print("Você deve escolher entre (1), (2) ou (3). Tente novamente!")
                input("Digite (0) para voltar ao menu: ")

main()

