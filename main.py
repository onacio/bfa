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
        #self.btn_gerar_relatorio.clicked.connect(self.gerar_relatorio)
        self.cb_unidade.currentTextChanged.connect(self.gerar_relatorio)
        
        

        self.unidades = {
            7209649: 'Sede I', 7209665: 'Sede II', 3912035: 'Maria Preta',
            5413958: 'Prudência Rosa', 2602016: 'Coqueiros', 2600692: 'Nagé',            
            2550156: 'Capanema', 2771551: 'São Roque I', 7168462: 'São Roque II',            
            7586175: 'Enseada', 9753508: 'Guapira', 3792714: 'Batatan',            
            3792676: 'Piedade', 7586183: 'Rio Grande',            
            }  
        
    def pegar_unidades(self):
        caminho = self.lbl_caminho.text()        
        bfa = Bfa()
        lista = bfa.pegar_unidades(caminho)        
        
        self.cb_unidade.addItems(lista)

    def gerar_relatorio(self):
        self.cb_profissional.clear()
        bfa = Bfa()
        
        cb_unidade = self.cb_unidade.currentText()
        cnes_unidade = 0

        for cnes, usf in self.unidades.items():             
            if cb_unidade == usf:
                cnes_unidade = cnes                

        prof = bfa.pegar_profissional(self.lbl_caminho.text(), cnes_unidade)        
        
        for valor in prof:      
            self.cb_profissional.addItem(str(valor))            
        
    def abrir_arquivo(self):        
        diretorio = QFileDialog.getExistingDirectory(self)
        self.lbl_caminho.setText(diretorio)
        if diretorio:
            bfa = Bfa()
            dados = bfa.consolidar(diretorio)     
            
            self.listWidget.clear()       
            
            for chave, valor in dados.items():                
                self.listWidget.addItem(QListWidgetItem(f'{chave}:'))                
                
                for ch, vl in valor.items():
                    self.listWidget.addItem(QListWidgetItem(f'-{ch} = {vl}'))
                
                self.listWidget.addItem(QListWidgetItem(f''))
        
        # Variável que armazena lista de unidades de saúde retornada da classe Bfa e método pegar_unidades
        unidades_saude = bfa.pegar_unidades(diretorio)   

        # Adiciona no combobox da tela a lista de unidades de saúde
        self.cb_unidade.addItems(unidades_saude)
        
        self.cb_unidade.setEnabled(True)
        self.cb_situacao.setEnabled(True)
        self.cb_profissional.setEnabled(True)  
        self.btn_gerar_relatorio.setEnabled(True)

        self.gerar_relatorio()

if __name__ == '__main__':
    qt = QApplication(sys.argv)
    app = JanelaPrincipal()
    app.show()
    sys.exit(qt.exec())
