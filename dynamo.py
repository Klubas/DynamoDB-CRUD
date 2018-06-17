#!/usr/bin/python
import _thread
from time import sleep
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QInputDialog, QApplication)
import sys, boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')

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

        #self.btn = QInputDialog()

        self.teste()

        self.show()
        
    def createTable(self):
        try:
            #_thread.start_new_thread(self.btnCreate.setEnabled, (0, ))
            self.btnCreate.setEnabled(0)
            sleep(5)
            #_thread.start_new_thread(self.thread_create_table, ('users', ))
            self.thread_create_table('users')

            # Wait until the table exists.
            table.meta.client.get_waiter('table_exists').wait(TableName='users')
        except Exception as e:
            print(e)
            self.teste()
        self.sairApp(1)

    def thread_create_table(self, nome):
        table = dynamodb.create_table(
        TableName=nome,
        KeySchema=[
            {
                'AttributeName': 'email',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'email',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    def deleteTable(self):
        try:
            table.delete()
            self.setEnabled(0)
        except Exception as e:
            self.teste()
            print(e)
        self.sairApp(2)

    def teste(self):
        if 'users' not in boto3.client('dynamodb').list_tables()['TableNames']:
            self.btnDel.setEnabled(0)
        else:
            self.btnCreate.setEnabled(0)

    def sairApp(self, code):
        sys.exit(code)
        
    
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
