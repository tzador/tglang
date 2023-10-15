import os
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np


with open("src/languages.json") as f:
    languages = json.load(f)


def read_features():
    features = set()
    for language in languages:
        path = f"data/features/{language}.json"
        if os.path.exists(path):
            with open(path) as f:
                for feature in json.load(f):
                    features.add(feature)
    features = list(features)
    features.sort()
    return features


features = read_features()


def order_features():
    X = []
    y = []

    l = -1
    for language in languages:
        l += 1
        print(l, language)
        path = f"data/snippets/{language}"
        if not os.path.exists(path):
            continue
        for file in os.listdir(path):
            with open(f"{path}/{file}") as f:
                snippet = f.read()
            print(f"{l} {file}")
            x = []
            for feature in features:
                x.append(1 if feature in snippet else 0)
            X.append(x)
            y.append(l)

    print("Training...")
    clf = RandomForestClassifier(n_estimators=100, max_depth=50)
    clf.fit(X, y)

    importances = clf.feature_importances_
    sorted_indices = np.argsort(importances)[::-1]

    important_features = []
    for i in sorted_indices:
        important_features.append(features[i])

    return important_features


with open("data/features-ordered.json", "w") as f:
    json.dump(order_features(), f)
