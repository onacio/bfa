import pandas as pd
import os


class Bfa:
    def __init__(self):        
        self.lista_dados = {}        
        self.unidades = {
            7209649: 'Sede I', 7209665: 'Sede II', 3912035: 'Maria Preta',
            5413958: 'Prudência Rosa', 2602016: 'Coqueiros', 2600692: 'Nagé',            
            2550156: 'Capanema', 2771551: 'São Roque I', 7168462: 'São Roque II',            
            7586175: 'Enseada', 9753508: 'Guapira', 3792714: 'Batatan',            
            3792676: 'Piedade', 7586183: 'Rio Grande',            
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
                percentual = self.percentual(lista['Acompanhados'], total_beneficiarios)
                lista['Percentual de acompanhamento'] = f'{percentual:.2f}'
            
            self.lista_dados[self.unidades[unidade[0]]] = lista
                        
        return self.lista_dados
    
    def percentual(self, numerador, denominador):        
        percentual = (numerador / denominador) * 100
        return percentual
    
    def pegar_profissional(self, caminho, unidade):        
        arquivos = os.listdir(caminho)

        for arquivo in arquivos:
            arq, ext = os.path.splitext(arquivo)
            
            if ext == '.xls':
                df = pd.read_html(caminho + '/' + arquivo)
                usf = df[0]['CNES da EAS de vincula??o'].unique()
                
                if unidade in usf:
                    prof = df[0]['Nome do prof. de vincula??o'].unique()
                    return prof
                
    def pegar_unidades(self, caminho):
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
