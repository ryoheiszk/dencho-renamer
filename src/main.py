import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkcalendar import Calendar
import datetime
import os
import json

# ファイルパスを保持するためのグローバル変数
global file_path


def drop(event):
    global file_path  # グローバル変数を関数内で使用する宣言
    file_path = event.data  # ファイルパスをグローバル変数に保存
    file_name = file_path.split('/')[-1]  # ファイル名のみを取得
    selected_file_label.config(text=file_name)  # ファイル名のみを表示


# 検索フィルタの更新処理
def update_list(event):
    search_term = event.widget.get().lower()
    client_list.delete(0, tk.END)
    for client in clients:
        if search_term in client.lower():
            client_list.insert(tk.END, client)


def rename_file(selected_date, original_path, document_type, client_name, amount):
    # 日付の取得
    date_str = selected_date.replace("/", "")

    # ファイルの拡張子を取得
    _, file_extension = os.path.splitext(original_path)

    # 新しいファイル名を生成
    new_file_name = f"{date_str}_{document_type}_{client_name}_{amount}{file_extension}"

    # 新しいファイルパスを生成
    new_file_path = os.path.join(os.path.dirname(original_path), new_file_name)

    # ファイルのリネーム
    try:
        os.rename(original_path, new_file_path)
        print(f"ファイルをリネームしました: {new_file_path}")

        # ファイル名の変更に成功したら、ラベルのテキストを更新
        selected_file_label.config(text=new_file_name)
        file_path = new_file_path  # 変更後のファイルパスを保存

        return new_file_path
    except OSError as e:
        print(f"ファイルのリネームに失敗しました: {e}")
        return None


def execute_action():
    global file_path, cal, client_list, amount_entry, tax_var, tax_toggle_var, selected_file_label, document_type_var

    # 選択された情報の取得
    file_name = selected_file_label.cget("text")
    selected_date = cal.get_date()
    selected_document_type = document_type_var.get()
    selected_client = client_list.get(
        tk.ACTIVE) if client_list.get(tk.ACTIVE) else "未選択"
    amount = amount_entry.get()
    tax_status = tax_var.get()
    tax_conversion = tax_toggle_var.get()

    # コンソールに出力（実際のアプリケーションでは、ここで必要な処理を行います）
    print(f"ファイル名: {file_name}")
    print(f"ファイルパス: {file_path}")
    print(f"日付: {selected_date}")
    print(f"取引先名: {selected_client}")
    print(f"ファイル種類: {selected_document_type}")
    print(f"金額: {amount}")
    print(f"入力された税区分: {tax_status}")
    print(f"税込←→税抜変換: {'有効' if tax_conversion else '無効'}")

    # 税込み税抜き変換
    converted_amount = int(amount)
    if tax_conversion:
        if tax_status == "税込み":
            converted_amount = round(int(amount)/1.1)
        if tax_status == "税抜き":
            converted_amount = round(int(amount)*1.1)

    # リネーム
    rename_file(selected_date=selected_date, original_path=file_path, document_type=selected_document_type,
                client_name=selected_client, amount=converted_amount)


def main():
    global root, selected_file_label, clients, client_list, cal, amount_entry, tax_var, tax_toggle_var, document_type_var

    root = TkinterDnD.Tk()
    root.title("取引情報入力")

    # ファイル選択部分のフレーム
    frame_file = tk.LabelFrame(root, text="ここにファイルをドロップ", height=100)
    frame_file.grid(row=0, column=0, columnspan=3, sticky='ew', padx=5, pady=5)
    frame_file.pack_propagate(False)
    selected_file_label = tk.Label(frame_file, text="ファイル名がここに表示されます")
    selected_file_label.pack(expand=True)

    # カレンダー
    frame_calendar = tk.LabelFrame(root, text="日付")
    frame_calendar.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
    today = datetime.date.today()
    cal = Calendar(frame_calendar, selectmode='day',
                   year=today.year, month=today.month, day=today.day)
    cal.pack()

    # 取引先名
    frame_client = tk.LabelFrame(root, text="取引先名")
    frame_client.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
    client_search_box = tk.Entry(frame_client)
    client_search_box.pack()
    client_list = tk.Listbox(frame_client)
    client_list.pack(fill=tk.BOTH, expand=True)

    _json_open = open('clients.json', 'r', encoding="utf-8")
    clients = json.load(_json_open)

    for client in clients:
        client_list.insert(tk.END, client)
    client_search_box.bind('<KeyRelease>', update_list)

    # 金額入力部分のフレーム
    frame_amount = tk.LabelFrame(root, text="金額")
    frame_amount.grid(row=2, column=1, sticky='ew', padx=5, pady=5)
    amount_entry = tk.Entry(frame_amount)
    amount_entry.pack(side='left', fill=tk.X, expand=True)
    tk.Label(frame_amount, text="円").pack(side='left')

    # 税込み/税抜きラジオボタン
    frame_tax = tk.Frame(frame_amount)
    frame_tax.pack(side='left', padx=5)
    tax_var = tk.StringVar(value="税込み")
    tk.Radiobutton(frame_tax, text="税込み", variable=tax_var,
                   value="税込み").pack(anchor='w')
    tk.Radiobutton(frame_tax, text="税抜き", variable=tax_var,
                   value="税抜き").pack(anchor='w')

    # 税込み/税抜き変換チェックボックス
    tax_toggle_var = tk.BooleanVar()
    tk.Checkbutton(frame_amount, text="税込←→税抜変換",
                   variable=tax_toggle_var).pack(side='left')

    # 実行ボタン
    execute_button = tk.Button(root, text="実行", command=execute_action)
    execute_button.grid(row=3, column=0, columnspan=3,
                        sticky='ew', padx=5, pady=5)

    # ドロップを受け取る設定
    frame_file.drop_target_register(DND_FILES)
    frame_file.dnd_bind('<<Drop>>', drop)

    # ドキュメントタイプのラジオボタン
    _json_open = open('document_types.json', 'r', encoding="utf-8")
    document_types = json.load(_json_open)

    document_type_var = tk.StringVar(value="請求書")  # デフォルト値を設定

    frame_document_type = tk.LabelFrame(root, text="書類の種類")
    frame_document_type.grid(row=1, column=2, sticky='nsew', padx=5, pady=5)

    # JSONファイルから読み込んだドキュメントタイプの数だけラジオボタンを生成
    for document_type in document_types:
        tk.Radiobutton(frame_document_type, text=document_type,
                       variable=document_type_var, value=document_type).pack(anchor='w')

    root.mainloop()


if __name__ == "__main__":
    main()
