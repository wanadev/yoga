setlocal

virtualenv __env__
call __env__\Scripts\activate.bat

pip install .
pip install nuitka

python -m nuitka --follow-imports --standalone --windows-dependency-tool=pefile winbuild\yogawin.py

call __env__\Scripts\deactivate.bat

endlocal
