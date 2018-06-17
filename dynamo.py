#!/usr/bin/python
import _thread
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

        self.teste()

        self.show()
        
    def createTable(self):
        try:
            nome = 'users'
            table = dynamodb.create_table(
            TableName=nome,
            KeySchema=[
                {
                    'AttributeName': 'UUID',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'UUID',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

            # Wait until the table exists.
            table.meta.client.get_waiter('table_exists').wait(TableName=nome)

        except Exception as e:
            print(e)
        self.sairApp()


    def deleteTable(self):
        try:
            table.delete()
        except Exception as e:
            print(e)
        self.sairApp()

    def teste(self):
        if 'users' not in boto3.client('dynamodb').list_tables()['TableNames']:
            self.btnDel.setEnabled(0)
        else:
            self.btnCreate.setEnabled(0)

    def sairApp(self):
        sys.exit(app.exec_())
        
    
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
