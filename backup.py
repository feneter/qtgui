import sys

from PyQt5.QtWidgets import (QPushButton, QMainWindow, QWidget, QVBoxLayout, QFileDialog, QApplication,
                                QCheckBox)
from PyQt5.QtGui import QIcon

from lib.db_handler_fn import insert_data, get_data, create_table
from lib.utils import home_directory


class BackupApp(QWidget):

    def __init__(self):
        super().__init__()
        # self.db_handler = DBHandler("backup_config.db")
        # create_table()
        self.vbox = QVBoxLayout()
        selectButton = QPushButton("Add folder to backup", self)
        selectButton.clicked.connect(self.select_directory)
        self.vbox.addWidget(selectButton)
        self.pre_load_data()
        self.setLayout(self.vbox) 
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Backup: Select Folders')    
        self.show()
    
    def select_directory(self):
        selected_dir = QFileDialog.getExistingDirectory(parent=self, caption="Select a directory to backup", directory=home_directory)
        # add to db
        # add to layout
        if not selected_dir: # imagine user closed/cancelled dialog without selecting a folder
            return
        chkbox = QCheckBox(selected_dir, self)
        insert_data("backup", selected_dir)
        chkbox.setChecked(True)
        chkbox.stateChanged.connect(self.save)
        self.vbox.addWidget(chkbox)

    def save(self, state):
        if state == 2: #  button is checked
            insert_data("backup", self.sender().text())
            # self.db_handler.insert("backup_config", filename=self.sender().text())
        elif state == 0:
            print(f"Button  unhecked for: {self.sender().text()}")
            # self.db_handler.delete("backup_config", filename=self.sender().text())
        else:
            print("There's no way to handle tristates for now")

    def pre_load_data(self):
        files = get_data()
        if not files:
            return

        for f in files:
            bk_file, = f
            chkbox = QCheckBox(bk_file, self)
            chkbox.setChecked(True)
            chkbox.stateChanged.connect(self.save)
            self.vbox.addWidget(chkbox)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = BackupApp()
    sys.exit(app.exec_())