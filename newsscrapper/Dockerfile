
FROM python:3.8

WORKDIR /usr/src/app


COPY . .

RUN pip install scrapy
RUN pip install requests
RUN pip install langdetect
RUN pip install bs4
RUN pip install ftfy
RUN pip install datefinder
RUN pip install lxml
RUN pip install feedparser



RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]