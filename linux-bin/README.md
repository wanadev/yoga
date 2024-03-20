# YOGA Linux binary

This forlder contains scripts to compile yoga as an executable binary for Linux.

## Requirements

* Python 3.x
* Python 3 headers (Debian/Ubuntu: `apt install python3-dev`)
* Virtualenv (Debian/Ubuntu: `apt install python3-venv`)
* Build tools and CMake (Debian/Ubuntu: `apt install build-essential cmake`)


## Build standalone version from source

Clone this repository:

    git clone https://github.com/wanadev/yoga.git
    cd yoga
    git submodule init
    git submodule update

Run the build script (from the root directory of this repository):

    ./linux-bin/build.sh

Once the build finished, you will find the result in the `yoga-bin.dist` folder. To run YOGA, use the `yoga` executable:

    ./yoga-bin.dist/yoga.bin -h
