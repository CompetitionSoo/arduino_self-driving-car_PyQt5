# 웹캠 Hbox로 만든 PyQt5 화면구현 + 키 입력시 버튼 동작
# https://www.toptal.com/developers/gitignore/  #gitignore 관련

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QGridLayout, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer, Qt

import cv2
import numpy as np
import time

class App(QMainWindow):
    
    ip = '192.168.137.199'

    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        self.initUI()

    def initUI(self):
        
        widget = QWidget() 

        self.video_label = QLabel(self)
        self.video_label.setGeometry(0, 0, 800, 600)

        # 타이머 설정하여 일정 간격으로 프레임 업데이트
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(10) 
        
        # self 는 현재 MainWindow 
        # 아래 코드는 MainWindow 안에다 Widget 추가하기 코드! 
        self.setCentralWidget(widget)
        self.setWindowTitle('강영수의 AI CAR CONTROL WINDOW')
        self.move(600, 400)
        self.resize(400, 300)
        self.show()
        

        btn_speed_40 = QPushButton('속도 40', self)
        btn_speed_40.resize(100, 50) 

        btn_speed_50 = QPushButton('속도 50', self)
        btn_speed_50.resize(100, 50) 

        btn_speed_60 = QPushButton('속도 60', self)
        btn_speed_60.resize(100, 50) 

        btn_speed_80 = QPushButton('속도 80', self)
        btn_speed_80.resize(100, 50) 

        btn_speed_100 = QPushButton('속도 100', self)
        btn_speed_100.resize(100, 50) 

        btn_left_turn = QPushButton('왼쪽으로 돌기', self)
        btn_left_turn.resize(100, 50)

        btn_forward = QPushButton('앞으로', self)
        btn_forward.resize(100, 50)  

        btn_right_turn = QPushButton('오른쪽으로 돌기', self)
        btn_right_turn.resize(100, 50) 

        btn_left = QPushButton('왼쪽', self)
        btn_left.resize(100, 50) 

        btn_stop = QPushButton('멈춤', self)
        btn_stop.resize(100, 50) 

        btn_right = QPushButton('오른쪽', self)
        btn_right.resize(100, 50) 

        btn_harr = QPushButton('Harr',self)
        btn_harr.resize(100,50)

        btn_backward = QPushButton('뒤로가기', self)
        btn_backward.resize(100, 50) 

        btn_line_tracing = QPushButton('라인트레이싱', self)
        btn_line_tracing.resize(100, 50) 

        btn_save = QPushButton('저장하기', self)
        btn_save.resize(100, 50) 
        
        btn_delete = QPushButton('삭제하기', self)
        btn_delete.resize(100, 50) 
        
        self.btn_state = QPushButton('현재상태', self)
        self.btn_state.setDisabled(True)  # 버튼 비활성화
        self.btn_state.resize(100, 50)
        
        
        # 버튼을 이벤트와 연결.
        btn_speed_40.pressed.connect(self.speed_40)
        btn_speed_50.pressed.connect(self.speed_50)
        btn_speed_60.pressed.connect(self.speed_60)
        btn_speed_80.pressed.connect(self.speed_80)
        btn_speed_100.pressed.connect(self.speed_100)

        btn_left_turn.pressed.connect(self.left_turn)
        btn_right_turn.pressed.connect(self.right_turn)

        btn_harr.pressed.connect(self.harr)
        btn_line_tracing.pressed.connect(self.line_tracing)
        btn_save.pressed.connect(self.save)
        btn_delete.pressed.connect(self.delete)

        btn_forward.pressed.connect(self.forward)
        btn_right.pressed.connect(self.right)
        btn_stop.pressed.connect(self.stop)
        btn_left.pressed.connect(self.left)
        btn_backward.pressed.connect(self.backward)

        hbox_speed = QHBoxLayout()
        hbox_speed.addWidget(btn_speed_40)
        hbox_speed.addWidget(btn_speed_50)
        hbox_speed.addWidget(btn_speed_60)
        hbox_speed.addWidget(btn_speed_80)
        hbox_speed.addWidget(btn_speed_100)

        hbox_move_1 = QHBoxLayout()
        hbox_move_1.addWidget(btn_left_turn)
        hbox_move_1.addWidget(btn_forward)
        hbox_move_1.addWidget(btn_right_turn)

        hbox_move_2 = QHBoxLayout()
        hbox_move_2.addWidget(btn_left)
        hbox_move_2.addWidget(btn_stop)
        hbox_move_2.addWidget(btn_right)

        hbox_move_3 = QHBoxLayout()
        hbox_move_3.addWidget(btn_harr)
        hbox_move_3.addWidget(btn_backward)
        hbox_move_3.addWidget(btn_line_tracing)

        hbox_move_4 = QHBoxLayout()
        hbox_move_4.addWidget(btn_save)
        hbox_move_4.addWidget(self.btn_state)
        hbox_move_4.addWidget(btn_delete)
        
        # # 그리드 레이아웃 설정
        # grid = QGridLayout()
        # # 속도관련
        # grid.addWidget(btn_speed_40, 0, 0)
        # grid.addWidget(btn_speed_50, 0, 1)
        # grid.addWidget(btn_speed_60, 0, 2)
        # grid.addWidget(btn_speed_80, 0, 3)
        # grid.addWidget(btn_speed_100, 0, 4)
        
        # # 방향키_1  왼쪽돌기 앞으로가기 오른쪽돌기
        # grid.addWidget(btn_left_turn, 1, 0)  # (row=1, col=0)
        # grid.addWidget(btn_forward, 1, 2)  # (row=1, col=1)
        # grid.addWidget(btn_right_turn, 1, 4)  # (row=1, col=2)
        # # 방향키_2  왼쪽 정지 오른쪽
        # grid.addWidget(btn_left, 2, 0)     # (row=2, col=0)
        # grid.addWidget(btn_stop, 2, 2)     # (row=2, col=1)
        # grid.addWidget(btn_right, 2, 4)    # (row=2, col=2)

        # # 얼굴객체인식, 뒤로가기, 라인트레이싱(자율주행모드)
        # grid.addWidget(btn_harr, 3, 0) # (row=3, col=0)
        # grid.addWidget(btn_backward, 3, 2) # (row=3, col=1)
        # grid.addWidget(btn_line_tracing, 3, 4) # (row=3, col=2)

        # # 저장하기, 삭제하기
        # grid.addWidget(btn_save, 4, 0) # (row=4, col=0)
        # grid.addWidget(btn_delete, 4, 4) # (row=4, col=2)

        vbox = QVBoxLayout(widget) # 세로 방향 레이아웃 
        vbox.addWidget(self.video_label) # 비디오 영상
        #vbox.addLayout(grid) 그리드로 레이아웃을 만들어보았는데 배치가 열의 너비를 조절하기에는 hboxlayout 이 적합해서 주석처리하였습니다.
        vbox.addLayout(hbox_speed) 
        vbox.addStretch(1)
        vbox.addLayout(hbox_move_1) 
        vbox.addStretch(1)
        vbox.addLayout(hbox_move_2) 
        vbox.addStretch(1)
        vbox.addLayout(hbox_move_3) 
        vbox.addStretch(1)
        vbox.addLayout(hbox_move_4) 

    
    def update_status(self, status="대기중"):
        self.btn_state.setText(f'현재상태: {status}')

    def update_frame(self):
        ret, img = self.cap.read()
        if ret :
            try: 
                # OpenCV의 BGR 이미지를 RGB로 변환
                frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                # OpenCV의 이미지를 QImage로 변환
                height, width, _ = frame.shape
                bytes_per_line = 3 * width
                q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)

                # QPixmap을 QLabel에 표시
                pixmap = QPixmap.fromImage(q_image)
                self.video_label.setPixmap(pixmap)
            except Exception as e :
                print(e)
