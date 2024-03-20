# YOGA: Windows Build

## Requirements

* Git Bash (https://git-scm.com/downloads)
* Python 3.x **64bit** (https://www.python.org/downloads/windows/)
* Virtualenv (`pip install virtualenv` if not installed by the Python installer)
* CMake (https://cmake.org/download/)
* Visual Studio Build Tools (MSVC and MSBuild)


## Build standalone version from source

Clone this repository (using Git Bash):

    git clone https://github.com/wanadev/yoga.git
    cd yoga
    git submodule init
    git submodule update

Run the build script (from the root directory of this repository):

    ./winbuild/builddist.bat

Once the build finished, you will find the result in the `yogawin.dist` folder. To run YOGA, use the `yoga.exe` executable:

    ./yogawin.dist/yoga.exe -h
