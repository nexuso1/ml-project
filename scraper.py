REDDIT_CLIENT_ID = "BpU3gU0TUYg2Kj_c6QPVPg"
REDDIT_SECRET_KEY = "jpMFV1SmlY9IBHtQZmBn5UhEOWdNWg" # not so secret
STORAGE_FOLDER_NAME = "Data"
REDDIT_DATA_FILENAME = "reddit.json"
VERSION = "0.0.1"

import praw
import json
import datetime as dt
from psaw import PushshiftAPI
from os import path


def start_reddit_api():
    pwd = str()
    with open('pw.txt', 'r') as file:
        pwd = file.read()
    
    reddit = praw.Reddit(
        client_id = REDDIT_CLIENT_ID,
        client_secret = REDDIT_SECRET_KEY,
        password = pwd,
        user_agent = "WSB_SCRAPER/{}".format(VERSION),
        username = "ml_project"
    )

    api = PushshiftAPI(reddit)
    return api 

def get_historic_posts(api, search_string, subreddit, start_date, end_date):
    start_date = int(dt.datetime(2021, 1, 6).timestamp())
    end_date = int(dt.datetime(2021, 1, 14).timestamp())
    result = api.search_submissions(after=start_date,
                           before=end_date,
                           subreddit=subreddit,
                           is_self=True,
                           user_removed=False,
                           mod_removed=False,
                           q=search_string)
    
    return list(result)

def serialize_submissions(submissions):
    out_dict = dict()
    destination = path.join('.', STORAGE_FOLDER_NAME, REDDIT_DATA_FILENAME)
    count = 0
    for post in submissions:
        if not (post.selftext == '[removed]' or post.selftext == '[deleted]'):
            out_dict[post.id] = {
                'score' : post.score,
                'selftext' : post.selftext,
                'title' : post.title,
                'created_utc' : post.created_utc,
                'upvote_ratio' : post.upvote_ratio,
                'num_comments' : post.num_comments,
            }

            count += 1

            try:
                name = post.author.name
                id = post.author.id

                author = {
                    'name' : name,
                    'id' : id,
                }
                out_dict[post.id]['author'] = author
            except:
                out_dict[post.id]['author'] = None


    with open(destination, 'w') as file:
        json.dump(out_dict, file, indent=4)

    print("Saved {} Reddit posts".format(count))

def main():
    api = start_reddit_api()
    res = get_historic_posts(api, 'gme|gamestop', 'wallstreetbets')
    serialize_submissions(res)
 

if __name__ == "__main__":
    main()