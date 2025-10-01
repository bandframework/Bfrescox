#!/bin/bash

python -m pip install --upgrade pip
python -m pip install tox
echo
which python
which pip
which tox
echo
python --version
pip --version
tox --version
echo
pip list
