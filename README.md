# Instagram Data Scraper CLI

A simple CLI inherited from instaloader

## Setup

{python3 -m vevn igscraper </br>
source igscraper/bin/activate  </br>
pip install instagram-scraper} not needed now (or check pls) </br>
pip install instaloader </br>

## To Run
export IG_USER= <your_username> </br>
export IG_PASS= <your_password>

```
python scrape.py username -m M
```

Default value of M is 20. to get all media use --all </br>

currently use python3 scrape.py username only , have to fix this.

## Multi User

```
python scrape.py username1 username2 username3
```