# https://digitalwerk.gitlab.io/solutions/adtf_content/adtf_base/adtf_core/page_qt_key_event_runner.html 키 입력 관련 확인
    def keyPressEvent(self, event):
        print(event.key())
        if event.key() == 16777216:  # ESC 는 27 = close
            self.close()

        elif event.key() == Qt.Key_1:
            self.speed_40()
        
        elif event.key() == Qt.Key_2:
            self.speed_50()
        
        elif event.key() == Qt.Key_3:
            self.speed_60()
        
        elif event.key() == Qt.Key_4:
            self.speed_80()
        
        elif event.key() == Qt.Key_5:
            self.speed_100()

        elif event.key() == 87:  # W = 87 이다 아스키코드를 활용해서 넣어 보았음
            self.forward()

        elif event.key() == 65:  # A = 65 
            self.left()

        elif event.key() == 83:  #  S = 83 
            self.stop()

        elif event.key() == 68:  # D = 87 
            self.right()

        elif event.key() == 88:  # x = 88 
            self.backward()

        elif event.key() == Qt.Key_Q: # Q = 왼쪽으로돌기
            self.left_turn()

        elif event.key() == Qt.Key_E: # E = 오른쪽으로돌기
            self.right_turn()

        elif event.key() == Qt.Key_Z: # Z = Harr 
            self.harr()

        elif event.key() == Qt.Key_C: # C = 라인트레이싱
            self.line_tracing()
        
        elif event.key() == Qt.Key_I: # I = 저장하기
            self.save()

        elif event.key() == Qt.Key_O: # O = 삭제하기
            self.delete()

    def closeEvent(self, event):
        event.accept()

    def speed_40(self):
        print("속도40")
        
    def speed_50(self):
        print("속도50")

    def speed_60(self):
        print("속도60")

    def speed_80(self):
        print("속도80")
    
    def speed_100(self):
        print("속도100")        

    def left_turn(self):
        print("왼쪽으로돌기")
        self.update_status("왼쪽으로 돌기")
    
    def right_turn(self):
        print("오른쪽으로돌기")
        self.update_status("오른쪽으로 돌기")


    def forward(self) :
        print("앞으로")
        self.update_status("앞으로")

    def right(self) :
        print("오른쪽")
        self.update_status("오른쪽")
    
    def stop(self) :
        print("멈춤")
        self.update_status("멈춤")

    def left(self) :
        print("왼쪽")
        self.update_status("왼쪽")

    def backward(self) :
        print("뒤로가기")
        self.update_status("뒤로가기")
    
    def harr(self):
        print("Harr")
        self.update_status("Harr")
    
    def line_tracing(self):
        print("라인트레이싱(자율주행)")
        self.update_status("라인트레이싱")

    def save(self):
        print("저장하였습니다.")
    
    def update_status(self, status="대기중"):
        self.btn_state.setText(f'현재상태: {status}')
    
    def delete(self):
        print("삭제하였습니다.")

   


if __name__ == '__main__':
    print(sys.argv)
    app = QApplication(sys.argv)
    view = App()
    sys.exit(app.exec_())
