import json
import joblib
import os
import numpy as np

D = 50
F = 1000
N = 10

clf = joblib.load(f"data/random-forest-truncated-D50-F1000-N10-A94.39.pkl")

with open("src/languages.json") as f:
    languages = json.load(f)

with open("data/features-ordered.json") as f:
    features = json.load(f)


def classify(snippet):
    x = []
    for feature in features[:F]:
        x.append(1 if feature in snippet else 0)

    def predict(tree):
        tree_ = tree.tree_

        def recurse(node):
            if tree_.feature[node] != -2:
                if x[tree_.feature[node]] == 0:
                    return recurse(tree_.children_left[node])
                else:
                    return recurse(tree_.children_right[node])
            else:
                return clf.classes_[np.argmax(tree_.value[node])]

        return recurse(0)

    votes = [0] * len(languages)
    for tree in clf.estimators_:
        votes[predict(tree)] += 1

    l = np.argmax(votes)
    return languages[l]


total = 0
correct = 0

for language in languages:
    path = f"data/snippets/{language}"
    if not os.path.exists(path):
        continue
    for file in os.listdir(path):
        with open(f"{path}/{file}") as f:
            snippet = f.read()
            predicted = classify(snippet)
            total += 1
            if language == predicted:
                correct += 1
            print(language, f"Accuracy: {correct / total}")
