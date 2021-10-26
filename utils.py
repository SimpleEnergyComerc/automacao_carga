import pandas as pd
import re 

def read_file(arquivo):
    with open(arquivo, 'r') as file:
        texto = file.readlines()
    return texto


def carga_to_df(texto):
    """
    Recebe o nome dor arquivo com os dados no formato da planilha de carga e retorna um dataframe

    :param str texto: String contendo dados de carga no formato do DADGER/DECK
    :return: Data Frame convertido a partir da string recebida
    """

    previous_line = ""
    vetor_rev = []
    gravando_rev = False
    for line in texto: 
        line_split = line.split()
        aux_list = []
        if 'MWmed' in line_split:
            headers = line_split.copy()
            i_pos = 0
            i_mwmed = 1
            for header in headers:
                if 'MWmed' in header:
                    headers[i_pos] = headers[i_pos] + str(i_mwmed)
                    i_mwmed += 1
                i_pos += 1
            
        if line_split[0] == 'DP':
            for value in line_split:
                if re.match(r'^-?\d+(?:\.\d+)$', value) is None:
                    aux_list.append(value)
                else:
                    aux_list.append(float(value))

            vetor_rev.append(aux_list)
    
    df = pd.DataFrame(vetor_rev, columns=headers)
    return df

def extrair_carga_dadger(arquivo, bloco):
    """
    Extrai do arquivo DADGER a parte referente ao reservatório ou carga, conforme selecionado nos parâmetros da função.

    :param .txt arquivo: Path do arquivo txt no formato do Deck contendo dados de carga e/ou reservatório
    :param str bloco: string no formato 'carga' ou 'reservatório' indicando quais dados desejamos extrair
    :return list text_list: retorna uma lista de strings referente aos dados extraidos do arquivo
    """ 
    with open(arquivo) as file:
        text_list = []
        save_line = False
        bloco_carga = False
        if bloco == 'carga':
            bloco_carga_nome = "BLOCO 6 *** CARGA DOS SUBSISTEMAS ***" 
        elif bloco == 'reservatorio':
            bloco_carga_nome = "BLOCO 3"
        linha_divisao = "&---------------------------------------------------------------------"
        linha_divisao_counter = 0 
        for line in file:
            if bloco_carga_nome in line:
                bloco_carga = True
            if bloco_carga and (linha_divisao in line):
                linha_divisao_counter += 1
                if linha_divisao_counter == 2:
                    break
            
            if linha_divisao_counter == 1:
                text_list.append(line)
    return text_list





def convert_to_text(df_raw):
    """
    Converte um data frame de cargas no formato txt para ser inserido posteiormente no deck.

    :param DataFrame df_raw: Recebe o data_frame contendo os dados de carga
    :return str full_text: Retorna o DataFrame convertido em string no formato do DADGER/Deck do DECOMP
    """
    def generate_string(tamanho):
        string = " "
        string = string*tamanho
        return string

    def insert_string(string_size, value, from_direction='Right'):
        if type(value).__name__ == 'int':
            value_string = str(float(value))
        else:
            value_string = str(value)
        string = generate_string(string_size)
        string2list = list(string)
        if from_direction == 'Right':
            for i in reversed(range(0,len(value_string))):
                string2list[i] = value_string[-i -1]
            return "".join(string2list[::-1])
        elif from_direction == 'Left':
            for i in range(0,len(value_string)):
                string2list[i] = value_string[i]
            return "".join(string2list)

    full_text = ""
    previous_ip = 0
    current_ip = 0
    for i, row in df_raw.iterrows():
        current_ip = int(row['IP'])

        if i == 0:
            current_ip = int(row['IP'])
            previous_ip = int(row['IP'])
        if previous_ip != current_ip:
            full_text = full_text + "&" + '\n'

        dp = insert_string(5, row.values[0], from_direction='Left')
        ip = insert_string(5, row.values[1], from_direction='Left')
        s = insert_string(4, row.values[2], from_direction='Left')
        pat = insert_string(5, row.values[3], from_direction='Left')
        mwmed1 = insert_string(10, row.values[4], from_direction='Right')
        pat1 = insert_string(10, row.values[5], from_direction='Right')
        mwmed2 = insert_string(10, row.values[6], from_direction='Right')
        pat2 = insert_string(10, row.values[7], from_direction='Right')
        mwmed3 = insert_string(10, row.values[8], from_direction='Right')
        pat3 = insert_string(10, row.values[9], from_direction='Right')
        if len(str(row.values[2])) > 1:
            ip = insert_string(4, row.values[1], from_direction='Left')
            s = insert_string(5, row.values[2], from_direction='Left')
        full_text = full_text + dp + ip + s + pat + mwmed1 + pat1 + mwmed2 + pat2 + mwmed3 + pat3 + '\n'
        previous_ip = int(row['IP'])

    full_text = full_text + "&" + '\n'
    return full_text

