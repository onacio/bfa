import sys
from PyQt6.QtWidgets import *
from tela_principal import Ui_MainWindow
from Bfa import Bfa


class JanelaPrincipal(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()        
        self.setupUi(self)
        self.btn_relatorio.setEnabled(False)
        self.btn_abrir.clicked.connect(self.abrir_arquivo)
        self.btn_relatorio.clicked.connect(self.percentual)

    def abrir_arquivo(self):
        arquivo = QFileDialog.getOpenFileName(filter='*.xls')
        
        self.lbl_caminho.setText(arquivo[0])
        self.listWidget.clear()
        
        bfa = Bfa(arquivo[0])
        
        lista = bfa.informacoes()
        count = 0
        for chave, valor in lista.items():
            self.listWidget.addItem(QListWidgetItem(f'{chave} = {valor}'))
            count += valor
        
        percentual = (lista['Acompanhados'] / count) * 100
        self.listWidget.addItem(f'Total = {count}')
        self.listWidget.addItem('Percentual de acompanhamento = {:.2f}%'.format(percentual))

        self.btn_relatorio.setEnabled(True)
    
    # Método criado para testar o método da classe Bfa que retorna o percentual de acompahados
    def percentual(self):
        caminho = self.lbl_caminho.text()
        bfa = Bfa(caminho)
        print(bfa.percentual())
        

if __name__ == '__main__':
    qt = QApplication(sys.argv)
    app = JanelaPrincipal()
    app.show()
    sys.exit(qt.exec())
