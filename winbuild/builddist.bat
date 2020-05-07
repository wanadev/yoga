setlocal

virtualenv __env__
call __env__\Scripts\activate.bat

pip install .
pip install nuitka

REM Hack to workaround an issue with the way Nuitka handles the icons...
mkdir yogawin.build
copy winbuild\yoga-icon.ico yogawin.build\yoga-icon.ico
copy winbuild\yoga-icon.ico yoga-icon.ico

python -m nuitka --follow-imports --standalone --windows-dependency-tool=pefile --windows-icon=yoga-icon.ico winbuild\yogawin.py
move yogawin.dist\yogawin.exe yogawin.dist\yoga.exe
copy winbuild\README-windows-dist.md yogawin.dist\README.txt
copy LICENSE yogawin.dist\LICENSE.txt

REM Remove the icon that was put here to workaround Nuika icon issue...
del yoga-icon.ico

call __env__\Scripts\deactivate.bat

endlocal
