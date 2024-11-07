from collections import Counter
from itertools import permutations

def transposition_cipher(plaintext, key):
    """
    Cifra uma mensagem usando a técnica de transposição colunar.

    Parâmetros:
    - plaintext: mensagem original.
    - key: palavra chave para criptografar.

    Retorna:
    - ciphertext: mensagem cifrada.
    """

    matriz = [[] for _ in range(len(key))]
    counter = 0
    for letra in plaintext:
        if letra != " ":
            matriz[counter].append(letra.upper())
            counter = (counter + 1) % len(key) 

    matriz = completa_matriz(matriz)    
    matriz = ordena_matriz(matriz, key)

    ciphertext = ""
    for coluna in matriz:
        for letra in coluna:
            ciphertext += letra
        ciphertext += " "

    return ciphertext


def completa_matriz(matriz):
    """
    Preenche os espaços vazios para se tornar uma matriz completa.

    Parâmetros:
    - matriz: matriz que será completada.

    Retorna:
    - matriz: matriz como linhas de mesmo tamanho.
    """

    tamanho = len(matriz[0])
    for coluna in matriz:
        if len(coluna) < tamanho:
            coluna.append("X")
    return matriz        


def ordena_matriz(matriz, key):
    """
    Ordena as colunas da matriz de acordo com a ordenação da chave.

    Parâmetros:
    - matriz: matriz contendo letras em cada coluna.
    - key: chave que ditará a ordem de leitura da matriz.

    Retorna:
    - nova_matriz: matriz com as colunas ordenadas.
    """

    nova_matriz = []
    letra_coluna = [(l, c) for l,c in zip(key, matriz)]
    letra_coluna.sort(key=lambda x: x[0])
    for tupla in letra_coluna:
        nova_matriz.append(tupla[1])
    return nova_matriz  


def quebra_cifra(ciphertext):
    """
    Decifra uma mensagem crptografada por transposição de colunas.

    Parâmetros:
    - ciphertext: mensagem cifrada.

    Retorna:
    - possiveis_respostas: uma lista com as possiveis respostas e o tamanho de suas chaves.
    """

    ciphertext = ciphertext.replace(" ", "")
    chaves = acha_divisores(ciphertext)
    possiveis_respostas = []
    for chave in chaves:
        colunas = divide_texto(ciphertext, chave)
        mensagem = analise_frequencia(colunas)
        possiveis_respostas.append((chave, mensagem))
    return possiveis_respostas    


def acha_divisores(texto):
    """
    Encontra os divisores da quantidade de letras no texto.


    Parâmetros:
    - texto: uma mensagem.

    Retorna:
    - divisores: os números que dividem o tamanho do texto.
    """
    divisores = []
    for i in range(1, 11):
        if (len(texto) == i):
            break
        elif (len(texto) % i) == 0:
            divisores.append(i)
    divisores.remove(1)        
    return divisores        


def divide_texto(texto, key):
    """
    Separa o texto cifrado em colunas de uma matriz.

    Parâmetros:
    - texto: a mensagem.
    - key: o número de colunas da matriz.

    Retorna:
    - colunas: uma lista com uma sequencia de letras em cada item.
    """

    colunas = ["" for k in range(key)]
    linhas = len(texto) / key
    counter = -1
    for indice, letra in enumerate(texto):
        if (indice % linhas) == 0:
            counter += 1
        colunas[counter] += letra    
    return colunas


def analise_frequencia(bloco):
    """
    Recebe o texto dividido em blocos e analisa todas as possíveis permutações.
    Analisa a frequência de bigramas e trigramas para escolher a melhor permutação.

    Parâmetros:
    - bloco: uma lista com o ciphertext dividido em itens

    Retorna:
    - melhor_permutação: permutação com a maior quantidade de bigrafos e trigrafos
    """
    bi_comum = ["AR", "AN", "AO", "AR", "AD", "AC", "EM", "ES", "EN", "ER", "DA", "DE",
                "DO", "ON", "OR", "OS", "CA", "CO", "RA", "RE", "TA", "TE", "MA", "NT",
                "SE", "AL", "IA", "IS", "ME", "NA", "OD", "RI", "RO", "SA", "ST", "UE"]
    tri_comum = ["QUE", "ENT", "NTE", "ADO", "ADE", "ODE", "ARA", "EST", "RES", "CON",
                "COM", "STA", "DOS", "CAO", "PAR", "ACA", "MEN", "SDE", "ICA", "ESE",
                "ACO", "ADA", "POR", "NTO", "OSE", "DES", "ASE", "ERA", "OES", "UMA",
                "TRE", "IDA", "DAD", "ANT", "ARE", "ONT", "PRE", "IST", "TER", "AIS"]

    #bi_comum = {"DE", "ES", "AO", "OS", "DA"}
    #tri_comum = {"QUE", "ENT", "NTE", "EST"}
    
    melhor_permutacao = ""
    melhor_score = 0

    for permutacao in permutations(bloco):
        mensagem = ''.join(''.join(c) for c in zip(*permutacao))

        bigramas = [mensagem[i:i+2] for i in range(len(mensagem) - 1)]
        trigramas = [mensagem[i:i+3] for i in range(len(mensagem) - 2)]
        conta_bigramas = Counter(bigramas)
        conta_trigramas = Counter(trigramas)

        score_bi = sum(conta_bigramas[bg] for bg in bi_comum)
        score_tri = sum(conta_trigramas[tg] for tg in tri_comum)
        score_total = (3 * score_tri) + score_bi

        if score_total > melhor_score:
            score_total = melhor_score
            melhor_permutacao = permutacao

    return melhor_permutacao      
           

def main():
    """
    Função principal que coleta entradas do usuário e chama as funções do programa.
    """

    while True:
        # Menu
        print("==============================================================================================================")
        print("Digite (1) para criptografar uma mensagem com transposição de colunas.")
        print("Digite (2) para descriptografar uma mensagem.")
        print("Digite (3) para encerrar.")
        opcao = int(input("Escolha uma das opções acima: "))
        
        match opcao:
            # Criptografar mensagem.
            case 1:
                print("==============================================================================================================")
                mensagem = input("Digite a mensagem: ")
                chave = input("Digite a palavra chave sem repetir letras: ")
                while True:
                    if 2 in Counter(chave).values():
                        chave = (input("Digite a chave, sem repetir letras: "))
                    else:
                        break  
                ciphertext = transposition_cipher(mensagem, chave)
                print(f"A mensagem criptografada é: {ciphertext}")
                input("Digite (0) para voltar ao menu: ")
            
            # Descriptograr mensagem.
            case 2:
                print("==============================================================================================================")
                ciphertext = input("Digite o texto cifrado: ")
                print("As possíveis mensagens originais são: ")
                print(*quebra_cifra(ciphertext), sep="\n|\n")
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
