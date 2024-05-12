
FROM python:3

WORKDIR /usr/src/app


COPY . .

RUN pip3 install scrapy
RUN pip3 install requests
RUN pip3 install bs4


RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]