#!/bin/bash

set -e


# Create and/or activate the virtual env
mkdir -p build/

if [ ! -d build/__env__/ ] ; then
    python3 -m venv build/__env__/
    source build/__env__/bin/activate
    pip install -r linux-bin/requirements.txt
    pip install -e .
else
    source build/__env__/bin/activate
fi


# Build YOGA
python -m nuitka \
    --standalone \
    --follow-imports \
    --include-package=PIL \
    linux-bin/yoga-bin.py


# Rename YOGA binary
mv yoga-bin.dist/yoga-bin.bin yoga-bin.dist/yoga.bin


# Copy additional files
cp LICENSE yoga-bin.dist/LICENSE
cp linux-bin/README-linux-dist.md yoga-bin.dist/README.md
