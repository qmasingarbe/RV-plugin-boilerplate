rem This little bash script (for windows) will enable you to test your code quicly
rem 1. copy python file in development folder to install folder of rv
copy C:\path\to\python\file\in\ide\my_code.py C:\path\to\rv\plugin\directory\my_code.py
rem 2. kill any running instance of RV
taskkill \IM rv.exe
rem 3. launch a new instance of RV (with custom env or test file loading)
rem Please change the pasth to your RV executable
start "" "C:\Program Files\Shotgun\RV-7.1.1\bin\rv.exe"
exit