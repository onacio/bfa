import pandas as pd


class Bfa:
    def __init__(self, arquivo):        
        self.df = pd.read_html(arquivo)

    def informacoes(self):
        resumo = self.df[0]['Acompanhado'].value_counts()

        lista = {}

        if 'SEM INFORMAÇÃO' in resumo:            
            lista['Não acompanhados'] = resumo['SEM INFORMAÇÃO']            
        
        if 'SIM' in resumo:
            lista['Acompanhados'] = resumo['SIM']
        
        if 'NÃO' in resumo:
            lista['Outros não acompanhados'] = resumo['NÃO']

        return lista
    
    # Método criado para retornar o percentual de acompanhados
    # Não usada
    def percentual(self):
        resumo = self.df[0]['Acompanhado'].value_counts()

        print(resumo)

        soma = 0
        for chave, valor in resumo.items():
            soma += valor
        
        per = (resumo['SIM'] / soma) * 100

        return per