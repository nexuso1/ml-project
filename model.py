import sklearn
import argparse
import sklearn.preprocessing
import sklearn.naive_bayes

parser = argparse.ArgumentParser()
# These arguments will be set appropriately by ReCodEx, even if you change them.
parser.add_argument("--datset_path", default=".\\Data\\reddit_annotated.json", type=str, help="Path to annotated dataset")
parser.add_argument("--seed", default=42, type=int, help="Random seed")
parser.add_argument("--test_size", default=0.5, type=lambda x:int(x) if x.isdigit() else float(x), help="Test set size")

def train_model():
    model = sklearn.naive_bayes.MultinomialNB()

def main(args):
    pass

if __name__ == "__main__":
    args = parser.parse_args([] if "__file__" not in globals() else None)
    main(args)