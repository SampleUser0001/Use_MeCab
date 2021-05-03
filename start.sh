#!/bin/bash

INPUT_FILE=/app/input/${VIDEO_ID}.json
python app.py ${VIDEO_ID} ${INPUT_FILE} 

# export PATH=/usr/local/mecab/bin:$PATH
# mecab input/comments.txt -o tmp/result.txt
# csplit -z -f output/result -n 5 tmp/result.txt /EOS/ {*} 1> /dev/null

