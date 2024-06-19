import pandas as pd
from PyQt6.QtWidgets import *
import os


class Bfa:
    
    def consolidar(self, path):
        arquivos = os.listdir(path)        
        unidades = {
            7209649: 'Sede I', 7209665: 'Sede II', 3912035: 'Maria Preta',
            5413958: 'Prudência Rosa', 2602016: 'Coqueiros', 2600692: 'Nagé',            
            2550156: 'Capanema', 2771551: 'São Roque I', 7168462: 'São Roque II',            
            7586175: 'Enseada', 9753508: 'Guapira', 3792714: 'Batatan',            
            3792676: 'Piedade', 7586183: 'Rio Grande',            
            }        
        
        for arquivo in arquivos:            
            arq, ext = os.path.splitext(arquivo)
            lista = {}
            
            if ext == '.xls':
                df = pd.read_html(path + '/' + arquivo)                
                resumo = df[0]['Acompanhado'].value_counts()                
                
                unidade = df[0]['CNES da EAS de vincula??o'].unique()
                
                if unidade[0] in unidades:                    
                    self.listWidget.addItem(QListWidgetItem(f'Unidade de saúde: = {unidades[unidade[0]]}'))                

                total_beneficiarios = sum(lista.values())

                if 'SEM INFORMAÇÃO' in resumo:            
                    lista['Não acompanhados'] = resumo['SEM INFORMAÇÃO']            
                
                if 'SIM' in resumo:
                    lista['Acompanhados'] = resumo['SIM']
                
                if 'NÃO' in resumo:
                    lista['Outros não acompanhados'] = resumo['NÃO']
                
                for chave, valor in lista.items(): 
                    per = self.percentual(valor, total_beneficiarios)                   
                    self.listWidget.addItem(QListWidgetItem(f'{chave} = {valor} {per}%'))
                
                self.listWidget.addItem(QListWidgetItem(f''))

    
    def percentual(self, numerador, denominador):        
        percentual = (denominador / numerador) * 100
        return percentual
                