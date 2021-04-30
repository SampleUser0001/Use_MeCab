# 任意のイメージを取得
FROM python:3.10-rc-slim-buster

RUN apt update && apt upgrade -y
RUN apt install -y wget gcc make g++

WORKDIR /root

RUN wget -O "mecab.tar.gz" "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7cENtOXlicTFaRUE"
RUN wget -O "mecab-ipadic.tar.gz" "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7MWVlSDBCSXZMTXM"

RUN tar xvfz mecab.tar.gz
RUN tar xvfz mecab-ipadic.tar.gz

WORKDIR /root/mecab-0.996
RUN ./configure --enable-utf8-only --prefix=/usr/local/mecab && make && make install

WORKDIR /root/mecab-ipadic-2.7.0-20070801
RUN ./configure --prefix=/usr/local/mecab --with-mecab-config=/usr/local/mecab/bin/mecab-config --with-charset=utf8 && make && make install 

# RUN export PATH=/usr/local/mecab/bin:$PATH

# RUN pip3 install mecab-python3

WORKDIR /app

COPY app /app
COPY start.sh /start.sh

RUN chmod 755 /start.sh

CMD [ "/start.sh" ]
