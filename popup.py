from banco import DataBase, Tabela
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QInputDialog, QApplication)
import sys

class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):

        self.btnCreate = QPushButton('CREATE TABLE', self)
        self.btnCreate.move(20, 20)
        self.btnCreate.setFixedSize(100, 20)
        self.btnCreate.clicked.connect(self.createTable)

        self.btnDel = QPushButton('DELETE TABLE', self)
        self.btnDel.move(20, 50)
        self.btnDel.setFixedSize(100, 20)
        self.btnDel.clicked.connect(self.deleteTable)

        self.btnBackup = QPushButton('BACKUP', self)
        self.btnBackup.move(20, 80)
        self.btnBackup.setFixedSize(100, 20)
        self.btnBackup.clicked.connect(self.backup)

        self.btnRestaura = QPushButton('RESTAURA', self)
        self.btnRestaura.move(20, 110)
        self.btnRestaura.setFixedSize(100, 20)
        self.btnRestaura.clicked.connect(self.restaura)

        self.btnListaBackups =QPushButton('LISTAR', self)
        self.btnListaBackups.move(20, 140)
        self.btnListaBackups.setFixedSize(100, 20)
        self.btnListaBackups.clicked.connect(self.lista_backup)

        self.db = DataBase()
        self.table = Tabela('users', 'email', self.db)

        self.teste()
        self.show()
        
    def createTable(self):
        self.btnCreate.setEnabled(0)
        self.db.create_table('users', 'email', 5, 5)
        self.sairApp(1)

    def deleteTable(self):
        #Deve ser implementado de outra forma, acessando a clase DataBase()
        #gambiarra
        import boto3
        table = boto3.resource('dynamodb').Table('users')
        table.delete()
        
        #self.db.delete_table(self.table)
        #self.table.delete_table(self.table)
        self.sairApp(2)
    
    def backup(self):
        print(self.db.faz_backup('users'))
    
    def restaura(self):
        print(self.db.restaura_backup())
    
    def lista_backup(self):
        print(self.db.lista_backups('users'))
    
    def teste(self):
        if 'users' not in self.db.tabelas():
            self.btnDel.setEnabled(0)
        else:
            self.btnCreate.setEnabled(0)

    def sairApp(self, code):
        sys.exit(code)
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
