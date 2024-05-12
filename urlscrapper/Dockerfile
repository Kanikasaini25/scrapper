
FROM python:3.8

WORKDIR /usr/src/app


COPY . .

RUN pip install scrapy
RUN pip install requests
RUN pip install validators
RUN pip install bs4

RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]