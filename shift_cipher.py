letras_para_numeros = {chr(i): i - ord('A') for i in range(ord('A'), ord('Z') + 1)}     # dicionario que mapeia letras em numeros de 0 a 25
numeros_para_letras = {n: l for l, n in letras_para_numeros.items()}                    # dicionario que mapeia numeros de 0 a 25 em letras


def shift_cipher(plaintext, deslocamento):           
    """
    Criptografa uma mensagem desejada, utilizando substituição moalfabética.

    Parâmetros:
    - plaintext: a mensagem original.
    - deslocamento: quastas posições cada letra deverá ser deslocada.

    Retorna:
    - ciphertext: a mensagem cifrada.
    """

    ciphertext = ""
    for letra in plaintext:                                                                       
        ciphertext += new_letra(letra, deslocamento)        
    return ciphertext                                           


def new_letra(letra, deslocamento):      
    """
    Criptografa uma letra.

    Parâmetros:
    - letra: a letra que irá ser encriptada.
    - deslocamento: quantas posições a letra será deslocada.

    Retorna:
    - nova_letra: a letra criptografada após o deslocamento.
    """

    if letra == " ":
        return " "
    numero = letras_para_numeros[letra.upper()]                 
    novo_numero = (numero + deslocamento) % 26                  
    nova_letra = numeros_para_letras[novo_numero]               
    return nova_letra                                           


def forca_bruta(ciphertext):       
    """
    Descriptografa uma mensagem utilizando a técnica de força bruta.

    Parâmetros:
    - ciphertext: o texto criptografado.

    Retorna:
    - mensagens: uma lista que associa cada possível deslocamento com uma mensagem original.
    """   

    mensagens = []                        
    for deslocamento in range(1,26):                              
        plaintext = ""
        for letra in ciphertext:
            plaintext += new_letra(letra, -(deslocamento))
        mensagens.append((deslocamento, plaintext))
    return mensagens                                            
            

def distribuicao_frequencia(ciphertext):                                
    """
    Descriptografa uma mensagem utilizando a técnica de distribuição de frequências. 
    Assume que tanto 'a' quanto 'e' ou 'o' podem ser a letra de maior frequência.

    Parâmetros:
    - ciphertext: o texto criptografado.

    Retorna:
    - mensagens: uma lista que associa o deslocamento com a mensagem original.
    """
    
    sem_espaco = ciphertext.replace(" ", "")

    letra_frequente = max(set(sem_espaco), key=sem_espaco.count)            
    desloc_a = (letras_para_numeros[letra_frequente.upper()] -  0) % 26    
    desloc_e = (letras_para_numeros[letra_frequente.upper()] -  4) % 26     
    desloc_o = (letras_para_numeros[letra_frequente.upper()] - 14) % 26     
    
    plaintext_a = ""
    plaintext_e = ""
    plaintext_o = ""

    for letra in ciphertext:
        plaintext_a += new_letra(letra, -(desloc_a))
        plaintext_e += new_letra(letra, -(desloc_e))
        plaintext_o += new_letra(letra, -(desloc_o))

    mensagens = [(desloc_a, plaintext_a),
                 (desloc_e, plaintext_e),
                 (desloc_o, plaintext_o)]

    return mensagens

def main():
    """
    Função principal que coleta entradas do usuário e chama as funções do programa.
    """

    while True:
        # Menu
        print("==============================================================================================================")
        print("Digite (1) para criptografar uma mensagem.")
        print("Digite (2) para descriptografar uma mensagem pela técnica de força bruta.")
        print("Digite (3) para descriptografar uma mensagem pela técnica de destribuição de frequências.")
        print("Digite (4) para encerrar.")
        opcao = int(input("Escolha uma das opções acima: "))
        
        match opcao:
            # Criptografar mensagem.
            case 1:
                print("==============================================================================================================")
                mensagem = input("Digite a mensagem: ")
                deslocamento = int(input("Digite o deslocamento: "))
                ciphertext = shift_cipher(mensagem, deslocamento)
                print(f"A mensagem criptografada é: {ciphertext}")
                pausa = input("Digite (0) para voltar ao menu: ")
            
            # Descriptograr usando força bruta.
            case 2:
                print("==============================================================================================================")
                ciphertext = input("Digite o texto cifrado: ")
                print("As possíveis mensagens originais e seus respectivos deslocamentos são: ")
                print(*forca_bruta(ciphertext), sep="\n")
                pausa = input("Digite (0) para voltar ao menu: ")
            
            # Descriptografar usando distribuição de frequências.
            case 3:
                print("==============================================================================================================")
                ciphertext = input("Digite o texto cifrado: ")
                print("As possíveis mensagens originais e seus respectivos deslocamentos são: ")
                print(*distribuicao_frequencia(ciphertext), sep="\n")
                pausa = input("Digite (0) para voltar ao menu: ")
            
            # Encerrar programa.
            case 4:
                print("==============================================================================================================")
                print("Programa encerrado =)")
                break

            # Caso de resposta inválida.    
            case _:
                print("==============================================================================================================")
                print("Você deve escolher entre (1), (2), (3) ou (4). Tente novamente!")
                pausa = input("Digite (0) para voltar ao menu: ")

main()