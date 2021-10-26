import pandas as pd

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
        if 'MWmed' in line_split:
            headers = line_split.copy()
        
        if line_split[0] == 'DP':
            vetor_rev.append(line_split)
    
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



if __name__ == '__main__':
    #nome_arquivo = 'CargaDecomp_PMO_Outubro21(Rev 3).txt'
    #arquivo = read_file(nome_arquivo)
    dadger = "DADGER.RV3"
    arquivo = extrair_carga_dadger(dadger, 'carga')
    x = carga_to_df(arquivo)
    z = convert_to_text(x)
    print(z)