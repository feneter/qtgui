import sys
import os

from PyQt5.QtWidgets import (QApplication, QWidget, QAction, qApp, QMenu, QTextEdit, QGridLayout, 
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QDesktopWidget)
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import QFileInfo, Qt, QTimer
import time

root = QFileInfo(__file__).absolutePath()
PICTURES_DIR='/home/fugit/Documents/symmetric-fugit2-path-black' #'/some/dir/name/here' # change this to some directory

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.images = [entry.path for entry in os.scandir(PICTURES_DIR)]
        self.current_image = -1
        self.is_playing = False
        self.is_paused = False
        self.stop = False
        self.initUI()
        self.timer = QTimer()
        self.timer.setInterval(1000)


    @property
    def next_image_location(self):
        if self.current_image == len(self.images) - 1:
            self.current_image = -1
        self.current_image += 1
        return self.images[self.current_image]


    @property
    def prev_image_location(self):
        if self.current_image == 0:
            self.current_image = len(self.images)
        self.current_image -= 1
        return self.images[self.current_image]

        
    @property
    def last_img_location(self):
        return self.images[len(self.images)-1]


    @property
    def first_img_location(self):
        return self.images[0]


    def initUI(self):
        grid = QGridLayout()
        # Controls
        controls_box = QVBoxLayout()
        #controls_box.addStretch(1)
        next_btn = QPushButton('Next', self)
        next_btn.clicked.connect(self.next_img)
        prev_btn = QPushButton('Prev', self)
        prev_btn.clicked.connect(self.prev_img)
        last_btn = QPushButton('Last', self)
        last_btn.clicked.connect(self.last_img)
        first_btn =QPushButton('First', self)
        first_btn.clicked.connect(self.first_img)
        self.play_or_pause_btn = QPushButton('Play', self)
        self.play_or_pause_btn.clicked.connect(self.play_or_pause)

        controls_box.addWidget(next_btn)
        controls_box.addWidget(prev_btn)
        controls_box.addWidget(self.play_or_pause_btn)
        controls_box.addWidget(last_btn)
        controls_box.addWidget(first_btn)

        # image display
        self.img = QLabel(self) # for Q, we can display on image on a Label
        self.img.setScaledContents(True) # to maintain aspect ratio
        self.img.setPixmap(QPixmap(self.next_image_location)) # setting the image to display as Pixmap
        # albums list 
        self.albums = QHBoxLayout()
        #albums.addStretch(1)

        for i in range(1, 5):
            self.albums.addWidget(QPushButton(f"Albamu {i}"))

        #packing
        grid.addWidget(self.img, 1, 0, 5, 1, alignment=Qt.AlignCenter)
        grid.addLayout(controls_box, 1, 1, 5, 1, alignment=Qt.AlignCenter)
        grid.addLayout(self.albums, 6, 0, 1, 2, alignment=Qt.AlignCenter)
        self.setLayout(grid)
        self.setWindowIcon(QIcon(f'{root}/imgs/logo.png'))
        self.setWindowTitle('Albamu ya Picha')
        self.center()
        self.show()

    def next_img(self):
        """Set the next image as Pixmap to display"""
        self.img.setPixmap(QPixmap(self.next_image_location))

    def prev_img(self):
        """Set the previous image as Pixmap to display"""
        self.img.setPixmap(QPixmap(self.prev_image_location))
    
    def last_img(self):
        """Set the last image as Pixmap to display"""
        self.img.setPixmap(QPixmap(self.last_img_location))

    def first_img(self):
        """Set the first image as Pixmap to display"""
        self.img.setPixmap(QPixmap(self.first_img_location))
    
    def play_or_pause(self):
        # the program has just been started
        if not self.is_playing and not self.is_paused:
            self.play_or_pause_btn.setText("Pause")
            # start playing
            self.timer.timeout.connect(self.next_img)
            self.timer.start()
            self.is_playing = True
            self.is_paused = False
        
        # button is clicked when the player is paused, we want the next option 
        # #to be play and we resume playing, and get out of paused status
        elif self.is_playing:
            self.play_or_pause_btn.setText("Play")
            # stop playing
            self.timer.stop()
            self.is_playing = False
            # next command will be Play
            self.is_paused = True
        # button is clicked, and it is playing. we want to pause playing
        elif not self.is_playing:
            self.play_or_pause_btn.setText("Pause")
            # start playing
            self.timer.timeout.connect(self.next_img)
            self.timer.start()
            self.is_playing = True
            # next command is to pause
            self.is_paused = False
        #self.play()

    def play(self):
        while self.is_playing:
            for img in self.images:
                self.img.setPixmap(QPixmap(img))
        else:
            print("No more images")

    def center(self):
        """
        Centers the widget on the screen
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center() # get screen resolution and center point
        qr.moveCenter(cp) # 
        self.move(qr.topLeft())

if __name__ == '__main__':

    app = QApplication(sys.argv)
    album = App()
    sys.exit(app.exec_())
