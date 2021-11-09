import json
import pandas as pd
import argparse

# This wouldn't have been needed if I'd saved the posts properly the first time, but oh well

parser = argparse.ArgumentParser()

parser.add_argument("--target", default=".\\Data\\reddit_annotated.json", type=str, help="Path to post annotations")
parser.add_argument("--data", default=".\\Data\\reddit.json", type=str, help="Path to post data")
parser.add_argument("--train_out", default=".\\Data\\reddit_train_dataset.json", type=str, help="Path to output train dataset")
parser.add_argument("--total_out", default=".\\Data\\reddit_total_dataset.json", type=str, help="Path to output total dataset (all posts)")

def create_datasets(data_path : str, target_path : str) -> tuple[pd.DataFrame, pd.DataFrame]:
    dataset_data = {}
    annotated_data = {}
    train_dataset = {}
    total_dataset = {}
    with open(data_path, 'r') as file:
        dataset_data = json.load(file)
        file.close()

    with open(target_path, 'r') as file:
        annotated_data = json.load(file)
        file.close()

    idx = 0
    for post in annotated_data:
        train_dataset[idx] = dataset_data[post]
        train_dataset[idx]['id'] = post
        train_dataset[idx]['target'] = annotated_data[post]
        idx += 1

    idx = 0
    for post in dataset_data:
        total_dataset[idx] = dataset_data[post]
        total_dataset[idx]['id'] = post
        idx += 1
    
    train = pd.DataFrame(train_dataset).T
    total = pd.DataFrame(total_dataset).T
    
    return train, total 



def save_datasets(train : pd.DataFrame, total:pd.DataFrame, train_path, total_path):
    train.to_json(train_path, indent=4)
    total.to_json(total_path, indent=4)


def main(args):
    train, total = create_datasets(args.data, args.target)
    save_datasets(train, total, args.train_out, args.total_out)
    

if __name__ == "__main__":
    args = parser.parse_args([] if "__file__" not in globals() else None)
    main(args)