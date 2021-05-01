#!/bin/bash

INPUT_FILE=/app/input/chatlog_replay_pmTQqhpHAHs.json
python app.py ${INPUT_FILE}

# export PATH=/usr/local/mecab/bin:$PATH
# mecab input/comments.txt -o tmp/result.txt
# csplit -z -f output/result -n 5 tmp/result.txt /EOS/ {*} 1> /dev/null

