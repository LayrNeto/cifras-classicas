# Cifras Clássicas

* [Descrição](#descrição)
* [Introdução](#introdução)
* [Criptografia por Substituição](#criptografia-por-substituição)
* [Descriptografia por Substituição](#algoritmos-de-descriptografia-de-substituição)
    * [Força Bruta](#força-bruta)
    * [Distribuição de Frequências](#distribuição-de-frequências)
* [Algoritmos de transposição](#algoritmos-de-transposição)
    * [Transposição Colunar](#transposição-colunar)
        * [Criptografia](#criptografia)
        * [Descriptografia](#descriptografia)
    * [Rail Fence](#transposição-rail-fence)
        * [Criptografia](#criptografia-1)
        * [Descriptografia](#descriptografia-1)
* [Comparação entre algoritmos](#comparação-entre-algortimos)
* [Conclusão](#conclusão)
* [Referências](#referências)

## Descrição
Este projeto implementa algoritmos para cifrar e decifrar mensagens usando técnicas de **substituição monoalfabética** e transposição. A descriptografia por substituição ocorre de duas maneiras, **força bruta** e análise por **distribuição de frequências**, enquanto os métodos escolhidos para a transposição são o **Rail Fence** e **transposição colunar**. Nesse projeto, os termos criptografia e descriptografia serão utilizados como sinônimos de cifra e decifra. 

## Introdução
Esse projeto utiliza-se de duas abordagens principais para cifrar e decifrar:
1. **Substituição Monoalfabética**: Cada letra é substituída por outra com base em uma chave de deslocamento fixa.

2. **Transposição**: A posição das letras é alterada de acordo com uma regra específica (colunar ou rail fence).

## Criptografia por Substituição
O algoritmo mapeia as letras do alfabeto em inteiros módulo 26, sendo `A = 0` e `Z = 25`. Diante de uma chave especificada, a criptografia se dá pelo deslocamento de todas as letras no valor escolhido.
#
```py
def shift_cipher(plaintext, deslocamento):           
    ciphertext = ""
    for letra in plaintext:                                 
        ciphertext += new_letra(letra, deslocamento)        
    return ciphertext      
```
1. Itera sobre cada letra da mensagem, concatenando o ciphertext com a letra após deslocamento.

2. Retorna o texto cifrado.
#
```py
def new_letra(letra, deslocamento):
    if letra == " ":
        return " "
    numero = letras_para_numeros[letra.upper()]                 
    novo_numero = (numero + deslocamento) % 26                  
    nova_letra = numeros_para_letras[novo_numero]               
    return nova_letra                             
```

1. Pega o número associado a letra e adiciona-o ao valor do deslocamento, módulo 26.

2. Tranforma o novo número em uma nova letra.

3. Retorna a letra deslocada.
#
- **Complexidade**: Aproximadamente O(n), onde n é a quantidade de letras no texto.


## Algoritmos de Descriptografia de Substituição

### Força Bruta
A descriptografia por força bruta tenta todos os possíveis deslocamentos e associa-os com um texto correspondente, dando como saída uma lista com esses valores. Este método pode ser demorado para problemas com um espaço amostral muito grande, assim como para textos muito longos, mas se torna viável neste caso por se limitar aos 26 caracteres do alfabeto romano.
#
```py
def forca_bruta(ciphertext):       
    mensagens = []                        
    for deslocamento in range(1,26):                              
        plaintext = ""
        for letra in ciphertext:
            plaintext += new_letra(letra, -(deslocamento))
        mensagens.append((deslocamento, plaintext))
    return mensagens
```

1. Repete 25 vezes, buscando cada possibilidade de deslocamento. 

2. Itera sobre cada letra do texto, retirando a diferença entre as letras e as chaves para achar o novo caractere.

3. Retorna uma lista com todas as possíveis respostas.
#
- **Complexidade**: Aproximadamente `O(nm)`, onde `n` é o número de caracteres únicos da chave e `m` o espaço amostral de caracteres, 26 nesse caso.

- **Tempo de Execução**: Pode ser muito alto para grandes mensagens, tornando a força bruta pouco viável em textos extensos e com grande variedades de caracteres.

### Distribuição de Frequências
Esta técnica compara a letra mais recorrente do ciphertext com as mais frequentes da língua portuguesa, obtendo-se o deslocamento da mensagem a partir da diferença na posição no alfabeto entre as letras. A análise é feita com base nas letras `A`, `E` e `O`, que sozinhas acumulam perto de 40% da frequência de letras do português.
#
```py
def distribuicao_frequencia(ciphertext):     
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
```
1. Trabalha com 3 possibilidades de letras mais frequêntes, `A`, `E` e `O`. 

2. Reduz a diferença entre o inteiro associado à letra recorrente do ciphertext e as letras recorrentes do português, para obter o deslocamento da mensagem.

3. Itera sobre cada letra do texto e concatena sua versão pós deslocamento com cada um dos 3 plaintext.

4. Retorna as 3 possibilidades de mensagens, e seus deslocamentos associados.
#
```py
letra_frequente = max(set(sem_espaco), key=sem_espaco.count)
``` 
1. Conta as repetições de cada letra do ciphertext

#

- **Complexidade**: Aproximadamente `O(n)`, onde `n` é a quantidade de letras no texto.

- **Tempo de Execução**: Geralmente mais rápido que a força bruta, mas depende da correspondência com as frequências do idioma.

## Algoritmos de Transposição

### Transposição Colunar

#### Criptografia
No método de **transposição colunar**, a mensagem é organizada em uma matriz a partir de uma chave específica (sem repetição de letras), associando-se cada coluna com uma letra da chave. A organização das colunas é definida pela ordenação alfabética da chave, gerando o texto crifrado segundo a leitura horizontal das linhas da matriz. Em colunas menores adiciona-se um `X` para manter o tamanho da matriz uniforme.
#
```py
def transposition_cipher(plaintext, key):
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
```
1. Cria uma matriz com quantidade de colunas definidas pelo tamanho da chave.

2. Itera sobre cada letra e adiciona uma por coluna, enquanto houver colunas incompletas.

3. Preenche espaços vazios e ordena as colunas da matriz.

4. Concatena ao ciphertext as letras de cada linha.

5. Retorna o texto cifrado.
#
```py
def completa_matriz(matriz):
    tamanho = len(matriz[0])
    for coluna in matriz:
        if len(coluna) < tamanho:
            coluna.append("X")
    return matriz        
```
1. Se houver colunas menores que a primeira, preenche os espaços vazios com `X`.

2. Retorna a matriz completa.
#
```py
def ordena_matriz(matriz, key):
    nova_matriz = []
    letra_coluna = [(l, c) for l,c in zip(key, matriz)]
    letra_coluna.sort(key=lambda x: x[0])
    for tupla in letra_coluna:
        nova_matriz.append(tupla[1])
    return nova_matriz  

```
1. Associa cada letra a uma coluna, formando uma lista de tuplas.

2. Ordena a lista, com base na ordem alfabética das letras.

3. Itera sobre cada tupla, adicionando as coluna a uma nova matriz.

4. Retorna a matriz ordenada.
#

- **Complexidade**: Aproximadamente `O(nm)`, onde `n` é a quantidade de letras no texto e `m` o tamanho da chave.

- **Técnica de Permutação**: A mensagem é organizada em uma matriz e ordenada conforme a chave.

- **Exemplo**:
   ```py
    Plaintext: "EXEMPLO DE TRANSPOSICAO"
    Chave: "CIFRA"
    Colunas: 
     C I F R A                  A C F I R       
     =========                  =========
     E M P L O       ===>       O E P M L       
     D E T R A                  A D T E R
     N S P O S                  S N P S O
     I C A O X                  X I A C O

    Ciphertext: "OEPML ADTER SNPSO XIACO"
    ```

#### Descriptografia
Sendo um ataque **ciphertext-only**, o programa busca primeiro encontrar o tamanho da chave e então achar a melhor permutação de colunas. *O algoritmo ainda não conta com funcionamento total, falhando em encontrar a resposta correta por meio da análise de frequências.*
#
```py
def quebra_cifra(ciphertext):
    ciphertext = ciphertext.replace(" ", "")
    chaves = acha_divisores(ciphertext)
    possiveis_respostas = []
    for chave in chaves:
        colunas = divide_texto(ciphertext, chave)
        mensagem = analise_frequencia(colunas)
        possiveis_respostas.append((chave, mensagem))
    return possiveis_respostas    
```
1. Encontra os possíveis tamanhos das chaves.

2. Itera sobre cada chave, formando uma matriz pra cada uma delas.

3. Analisa qual a melhor permutação possível para uma dada matriz.

4. Retorna uma lista com os tamanhos das chaves e a melhor resposta para cada uma delas.
#
```py
def acha_divisores(texto):
    divisores = []
    for i in range(1, 11):
        if (len(texto) == i):
            break
        elif (len(texto) % i) == 0:
            divisores.append(i)
    divisores.remove(1)        
    return divisores        
```
1. Estabelece um limite para o tamanho da chave de 10.

2. Para cada iteração de 1 a 10, verifica se o número é divisor do tamanho do texto.

3. Ignora se o divisor for 1 ou o próprio tamanho do texto.

4. Retorna uma lista com os divisores entre 2 e 10.
#
```py
def divide_texto(texto, key):
    colunas = ["" for k in range(key)]
    linhas = len(texto) / key
    counter = -1
    for indice, letra in enumerate(texto):
        if (indice % linhas) == 0:
            counter += 1
        colunas[counter] += letra    
    return colunas
```
1. Divide um texto dado em uma matriz de colunas delimitadas pelo valor da chave.

2. Cada item da lista, será uma coluna com uma sequência de caracteres.

3. Retorna uma lista com o texto dividido em colunas de tamanho igual.

#
```py
def analise_frequencia(bloco):
    bi_comum = ["AR", "AN", "AO", "AR", "AD", "AC", "EM", "ES", "EN", "ER", "DA", "DE",
                "DO", "ON", "OR", "OS", "CA", "CO", "RA", "RE", "TA", "TE", "MA", "NT",
                "SE", "AL", "IA", "IS", "ME", "NA", "OD", "RI", "RO", "SA", "ST", "UE"]
    
    tri_comum = ["QUE", "ENT", "NTE", "ADO", "ADE", "ODE", "ARA", "EST", "RES", "CON",
                "COM", "STA", "DOS", "CAO", "PAR", "ACA", "MEN", "SDE", "ICA", "ESE",
                "ACO", "ADA", "POR", "NTO", "OSE", "DES", "ASE", "ERA", "OES", "UMA",
                "TRE", "IDA", "DAD", "ANT", "ARE", "ONT", "PRE", "IST", "TER", "AIS"]
    
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
```
1. Estabelece quais são os bigramas e os trigramas mais comuns da língua portuguesa.

2. Itera sobre todas as possíveis permutação de colunas.

3. Conta quantos bigramas e trigramas da permutação fazem parte da lista dos comuns.

4. Calcula a pontuação como a soma da quantidade de bigramas e de trigramas comuns, dando peso 3 para esse.

5. Retorna a permutação que obter maior pontuação
#
- **Complexidade**: Aproximadamente `O(n!)`, onde `n` é o tamanho da maior chave encontrada.

- **Tempo de Execução**: Extremamente alto, germinando lentidão a partir da chave 10 e mostrando-se inviável para valores ainda maiores.

### Transposição Rail Fence

#### Criptografia
No método de transposição **Rail Fence**, a mensagem é organizada em linhas, quantificadas pelo valor da chave. A leitura das linhas ocorre em direção diagonal, num movimento de ida e volta. A mensagem cifrada é resultada da leitura das letras de cada linha.
#
```py
def rail_fence(texto, linhas):
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
```
1. Cria uma lista com tamanho igual à quantidade de rails.

2. `counter` é o index atual da lista.

3. `ida_volta` indica True se está avançando e False se está retornando.

4. Itera sobre cada letra e adiciona à posição atual da lista.

5. Atualiza o index da lista e o estado de ida ou de volta.

6. Concatena ao ciphertext cada linha da lista.

7. Retorna o texto cifrado.
#
```py
def ida_ou_volta(counter, linhas, ida_volta):
    if ida_volta:
        counter += 1
    else:    
        counter -= 1

    if counter == linhas:
        counter -= 2
        ida_volta = False 
    if counter == -1:
        counter += 2
        ida_volta = True    

    return counter, ida_volta
```
1. Se está indo, incrementa o index.

2. Se está voltando, subtrai o index.

3. Se a posição atual é a última linha, retorna à última posição e volta.

4. Se a posição atual é a primeira linha, retorna à ultima posição e avança.

5. Retorna o index atual e a direção da movimentação.
#
- **Complexidade**: Aproximadamente `O(n)`, onde `n` é a quantidade de letras no texto.

- **Técnica de Permutação**: A mensagem é organizada em diagonais limitadas pela quantidade de linhas.

- **Exemplo**:
   ```py
    Plaintext: "EXEMPLO RAIL FENCE"
    Chave: 3
    Colunas: 
     
     E - - - P - - - A - - - E - - -    
     - X - M - L - R - I - F - N - E
     - - E - - - O - - - L - - - C -

    Ciphertext: "EPAE XMLRIFNE EOLC"
    ```
#### Descriptografia
Sendo um ataque **ciphertext-only**, o programa utiliza de força bruta para encontrar a quantidade de linhas, e então busca recriar o algoritmo de criptografia para decifrar o texto.
#
```py
def quebra_cifra(texto, max_linhas:int):
    possiveis_mensagens = []

    if len(texto) < max_linhas:
        max_linhas = len(texto)

    for linha in range(2, max_linhas):
        lista = tamanho_linhas(texto, linha)
        ciphertext = separa_texto(texto, lista)
        plaintext = decifra_rail(ciphertext, linha)
        possiveis_mensagens.append((linha, plaintext))

    return possiveis_mensagens
```
1. Estabelece que a quantidade de rails a serem avaliadas pode ser no máximo do tamanho do texto.

2. Itera sobre a quantidade máxima de linhas e descobre quantos caracteres teriam em cada rail, dependendo da chave.

3. A partir da quantidade de caracteres por linha, divide as letras do texto em rails.

4. Desfaz o Rail Fence para encontrar a mensagem original.

5. Retorna uma lista com todas as chaves e suas respectivas mensagens.
#
```py
def tamanho_linhas(texto, linhas):
    lista = [0 for _ in range(linhas)] 
    texto = texto.replace(" ", "")
    counter = 0
    ida_volta = True

    for letra in texto:
        lista[counter] += 1
        
        counter, ida_volta = ida_ou_volta(counter, linhas, ida_volta)   

    return lista
```
1. Cria uma lista com tamanho igual à quantidade de rails.

2. `counter` é o index atual da lista.

3. `ida_volta` indica True se está avançando e False se está retornando.

4. Itera sobre cada letra e incrementa um item da lista cada vez que seu index aparecer.

5. Atualiza o index da lista e o estado de ida ou de volta.

6. Retorna a lista contendo a quantidade de caracteres originais em cada um de seus itens.
#
```py
def separa_texto(texto, lista):
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
```
1. Cria uma lista com tamanho igual à quantidade de rails.

2. `counter` é a quantidade de letras adicionadas à um item da lista.

3. `idx` é o index atual da lista.

4. Itera sobre cada letra e concatena ao item atual da lista.

5. Ao colocar o máximo de letras em um index, passa para o próximo.

6. Retorna a lista contendo o texto cifrado dividido em linhas.
#
```py
def decifra_rail(texto_separado, linhas):
    tamanho_texto = sum(len(t) for t in texto_separado)
    plaintext = ""
    counter = 0
    ida_volta = True 

    for letra in range(tamanho_texto):
        letra, texto_separado[counter] = pop(texto_separado[counter])
        plaintext += letra
        
        counter, ida_volta = ida_ou_volta(counter, linhas, ida_volta)

    return plaintext        
```
1. `tamanho_texto` é a quantidade de letras do ciphertext

2. `counter` é o index atual da lista.

3. `ida_volta` indica True se está avançando e False se está retornando.

4. Itera na quantidade de letras do texto. 

5. Remove a primeira letra da posição atual da lista e concatena com o plaintext.

6. Atualiza o index da lista e o estado de ida ou de volta.

7. Retorna a mensagem decifrada.
#
```py
def pop(string):
    if string:
        primeiro_caractere = string[0]
        nova_string = string[1:]
        return primeiro_caractere, nova_string
    else:
        return '', string
```
1. Remove o primeiro caractere de uma string.

2. Retorna o caractere e a string pós remoção.
#

- **Complexidade**: Aproximadamente `O(nm)`, onde `n` é o comprimento do texto e `m` é a quantidade máxima de rails.

- **Tempo de Execução**: Rápido, viável até em casos com texto grande, sendo uma executado em tempo polinommial.

## Comparação entre Algortimos

| Algoritmo                    | Complexidade de Criptografia | Complexidade de Descriptografia | Tempo de Execução | Viabilidade |
|:-----------------------------|:------------:|:------------:|:------------------:|:----------------------------------:|
| Força Bruta                  | `O(n)`       | `O(nm)`      | Razoável          | Pouco viável para textos grandes  |
| Distribuição de Frequências  | `O(n)`       | `O(n)`       | Rápido            | Alta viabilidade                  |
| Transposição Colunar         | `O(nm)`      | `O(n!)`      | Muito Alto        | Inviável                          |
| Rail Fence                   | `O(n)`       | `O(nm)`      | Rápido            | Muito viável                      |

## Conclusão
O desenvolvimento deste projeto forneceu uma visão abrangente sobre a implementação e análise de diferentes algoritmos de cifras clássicas. A utilização dos métodos de substituição monoalfabética e transposição permitiu observar as forças e limitações de cada técnica em termos de segurança, complexidade computacional e viabilidade de uso.

Os resultados demonstraram que:
- **Força Bruta** é um método eficaz para mensagens com espaço amostral curto, demonstrando utilidade quando limitado ao alfabeto romano.

- **Distribuição de Frequências** se mostrou mais eficiente e inteligente que o método de força bruta, pois reduz drásticamente a quantidade de análises, limitando-se a um grupo pequeno de caracteres escolhidos pelo programador.

- **Transposição Colunar** provou-se como o método mais difícil de lidar, carregando um processo de cifra de fácil resolução, ao passo que apresentava complexidade fatorial no algoritmo de decifra. Na análise de quem defende, atestou como método mais seguro dentre as opções. Na análise de quem ataca, revelou-se como uma técnica de difícil combate, já que depende da análise de frequências da língua e também devido à sua complexidade e tempo de execução altos.

- **Rail Fence** dentre os algoritmos de transposição é o de menor complexidade, apresentando simplicidade e destacando-se em termos de velocidade, mas tendo um algoritmo de quebra de baixa exigência computacional.

A viabilidade das estratégias varia conforme o contexto. Enquanto a transposição colunar pode ser impraticável, a distribuição de frequências e a transposição Rail Fence fornecem um equilíbrio entre complexidade e desempenho.

Em conclusão, a escolha do algoritmo deve considerar tanto o nível de segurança desejado quanto a eficiência necessária para a aplicação. Esta análise serve como um guia para entender como essas técnicas podem ser usadas e otimizadas, além de fornecer preparo para algoritmos ainda mais complexos e inteligentes que estão por vir.

## Referências

- https://www.dcc.fc.up.pt/~rvr/naulas/tabelasPT/
- https://wiki.imesec.ime.usp.br/books/criptografia/page/cifras-de-transposi%C3%A7%C3%A3o
- https://www.gta.ufrj.br/ensino/eel879/trabalhos_vf_2010_2/gabriel/cript.htm
- https://crypto.stackexchange.com/questions/1550/obtaining-the-key-length-of-a-columnar-transposition-given-a-known-plaintext-wo/1578#1578
