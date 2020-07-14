# Buscador de repetições em DNA usando conceito do algoritmo Apriori

Buscador de repetições em sequência de DNA feito para disciplina de Bioinformática do curso de Ciências da Computação pela Universidade Estadual Paulista "Júlio de Mesquita Filho", Campus de Rio Claro.

Este programa utiliza-se do conceito do algoritmo Apriori para diminuir o número de buscas por repetições exatas em uma sequencia genética de DNA com as letras A, C, G, T.

### Requerimentos
Para funcionamento total deste programa deve-se executá-lo tendo as seguintes configurações e bibliotecas:
- python 3.5 ou superior
- pandas 1.0.1 ou superior
- re
- optparse

### Como executar
Para execução do programa utilize-se do python3 para executar o arquivo rep_finder.py passando os argumentos:

    -i	: arquivo de entrada em txt
    -o: arquivo de saída em .xlsx
    -s: suporte mínimo de ocorrência de uma repetição (valor absoluto ou valor relativo com %)
    -h: ajuda para execução

### Exemplo:

    python3 rep_finder.py -i base.txt -o arquivo_saida.xlsx -s 2

