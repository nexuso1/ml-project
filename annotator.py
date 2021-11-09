import json
import re
from os import path

DATA_FOLDER = "Data"

# Heuristic for skipping posts, returns true if there are atleast 2 
# occurences of either gme or gamestop (case insensitive) in the text post
def filter_post(post):
    res = re.findall("gme|gamestop", post['selftext'], re.IGNORECASE)
    if (len(res) > 1):
        return True

    return False

# Removes the 'irrelevant' posts from the file
def format_json(json_file):
    json_file.pop('irrelevant')
    return json_file

# Pauses annotation by dumping the dict into a json
def save_progress(res : dict, dest_irr :str , dest_data : str):
    with open(dest_irr, 'w') as file:
        json.dump(res, file, indent=4)
        file.close()

    with open(dest_data, 'w') as file:
        json.dump(format_json(res), file, indent=4)
        file.close()

# Go through all the posts and remember the answer given by the user
# Commands:
#   '1' = positive, '0' = negative, '3' - irrelevant, 'pause' - save progress
def annotate(n: int, filename : str):

    filtered = 0
    with open(path.join(DATA_FOLDER, filename), 'r') as file:
        posts = json.load(file)
        dest_irr = path.join(DATA_FOLDER, "reddit_annotated_with_irrelevant.json")
        dest_data = path.join(DATA_FOLDER, 'reddit_annotated.json')
        res = {}

        # Resume if not done
        if(path.isfile(dest_irr)):
            with open(dest_irr, 'r') as file:
                res = json.load(file)

            file.close()

        count = len(res.keys())

        # Make a sub-dictionary so that irrelevant posts are skipped
        if not 'irrelevant' in res.keys():
            res['irrelevant'] = {}

        for post in posts:
            if count == n:
                break

            if post in res:
                continue

            if post in res['irrelevant']:
                continue

            if not filter_post(posts[post]):
                filtered += 1
                continue

            print()
            print(count)
            print("Filtered so far: {}".format(filtered))
            print("title:" + posts[post]['title'])
            print("text: " + posts[post]['selftext'])
            value = input(
                "Positive/Negative/Irrelevant/Pause = 1/0/3/pause : ")
            if value == "3":
                if not post in res['irrelevant']:
                    res['irrelevant'][post] = 1
                continue

            if value == "pause":
                save_progress(res, dest_irr, dest_data)
                return

            count += 1
            res[post] = value
            print("====")

    save_progress(res, dest_irr, dest_data)


def main():
    annotate(500, "reddit.json")


if __name__ == "__main__":
    main()
