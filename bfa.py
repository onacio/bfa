import pandas as pd
import os


class Bfa:
    def __init__(self):        
        self.lista_dados = {}        
        self.unidades = {
            7209649: 'SEDE I', 7209665: 'SEDE II', 3912035: 'MARIA PRETA',
            5413958: 'PRUDÊNCIA ROSA', 2602016: 'COQUEIROS', 2600692: 'NAGÉ',            
            2550156: 'CAPANEMA', 2771551: 'SÃO ROQUE I', 7168462: 'SÃO ROQUE II',            
            7586175: 'ENSEADA', 9753508: 'GUAPIRA', 3792714: 'BATATAN',            
            3792676: 'PIEDADE', 7586183: 'RIO GRANDE',            
            }  
    
    def consolidar(self, diretorio):        
        arquivos = os.listdir(diretorio)        
        
        for arquivo in arquivos:            
            arq, ext = os.path.splitext(arquivo)
            
            lista = {}      
            
            if ext == '.xls':
                df = pd.read_html(diretorio + '/' + arquivo)                                
                resumo = df[0]['Acompanhado'].value_counts()                
                
                unidade = df[0]['CNES da EAS de vincula??o'].unique()

                if 'SIM' in resumo:
                    lista['Acompanhados'] = resumo['SIM']

                if 'SEM INFORMAÇÃO' in resumo:            
                    lista['Não acompanhados'] = resumo['SEM INFORMAÇÃO']            
                                
                if 'NÃO' in resumo:
                    lista['Outros não acompanhados'] = resumo['NÃO']
                
                total_beneficiarios = sum(lista.values())
                percentual = self.calcular_percentual(lista['Acompanhados'], total_beneficiarios)
                lista['Percentual de acompanhamento'] = f'{percentual}'
                #lista['Percentual de acompanhamento'] = f'{percentual:.2f}'
            
            self.lista_dados[self.unidades[unidade[0]]] = lista
                        
        return self.lista_dados
    
    def calcular_percentual(self, numerador, denominador):        
        percentual = (numerador / denominador) * 100
        return percentual
    
    def obter_profissional(self, caminho, unidade):        
        arquivos = os.listdir(caminho)

        for arquivo in arquivos:
            arq, ext = os.path.splitext(arquivo)
            
            if ext == '.xls':
                df = pd.read_html(caminho + '/' + arquivo)
                usf = df[0]['CNES da EAS de vincula??o'].unique()
                
                if unidade in usf:
                    prof = df[0]['Nome do prof. de vincula??o'].unique()
                    return prof
                
    def obter_unidades(self, caminho):
        arquivos = os.listdir(caminho)
        
        lista_unidades = []

        for arquivo in arquivos:
            arq, ext = os.path.splitext(arquivo)
            
            if ext == '.xls':
                df = pd.read_html(caminho + '/' + arquivo)
                unidades_saude = df[0]['CNES da EAS de vincula??o'].unique()
                for unidade in unidades_saude:
                    if unidade in self.unidades:                        
                        lista_unidades.append(self.unidades[unidade])                        
        
        return lista_unidades
    
    def obter_acompanhado(self, caminho, unidade, profissional):
        arquivos = os.listdir(caminho)
                        
        for arquivo in arquivos:
            arq, ext = os.path.splitext(arquivo)
            
            if ext == '.xls':
                df = pd.read_html(caminho + '/' + arquivo)
                unidades_saude = df[0]['CNES da EAS de vincula??o'].unique()
                if unidade == unidades_saude:
                    df_novo = df[0]
                    df_prof = df_novo[df_novo['Nome do prof. de vincula??o'] == profissional]
                    return df_prof['Acompanhado'].unique()