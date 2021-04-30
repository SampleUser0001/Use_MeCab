#!/bin/bash

export PATH=/usr/local/mecab/bin:$PATH

mecab input/comments.txt -o tmp/result.txt
csplit -z -f output/result -n 5 tmp/result.txt /EOS/ {*} 1> /dev/null

python app.py
