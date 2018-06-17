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
uuid_col = 1

class UUID():
    def __init__(self):
        self.uuid = '0'
        
    def getUUID(self):
        return self.uuid

    def setUUID(self, arg):
        self.uuid = arg
    
    def resetUUID(self):
        self.uuid = '0'
    
    def isUUID(self):
        if self.uuid == '0':
            return 0
        else: 
            return 1

class myThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        s = subprocess.Popen(["python", self.name], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        s.wait()
        return s.returncode

class AppWindow(QDialog, Ui_Dialog):

    def __init__(self):
        super().__init__()

        global uuid_sel
        uuid_sel = UUID()

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

        self.lbUUID.setText(uuid_sel.getUUID())
        self.btnDel.setEnabled(0)

        self.showNormal()


    def preencherCampos(self):
        uuid_sel.setUUID(self.tblWidget.item(self.tblWidget.currentRow(), uuid_col).text())

        response = table.query(
            KeyConditionExpression=Key('UUID').eq(uuid_sel.getUUID())
        )
        items = response['Items'][0]  #"matriz tridimensional"
    
        self.leUsername.setText(items['username'])
        self.leNome.setText(items['first_name'])
        self.leSobrenome.setText(items['last_name'])
        self.leEmail.setText(items['email'])

        self.btnSalvar.setText('Atualizar')
        self.btnDel.setEnabled(1)

        if items['conta'] == "ADMIN":
            self.cbConta.setCurrentIndex(2)
        elif items['conta'] == "USUARIO":
            self.cbConta.setCurrentIndex(1)
        else:
            self.cbConta.setCurrentIndex(0)
            
        self.lbUUID.setText(uuid_sel.getUUID())

    
    def salvarItem(self):
    #testa se existe
        if (self.leNome.text() != '' and self.leEmail.text() != '' 
            and self.leSobrenome.text() != '' and self.leUsername.text() != ''):
            if table.query(KeyConditionExpression=Key('UUID').eq(uuid_sel.getUUID()))['Items']:
                self.update()
            elif not uuid_sel.isUUID():
                self.create()
            self.limpaCampos()
            self.updateTblVw()
    
    def create(self):
        table.put_item(
            Item={
                'UUID': repr(datetime.datetime.now().timestamp()).replace(".", ""),
                'username': self.leUsername.text(),
                'first_name': self.leNome.text(),
                'last_name': self.leSobrenome.text(),
                'email': self.leEmail.text(),
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
            Key={'UUID': uuid_sel.getUUID()},
            UpdateExpression='SET username = :val1 , first_name = :val2 , last_name = :val3 , conta = :val4 , email = :val5',
            ExpressionAttributeValues={
                ':val1': self.leUsername.text(),
                ':val2': self.leNome.text(),
                ':val3': self.leSobrenome.text(),
                ':val4': self.cbConta.currentText(),
                ':val5': self.leEmail.text()
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
                self.tblWidget.setItem(j ,uuid_col , QTableWidgetItem(i['UUID']))
                j = j + 1
            
            self.tblWidget.sortItems(username_col, Qt.AscendingOrder)
        else:
            self.tblWidget.clearContents()
            self.nova_thread()

    def limpaCampos(self):
        uuid_sel.resetUUID()
        self.leUsername.setText('')
        self.leNome.setText('')
        self.leSobrenome.setText('')
        self.leEmail.setText('')
        self.cbConta.setCurrentIndex(0)
        self.lbUUID.setText(uuid_sel.getUUID())
        self.btnDel.setEnabled(0)
        self.btnSalvar.setText('Salvar')
    
    def nova_thread(self):
        self.threader('dynamo.py')

    def threader(self, nome):
        try:
            ativo = self.isEnabled()
            self.setEnabled(0)
            thread = myThread(0, nome)
            s = thread.run()
            print(s)
            if s == 2: #delete table
                self.setEnabled(0)
            elif s == 1: #create table
                self.setEnabled(1)
            else:   #exit
                self.setEnabled(ativo)
            sleep(2)
            self.updateTblVw()
        except Exception as e:
            print(e)

    def deleteTableItem(self):
        table.delete_item(
            Key={
                'UUID': uuid_sel.getUUID()
            }
        )
        self.updateTblVw()
        self.limpaCampos()

    def sairApp(self):
        sys.exit()

app = QApplication(sys.argv)
w = AppWindow()
sys.exit(app.exec_())