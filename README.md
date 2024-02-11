# デンチョー・リネーマー

ChatGPTが全部作った
コード、レイアウトや処理など汚い試作版
Exe化したときのロケールの都合で、カレンダーがワンクリック余計で微妙ではある。

展開方法

```bash
python -m venv .venv
./.venv/Scripts/activate.ps1
cd src
pip install -r requirements.txt
python main.py
```

pyinstaller

```
pyinstaller src/dencho-renamer.py --onefile --noconsole --collect-data tkinterdnd2 --hidden-import babel.numbers
```
`clients.json`と`document_types.json`を同じディレクトリに配置してZipにしておくなど。

![](screenshot.jpg)
