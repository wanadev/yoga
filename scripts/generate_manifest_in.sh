#!/bin/bash

##
## Lists the files to include in sdist distribution. This can be used to
## generate the MANIFEST.in contents:
##
##     scripts/generate_manifest_in.sh > MANIFEST.in
##

echo "include README.rst"
echo "include LICENSE"

echo

find yoga/model -name "*.h" -exec echo "include" "{}" ";"
find yoga/model -name "*.c" -exec echo "include" "{}" ";"
find yoga/model -name "*.cpp" -exec echo "include" "{}" ";"

echo

echo "include assimp/CREDITS"
echo "include assimp/LICENSE"
echo "include assimp/README.md"
echo "include assimp/CMakeLists.txt"
find assimp -type f -name "*.in" -exec echo "include" "{}" ";" \
     | grep -v "^include assimp/\(include\|cmake-modules\|contrib\|test\|doc\)/"
find assimp/cmake-modules -type f -exec echo "include" "{}" ";"
find assimp/code -type f -exec echo "include" "{}" ";"
find assimp/contrib -type f -exec echo "include" "{}" ";" \
     | grep -v "^include assimp/contrib/gtest"
find assimp/include -type f -exec echo "include" "{}" ";"

echo

echo "recursive-exclude test *"
