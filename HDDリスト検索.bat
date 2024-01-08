@echo off
REM Pythonのパスを指定します。デフォルトの場所にインストールされている場合は以下のようになります。
REM set PYTHON_PATH=C:\Python39\python.exe

REM Pythonスクリプトのパスを指定します。
set SCRIPT_PATH=D:\Python\SearchHddList\main.py

REM Pythonスクリプトを実行します。
REM %PYTHON_PATH% %SCRIPT_PATH%
python %SCRIPT_PATH%

REM ユーザーがキーを押してウィンドウを閉じるのを待ちます。
pause
