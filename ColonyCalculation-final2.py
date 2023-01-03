import os
import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.uic.properties import QtGui
from PyQt5 import QtCore, QtGui, QtWidgets
import math
import time
import pandas as pd

class MyWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.ui = uic.loadUi("./ui/colony2.ui")
        #print(self.ui.__dict__)  # 查看ui文件中有哪些控件
        self.drag_file_frame = self.ui.lineEdit
        self.choose_file = self.ui.toolButton
        self.choose_file.clicked.connect(self.slot_btn_chooseFile)
        self.start_system = self.ui.buttonstart
        self.start_system.clicked.connect(self.colony_calculation)
        #self.get_icon = self.ui.label_6
        self.ui.label_6.setPixmap(QtGui.QPixmap("./img/icon_2.png"))
        self.msg = self.ui.textBrowser
        #设置时钟操作
        self.lcd = self.ui.lcdNumber
        self.lcd.setDigitCount(10)  # 设置数字个数
        self.lcd.setMode(QLCDNumber.Dec)  # 数字十进制
        self.lcd.setSegmentStyle(QLCDNumber.Flat)  # 平面模式
        self.lcd.display(time.strftime('%X', time.localtime()))
        self.timer = QTimer(self)
        self.timer.setInterval(1000)  # 设置定时器 1S触发一次
        self.timer.timeout.connect(self.refresh)
        self.timer.start()  # 启动定时器
    def refresh(self):
        self.lcd.display(time.strftime('%X', time.localtime()))
        #self.timer.timeout.connect(self.show_time)
        #self.ui.label_3.setText(f'{time.strftime("%Y-%m-%d, %H-%M-%S", time.localtime())}')


    def slot_btn_chooseFile(self):

        self.fileName_choose, self.filetype = QFileDialog.getOpenFileName(self,
                                    "select file",
                                    './', # 起始路径
                                    "All Files (*);;Excel Files(*.xlsx *.xls)")   # 设置文件扩展名过滤,用双分号间隔

        if self.fileName_choose == "":
            print("\n取消选择")
            self.drag_file_frame.setText('请选择需要的Excel文件')
            return

        print("\n你选择的文件为:")
        print(self.fileName_choose)
        self.drag_file_frame.setText(f'{self.fileName_choose}')
        #print("文件筛选器类型: ",filetype)

    def colony_calculation(self):

        global fileName_choose
        df1 = pd.read_excel(self.fileName_choose, header=0)
        colonies = df1['Counted Colonies']
        # 所有菌落数为0的值均需要写为1
        colonies.replace(to_replace=0, value=1, inplace=True)
        # df1['dilution'] = df1['Plate Id'].str.split('-').apply(lambda x: x[-2])
        #print(df1)
        plate_id = df1.pop('Plate Id')  # 观察表格，Plate Id这一列，想要分组的话，需要把它末尾的-1 -2 -3 去掉，才能保证同名成组
        # print(plate_id)
        plate_id = plate_id.str[:-2]  # plate id列，只取从最开头到倒数第3个字符即可
        # print(plate_id)
        df1['Plate Id'] = plate_id  # 把新的值重新赋给df1，这样df1就可以执行groupby操作
        # print(df1)
        df2 = df1.groupby('Plate Id', as_index=False).mean()  # 求平均值,Plate Id列不要变索引

        # print(df2.columns)
        df3 = df2.loc[:, ['Plate Id', 'Counted Colonies','Concentration']]  # 只要plate id 和 counted colonies 两列
        df3['dilution'] = df3['Plate Id'].str.split('-').apply(lambda x: x[-1])  # plate Id以“-”分隔的最后一位是稀释的倍数
        str1 = self.ui.lineEdit_2.text() #获取输入框里边长值
        area_of_cover = int(str1)
        # area_of_cover = int(input('please input the side length of plastic cover:\t'))
        df3['U_value'] = df3.apply(
            lambda x: math.log10(
                (float(x['Counted Colonies']) * float(x['dilution']) * 10.0 * 20.0) / (area_of_cover ** 2)), axis=1)
        SA_colonies = df3.loc[df3['Plate Id'].str.contains('SA')].copy()
        # print(SA_colonies)
        SA_Ut = SA_colonies.loc[SA_colonies['Plate Id'].str.contains('Ut')].copy()
        SA_Ut_value = SA_Ut.loc[:, ['U_value']].values[0][0]
        print('SA_Ut_value is:\t', SA_Ut_value)
        self.msg.append(f'SA_Ut_value is: {SA_Ut_value}\n')

        def calculation_R(x, Ut):
            return Ut - x

        R_value = SA_colonies['U_value'].apply(calculation_R, Ut=SA_Ut_value)
        # print(type(R_value))
        SA_colonies['Reduction'] = R_value
        SA_colonies['Rate(%)'] = SA_colonies['Reduction'].map(lambda x: 100 * (1 - 10 ** (-1 * x)))
        empty_rows = list(len(SA_colonies.columns) * '#')
        SA_colonies.loc[len(SA_colonies)] = empty_rows
        # print(SA_colonies)

        EC_colonies = df3.loc[df3['Plate Id'].str.contains('EC')].copy()  # 所有Plate Id里含‘EC’的行全部取出并copy一份
        EC_Ut = EC_colonies.loc[EC_colonies['Plate Id'].str.contains('Ut')].copy()
        EC_Ut_value = EC_Ut.loc[:, ['U_value']].values[0][0]
        print('EC_Ut_value is \t', EC_Ut_value)
        self.msg.append(f'EC_Ut_value is: {EC_Ut_value}\n')
        EC_colonies['Reduction'] = EC_colonies['U_value'].map(lambda x: EC_Ut_value - x)
        EC_colonies['Rate(%)'] = EC_colonies['Reduction'].map(lambda x: 100 * (1 - 10 ** (-1 * x)))
        # print(EC_colonies)

        # 输出excel
        df4 = pd.concat([SA_colonies, EC_colonies], axis=0, join='outer', ignore_index=True)
        print(df4)
        time_now = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        dir_path = os.path.dirname(self.fileName_choose)
        dir_file = os.path.join(dir_path,f'calculated colonies-{time_now}.xlsx')
        df4.to_excel(dir_file)
        self.msg.append('The results have been exported. Congratulations! \n You can close the window now')
        print('Done!')
if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = MyWindow()
    # 展示窗口
    w.ui.show()

    sys.exit(app.exec_())