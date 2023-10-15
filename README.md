[https://github.com/tzador/tglang](https://github.com/tzador/tglang)

# TGLang - Computer Language Detector

This is a library (in C) for detecting computer languages of a code snippet.

It heavily relies on ChatGPT to generate a dataset of 100 languages codesnippets,
as well as creating indicative substrings that frequently occur in those languages.
We use substrings to vectorize a snippet of code, by putting 1 if a given substrings is in the snippet, 0 otherwise.

# Data set generation

First we generate the code snippets using a typescript script and OpenAI api.
Pretty much it boils down to "generate me a code snippet in languagte C".
Both for faster code snippet generation and since chat completion seems to be repetitive,
I have used gpt-3.5-instruct model to complete string prefixes.
More details in `src/1_dataset.ts`

# Feature generation

For each of the 10 languages, in a repetitive loop of 30, we ask chat gpt to give us a
JSON list of strings that occure in the language source code and are indicative of the langauge.
We collect all of them into a set and use it to vectorize our snippets.

# Training a Random Forest to figure out which features are important

After vecdtorizing our snippets using all of the features, we train a random forest.
As side effect, random forest can tell us which features are important and which less important.
We keep the 1000 most important features.

# Train final random forest using selected features

We retrain the random forest, but use only top 1000 important features for vectorization.
We store it in the file for further processing.

# Transpile the random forest into C code (if else branches)

A python script walks the threes in the forest and emits equivalent C code, which is bundled as library.
