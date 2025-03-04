import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel
from urllib.request import urlopen
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer

import numpy as np
import cv2
import os


class App(QMainWindow):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))   
    # images 폴더가 없으면 생성
    if not os.path.exists("images"):
            os.mkdir("images")    

    ip = '192.168.137.198'

    def __init__(self):
        super().__init__()
        self.stream = urlopen('http://' + App.ip +':81/stream')
        self.buffer = b""
        urlopen('http://' + App.ip + "/action?go=speed80")
        self.initUI()

    def initUI(self):
        
        widget = QWidget() 

        self.video_label = QLabel(self)
        self.video_label.setGeometry(0, 0, 800, 600)

        # 타이머 설정하여 일정 간격으로 프레임 업데이트
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(5) 

        btn_forward = QPushButton('FORWARD', self)
        btn_forward.resize(100, 50) 

        btn_stop = QPushButton('STOP', self)
        btn_stop.resize(100, 50) 
        
        btn_backward = QPushButton('BACKWARD', self)
        btn_backward.resize(100, 50) 

        btn_forward.pressed.connect(self.forward)

    

        btn_backward.pressed.connect(self.backward)

        btn_backward.released.connect(self.stop)

        hbox = QHBoxLayout() # 가로 방향 레이아웃 
        hbox.addStretch(1) # addStretch : 여백 추가 
        hbox.addWidget(btn_forward) # 요소 추가 
        hbox.addStretch(1)

        hbox.addWidget(btn_stop) # 요소 추가 
        hbox.addStretch(1)

        hbox.addWidget(btn_backward)
        hbox.addStretch(1)

        vbox = QVBoxLayout(widget) # 세로 방향 레이아웃 
        vbox.addWidget(self.video_label) 
        vbox.addLayout(hbox) # 가로 레이아웃을 세로 레이아웃 안에 추가
        vbox.addStretch(1)

        # self 는 현재 MainWindow 
        # 아래 코드는 MainWindow 안에다 Widget 추가하기 코드! 
        self.setCentralWidget(widget)

        self.setWindowTitle('AI CAR CONTROL WINDOW')
        self.move(600, 400)
        self.resize(400, 300)
        self.show()
    
    def update_frame(self):
        self.buffer += self.stream.read(4096)
        head = self.buffer.find(b'\xff\xd8')
        end = self.buffer.find(b'\xff\xd9')

        try: 
            if head > -1 and end > -1:
                jpg = self.buffer[head:end+2]
                self.buffer = self.buffer[end+2:]
                img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
                img = cv2.flip(img, -1) # 이미지 상하반전 

                # OpenCV의 BGR 이미지를 RGB로 변환
                frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                # OpenCV의 이미지를 QImage로 변환
                height, width, channels = frame.shape
                bytes_per_line = 3 * width
                q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)

                # QPixmap을 QLabel에 표시
                pixmap = QPixmap.fromImage(q_image)
                self.video_label.setPixmap(pixmap)
        except Exception as e :
            print(e)

    def closeEvent(self, event):
        event.accept()

    def forward(self) :
        urlopen('http://' + App.ip + "/action?go=forward")
    
    def left(self) :
        urlopen('http://' + App.ip + "/action?go=left")

    def right(self) :
        urlopen('http://' + App.ip + "/action?go=right")

    def backward(self) :
        urlopen('http://' + App.ip + "/action?go=backward")
    
    def stop(self) :
        urlopen('http://' + App.ip + "/action?go=stop")

if __name__ == '__main__':
    print(sys.argv)
    app = QApplication(sys.argv)
    view = App()
    sys.exit(app.exec_())
