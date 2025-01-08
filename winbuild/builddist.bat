setlocal

virtualenv __env__
call __env__\Scripts\activate.bat

pip install .
pip install -r winbuild\requirements.txt

python -m nuitka ^
    --standalone ^
    --follow-imports ^
    --assume-yes-for-downloads ^
    --include-package=PIL ^
    --include-package=_cffi_backend ^
    --windows-icon-from-ico=winbuild\yoga-icon.ico ^
    winbuild\yogawin.py
move yogawin.dist\yogawin.exe yogawin.dist\yoga.exe
copy winbuild\README-windows-dist.md yogawin.dist\README.txt
copy LICENSE yogawin.dist\LICENSE.txt

endlocal


