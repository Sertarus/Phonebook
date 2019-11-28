import re

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlQuery, QSqlDatabase
from PyQt5.QtWidgets import QAbstractItemView, QTableWidgetItem


class PhonebookWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(874, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(130, 100, 574, 221))
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(["Full name", "Number", "Country", "Town", "Street", "Home number"])
        self.db = QSqlDatabase.addDatabase("QODBC")
        self.db.setDatabaseName(r"DRIVER={Driver do Microsoft Access (*.mdb)};\
                            FIL={MS Access}; DBQ=C:\Users\User\IdeaProjects\CourseWork\src\main\Resources\Database1.mdb")
        self.db.open()
        self.refill_table()
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.name_input = QtWidgets.QLineEdit(self.centralwidget)
        self.name_input.setGeometry(QtCore.QRect(130, 370, 121, 31))
        self.name_label = QtWidgets.QLabel(self.centralwidget)
        self.name_label.setGeometry(QtCore.QRect(150, 410, 81, 16))
        self.number_label = QtWidgets.QLabel(self.centralwidget)
        self.number_label.setGeometry(QtCore.QRect(300, 410, 81, 16))
        self.number_input = QtWidgets.QLineEdit(self.centralwidget)
        self.number_input.setGeometry(QtCore.QRect(280, 370, 121, 31))
        self.country_input = QtWidgets.QLineEdit(self.centralwidget)
        self.country_input.setGeometry(QtCore.QRect(430, 370, 121, 31))
        self.country_label = QtWidgets.QLabel(self.centralwidget)
        self.country_label.setGeometry(QtCore.QRect(450, 410, 81, 16))
        self.town_label = QtWidgets.QLabel(self.centralwidget)
        self.town_label.setGeometry(QtCore.QRect(600, 410, 81, 16))
        self.town_input = QtWidgets.QLineEdit(self.centralwidget)
        self.town_input.setGeometry(QtCore.QRect(580, 370, 121, 31))
        self.street_input = QtWidgets.QLineEdit(self.centralwidget)
        self.street_input.setGeometry(QtCore.QRect(280, 440, 121, 31))
        self.street_label = QtWidgets.QLabel(self.centralwidget)
        self.street_label.setGeometry(QtCore.QRect(300, 480, 81, 16))
        self.home_number_input = QtWidgets.QLineEdit(self.centralwidget)
        self.home_number_input.setGeometry(QtCore.QRect(430, 440, 121, 31))
        self.home_number_label = QtWidgets.QLabel(self.centralwidget)
        self.home_number_label.setGeometry(QtCore.QRect(450, 480, 81, 16))
        self.error_label = QtWidgets.QLabel(self.centralwidget)
        self.error_label.setGeometry(QtCore.QRect(400, 520, 150, 16))
        self.add_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_button.setGeometry(QtCore.QRect(760, 370, 75, 23))
        self.add_button.pressed.connect(self.add_row)
        self.delete_button = QtWidgets.QPushButton(self.centralwidget)
        self.delete_button.setGeometry(QtCore.QRect(760, 160, 81, 23))
        self.delete_button.pressed.connect(self.delete_row)
        self.find_button = QtWidgets.QPushButton(self.centralwidget)
        self.find_button.setGeometry(QtCore.QRect(760, 440, 75, 23))
        self.find_button.pressed.connect(self.find_row)
        self.full_list_button = QtWidgets.QPushButton(self.centralwidget)
        self.full_list_button.setGeometry(QtCore.QRect(760, 200, 81, 23))
        self.full_list_button.pressed.connect(self.refill_table)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        self.name_label.setText(_translate("MainWindow", "Full name"))
        self.number_label.setText(_translate("MainWindow", "Number"))
        self.country_label.setText(_translate("MainWindow", "Country"))
        self.town_label.setText(_translate("MainWindow", "Town"))
        self.street_label.setText(_translate("MainWindow", "Street"))
        self.home_number_label.setText(_translate("MainWindow", "Home number"))
        self.add_button.setText(_translate("MainWindow", "Add"))
        self.delete_button.setText(_translate("MainWindow", "Delete current"))
        self.find_button.setText(_translate("MainWindow", "Find"))
        self.full_list_button.setText(_translate("MainWindow", "Full list"))

    def refill_table(self):
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.clear()
        self.tableWidget.setHorizontalHeaderLabels(["Full name", "Number", "Country", "Town", "Street", "Home number"])
        query = QSqlQuery(self.db)
        query.exec("SELECT COUNT(*) FROM Numbers")
        query.next()
        self.tableWidget.setRowCount(query.value(0))
        query.exec("SELECT * FROM Numbers")
        counter = 0
        while query.next():
            self.tableWidget.setItem(counter, 1, QTableWidgetItem(query.value(1)))
            second_query = QSqlQuery(self.db)
            second_query.exec("SELECT * FROM People WHERE ID={}".format(query.value(2)))
            while second_query.next():
                self.tableWidget.setItem(counter, 0, QTableWidgetItem(second_query.value(1)))
                third_query = QSqlQuery(self.db)
                third_query.exec("SELECT * FROM Locations WHERE ID={}".format(second_query.value(2)))
                while third_query.next():
                    self.tableWidget.setItem(counter, 2, QTableWidgetItem(third_query.value(1)))
                    self.tableWidget.setItem(counter, 3, QTableWidgetItem(third_query.value(2)))
                    self.tableWidget.setItem(counter, 4, QTableWidgetItem(third_query.value(3)))
                    self.tableWidget.setItem(counter, 5, QTableWidgetItem(third_query.value(4)))
            counter += 1
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.sortItems(0, Qt.AscendingOrder)

    def delete_row(self):
        query = QSqlQuery(self.db)
        current_phone_number = self.tableWidget.item(self.tableWidget.currentRow(), 1).text()
        query.exec("SELECT P_ID FROM Numbers WHERE Number='{}'".format(current_phone_number))
        query.next()
        current_p_id = query.value(0)
        query.exec("SELECT COUNT(*) FROM Numbers WHERE P_ID={}".format(current_p_id))
        query.next()
        if query.value(0) != 1:
            query.exec("DELETE FROM Numbers WHERE Number='{}'".format(current_phone_number))
        else:
            query.exec("SELECT * FROM Numbers WHERE Number='{}'".format(current_phone_number))
            query.next()
            current_p_id = query.value(2)
            query.exec("DELETE FROM Numbers WHERE Number='{}'".format(current_phone_number))
            query.exec("SELECT * FROM People WHERE ID={}".format(current_p_id))
            query.next()
            current_l_id = query.value(2)
            query.exec("SELECT COUNT(*) FROM People WHERE L_ID={}".format(current_l_id))
            query.next()
            if query.value(0) != 1:
                query.exec("DELETE FROM People WHERE ID={}".format(current_p_id))
            else:
                query.exec("DELETE FROM People WHERE ID={}".format(current_p_id))
                query.exec("DELETE FROM Locations WHERE ID={}".format(current_l_id))
        self.refill_table()

    def add_row(self):
        name = ""
        number = ""
        country = ""
        town = ""
        street = ""
        home_number = ""
        if re.match(r'(\D+\s*)+', self.name_input.text()) is not None:
            name = self.name_input.text()
        else:
            self.error_label.setText("Incorrect name")
        if re.match(r'\+\d\(\d\d\d\)\s*\d\d\d-\d\d\d\d', self.number_input.text()) is not None:
            number = self.number_input.text()
        else:
            self.error_label.setText("Incorrect number")
        if re.match(r"([A-Z]|[А-Я])+", self.country_input.text()) is not None:
            country = self.country_input.text()
        else:
            self.error_label.setText("Incorrect country")
        if re.match(r"([A-Z]|[А-Я])+", self.town_input.text()) is not None:
            town = self.town_input.text()
        else:
            self.error_label.setText("Incorrect town")
        if re.match(r"([A-Z]|[А-Я])+", self.street_input.text()) is not None:
            street = self.street_input.text()
        else:
            self.error_label.setText("Incorrect street")
        if re.match(r'\d+', self.home_number_input.text()) is not None:
            home_number = self.home_number_input.text()
        else:
            self.error_label.setText("Incorrect Home number")
        query = QSqlQuery(self.db)
        query.exec("SELECT COUNT(*) FROM Numbers WHERE Number='{}'".format(number))
        query.next()
        if name != "" and number != "" and country != "" and town != "" and street != "" and home_number != "" and \
                query.value(0) == 0:
            query.exec("SELECT ID FROM Locations WHERE Country='{0}' AND Town='{1}' AND"
                       " Street='{2}' AND [HomeNumber]='{3}'".format(country, town, street, home_number))
            query.next()
            if query.value(0) is None:
                query.exec("INSERT INTO Locations(Country, Town, Street, [HomeNumber]) "
                           "VALUES('{0}', '{1}', '{2}', '{3}')".format(country, town, street, home_number))
                query.exec("SELECT @@IDENTITY")
                query.next()
            current_l_id = query.value(0)
            query.exec("INSERT INTO People([FullName], L_ID) VALUES ('{0}', {1})".format(name, current_l_id))
            query.exec("SELECT @@IDENTITY")
            query.next()
            current_p_id = query.value(0)
            query.exec("INSERT INTO Numbers([Number], P_ID) VALUES ('{0}', {1})".format(number, current_p_id))
            self.refill_table()
            self.error_label.setText("")

    def find_row(self):
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(["Full name", "Number", "Country", "Town", "Street", "Home number"])
        name = self.name_input.text()
        number = self.number_input.text()
        country = self.country_input.text()
        town = self.town_input.text()
        street = self.street_input.text()
        home_number = self.home_number_input.text()
        query = QSqlQuery(self.db)
        query.exec("SELECT * FROM Numbers WHERE Number LIKE '%{}%'".format(number))
        while query.next():
            current_number = query.value(1)
            current_number_id = query.value(2)
            second_query = QSqlQuery(self.db)
            second_query.exec("SELECT * FROM People WHERE FullName LIKE '%{0}%' AND"
                              " ID={1}".format(name, current_number_id))
            while second_query.next():
                current_name = second_query.value(1)
                current_name_id = second_query.value(2)
                third_query = QSqlQuery(self.db)
                third_query.exec("SELECT * FROM Locations WHERE Country LIKE '%{0}%' AND"
                                 " Town LIKE '%{1}%' AND Street LIKE '%{2}%' AND"
                                 " HomeNumber LIKE '%{3}%'"
                                 " AND ID={4}".format(country, town, street, home_number, current_name_id))
                while third_query.next():
                    row_position = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(row_position)
                    self.tableWidget.setItem(row_position, 0, QTableWidgetItem(current_name))
                    self.tableWidget.setItem(row_position, 1, QTableWidgetItem(current_number))
                    self.tableWidget.setItem(row_position, 2, QTableWidgetItem(third_query.value(1)))
                    self.tableWidget.setItem(row_position, 3, QTableWidgetItem(third_query.value(2)))
                    self.tableWidget.setItem(row_position, 4, QTableWidgetItem(third_query.value(3)))
                    self.tableWidget.setItem(row_position, 5, QTableWidgetItem(third_query.value(4)))
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.sortItems(0, Qt.AscendingOrder)