import sys
from PyQt6.QtWidgets import *
from tela_principal import Ui_MainWindow
from bfa import Bfa


class JanelaPrincipal(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()        
        self.setupUi(self)
        self.cb_unidade.setEnabled(False)
        self.cb_situacao.setEnabled(False)
        self.cb_profissional.setEnabled(False)
        self.btn_gerar_relatorio.setEnabled(False)
        self.btn_abrir.clicked.connect(self.abrir_arquivo)        
        self.cb_unidade.currentTextChanged.connect(self.obter_profissional)
        self.cb_profissional.currentTextChanged.connect(self.obter_acompanhado)

        self.unidades = {
            7209649: 'SEDE I', 7209665: 'SEDE II', 3912035: 'MARIA PRETA',
            5413958: 'PRUDÊNCIA ROSA', 2602016: 'COQUEIROS', 2600692: 'NAGÉ',            
            2550156: 'CAPANEMA', 2771551: 'SÃO ROQUE I', 7168462: 'SÃO ROQUE II',            
            7586175: 'ENSEADA', 9753508: 'GUAPIRA', 3792714: 'BATATAN',            
            3792676: 'PIEDADE', 7586183: 'RIO GRANDE',            
            }  
      
    def obter_profissional(self):
        self.cb_profissional.clear()
        bfa = Bfa()
        
        cb_unidade = self.cb_unidade.currentText()
        cnes_unidade = 0

        for cnes, usf in self.unidades.items():             
            if cb_unidade == usf:
                cnes_unidade = cnes                

        prof = bfa.obter_profissional(self.lbl_caminho.text(), cnes_unidade)        
        
        for valor in prof:      
            self.cb_profissional.addItem(str(valor))            
        
    def abrir_arquivo(self):        
        diretorio = QFileDialog.getExistingDirectory(self)
        self.lbl_caminho.setText(diretorio)
        if diretorio:
            bfa = Bfa()
            dados = bfa.consolidar(diretorio)     
            
            self.listWidget.clear()   

            percentual_acompanhados = 0.0    
            cont = 0
            
            for chave, valor in dados.items():                
                self.listWidget.addItem(QListWidgetItem(f'{chave}:'))                
                
                for ch, vl in valor.items():
                    self.listWidget.addItem(QListWidgetItem(f'-{ch} = {vl}'))

                    if ch == 'Percentual de acompanhamento':
                        percentual_acompanhados += float(vl)
                        cont += 1
                
                self.listWidget.addItem(QListWidgetItem(f''))

            media = percentual_acompanhados / cont
            
            self.lbl_percentual_geral.setText(f'{media:.2f} %')
        
        # Variável que armazena lista de unidades de saúde retornada da classe Bfa e método pegar_unidades
        unidades_saude = bfa.obter_unidades(diretorio)   

        # Adiciona no combobox da tela a lista de unidades de saúde
        self.cb_unidade.addItems(unidades_saude)        
        
        self.cb_unidade.setEnabled(True)
        self.cb_situacao.setEnabled(True)
        self.cb_profissional.setEnabled(True)  
        self.btn_gerar_relatorio.setEnabled(True)

        self.obter_profissional()
    
    def obter_acompanhado(self):
        bfa = Bfa()
        unidade_saude = next((k for k, v in self.unidades.items() if v == self.cb_unidade.currentText()), None)
        
        acompanhado = bfa.obter_acompanhado(
            self.lbl_caminho.text(), 
            unidade_saude,             
            self.cb_profissional.currentText()
            )
        
        self.cb_situacao.clear()
        self.cb_situacao.addItems(acompanhado)

if __name__ == '__main__':
    qt = QApplication(sys.argv)
    app = JanelaPrincipal()
    app.show()
    sys.exit(qt.exec())
