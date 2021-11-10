# Instagram Data Scraper CLI

A simple CLI inherited from instaloader

## Setup

python3 -m vevn igscraper  
source igscraper/bin/activate  
pip install instagram-scraper  
pip install instaloader  

## To Run
export IG_USER= <your_username>  
export IG_PASS= <your_password>  

## Single User
```
python scrape.py username
```

## Multi User

```
python scrape.py username1 username2 username3
```

## Getting All Followers
* Make sure to have run Single user on username
```
python scrape.py username -a
```
 
## output
Directory with images, metedata file , followees list text file, nolocation.txt - names of files which don't have location </br>
some json zip files of all other metadata data and logs  (Can be ignored)