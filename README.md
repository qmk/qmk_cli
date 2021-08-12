# QMK CLI
[![CLI Setup](https://github.com/qmk/qmk_cli/workflows/CLI%20Setup/badge.svg)](https://github.com/qmk/qmk_cli/actions?query=workflow%3A%22CLI+Setup%22)  

A program to help users work with [QMK Firmware](https://qmk.fm/).

# Features

* Interact with your qmk_firmware tree from any location
* Use `qmk clone` to pull down anyone's `qmk_firmware` fork
* Setup your build environment with `qmk setup`
* Use `qmk console` to get debugging information from your keyboard(s)
* Check that your environment is correctly setup with `qmk doctor`
* Integrates with qmk_firmware for additional functionality:
    * `qmk compile`
    * `qmk info`
    * `qmk flash`
    * `qmk lint`
    * ...and many more!

# Packages

We provide "install and go" packages for many Operating Systems.

## Linux

Packages for several distributions available here: https://github.com/qmk/qmk_fpm

## macOS

Using [Homebrew](https://brew.sh):

    brew install qmk/qmk/qmk

## Windows

Download our custom MSYS2 installer here: https://msys.qmk.fm/

# Quickstart

* `python3 -m pip install qmk`
* `qmk setup`

# Building

We follow PEP517, you can install using [build](https://pypi.org/project/build/):

Setup:

    python3 -m pip install build

Build:

    python3 -m build

You can read more about working with PEP517 packages in the [Python Packaging User Guide](https://packaging.python.org/guides/distributing-packages-using-setuptools/#packaging-your-project).

# Documentation

Full documentation: <https://docs.qmk.fm/#/tutorial>
