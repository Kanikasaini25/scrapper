#!/bin/sh

python3 -u rss_spider.py &
python3 -u rss_spider_hindi.py
python3 -u live_uptoday.py

