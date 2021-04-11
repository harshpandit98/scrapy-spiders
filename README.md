# scrapy-spiders
Repository containing web scrapers.

# setup guide

clone with https / ssh repo url to a directory
- git clone repo_url

create virtualenv (python 3.6 or higher prefered)
- virtualenv env

activate virtualenv
- source ./venv/bin/active

install requirements
- pip install -r requirements.txt

run example
- scrapy runspider filename.py -o output_filename.csv

i.e, scrapy runspider escoth.py -O escoth_data.csv

parameters:
- -o: append to the output_filename.csv if exists

- -O: overwrite the output_filename.csv if exists

- ctrl+c: quits the spider