# QMK CLI

> A program to help users work with [QMK Firmware](https://qmk.fm/).

[![Latest Release](https://img.shields.io/github/v/tag/qmk/qmk_cli?color=3D87CE&label=Latest&sort=semver&style=for-the-badge)](https://github.com/qmk/qmk_cli/tags)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/qmk/qmk_cli/cli_setup.yml?logo=github&style=for-the-badge)](https://github.com/qmk/qmk_cli/actions?query=workflow%3ACLI+branch%3Amaster)
[![Discord](https://img.shields.io/discord/440868230475677696.svg?logo=discord&logoColor=white&color=7289DA&style=for-the-badge)](https://discord.gg/qmk)

## Features

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

## Quickstart

Follow our [documentation to get started](https://docs.qmk.fm/newbs_getting_started).

## Packages

We provide "install and go" packages for many Operating Systems.

### macOS

Using [Homebrew](https://brew.sh):

    brew install qmk/qmk/qmk

### Windows

Download our custom MSYS2 installer here: https://msys.qmk.fm/

## Building

We follow PEP517, you can install using [build](https://pypi.org/project/build/):

Setup:

    python3 -m pip install build

Build:

    python3 -m build

You can read more about working with PEP517 packages in the [Python Packaging User Guide](https://packaging.python.org/guides/distributing-packages-using-setuptools/#packaging-your-project).

## Documentation

Full documentation: <https://docs.qmk.fm/#/tutorial>
