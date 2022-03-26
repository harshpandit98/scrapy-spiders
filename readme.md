# Setup guide

Clone with ssh repo url to a directory

`git clone --single-branch --branch add/target git@github.com:harshpandit98/scrapy-spiders.git`

Create virtualenv (python 3.8 or higher prefered)
- `virtualenv venv`

Activate virtualenv
- `source ./venv/bin/active`

Install requirements
- `pip install -r requirements.txt`

run example
- scrapy crawl target -o ex.json -a url="https://www.target.com/p/-/A-81260450"

parameters:
- -a url: product url

- -o: append to the output_filename.json if exists

- -O: overwrite the output_filename.json if exists

- ctrl+c: quits the spider