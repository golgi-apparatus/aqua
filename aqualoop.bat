:loop
python aqua.py
if ERRORLEVEL == 9002 (
	set /P c="start aqua again?? (y/n)"
	if /I "%c%" EQU "N" goto quit
)
goto loop
:quit