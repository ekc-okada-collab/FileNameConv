# このスクリプトは、ファイル名を一括処理するためのものです。
# main.py
import os
import sys
import glob

from PyQt6 import QtCore, QtGui

from PyQt6.QtWidgets import (QApplication, QWidget,
                             QMainWindow, QLabel,
                             QLineEdit, QPushButton,
                             QHBoxLayout, QVBoxLayout,
                             QCheckBox, QFrame,
                             QSpacerItem, QSizePolicy,
                             QTextEdit, QProgressBar,
                             QFileDialog, QMessageBox)
from PyQt6.QtGui import QIcon, QAction


class MainWindow(QMainWindow):
    dir_path = ""
    file_names = []
    step = 0

    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        # ウィンドウの設定
        self.setWindowTitle("File Name Converter")
        self.setFixedSize(600,400)
        # self.setGeometry(100, 100, 600, 400)
        self.centralWidget = QWidget(parent=self)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayoutWidget = QWidget(parent=self.centralWidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 580, 380))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_path = QLabel(parent=self.verticalLayoutWidget)
        self.label_path.setObjectName("label_path")
        self.verticalLayout.addWidget(self.label_path)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lineEdit_path = QLineEdit(parent=self.verticalLayoutWidget)
        self.lineEdit_path.setObjectName("lineEdit_path")
        self.horizontalLayout_2.addWidget(self.lineEdit_path)
        self.pushButton_select_path = QPushButton(parent=self.verticalLayoutWidget)
        self.pushButton_select_path.setObjectName("pushButton_select_path")
        self.pushButton_select_path.setText("参照...")
        self.pushButton_select_path.clicked.connect(self.open_folder_dialog)
        self.horizontalLayout_2.addWidget(self.pushButton_select_path)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.label_log = QLabel(parent=self.verticalLayoutWidget)
        self.label_log.setObjectName("label_log")
        self.label_log.setText("情報")
        self.verticalLayout.addWidget(self.label_log)
        self.textEdit_log = QTextEdit(parent=self.verticalLayoutWidget)
        self.textEdit_log.setObjectName("textEdit_log")
        self.verticalLayout.addWidget(self.textEdit_log)
        self.line = QFrame(parent=self.verticalLayoutWidget)
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.checkBox_removeHeaderCharactor = QCheckBox(parent=self.verticalLayoutWidget)
        self.checkBox_removeHeaderCharactor.setObjectName("checkBox_removeHeaderCharactor")
        self.checkBox_removeHeaderCharactor.setText("先頭の文字を")
        self.horizontalLayout.addWidget(self.checkBox_removeHeaderCharactor)
        self.lineEdit_removeNumber = QLineEdit(parent=self.verticalLayoutWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_removeNumber.sizePolicy().hasHeightForWidth())
        self.lineEdit_removeNumber.setSizePolicy(sizePolicy)
        self.lineEdit_removeNumber.setObjectName("lineEdit_removeNumber")
        self.lineEdit_removeNumber.setText("3")
        self.horizontalLayout.addWidget(self.lineEdit_removeNumber)
        self.label_2 = QLabel(parent=self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.label_2.setText("文字を取り除く。")
        self.horizontalLayout.addWidget(self.label_2)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line_2 = QFrame(parent=self.verticalLayoutWidget)
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.btn_run = QPushButton(parent=self.verticalLayoutWidget)
        self.btn_run.setObjectName("btn_run")
        self.btn_run.setText("実行")
        self.horizontalLayout_3.addWidget(self.btn_run)
        self.btn_quit = QPushButton(parent=self.verticalLayoutWidget)
        self.btn_quit.setObjectName("btn_quit")
        self.btn_quit.setText("終了")
        self.btn_quit.clicked.connect(self.close)
        self.horizontalLayout_3.addWidget(self.btn_quit)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.setCentralWidget(self.centralWidget)
        self.menubar = self.menuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.statusbar = self.statusBar()
        self.statusbar.setObjectName("statusbar")
        self.statusbar.showMessage("Ready")
        self.label_path.setText("参照パス")
        
        

        self.show()
    
    def open_folder_dialog(self):
        folder = QFileDialog.getExistingDirectory(self, "フォルダを選択")
        if folder:
            self.lineEdit_path.setText(folder)
            self.dir_path = folder
            self.file_names = get_file_names(folder)
            if self.file_names:
                for file in self.file_names:
                    self.textEdit_log.append(file)





def get_file_names(directory):
    """
    指定されたディレクトリ内の全てのファイル名を取得します。
    
    :param directory: 対象のディレクトリパス
    :return: ファイル名のリスト
    """
    file_names = []
    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)):
            file_names.append(file)
    return file_names

def add_prefix(file, prefix=""):
    """
    ファイル名にプレフィックスを追加します。
    
    :param file: 対象のファイル名
    :param prefix: 追加するプレフィックス
    :return: プレフィックスが追加されたファイル名
    """
    name = os.path.basename(file)
    # プレフィックスを追加
    new_name = f"{prefix}{name}"
    return new_name

def remove_prefix(file, prefix=""):
    """
    ファイル名からプレフィックスを削除します。
    
    :param file: 対象のファイル名
    :param prefix: 削除するプレフィックス
    :return: プレフィックスが削除されたファイル名
    """
    name = os.path.basename(file)
    # プレフィックスが存在する場合は削除
    if name.startswith(prefix):
        new_name = name[len(prefix):]
    else:
        new_name = name
    return new_name

def slice_file_name(file, start=0, end=None):
    """
    ファイル名をスライスします。
    
    :param file: 対象のファイル名
    :param start: スライスの開始位置
    :param end: スライスの終了位置
    :return: スライスされたファイル名
    """
    name = os.path.basename(file)
    # スライスを適用
    new_name = name[start:end]
    return new_name

def edit_file_names(files, prefix=""):
    filecount = len(files)
    if filecount == 0:
        print("No files found in the directory.")
        return []

    """
    ファイル名のリストをスライスします。
    :param files: ファイル名のリスト
    :return: スライスされたファイル名のリスト
    例:
    files = ["file1.txt", "file2.txt", "file3.txt"]
    で、start=3, end=None の場合、sliced_files = ["1.txt", "2.txt", "3.txt"]
    """   
    sliced_files = []
    for file in files:
        new_file = slice_file_name(file, start=3, end=None)
        sliced_files.append(new_file)

    """
    ファイル名のリストにプレフィックスを追加します。
    :param files: ファイル名のリスト
    :param prefix: 追加するプレフィックス
    :return: プレフィックスが追加されたファイル名のリスト
    """
    edited_files = []
    for i, file in enumerate(sliced_files):
        prefix = f"{i+1:03d}_"
        new_file = add_prefix(file, prefix)
        edited_files.append(new_file)
    return edited_files
    

def main2():
    # コマンドライン引数からディレクトリを取得
    if len(sys.argv) < 2:
        print("Usage: python main.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]

    # ディレクトリが存在するか確認
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory.")
        sys.exit(1)

    # ディレクトリ内の全てのファイルを取得
    files = get_file_names(directory)

    edit_files = edit_file_names(files, prefix="edited_")

    # ファイル名を表示
    for file in edit_files:
        print(file)


def main(args):
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())

if __name__ == "__main__":
    main(sys.argv)