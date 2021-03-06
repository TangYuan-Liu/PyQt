# -*- coding: cp936 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')
from PyQt4 import QtGui
import os
import sqlite3

class PWKeeper(QtGui.QMainWindow):

    def __init__(self):
        super(PWKeeper, self).__init__()
        self.initToolbar()
        self.initGrid()
        self.current_row = 0
        self.setGeometry(300,300,650,300)
        self.setWindowTitle("PWKeeper")
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.initDB()

    def initToolbar(self):
        newAction = QtGui.QAction(QtGui.QIcon("new.png"),"New",self)
        editAction = QtGui.QAction(QtGui.QIcon("edit.png"),"New",self)
        delAction = QtGui.QAction(QtGui.QIcon("del.png"),"New",self)
        newAction.setShortcut("Ctrl+N")
        editAction.setShortcut("Ctrl+E")
        delAction.setShortcut("Delete")
        newAction.triggered.connect(self.newAction_def)
        editAction.triggered.connect(self.editAction_def)
        delAction.triggered.connect(self.delAction_def)
        self.tb_new = self.addToolBar("New")
        self.tb_edit = self.addToolBar("Edit")
        self.tb_del = self.addToolBar("Del")
        self.tb_new.addAction(newAction)
        self.tb_edit.addAction(editAction)
        self.tb_del.addAction(delAction)

    

    def initGrid(self):
        self.grid = QtGui.QTableWidget()
        self.setCentralWidget(self.grid)
        self.grid.setColumnCount(4)
        self.grid.setRowCount(0)
        column_width = [90, 150, 270, 150]
        for column in range(4):
            self.grid.setColumnWidth(column, column_width[column])

        headerlabels = ["Website", "Username", "Password", "Url"]
        self.grid.setHorizontalHeaderLabels(headerlabels)
        self.grid.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.grid.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

    def showDialog(self, ws = '', un = '', pw = '', url = ''):

        edit_dialog = QtGui.QDialog(self)
        group = QtGui.QGroupBox("Edit Info", edit_dialog)

        lbl_website = QtGui.QLabel("Website:", group)
        le_website = QtGui.QLineEdit(group)
        le_website.setText(ws)
        lbl_username = QtGui.QLabel("Username:", group)
        le_username = QtGui.QLineEdit(group)
        le_username.setText(un)
        lbl_password = QtGui.QLabel("Password:",group)
        le_password = QtGui.QLineEdit(group)
        le_password.setText(pw)
        lbl_url = QtGui.QLabel("Url:",group)
        le_url = QtGui.QLineEdit(group)
        le_url.setText(url)
        ok_button = QtGui.QPushButton("OK",edit_dialog)
        cancel_button = QtGui.QPushButton("CANCEL",edit_dialog)

        ok_button.clicked.connect(edit_dialog.accept)
        ok_button.setDefault(True)
        cancel_button.clicked.connect(edit_dialog.reject)

        group_layout = QtGui.QVBoxLayout()
        group_item = [lbl_website, le_website,
                      lbl_username, le_username,
                      lbl_password, le_password,
                      lbl_url, le_url]

        for item in group_item:
            group_layout.addWidget(item)

        group.setLayout(group_layout)
        group.setFixedSize(group.sizeHint())
        
        button_layout = QtGui.QHBoxLayout()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        dialog_layout = QtGui.QVBoxLayout()
        dialog_layout.addWidget(group)
        dialog_layout.addLayout(button_layout)
        edit_dialog.setLayout(dialog_layout)
        edit_dialog.setFixedSize(edit_dialog.sizeHint())

        if edit_dialog.exec_():
            website = le_website.text()
            username = le_username.text()
            password = le_password.text()
            url = le_url.text()

            return True, website, username, password, url
        
        return False, None, None, None, None
    
    def showHint(self):
        hint_msg = QtGui.QMessageBox()
        hint_msg.setText("NO selected row")
        hint_msg.addButton(QtGui.QMessageBox.Ok)
        hint_msg.exec_()

    def newAction_def(self):
        data = self.showDialog()
        c = self.conn.cursor()
        if data[0]:
            self.current_row += 1
            self.grid.insertRow(self.current_row - 1)
            for i in range(4):
                new_item = QtGui.QTableWidgetItem(data[i + 1])
                self.grid.setItem(self.current_row - 1, i, new_item)
            
            c.execute("INSERT INTO INFO (ID,WEBSITE,USERNAME,PASSWORD,URL) VALUES (%d,'%s','%s','%s','%s')" %(self.current_row, data[1], data[2], data[3], data[4]))     
            #c.execute("INSERT INTO INFO (ID,WEBSITE,USERNAME,PASSWORD,URL) VALUES (1,'baidu','sdfs','sdfsd','asdfsdf')")
            self.conn.commit()
            
            
 
    def editAction_def(self):
        selected_row = self.grid.selectedItems()
        c = self.conn.cursor()
        if selected_row:
            edit_row = self.grid.row(selected_row[0])
            old_data = []
            for i in range(4):
                old_data.append(self.grid.item(edit_row, i).text())
            new_data = self.showDialog(*old_data)

            if new_data[0]:
                for i in range(4):
                    new_item = QtGui.QTableWidgetItem(new_data[i+1])
                    self.grid.setItem(edit_row, i, new_item)
                c.execute("UPDATE INFO SET WEBSITE = '%s',USERNAME = '%s',PASSWORD = '%s',URL = '%s' WHERE ID = '%d'" %(new_data[1],new_data[2],new_data[3],new_data[4],edit_row+1))
                #c.execute("UPDATE INFO SET WEBSITE = 'csrc',USERNAME='mama',PASSWORD='mama',URL='SS' WHERE ID=3")
                self.conn.commit()
                
            else:
                self.showHint()

    def delAction_def(self):
        selected_row = self.grid.selectedItems()
        c = self.conn.cursor()
        if selected_row:
            del_row = self.grid.row(selected_row[0])
            self.grid.removeRow(del_row)
            c.execute("DELETE FROM INFO WHERE ID = %d" % (del_row + 1))
            for index in range(del_row + 2, self.current_row + 1):
                self.conn.execute("UPDATE INFO SET ID = %d WHERE ID = %d" %((index - 1), index))
            self.current_row -= 1
        else:
            self.showHint()

    def initDB(self):
        if os.path.exists("info.db"):
            
            print("Find database")
            self.conn = sqlite3.connect("info.db")    
            self.conn.isolation_level = None
            self.initWindow()
            
               
            
            
            
        else:
            self.conn = sqlite3.connect("info.db")
            self.conn.isolation_level = None
            c = self.conn.cursor()
            c.execute('''CREATE TABLE INFO(ID int PRIMARY KEY NOT NULL,WEBSITE char(255),USERNAME char(255),PASSWORD char(255),URL char(255));''')
            """
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM INFO")
            self.displayData = cur.fetchall()
            cur.close()
            self.current_row = len(self.displayData)
            
            """
            self.conn.commit()


    def initWindow(self):
        c = self.conn.cursor()
        table = c.execute("SELECT ID,WEBSITE,USERNAME,PASSWORD,URL from INFO")
        
        history = []
        for row in table:
            history.append(row)
        
        for i in range(len(history)):
            self.grid.insertRow(i)
            data = history[i]
            for j in range(4):
                new_item = QtGui.QTableWidgetItem(data[j+1])
                self.grid.setItem(i, j, new_item)
        self.current_row = len(history)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    pwk = PWKeeper()
    pwk.show()
    app.exec_()
    pwk.conn.close()
    sys.exit(0)
