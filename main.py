# このスクリプトは、ファイル名を一括処理するためのものです。
# main.py

import os
import sys
import glob

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
    

def main():
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

if __name__ == "__main__":
    main()