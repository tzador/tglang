import os
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib


with open("src/languages.json") as f:
    languages = json.load(f)

with open("data/features-ordered.json") as f:
    features = json.load(f)

for F in range(1000, len(features), 500):
    print("#F", F)

    X = []
    y = []

    l = -1
    for language in languages:
        l += 1
        path = f"data/snippets/{language}"
        if not os.path.exists(path):
            continue
        print(f"{l} {language}")
        for file in os.listdir(path):
            with open(f"{path}/{file}") as f:
                snippet = f.read()
            x = []
            for feature in features[:F]:
                x.append(1 if feature in snippet else 0)
            X.append(x)
            y.append(l)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

    for N in [10, 20, 30, 50, 100]:
        print("Training...", F, N)
        clf = RandomForestClassifier(n_estimators=100, max_depth=50)
        clf.fit(X_train, y_train)

        print("Testing...", F, N)
        y_pred = clf.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy {F} {N}: {accuracy*100:.2f}%")

        joblib.dump(
            clf, f"data/random-forest-truncated-D50-F{F}-N{N}-A{accuracy*100:.2f}.pkl")
