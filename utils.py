import pandas as pd



def carga_to_df(arquivo):
    """
    Recebe o nome dor arquivo com os dados no formato da planilha de carga e retorna um dataframe
    """
    with open(arquivo, 'r') as file:
        previous_line = ""
        vetor_rev = []
        gravando_rev = False
        for line in file: 
            line_split = line.split()
            if 'MWmed' in line_split:
                headers = line_split.copy()
            
            if line_split[0] == 'DP':
                vetor_rev.append(line_split)
        
        df = pd.DataFrame(vetor_rev, columns=headers)
    return df


if __name__ == '__main__':
    arquivo = 'CargaDecomp_PMO_Outubro21(Rev 3).txt'
    x = carga_to_df(arquivo)
    print(x)