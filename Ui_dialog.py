# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Lucas\Documents\MEGAsync\Universidade\Terceiro Ano\Banco de dados\DynamoProjeto\dialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.setEnabled(True)
        Dialog.resize(621, 439)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setVerticalSpacing(10)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.leNome = QtWidgets.QLineEdit(Dialog)
        self.leNome.setObjectName("leNome")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.leNome)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.leSobrenome = QtWidgets.QLineEdit(Dialog)
        self.leSobrenome.setObjectName("leSobrenome")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.leSobrenome)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.leUsername = QtWidgets.QLineEdit(Dialog)
        self.leUsername.setObjectName("leUsername")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.leUsername)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.leEmail = QtWidgets.QLineEdit(Dialog)
        self.leEmail.setObjectName("leEmail")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.leEmail)
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.cbConta = QtWidgets.QComboBox(Dialog)
        self.cbConta.setObjectName("cbConta")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.cbConta)
        self.horizontalLayout.addLayout(self.formLayout)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout.setSpacing(8)
        self.verticalLayout.setObjectName("verticalLayout")
        self.btnSalvar = QtWidgets.QPushButton(Dialog)
        self.btnSalvar.setDefault(True)
        self.btnSalvar.setObjectName("btnSalvar")
        self.verticalLayout.addWidget(self.btnSalvar)
        self.btnDel = QtWidgets.QPushButton(Dialog)
        self.btnDel.setObjectName("btnDel")
        self.verticalLayout.addWidget(self.btnDel)
        self.btnSair = QtWidgets.QPushButton(Dialog)
        self.btnSair.setObjectName("btnSair")
        self.verticalLayout.addWidget(self.btnSair)
        self.btnDiscard = QtWidgets.QPushButton(Dialog)
        self.btnDiscard.setObjectName("btnDiscard")
        self.verticalLayout.addWidget(self.btnDiscard)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btnTables = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnTables.sizePolicy().hasHeightForWidth())
        self.btnTables.setSizePolicy(sizePolicy)
        self.btnTables.setMaximumSize(QtCore.QSize(30, 20))
        self.btnTables.setDefault(False)
        self.btnTables.setFlat(False)
        self.btnTables.setObjectName("btnTables")
        self.horizontalLayout_2.addWidget(self.btnTables)
        self.btnRefresh = QtWidgets.QPushButton(Dialog)
        self.btnRefresh.setMaximumSize(QtCore.QSize(30, 20))
        self.btnRefresh.setObjectName("btnRefresh")
        self.horizontalLayout_2.addWidget(self.btnRefresh)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout_3, 2, 0, 1, 1)
        self.tblWidget = QtWidgets.QTableWidget(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tblWidget.sizePolicy().hasHeightForWidth())
        self.tblWidget.setSizePolicy(sizePolicy)
        self.tblWidget.setObjectName("tblWidget")
        self.tblWidget.setColumnCount(2)
        self.tblWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tblWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblWidget.setHorizontalHeaderItem(1, item)
        self.tblWidget.horizontalHeader().setDefaultSectionSize(300)
        self.gridLayout.addWidget(self.tblWidget, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.leNome, self.leSobrenome)
        Dialog.setTabOrder(self.leSobrenome, self.leUsername)
        Dialog.setTabOrder(self.leUsername, self.leEmail)
        Dialog.setTabOrder(self.leEmail, self.cbConta)
        Dialog.setTabOrder(self.cbConta, self.btnSalvar)
        Dialog.setTabOrder(self.btnSalvar, self.btnDel)
        Dialog.setTabOrder(self.btnDel, self.btnSair)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "CRUD Amazon DynamoDB"))
        self.label.setText(_translate("Dialog", "Nome"))
        self.label_2.setText(_translate("Dialog", "Sobrenome"))
        self.label_3.setText(_translate("Dialog", "Username"))
        self.label_4.setText(_translate("Dialog", "email"))
        self.label_5.setText(_translate("Dialog", "Tipo de Conta"))
        self.btnSalvar.setText(_translate("Dialog", "Salvar"))
        self.btnDel.setText(_translate("Dialog", "Apagar"))
        self.btnSair.setText(_translate("Dialog", "Sair"))
        self.btnDiscard.setText(_translate("Dialog", "Descartar"))
        self.btnTables.setText(_translate("Dialog", "..."))
        self.btnRefresh.setText(_translate("Dialog", "R"))
        item = self.tblWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Username"))
        item = self.tblWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Email"))

