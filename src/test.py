import json
import os
import subprocess

with open("src/languages.json") as f:
    languages = json.load(f)

total = 0
correct = 0

l = -1
for language in languages:
    l += 1
    path = f"../data/snippets/{language}"
    if not os.path.exists(path):
        continue
    for file in os.listdir(path):
        result = subprocess.run(
            ["./test", f"{path}/{file}"], capture_output=True)
        detected = int(result.stdout.decode("utf-8"))
        total += 1
        if detected == l:
            correct += 1
        print(l, correct / total)
