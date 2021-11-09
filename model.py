import sklearn
import argparse
import pickle
import lzma
import pandas as pd
import sklearn.metrics
import sklearn.model_selection
import sklearn.naive_bayes
import sklearn.feature_extraction.text

parser = argparse.ArgumentParser()
# These arguments will be set appropriately by ReCodEx, even if you change them.
parser.add_argument("--dataset_path", default=".\\Data\\reddit_train_dataset.json", type=str, help="Path to annotated dataset")
parser.add_argument("--seed", default=42, type=int, help="Random seed")
parser.add_argument("--test_size", default=0.5, type=lambda x:int(x) if x.isdigit() else float(x), help="Test set size")
parser.add_argument("--model_path", default="bayesian_model.MODEL")

# Create a Naive Bayesian model based on the data inside the input DataFrame
def train_model(data : pd.DataFrame):
    model = sklearn.naive_bayes.MultinomialNB() # Since we have multiple class
    vectorizer = sklearn.feature_extraction.text.CountVectorizer(stop_words='english') # Generates the frequencies of each releveant word, filtering english stop words
    features = vectorizer.fit_transform(data.selftext)
    train_data, test_data, train_target, test_target = sklearn.model_selection.train_test_split(features, data.target, test_size=args.test_size, random_state=args.seed)
    model.fit(train_data, train_target)

    preds = model.predict(test_data)
    accuracy = sklearn.metrics.accuracy_score(test_target, preds) 
    print("Test accuracy was {:4f}%.".format(accuracy*100))
    return model

def main(args):
    df = pd.read_json(args.dataset_path)
    model = train_model(df)
    
    # Save the model file
    with lzma.open(args.model_path, "wb") as model_file:
            pickle.dump(model, model_file)

if __name__ == "__main__":
    args = parser.parse_args([] if "__file__" not in globals() else None)
    main(args)