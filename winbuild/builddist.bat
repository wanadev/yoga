setlocal

virtualenv __env__
call __env__\Scripts\activate.bat

pip install .
pip install -r winbuild\requirements.txt

REM Hack to workaround an issue with the way Nuitka handles the icons...
mkdir yogawin.build
copy winbuild\yoga-icon.ico yogawin.build\yoga-icon.ico
copy winbuild\yoga-icon.ico yoga-icon.ico

python -m nuitka --follow-imports --assume-yes-for-downloads --include-package=PIL --standalone --windows-icon-from-ico=yoga-icon.ico winbuild\yogawin.py
move yogawin.dist\yogawin.exe yogawin.dist\yoga.exe
copy winbuild\README-windows-dist.md yogawin.dist\README.txt
copy LICENSE yogawin.dist\LICENSE.txt

REM Remove the icon that was put here to workaround Nuika icon issue...
del yoga-icon.ico

endlocal


