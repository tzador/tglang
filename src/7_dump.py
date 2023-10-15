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


def to_c_string_literal(s: str) -> str:
    escape_mappings = {
        '\\': '\\\\',
        '"': '\\"',
        '\n': '\\n',
        '\t': '\\t',
        '\r': '\\r',
        '\a': '\\a',
        '\b': '\\b',
        '\f': '\\f',
        '\v': '\\v',
        '%': '\\%',
        '?': '\\?'
    }
    escaped = ''.join(escape_mappings.get(char, char) for char in s)
    return '"' + escaped + '"'


with open("src/tglang.c", "w") as f:
    print('#include "tglang.h"', file=f)
    print('#include <stdlib.h>', file=f)
    print('#include <string.h>', file=f)

    print(
        "enum TglangLanguage tglang_detect_programming_language(const char *text) {", file=f)

    print("  int x[] = {", file=f)
    for feature in features[:F]:
        print(
            f"    strstr(text, {to_c_string_literal(feature)}) ? 1 : 0,", file=f)
    print("  };", file=f)

    print("  int votes[] = {", file=f)
    for language in languages:
        print(f"    0,", file=f)
    print("    0,", file=f)
    print("  };", file=f)

    for tree in clf.estimators_:
        tree_ = tree.tree_

        def recurse(node):
            if tree_.feature[node] != -2:
                print(f"  if (x[{tree_.feature[node]}] == 0) {{", file=f)
                recurse(tree_.children_left[node])
                print(f"  }} else {{", file=f)
                recurse(tree_.children_right[node])
                print(f"  }}", file=f)
            else:
                l = clf.classes_[np.argmax(tree_.value[node])]
                print(f"  votes[{l}] += 1;", file=f)
        recurse(0)
    print(file=f)
    print("  int b = -1;", file=f)
    print("  int m = -1;", file=f)
    print(f"  for (int i = 0; i < {len(languages)}; i++) {{", file=f)
    print("    if (votes[i] > m) {", file=f)
    print("      m = votes[i];", file=f)
    print("      b = i;", file=f)
    print("    }", file=f)
    print("  }", file=f)

    print("  return b;", file=f)

    print("}", file=f)
