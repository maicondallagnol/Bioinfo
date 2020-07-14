import pandas as pd
import re
from optparse import OptionParser


def busca_repeticoes(repeticoes, listas, suporte):
    """
    :param repeticoes: dicionário de repeticoes e os index das strings onde buscá-las
    :param listas: lista de strings com as sequências de ACGT
    :param suporte: ocorrencias minima para a repetição aparecer
    :return: retorna dict com as ocorrencias de repetições de entrada

    :Exemplo:
    repeticoes = {'AA': [0,1,2,6], 'AC': [0,1,2]}
    listas = ['AAACAA', 'CCAATG', 'CACTGA']

    return {'AA':{0:[0, 4], 1:[2]}, 'AC': {0:[2]}, ...}
    """
    dict_repeticoes = {}

    # Itera sob as repetições passadas e os index das listas onde procurá-las
    for repeticao, index_listas in repeticoes.items():
        lista_repeticoes = []
        num_repeticoes = 0

        # Itera sob os index das listas para procurar uma repetição em uma string das listas
        for index_lista in index_listas:

            # Usa regex (re) para buscar as ocorrencias na string
            search = [m.start() for m in re.finditer(repeticao, listas[index_lista])]

            # Se encontrar ao menos uma ocorrência armazena na lista de
            # tuplas com index da string e das ocorrencias da repetição
            if search:
                lista_repeticoes.append((index_lista, search))
                num_repeticoes += len(search)

        # Após percorrer todas as strings checa se houve ao menos 1 ocorrencia
        # Se houver o mínimo transforma a lista de tuplas em dict
        if num_repeticoes >= suporte:
            dict_repeticoes[repeticao] = dict(lista_repeticoes)

    return dict_repeticoes


def cria_combinacoes(dict_repeticoes):
    """
    Cria as combinações com base nas repetições encontradas
    :param dict_repeticoes: dicionário com as repetições encontradas
    :return: retorna dicionário com as combinações e os index de onde
    a combinação veio (evita busca onde não existe a repetição)
    """
    lista_termos = list(dict_repeticoes.keys())
    combinacoes = {}

    # Itera todas as repetições encontradas na iteração anterior
    for valor1 in lista_termos:
        for valor2 in lista_termos:

            # Se houver uma intersecçao quase total entre 2 repetiçoes coloca em
            # combinaçoes a junção das duas e os index onde uma das duas apareceu
            # Ex:  "AAC" e "ACG" -> "AACG"
            if valor1[1:] == valor2[:-1]:
                combinacoes.update({valor1 + valor2[-1]: sorted(
                    set(list(dict_repeticoes[valor1].keys()) + list(dict_repeticoes[valor2].keys())))})

    return combinacoes


def define_suporte(listas, suporte):
    """
    Seta suporte minimo das ocorrencias
    :param listas: lista das string para pegar o tamanho
    :param suporte: suporte em valor absoluto ou relativo
    :return:
    """

    # Transforma de string para float e já no valor absoluto
    if suporte[-1] == '%':
        return len(listas) * (float(suporte[:-1])/100)

    else:
        return float(suporte)


def acha_repeticoes(listas, suporte):
    """
    Busca ocorrencias de repetições nas strings em :listas:, criando um dicionário
    com o index das linhas e suas ocorrências
    :param listas: lista de strings com as sequências de ACGT
    :param suporte: valor minimo de ocorrencias para uma repetiçao ser contada
    :return: dicionário de repetições que indexa dicionários de index das linhas que por sua vez indexa as ocorrencias
    das repetições

    :Exemplo:
    listas = ['AAACAA', 'CCAATG', 'CACTGA']

    return {'AA':{0:[0, 4], 1:[2]}, 'AC': {0:[2]}, ...} <- formato records para lib pandas
    """

    dict_comb = {}

    # Define o suporte minimo de ocorrencia de uma repeticao
    suporte = define_suporte(listas, suporte)

    # Inicia a combinação com todas as opções usando 2 letras e buscando em todas as string
    combinacao = dict(
        [(valor1 + valor2, range(len(listas))) for valor1 in ['A', 'C', 'G', 'T'] for valor2 in ['A', 'C', 'G', 'T']])

    # Enquanto houver combinações e repeticoes as iterações ocorrem
    while (1):

        # Busca as repetições nas strings em listas
        dict_repeticoes = busca_repeticoes(combinacao, listas, suporte)

        # Checa se houve repetições, se não houve então acaba as iterações
        lista_termos = list(dict_repeticoes.keys())
        if not lista_termos:
            break

        else:

            # Atualiza o dicionário externo com as repetições encontradas nesta iteração e com as combinações entradas
            dict_comb.update(dict_repeticoes.copy())

            # Gera novas combinações para a próxima iteração usando as repetições encontradas
            combinacao = cria_combinacoes(dict_repeticoes)

            # Se não foi possível fazer novas combinações para serem buscadas então as iterações também acabam
            if not combinacao:
                break

    return dict_comb


def gera_tabela(dict_comb):
    """
    Gera uma tabela usando pandas DataFrame
    :param dict_comb: dicionario com as repetiçoes, os index das string onde aparecem e os index na string
    :return: tabela do tipo DataFrame
    """

    # Gera a tabela, arruma o index para nao começar em zero, ordena
    # com o index e depois ordena com base no tamanho repetiçao
    table = pd.DataFrame.from_records(dict_comb)
    table.index = table.index + 1
    table.sort_index(inplace=True)
    table = table[sorted(table.columns, key=len)]

    return table


def carrega_arquivo(nome_arq):
    arq = open(nome_arq, 'r')

    listas = []

    for linha in arq:
        listas.append(linha.strip())

    return listas

def salva_tabela(tabela, output):
    """
    Salva a tabela em xlsx
    :param tabela: tabela
    :param output: nome do arquivo de saída
    :return:
    """
    if output[-5:] != '.xlsx':
        output += '.xlsx'

    tabela.to_excel(output)


if __name__ == '__main__':
    optparser = OptionParser()

    optparser.add_option('-i', '--inputFile',
                         dest='input',
                         help='Arquivo de entrada em txt com strings separadas em linhas',
                         default="base.txt")

    optparser.add_option('-o', '--outputFile',
                         dest='output',
                         help='Arquivo de saída em xlsx',
                         default="saida.xlsx")

    optparser.add_option('-s', '--support',
                         dest='sup',
                         help='Suporte mínimo para as repeticoes',
                         default='2')

    (options, args) = optparser.parse_args()

    listas = carrega_arquivo(options.input)
    print("Arquivos carregados", end='\n')

    dict_repeticoes = acha_repeticoes(listas, options.sup)
    print("Repetições encontradas", end='\n')

    tabela = gera_tabela(dict_repeticoes)
    print("Tabelas Geradas", end='\n')

    salva_tabela(tabela, options.output)
    print("Tabela exportada!", end='\n')
