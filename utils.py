import pandas as pd

def read_file(arquivo):
    with open(arquivo, 'r') as file:
        texto = file.readlines()
    return texto


def carga_to_df(texto):
    """
    Recebe o nome dor arquivo com os dados no formato da planilha de carga e retorna um dataframe
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

if __name__ == '__main__':
    #nome_arquivo = 'CargaDecomp_PMO_Outubro21(Rev 3).txt'
    #arquivo = read_file(nome_arquivo)
    dadger = "DADGER.RV3"
    arquivo = extrair_carga_dadger(dadger, 'carga')
    x = carga_to_df(arquivo)
    print(x)