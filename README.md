# QMK CLI
[![CLI Setup](https://github.com/qmk/qmk_cli/workflows/CLI%20Setup/badge.svg)](https://github.com/qmk/qmk_cli/actions?query=workflow%3A%22CLI+Setup%22)  

A program to help users work with [QMK Firmware](https://qmk.fm/).

# Features

* Interact with your qmk_firmware tree from any location
* Use `qmk clone` to pull down anyone's `qmk_firmware` fork
* Setup your build environment with `qmk setup`
* Check that your environment is correctly setup with `qmk doctor`
* Integrates with your qmk_firmware for additional functionality:
    * `qmk c2json`
    * `qmk compile`
    * `qmk flash`
    * `qmk json2c`
    * `qmk lint`
    * `qmk new-keymap`

# Quickstart

* `python3 -m pip install qmk`
* `qmk setup`

Full documentation: <https://docs.qmk.fm/#/tutorial>
