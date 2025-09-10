# このスクリプトは、ファイル名を一括処理するためのものです。
# main.py
import os
import sys
import glob
import shutil

from PyQt6 import QtCore

from PyQt6.QtWidgets import (QApplication, QWidget,
                             QMainWindow, QLabel,
                             QLineEdit, QPushButton,
                             QHBoxLayout, QVBoxLayout,
                             QCheckBox, QFrame,
                             QSpacerItem, QSizePolicy,
                             QTextEdit,
                             QFileDialog, QMessageBox,
                             QComboBox)
from PyQt6.QtGui import QIcon


class MainWindow(QMainWindow):
    dir_path = ""
    file_type = ""
    file_names = []
    step = 0

    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        # ウィンドウの設定
        self.setWindowTitle("ファイル名一括変換ツール")
        self.setWindowIcon(QIcon("icon.png"))
        self.setFixedSize(600,400)
        # MainWindowの中央ウィジェットを設定
        self.centralWidget = QWidget(parent=self)
        self.centralWidget.setObjectName("centralWidget")
        #中央ウィジェットにメインになる垂直レイアウトウィジェットを配置
        self.verticalLayoutWidget = QWidget(parent=self.centralWidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 580, 380))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 10)
        self.verticalLayout.setObjectName("verticalLayout")
        # 1 垂直レイアウトウィジェットの1行目の要素（横レイアウトに3要素配置）
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        # 1-1 垂直レイアウトウィジェットの1行目の要素（横レイアウトの1要素目）
        self.label_fileType = QLabel(parent=self.verticalLayoutWidget)
        self.label_fileType.setObjectName("label_fileType")
        self.label_fileType.setText("対象ファイルの拡張子")
        self.horizontalLayout_6.addWidget(self.label_fileType)
        # 1-2 垂直レイアウトウィジェットの1行目の要素（横レイアウトの2要素目）
        self.comboBox_fileType = QComboBox(parent=self.verticalLayoutWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_fileType.sizePolicy().hasHeightForWidth())
        self.comboBox_fileType.setSizePolicy(sizePolicy)
        self.comboBox_fileType.setObjectName("comboBox_fileType")
        self.comboBox_fileType.addItems(["選択してください", "pdf", "jpg", "png", "txt", "csv", "zip", "docx", "xlsx", "pptx", "その他"])
        self.horizontalLayout_6.addWidget(self.comboBox_fileType)
        self.comboBox_fileType.setCurrentIndex(0)
        self.comboBox_fileType.currentTextChanged.connect(self.fileType_changed) # コンボボックスの値が変更されたときのイベント

        # 1-2-1 垂直レイアウトウィジェットの1行目の要素（横レイアウトの2要素目の補足テキスト）
        self.lineEdit_3 = QLineEdit(parent=self.verticalLayoutWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_3.setSizePolicy(sizePolicy)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setText("その他の場合は直接入力")
        self.horizontalLayout_6.addWidget(self.lineEdit_3)
        self.lineEdit_3.setEnabled(False)

        # 1-3 垂直レイアウトウィジェットの1行目の要素（横レイアウトの3要素目）
        self.label_sort = QLabel(parent=self.verticalLayoutWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_sort.sizePolicy().hasHeightForWidth())
        self.label_sort.setSizePolicy(sizePolicy)
        self.label_sort.setObjectName("label_sort")
        self.label_sort.setText("　　ファイルの並び順")
        self.horizontalLayout_6.addWidget(self.label_sort)
        # 1-4 垂直レイアウトウィジェットの1行目の要素（横レイアウトの4要素目）
        self.comboBox_sortFile = QComboBox(parent=self.verticalLayoutWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_sortFile.sizePolicy().hasHeightForWidth())
        self.comboBox_sortFile.setSizePolicy(sizePolicy)
        self.comboBox_sortFile.setObjectName("comboBox_sortFile")
        self.comboBox_sortFile.addItems(["名前順", "更新日時順", "作成日時順", "サイズ順"])
        self.horizontalLayout_6.addWidget(self.comboBox_sortFile)
        # 1-5 垂直レイアウトウィジェットの1行目の要素（横レイアウトの5要素目）
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        # 2 垂直レイアウトウィジェットの2行目の要素
        self.label_path = QLabel(parent=self.verticalLayoutWidget)
        self.label_path.setObjectName("label_path")
        self.label_path.setText("参照パス")
        self.verticalLayout.addWidget(self.label_path)
        # 3 垂直レイアウトウィジェットの3行目の要素（横レイアウトに2要素配置）
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        # 3-1 垂直レイアウトウィジェットの3行目の要素（横レイアウトの1要素目）
        self.lineEdit_path = QLineEdit(parent=self.verticalLayoutWidget)
        self.lineEdit_path.setObjectName("lineEdit_path")
        self.horizontalLayout_2.addWidget(self.lineEdit_path)
        # 3-2 垂直レイアウトウィジェットの3行目の要素（横レイアウトの2要素目）
        self.pushButton_select_path = QPushButton(parent=self.verticalLayoutWidget)
        self.pushButton_select_path.setObjectName("pushButton_select_path")
        self.pushButton_select_path.setText("参照...")
        self.pushButton_select_path.clicked.connect(self.open_folder_dialog)
        self.horizontalLayout_2.addWidget(self.pushButton_select_path)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        # 4 垂直レイアウトウィジェットの4行目の要素
        self.label_log = QLabel(parent=self.verticalLayoutWidget)
        self.label_log.setObjectName("label_log")
        self.label_log.setText("情報")
        self.verticalLayout.addWidget(self.label_log)
        # 5 垂直レイアウトウィジェットの5行目の要素
        self.textEdit_log = QTextEdit(parent=self.verticalLayoutWidget)
        self.textEdit_log.setObjectName("textEdit_log")
        self.verticalLayout.addWidget(self.textEdit_log)
        # 6 垂直レイアウトウィジェットの6行目の要素
        self.line = QFrame(parent=self.verticalLayoutWidget)
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        # 7 垂直レイアウトウィジェットの7行目の要素（横レイアウトに4要素配置）
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        # 7-1 垂直レイアウトウィジェットの7行目の要素（横レイアウトの1要素目）
        self.checkBox_removeHeaderCharactor = QCheckBox(parent=self.verticalLayoutWidget)
        self.checkBox_removeHeaderCharactor.setObjectName("checkBox_removeHeaderCharactor")
        self.checkBox_removeHeaderCharactor.setText("先頭の")
        self.horizontalLayout.addWidget(self.checkBox_removeHeaderCharactor)
        # 7-2 垂直レイアウトウィジェットの7行目の要素（横レイアウトの2要素目）
        self.lineEdit_removeNumber = QLineEdit(parent=self.verticalLayoutWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_removeNumber.sizePolicy().hasHeightForWidth())
        self.lineEdit_removeNumber.setSizePolicy(sizePolicy)
        self.lineEdit_removeNumber.setObjectName("lineEdit_removeNumber")
        self.lineEdit_removeNumber.setText("3")
        self.horizontalLayout.addWidget(self.lineEdit_removeNumber)
        # 7-3 垂直レイアウトウィジェットの7行目の要素（横レイアウトの3要素目）
        self.label_2 = QLabel(parent=self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.label_2.setText("文字を取り除く。")
        self.horizontalLayout.addWidget(self.label_2)
        # 7-4 垂直レイアウトウィジェットの7行目の要素（横レイアウトの4要素目）
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        # 8 垂直レイアウトウィジェットの8行目の要素
        self.line_2 = QFrame(parent=self.verticalLayoutWidget)
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        # 9 垂直レイアウトウィジェットの9行目の要素（横レイアウトに4要素配置）
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        # 9-1 垂直レイアウトウィジェットの9行目の要素（横レイアウトの1要素目）
        self.checkBox_addPrefix = QCheckBox(parent=self.verticalLayoutWidget)
        self.checkBox_addPrefix.setObjectName("checkBox_addPrefix")
        self.checkBox_addPrefix.setText("ファイル名の先頭に")
        self.horizontalLayout_4.addWidget(self.checkBox_addPrefix)
        # 9-2 垂直レイアウトウィジェットの9行目の要素（横レイアウトの2要素目）
        self.lineEdit_addPrefix = QLineEdit(parent=self.verticalLayoutWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_addPrefix.sizePolicy().hasHeightForWidth())
        self.lineEdit_addPrefix.setSizePolicy(sizePolicy)
        self.lineEdit_addPrefix.setObjectName("lineEdit_addPrefix")
        self.lineEdit_addPrefix.setText("4")
        self.horizontalLayout_4.addWidget(self.lineEdit_addPrefix)
        # 9-3 垂直レイアウトウィジェットの9行目の要素（横レイアウトの3要素目）
        self.label_addPrefix = QLabel(parent=self.verticalLayoutWidget)
        self.label_addPrefix.setObjectName("label_addPrefix")
        self.label_addPrefix.setText("桁の連番を追加する。")
        self.horizontalLayout_4.addWidget(self.label_addPrefix)       
        # 9-4 垂直レイアウトウィジェットの9行目の要素（横レイアウトの4要素目）
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        # 10 垂直レイアウトウィジェットの10行目の要素
        self.line_3 = QFrame(parent=self.verticalLayoutWidget)
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout.addWidget(self.line_3)
        # 11 垂直レイアウトウィジェットの11行目の要素（横レイアウトに3要素配置）
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        # 11-1 垂直レイアウトウィジェットの11行目の要素（横レイアウトの1要素目）
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        # 11-2 垂直レイアウトウィジェットの11行目の要素（横レイアウトの2要素目）
        self.btn_run = QPushButton(parent=self.verticalLayoutWidget)
        self.btn_run.setObjectName("btn_run")
        self.btn_run.setText("実行")
        self.btn_run.clicked.connect(self.edit_prefix)
        self.horizontalLayout_3.addWidget(self.btn_run)
        # 11-3 垂直レイアウトウィジェットの11行目の要素（横レイアウトの3要素目）
        self.btn_quit = QPushButton(parent=self.verticalLayoutWidget)
        self.btn_quit.setObjectName("btn_quit")
        self.btn_quit.setText("終了")
        self.btn_quit.clicked.connect(self.close)
        self.horizontalLayout_3.addWidget(self.btn_quit)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        # MainWindowに中央ウィジェットをセット
        self.setCentralWidget(self.centralWidget)
        # メニューバーの設定
        self.menubar = self.menuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        # ステータスバーの設定
        self.statusbar = self.statusBar()
        self.statusbar.setObjectName("statusbar")
        self.statusbar.showMessage("Ready")
        
        self.show()
    
    def open_folder_dialog(self):
        self.textEdit_log.clear()
        if not self.comboBox_fileType.currentText() or self.comboBox_fileType.currentText() == "選択してください":
            QMessageBox.warning(self, "警告", "対象ファイルの拡張子を選択してください。")
            return
        if self.comboBox_fileType.currentText() == "その他":
            if not self.lineEdit_3.text():
                QMessageBox.warning(self, "警告", "その他の場合は拡張子を直接入力してください。")
                return
            self.file_type = self.lineEdit_3.text().strip().lower()
        else:
            self.file_type = self.comboBox_fileType.currentText().strip().lower()
        
        if not self.comboBox_sortFile.currentText():
            QMessageBox.warning(self, "警告", "ファイルの並び順を選択してください。")
            return
        self.sort_type = self.comboBox_sortFile.currentText()
        



        # フォルダ選択ダイアログを開く
        folder = QFileDialog.getExistingDirectory(self, "フォルダを選択")
        if folder:
            self.lineEdit_path.setText(folder)
            self.dir_path = folder
            self.file_names = get_file_names(folder)
            self.textEdit_log.append(f"選択されたフォルダ: {self.dir_path}")
        self.textEdit_log.append(f"----------------------------------------")
        if not self.file_names:
            self.textEdit_log.append(f"フォルダ内に{self.file_type}ファイルがありません。")
            return
        else:
            # 指定された拡張子のファイルのみをフィルタリング
            self.file_names = [f for f in self.file_names if f.lower().endswith(f".{self.file_type}")]
            if not self.file_names:
                self.textEdit_log.append(f"フォルダ内に{self.file_type}ファイルがありません。")
                return
            self.textEdit_log.append(f"フォルダ内に{len(self.file_names)}個の{self.file_type}ファイルが見つかりました。")
            # ファイルの並び替え
            if self.sort_type == "名前順":
                self.file_names.sort()
            elif self.sort_type == "更新日時順":
                self.file_names.sort(key=lambda x: os.path.getmtime(os.path.join(self.dir_path, x)))
            elif self.sort_type == "作成日時順":
                self.file_names.sort(key=lambda x: os.path.getctime(os.path.join(self.dir_path, x)))
            elif self.sort_type == "サイズ順":
                self.file_names.sort(key=lambda x: os.path.getsize(os.path.join(self.dir_path, x)))
            for file in self.file_names:
                self.textEdit_log.append(file)
            self.textEdit_log.append(f"----------------------------------------")
        
    
    def edit_prefix(self):
        if not self.dir_path:
            QMessageBox.warning(self, "警告", "フォルダを選択してください。")
            return
        if not self.file_names:
            QMessageBox.warning(self, "警告", "フォルダ内にファイルがありません。")
            return
        self.textEdit_log.append(f"処理を開始します。")

        try:
            if not (self.checkBox_removeHeaderCharactor.isChecked() or self.checkBox_addPrefix.isChecked()):
                QMessageBox.warning(self, "警告", "いずれかの処理を選択してください。")
                return
            else:
                self.statusBar().showMessage("処理中...")
                if self.checkBox_removeHeaderCharactor.isChecked():
                    num = int(self.lineEdit_removeNumber.text())
                    if num < 0:
                        raise ValueError
                    self.step = num
                    self.textEdit_log.append(f"先頭の{num}文字を取り除きます。")
                if self.checkBox_addPrefix.isChecked():
                    num = int(self.lineEdit_addPrefix.text())
                    if num < 0:
                        raise ValueError
                    self.textEdit_log.append(f"ファイル名の先頭に{num}桁の連番を追加します。")

                for i, file in enumerate(self.file_names):
                    new_name = file
                    if self.checkBox_removeHeaderCharactor.isChecked():
                        num = int(self.lineEdit_removeNumber.text())
                        new_name = remove_prefix(new_name, prefix=file[:num])
                    else:
                        self.step = 0
                    if self.checkBox_addPrefix.isChecked():
                        num = int(self.lineEdit_addPrefix.text())
                        prefix = f"{i+1:0{num}d}_"
                        new_name = add_prefix(new_name, prefix=prefix)
                    else:
                        self.step = 0
                    self.textEdit_log.append(f"Renamed: {file} -> {new_name}")
                    out_dir = os.path.join(self.dir_path, "output")
                    os.makedirs(out_dir, exist_ok=True)
                    src = os.path.join(self.dir_path, file)
                    dst = os.path.join(out_dir, new_name)
                    shutil.copy(src, dst)
                self.textEdit_log.append(f"処理が完了しました。")
                self.textEdit_log.append(f"----------------------------------------")
                self.statusbar.showMessage("Ready")

        except ValueError:
            QMessageBox.warning(self, "警告", "正の整数を入力してください。")
            self.checkBox_removeHeaderCharactor.setChecked(False)
            self.checkBox_addPrefix.setChecked(False)
            self.lineEdit_removeNumber.setText("3")
            self.lineEdit_addPrefix.setText("4")
            self.step = 0
    
    def fileType_changed(self, text):
        if text == "その他":
            self.lineEdit_3.setEnabled(True)
            self.lineEdit_3.setText("")
        else:
            self.lineEdit_3.setEnabled(False)
            self.lineEdit_3.setText("その他の場合は直接入力")


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

def main(args):
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())

if __name__ == "__main__":
    main(sys.argv)