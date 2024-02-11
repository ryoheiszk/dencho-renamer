import PySimpleGUI as sg

sg.theme("BluePurple")

layout = [
    [
        sg.Text("テスト用アプリです")
    ], [
        sg.Text("牛乳(150円): "),
        sg.Combo(list(range(1,11)),key="-QUANTITY-"),
        sg.Text("個")
    ], [
        sg.Button("購入", key="-SUBMIT-")
    ], [
        sg.Text(key="-AMOUNT-", size=(120, 10))
    ]
]

window = sg.Window("テストアプリ", layout, size=(300, 150))

while True:
    event, values = window.read()

    if event == "-SUBMIT-":
        total = 150 * int(values["-QUANTITY-"])
        window["-AMOUNT-"].update(value=f"金額:{total}")

    if event == sg.WIN_CLOSED:
        break
