#!/bin/bash

cp -r $1 ~/qmk_cli

export PATH=~/.local/bin:$PATH
echo "PATH=$PATH" >> ~/.bashrc

export QMK_HOME=~/qmk_firmware
export CLI_DIR=~/qmk_cli

cd $CLI_DIR
python3 -m pip install -r requirements.txt
python3 setup.py sdist bdist_wheel
cd ~
python3 -m pip install --force-reinstall --no-index --no-deps --prefix=~/.local --find-links qmk_cli/dist qmk