def add_value_carga(df_raw_original, ip, delta, regions):
    """
    Permite a alteração dos valores de carga no DataFrame escolhendo o subsistema, semanas a frente e o valor delta a ser adicionado

    :param DataFrame df_raw_original: Recebe o data_frame contendo os dados de carga
    :param int ip: Recebe o valor IP que indica o numero de semanas a frente
    :param float delta: Valor em MW a ser somado na carga. Para subtrair basta escolher um sinal negativo
    :param list/str regions: Lista contendo os subsistemas que se deseja modificar, a qual pode conter as seguintes strings -> 'S', 'SE', 'NE', 'NE'. Caso o parâmetro tenha recebido
    apenas uma string, fora de uma lista, o código irá entender que se deseja modificar apenas um subistema
    :return DataFrame df_raw: Retorna o DataFrame modificado
    """
    if type(regions).__name__ == 'str':
        regions = [regions]
    dict_region = {
        'SE': '1',
        'S': '2',
        'NE': '3',
        'N': '4',
    }
    df_raw = df_raw_original.copy()
    for region in regions:
        df_raw.loc[(df_raw['IP'] == str(ip)) & (df_raw['S'] == dict_region[region]), 'MWmed1'] = df_raw.loc[(df_raw['IP'] == str(ip)) & (df_raw['S'] == dict_region[region]), 'MWmed1'] + delta
        df_raw.loc[(df_raw['IP'] == str(ip)) & (df_raw['S'] == dict_region[region]), 'MWmed2'] = df_raw.loc[(df_raw['IP'] == str(ip)) & (df_raw['S'] == dict_region[region]), 'MWmed2'] + delta
        df_raw.loc[(df_raw['IP'] == str(ip)) & (df_raw['S'] == dict_region[region]), 'MWmed3'] = df_raw.loc[(df_raw['IP'] == str(ip)) & (df_raw['S'] == dict_region[region]), 'MWmed3'] + delta
    return df_raw

def prepare_next_weeks(df_raw, weeks_ahead):
    """
    A fim de preparar o deck para as próximas semanas, essa função remove as semanas que já terão passado.

    :param DataFrame df_raw: Recebe o data_frame contendo os dados de carga.
    :return int weeks_ahead: Recebe o número de semanas no futuro em que se deseja deixar o deck formatado.
    """
    weeks_list = list(df_raw['IP'].unique())
    del weeks_list[:weeks_ahead]
    df_new = df_raw.loc[df_raw['IP'].isin(weeks_list)].copy()
    new_ip = list(range(1,len(weeks_list) + 1))
    new_ip = list(map(str, new_ip))
    replace_dict = dict(zip(weeks_list, new_ip))    
    df_new.loc[:,'IP'].replace(replace_dict, inplace = True)
    return df_new


if __name__ == '__main__':
    #nome_arquivo = 'CargaDecomp_PMO_Outubro21(Rev 3).txt'
    #arquivo = read_file(nome_arquivo)
    dadger = "DADGER.RV3"
    arquivo = extrair_carga_dadger(dadger, 'carga')
    x = carga_to_df(arquivo)
    y = add_value_carga(x, 4, 20000, 'SE')
    w = prepare_next_weeks(y,3)
    z = convert_to_text(w)
    print(z)
