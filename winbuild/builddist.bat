setlocal

virtualenv __env__
call __env__\Scripts\activate.bat

pip install .
pip install nuitka

python -m nuitka --follow-imports --standalone --windows-dependency-tool=pefile winbuild\yogawin.py
move yogawin.dist\yogawin.exe yogawin.dist\yoga.exe
copy winbuild\README-windows-dist.md yogawin.dist\README.txt
copy LICENSE yogawin.dist\LICENSE.txt

call __env__\Scripts\deactivate.bat

endlocal
