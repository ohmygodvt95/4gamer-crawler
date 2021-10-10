FROM python:3

WORKDIR /scrapy

RUN pip install Scrapy

COPY run /usr/local/bin/run-crawler

RUN chmod +x /usr/local/bin/run-crawler
