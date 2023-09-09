# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 11:21:14 2021

@author: BI6MHT
"""

from PyQt5.QtWidgets import (QWidget, QHBoxLayout, 
    QSplitter, QApplication, QPushButton,QLineEdit,QGridLayout,QInputDialog)
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
import implementation

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):      

        hbox = QHBoxLayout(self)
        self.setGeometry(300, 300, 300,200)
        self.setWindowTitle('Halfwave')
        
        # 图片展示
        pixmap = QPixmap("graphs/test.jpg")
        pixmap2 = QPixmap("graphs/test.jpg")
        
        self.lbl = QLabel(self)
        self.lbl.setPixmap(pixmap)
        self.lbl.setScaledContents(True)
        self.lb2 = QLabel(self)
        self.lb2.setPixmap(pixmap2)
        self.lb2.setScaledContents(True)
        # 分框
        #topleft = QFrame(self)
        #topleft.setFrameShape(QFrame.StyledPanel)

        #topright = QFrame(self)
        #topright.setFrameShape(QFrame.StyledPanel)

        #bottom = QFrame(self)
        #bottom.setFrameShape(QFrame.StyledPanel)

        self.btn = QPushButton('波长(m)', self)
        self.le = QLineEdit(self)
        # self.le.move(130, 22)
        
        self.btn1 = QPushButton('天线长度(lambda)', self)
        self.le1 = QLineEdit(self)
        
        self.btn3 = QPushButton('段数', self)
        self.le3 = QLineEdit(self)
        
        self.btn2 = QPushButton('提交', self)
        self.le2 = QLineEdit(self)
        
        
        grid = QGridLayout()
        grid.setSpacing(10)
        
        grid.addWidget(self.btn, 1, 0)
        grid.addWidget(self.le, 1, 1)
        
        grid.addWidget(self.btn1, 2, 0)
        grid.addWidget(self.le1, 2, 1)
        
        grid.addWidget(self.btn3, 3, 0)
        grid.addWidget(self.le3, 3, 1)
        
        grid.addWidget(self.btn2, 4, 0)
        grid.addWidget(self.le2, 4, 1)
        
        #self.btn.move(20, 20)
        self.btn.clicked.connect(self.showDialog)

        #self.btn1.move(20, 20)
        self.btn1.clicked.connect(self.showDialog2)
        
        self.btn3.clicked.connect(self.showDialog3)
        
        self.btn2.clicked.connect(self.Submit)
        
        # 创建控件
        gwg = QWidget()
        
        # 使用控件进行局部布局
        gwg.setLayout(grid)

        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(self.lbl)
        splitter1.addWidget(self.lb2)
        
        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(gwg)
        splitter2.addWidget(splitter1)

        splitter2.setStretchFactor(0, 100)    
        splitter2.setStretchFactor(1, 100)  
        
        hbox.addWidget(splitter2)



        self.setLayout(hbox)

 
        self.show()
        
        
        


    def onChanged(self, text):

        self.lbl.setText(text)
        self.lbl.adjustSize()        

    def showDialog(self):

        self.text, ok = QInputDialog.getText(self, '波长(m)', 
            '请输入波长:')
        
        if ok:
            self.le.setText(self.text)
        self.text = float(self.text)
            
    def showDialog2(self):

        self.text2, ok = QInputDialog.getText(self, '天线长度(lambda)', 
            '请输入天线长度:')
        
        if ok:
            self.le1.setText(self.text2)
        self.text2 = float(self.text2)
        
    def showDialog3(self):

        self.text3, ok = QInputDialog.getText(self, '(分段数)', 
            'Enter your name:')
        
        if ok:
            self.le3.setText(self.text3)
        self.text3 = int(self.text3)

    
    def Submit(self):
        implementation.momplot(self.text,self.text2,self.text3)
        self.le2.setText(str(self.text)+str(self.text2))
        pixmap = QPixmap("graphs/currents.png")
        pixmap2 = QPixmap("graphs/pattern.png")
        self.lbl.setPixmap(pixmap)
        self.lb2.setPixmap(pixmap2)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())