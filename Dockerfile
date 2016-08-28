FROM python:2.7.8

RUN pip install Scrapy

RUN mkdir /data

RUN mkdir -p /usr/src/app/scrap-bcc

WORKDIR /usr/src/app/scrap-bcc

COPY . /usr/src/app/scrap-bcc

VOLUME /data

EXPOSE 6023


CMD ["scrapy", "crawl", "bcc"]

