import os
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
import joblib


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

X = []
y = []

l = -1
for language in languages:
    l += 1
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

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

for max_depth in [40, 60, 80, 100, 200]:
    print("Training...", max_depth)
    clf = RandomForestClassifier(n_estimators=100, max_depth=max_depth, )
    clf.fit(X_train, y_train)

    joblib.dump(clf, f"data/random-forest-full-{max_depth}.pkl")

    print("Testing...")
    y_pred = clf.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy*100:.2f}%")
