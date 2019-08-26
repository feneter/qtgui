import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QLabel, QLineEdit, QGridLayout
from PyQt5.QtCore import QTimer
import subprocess
from threading import Thread
from time import sleep

class CommandRunner(QWidget):

    def __init__(self):
        super().__init__()
        # create widgets that we need
        self.command_label = QLabel("Command", self)
        self.command_entry = QLineEdit()

        self.target_label = QLabel("Parameters", self)
        self.target_entry = QLineEdit()

        self.output_label = QLabel("Output", self)
        self.output_area = QTextEdit()

        self.run_button = QPushButton("RUN", self)
        # connect run_button to some command on a click event
        self.run_button.clicked.connect(self.run_command)
        # tengeneza layout ya kuweka widgets
        layout = QGridLayout()

        # weka widgets kwenye layout
        layout.addWidget(self.command_label, 0, 0)
        layout.addWidget(self.command_entry, 0, 1)
        layout.addWidget(self.target_label, 1, 0)
        layout.addWidget(self.target_entry, 1, 1)
        layout.addWidget(self.output_label, 2, 0)
        layout.addWidget(self.run_button, 2, 1)
        layout.addWidget(self.output_area, 3, 0, 1, 2)

        # set layout kwa main widget
        self.setLayout(layout)
            
        self.setGeometry(600, 600, 300, 150)
        self.setWindowTitle('Command Runner')    
        self.show()

    def run_command(self):
        '''
        Gets the target address and the command and creates a command to run on the
        target address
        '''
        target = self.target_entry.text().split(' ')
        command = self.command_entry.text()
        args = [command]
        if target:
            for a in target:
                args.append(a)
        self.output_area.clear()
        thread =Thread(target=self.get_command_output, args=(args,), daemon=True)
        thread.start()

    def get_command_output(self, args):
        with subprocess.Popen(args, bufsize=1, stdout=subprocess.PIPE, universal_newlines=True) as proc:
            while True:
                output = proc.stdout.readline()
                if output == '' and proc.poll() is not None:
                    break
                if output:
                    self.output_area.append(output.strip())
                QTimer().start(1000)

if __name__ == '__main__':
    qapp = QApplication(sys.argv)
    command_runner_app = CommandRunner()
    sys.exit(qapp.exec_())
