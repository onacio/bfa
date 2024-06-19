import sys
from PyQt6.QtWidgets import *
from tela_principal import Ui_MainWindow
from bfa import Bfa


class JanelaPrincipal(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()        
        self.setupUi(self)
        self.btn_relatorio.setEnabled(False)
        self.btn_abrir.clicked.connect(self.abrir_arquivo)
        
    def abrir_arquivo(self):        
        diretorio = QFileDialog.getExistingDirectory(self)
        if diretorio:
            bfa = Bfa()
            dados = bfa.consolidar(diretorio)     
            
            self.listWidget.clear()       
            
            for chave, valor in dados.items():                
                self.listWidget.addItem(QListWidgetItem(f'{chave}:'))                
                
                for ch, vl in valor.items():
                    self.listWidget.addItem(QListWidgetItem(f'-{ch} = {vl}'))
                
                self.listWidget.addItem(QListWidgetItem(f''))
     

if __name__ == '__main__':
    qt = QApplication(sys.argv)
    app = JanelaPrincipal()
    app.show()
    sys.exit(qt.exec())
