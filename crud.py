import sys, subprocess, boto3, datetime, threading
import subprocess
from time import sleep
from boto3 import resource
from boto3.dynamodb.conditions import Key, Attr
from PyQt5.QtWidgets import (QDialog, QApplication, QWidget, QPushButton, QLineEdit, QTableWidgetItem, QTableWidget, QAbstractItemView)
from PyQt5.QtCore import Qt
from Ui_dialog import Ui_Dialog

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')

username_col = 0
email_col = 1

class User():
    def __init__(self):
        self.email = ''
        
    def getEmail(self):
        return self.email

    def setEmail(self, arg):
        self.email = arg
    
    def resetEmail(self):
        self.email = ''

class myThread (threading.Thread):
    def __init__(self, threadID, value):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.value = value
        self.returnCode = -1
    def run(self):
        s = subprocess.Popen(["python", self.value])
        s.wait()
        self.returnCode = s.returncode


class AppWindow(QDialog, Ui_Dialog):

    def __init__(self):
        super().__init__()

        global user_sel
        user_sel = User()

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
        user_sel.setEmail(self.tblWidget.item(self.tblWidget.currentRow(), email_col).text())

        response = table.query(
            KeyConditionExpression=Key('email').eq(user_sel.getEmail())
        )
        items = response['Items'][0]  #"matriz tridimensional"
    
        self.leUsername.setText(items['username'])
        self.leNome.setText(items['first_name'])
        self.leSobrenome.setText(items['last_name'])
        self.leEmail.setText(items['email'])

        self.leEmail.setEnabled(0)

        self.btnSalvar.setText('Atualizar')
        self.btnDel.setEnabled(1)

        if items['conta'] == "ADMIN":
            self.cbConta.setCurrentIndex(2)
        elif items['conta'] == "USUARIO":
            self.cbConta.setCurrentIndex(1)
        else:
            self.cbConta.setCurrentIndex(0)

    
    def salvarItem(self):
    #testa se existe
        if (self.leNome.text() != '' and self.leEmail.text() != '' 
            and self.leSobrenome.text() != '' and self.leUsername.text() != ''):
            if table.query(KeyConditionExpression=Key('email').eq(user_sel.getEmail()))['Items']:
                self.update()
            elif user_sel.getEmail() == '':
                self.create()
            self.limpaCampos()
            self.updateTblVw()
    
    def create(self):
        table.put_item(
            Item={
                'email': self.leEmail.text(),
                'username': self.leUsername.text(),
                'first_name': self.leNome.text(),
                'last_name': self.leSobrenome.text(),
                'conta': self.cbConta.currentText()
            }
        )
        """   SINTAXE DO DYNAMODB    
        {
            TableName: "Music",
            Item: {
                "Artist":"No One You Know",
                "SongTitle":"Call Me Today",
                "AlbumTitle":"Somewhat Famous",
                "Year": 2015,
                "Price": 2.14,
                "Genre": "Country",
                "Tags": {
                    "Composers": [
                        "Smith",
                        "Jones",
                        "Davis"
                    ],
                    "LengthInSeconds": 214
                }
            }
        }
        """

    def update(self):
        table.update_item(
            Key={'email': user_sel.getEmail()},
            UpdateExpression='SET username = :val1 , first_name = :val2 , last_name = :val3 , conta = :val4',
            ExpressionAttributeValues={
                ':val1': self.leUsername.text(),
                ':val2': self.leNome.text(),
                ':val3': self.leSobrenome.text(),
                ':val4': self.cbConta.currentText()
            }
        )
        """
        {
            TableName: "Music",
            Key: {
                "Artist":"No One You Know",
                "SongTitle":"Call Me Today"
            },
            UpdateExpression: "SET RecordLabel = :label",
            ExpressionAttributeValues: { 
                ":label": "Global Records"
            }
        }
        """

    def updateTblVw(self):
        if 'users' in boto3.client('dynamodb').list_tables()['TableNames']:
            response = table.scan(
                FilterExpression=Attr('conta').ne('0')
            )

            self.tblWidget.setRowCount(len(response['Items']))
            self.tblWidget.setColumnCount(2)
    
            j = 0
            for i in response['Items']:
                self.tblWidget.setItem(j ,username_col, QTableWidgetItem(i['username']))
                self.tblWidget.setItem(j ,email_col , QTableWidgetItem(i['email']))
                j = j + 1
            
            self.tblWidget.sortItems(username_col, Qt.AscendingOrder)
        else:
            self.tblWidget.clearContents()
            self.btnSalvar.setEnabled(0)

    def limpaCampos(self):
        user_sel.resetEmail()
        self.leUsername.setText('')
        self.leNome.setText('')
        self.leSobrenome.setText('')
        self.leEmail.setText('')
        self.cbConta.setCurrentIndex(0)
        self.btnDel.setEnabled(0)
        self.btnSalvar.setText('Salvar')
        self.leEmail.setEnabled(1)
    
    def nova_thread(self):
        self.threader('dynamo.py')

    def threader(self, nome):
        try:
            ativo = self.isEnabled()
            self.btnSalvar.setEnabled(0)
            thread = myThread(0, nome)
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

    def deleteTableItem(self):
        table.delete_item(
            Key={
                'email': user_sel.getEmail()
            }
        )
        self.updateTblVw()
        self.limpaCampos()

    def sairApp(self):
        sys.exit()

app = QApplication(sys.argv)
w = AppWindow()
sys.exit(app.exec_())
