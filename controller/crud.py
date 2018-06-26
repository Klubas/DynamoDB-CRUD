import datetime
import sys
sys.path.append('..')

from time import sleep
from model.user import User

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QAbstractItemView, QApplication, QDialog,
                             QLineEdit, QPushButton, QTableWidget,
                             QTableWidgetItem, QWidget)

from model.banco import DataBase, Tabela
from model.my_thread import myThread
from view.Ui_dialog import Ui_Dialog

username_col = 0
email_col = 1

class AppWindow(QDialog, Ui_Dialog):

    def __init__(self):
        super().__init__()

        self.db = DataBase()
        self.dbtable = Tabela('users', 'email', self.db)
        self.user_sel = User()

        self.setupUi(self)

        self.btnSalvar.clicked.connect(self.salvarItem)
        self.btnDel.clicked.connect(self.deleteTableItem)
        self.btnSair.clicked.connect(self.sairApp)
        self.tblWidget.cellDoubleClicked.connect(self.preencherCampos)
        self.btnDiscard.clicked.connect(self.limpaCampos)
        self.btnTables.clicked.connect(self.nova_thread)
        self.btnRefresh.clicked.connect(self.updateTblVw)

        self.cbConta.addItems(['DESATIVADO', 'USUARIO', 'ADMIN'])

        self.tblWidget.setShowGrid(0)
        self.tblWidget.verticalHeader().setVisible(0)
        self.tblWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tblWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.updateTblVw()

        self.btnDel.setEnabled(0)

        self.showNormal()

    def preencherCampos(self):
        email_sel = self.tblWidget.item(self.tblWidget.currentRow(), email_col).text()

        self.user_sel = self.dbtable.query_data_table(email_sel)  

        self.leUsername.setText(self.user_sel.username)
        self.leNome.setText(self.user_sel.first_name)
        self.leSobrenome.setText(self.user_sel.last_name)
        self.leEmail.setText(self.user_sel.email)

        self.leEmail.setEnabled(0)
        self.btnDel.setEnabled(1)
        self.btnSalvar.setText('Atualizar')
        
        if self.user_sel.conta == "ADMIN":
            self.cbConta.setCurrentIndex(2)
        elif self.user_sel.conta == "USUARIO":
            self.cbConta.setCurrentIndex(1)
        else:
            self.cbConta.setCurrentIndex(0)
    
    def salvarItem(self):
    #testa se existe
        if self.leNome.text() != '' and self.leEmail.text() != '' and self.leSobrenome.text() != '' and self.leUsername.text() != '' :
            
            self.user_sel = self.dbtable.query_data_table(self.user_sel.email)

            self.user_sel.username = self.leUsername.text()
            self.user_sel.first_name = self.leNome.text()
            self.user_sel.last_name = self.leSobrenome.text()
            self.user_sel.conta = self.cbConta.currentText()

            if self.user_sel.emailVazio():
                self.user_sel.email = self.leEmail.text()
                if self.dbtable.create(self.user_sel) == -2:
                    return
            elif not self.leEmail.isEnabled():
                if self.dbtable.update(self.user_sel) == -1:
                    return

            self.limpaCampos()
            self.updateTblVw()
    
    def deleteTableItem(self):
        self.dbtable.delete(self.user_sel.email)
        self.updateTblVw()
        self.limpaCampos()

    def updateTblVw(self):
        if 'users' in self.db.tabelas():
            response = self.dbtable.scan_ne('conta', 0)
            self.tblWidget.setRowCount(len(response['Items']))
            self.tblWidget.setColumnCount(2)
    
            j = 0
            for i in response['Items']:
                self.tblWidget.setItem(j, username_col, QTableWidgetItem(i['username']))
                self.tblWidget.setItem(j, email_col , QTableWidgetItem(i['email']))
                j = j + 1
            
            self.tblWidget.sortItems(username_col, Qt.AscendingOrder)
            self.user_sel = User()
        else:
            self.tblWidget.clearContents()
            self.btnSalvar.setEnabled(0)

    def limpaCampos(self):
        self.user_sel = User()
        self.leUsername.setText('')
        self.leNome.setText('')
        self.leSobrenome.setText('')
        self.leEmail.setText('')
        self.cbConta.setCurrentIndex(0)
        self.btnDel.setEnabled(0)
        self.btnSalvar.setText('Salvar')
        self.leEmail.setEnabled(1)
        
  #esse procedimento é pura e completa gambiarra
    def nova_thread(self, nome):
        try:
            ativo = self.isEnabled()
            self.btnSalvar.setEnabled(0)
            thread = myThread(0, 'popup.py')
            thread.start()
            while thread.is_alive(): pass
            s = thread.returnCode
            print(s)
            if s == 2: #delete table
                self.btnSalvar.setEnabled(0)
            elif s == 1: #create table
                self.btnSalvar.setEnabled(1)
            else:   #exit
                self.btnSalvar.setEnabled(ativo)
            sleep(2)
            self.updateTblVw()
        except Exception as e:
            print(e)

    def sairApp(self):
        sys.exit()

