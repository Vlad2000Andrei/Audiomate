echo off
echo ------------------------------------------------
echo Setting up AudioMate: Automatic Audio Animations
echo ------------------------------------------------

echo Checking Python3 installation....

python3 .\check_installed.py >NUL
if  errorlevel 123 goto installModules

echo ERR: Python not installed! Please install python and try again...
echo ERR: Installation link: https://apps.microsoft.com/store/detail/python-310/9PJPW5LDXLZ5?hl=en-us^&gl=US
python3 

goto finished

:installModules
echo Python installed! Installing required modules...

python3 -m pip install --upgrade pip
python3 -m pip install --upgrade numpy scipy moviepy matplotlib Pillow

echo .
echo .
echo ------------------------------------------------
echo Installation successful! Press any key to exit.
echo ------------------------------------------------

:finished
pause