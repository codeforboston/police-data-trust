#!/bin/bash
export LDFLAGS="-L/opt/homebrew/Cellar/openssl@3/3.0.3/lib"
export CPPFLAGS="-I/opt/homebrew/Cellar/openssl@3/3.0.3/include"
pip3 install -r requirements/dev_unix.txt