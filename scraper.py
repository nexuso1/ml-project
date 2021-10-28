REDDIT_CLIENT_ID = "BpU3gU0TUYg2Kj_c6QPVPg"
REDDIT_SECRET_KEY = "jpMFV1SmlY9IBHtQZmBn5UhEOWdNWg" # not so secret
VERSION = "0.0.1"

import requests
import praw




def start_reddit_api():
    reddit_auth = requests.auth.HTTPBasicAuth(REDDIT_CLIENT_ID, REDDIT_SECRET_KEY)
    password = str()

    with open('pw.txt', 'r') as file:
        password = file.read().strip()

    data = {
        'grant_type' : 'password',
        'username' : 'jamescalam',
        'password' : password
    }

    headers = { 'User-Agent' : 'Scraper ver {}'.format(VERSION)}

    token = requests.post("")

def main():
    start_reddit_api()
 

if __name__ == "__main__":
    main()