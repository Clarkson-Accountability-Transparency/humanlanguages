# Wikipedia Workbook: Measuring Gender Bias for a New Language

This workbook walks through building a Wikipedia-based corpus and measuring gender
bias for any language that has a Wikipedia edition. It generalizes the steps used
for Bengali and Hindi, and should work the same way for any other language.

You do not need to be an experienced programmer to follow this. Each step includes
the actual commands to run. This is designed to run in Google Colab, which gives
you free access to computing power and easy connection to Google Drive for saving
your work.

## Before you start

You will need:
- The two-letter or three-letter Wikipedia language code for your language (for
  example, `bn` for Bengali, `hi` for Hindi, `es` for Spanish). You can find this by
  going to `https://en.wikipedia.org/wiki/List_of_Wikipedias`.
- A defining set of 7 gendered word pairs in your language, translated from: woman
  and man, daughter and son, mother and father, girl and boy, queen and king, wife
  and husband, madam and sir. If some of these pairs do not translate cleanly into
  your language, that is worth noting, it happened for several of the original nine
  languages too.
- A profession set of words in your language. The original study used 32
  professions: nurse, teacher, writer, engineer, scientist, manager, driver,
  banker, musician, artist, chef, filmmaker, judge, comedian, inventor, worker,
  soldier, journalist, student, athlete, actor, governor, farmer, person, lawyer,
  adventurer, aide, ambassador, analyst, astronaut, astronomer, biologist. For each
  one, check whether your language has a single neutral word, separate
  masculine/feminine forms, or both a borrowed and a native form. This step often
  takes longer than expected, and is worth doing carefully.

## Step 1: Download the Wikipedia dump for your language

```python
!wget https://dumps.wikimedia.org/{your_language_code}wiki/latest/{your_language_code}wiki-latest-pages-articles.xml.bz2
```

Replace `{your_language_code}` with your actual code, for example `bn` for Bengali.
Check the file downloaded correctly:

```python
!ls -lh {your_language_code}wiki-latest-pages-articles.xml.bz2
```

## Step 2: Extract clean text from the dump

```python
!pip install wikiextractor
!python -m wikiextractor.WikiExtractor {your_language_code}wiki-latest-pages-articles.xml.bz2 --output extracted --json --processes 4
```

If this fails with errors related to regular expressions, this is a known
compatibility issue between older versions of WikiExtractor and newer versions of
Python. Installing an older version of the tool resolves it:

```python
!pip install wikiextractor==3.0.6
```

## Step 3: Combine the extracted files into one corpus file

```python
import json, os

count = 0
with open("corpus.txt", "w", encoding="utf-8") as f_out:
    for root, dirs, files in os.walk("extracted"):
        for filename in files:
            filepath = os.path.join(root, filename)
            with open(filepath, "r", encoding="utf-8") as f_in:
                for line in f_in:
                    try:
                        article = json.loads(line)
                        text = article.get("text", "").strip()
                        if text:
                            f_out.write(text + "\n")
                            count += 1
                    except json.JSONDecodeError:
                        continue

print(f"Wrote {count} articles to corpus.txt")
```

## Step 4: Save your corpus to Google Drive

Working in Colab means your files disappear when the session ends. Save your
progress as you go.

```python
from google.colab import drive
drive.mount('/content/drive')

import os
DRIVE_DIR = "/content/drive/MyDrive/YourLanguage_NLP_Bias_Project"
os.makedirs(DRIVE_DIR, exist_ok=True)
!cp corpus.txt "{DRIVE_DIR}/"
```

## Step 5: Train a Word2Vec model

```python
!pip install gensim
from gensim.models import Word2Vec
import re

def tokenize(text):
    text = re.sub(r'[,.!?"()\[\]—\-\'‘’]', ' ', text)
    return text.split()

sentences = []
with open("corpus.txt", encoding="utf-8") as f:
    for line in f:
        tokens = tokenize(line)
        if tokens:
            sentences.append(tokens)

print(f"Total sentences: {len(sentences)}")

model = Word2Vec(sentences, vector_size=300, window=5, min_count=5, workers=4, sg=1)
model.save(f"{DRIVE_DIR}/word2vec.model")
```

Note: the punctuation characters removed in `tokenize()` above are common in
English-derived punctuation. Check whether your language uses different
punctuation marks (for example, Bengali uses `।` as a sentence-ending mark instead
of a period) and add them to this list.

## Step 6: Count how often your target words appear

```python
word_counts = Counter()
with open("corpus.txt", encoding="utf-8") as f:
    for line in f:
        word_counts.update(tokenize(line))

# Check your defining set and profession set words are actually present
for word in your_defining_set_words:
    print(f"{word}: {word_counts[word]}")
```

If a word shows a count of 0, it either genuinely does not appear in your corpus,
or there is a typo or encoding issue worth double-checking.

## Step 7: Build the gender direction

```python
import numpy as np
from sklearn.decomposition import PCA

defining_pairs = [
    ("woman_translation", "man_translation"),
    ("daughter_translation", "son_translation"),
    # ... your remaining 5 pairs
]

diffs = []
for female_word, male_word in defining_pairs:
    if female_word in model.wv and male_word in model.wv:
        diffs.append(model.wv[female_word] - model.wv[male_word])
    else:
        print(f"Missing: {female_word} or {male_word}")

diffs = np.array(diffs)
pca = PCA(n_components=min(len(diffs), 10))
pca.fit(diffs)
gender_direction = pca.components_[0]
gap = pca.explained_variance_ratio_[0] - pca.explained_variance_ratio_[1]

print(f"PCA reliability gap: {gap:.3f}")
```

The reliability gap tells you how much you can trust the gender direction you just
built. In the original nine-language study, Wolof scored 1.00 (unreliable, due to a
very small corpus) and Chinese scored 0.06 (unreliable). Bengali scored 0.134 and
Hindi scored 0.072. If your gap is below roughly 0.06 to 0.10, treat your results
with caution, this may mean the gender direction is not reliably capturing gender
specifically.

## Step 8: Calculate bias scores

```python
def cosine_sim(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def direct_bias(word, gender_direction, model, c=1):
    if word not in model.wv:
        return None
    vec = model.wv[word]
    cos_sim = cosine_sim(vec, gender_direction)
    return abs(cos_sim) ** c * np.sign(cos_sim)

for profession_word in your_profession_words:
    bias = direct_bias(profession_word, gender_direction, model)
    print(f"{profession_word}: {bias}")
```

A positive score means the word leans female-associated; a negative score means it
leans male-associated.

## Step 9: Handle words with multiple forms

If a profession has more than one common form (a borrowed word and a native word,
or masculine and feminine forms), calculate the bias for each form separately, then
combine them using a frequency-weighted average, so the more commonly used form
counts for more:

```python
def weighted_bias(forms_with_counts, gender_direction, model):
    total_count = sum(count for _, count in forms_with_counts)
    if total_count == 0:
        return None
    weighted = 0
    for word, count in forms_with_counts:
        bias = direct_bias(word, gender_direction, model)
        if bias is not None:
            weighted += bias * (count / total_count)
    return weighted
```

## Step 10: Calculate corpus-level summary statistics

```python
simple_average = sum(all_bias_scores.values()) / len(all_bias_scores)

# Weighted average uses each profession's total occurrence count as its weight
weighted_average = sum(
    all_bias_scores[p] * profession_counts[p] for p in all_bias_scores
) / sum(profession_counts[p] for p in all_bias_scores)

print(f"Simple average: {simple_average:.4f}")
print(f"Weighted average: {weighted_average:.4f}")
```

Compare these two numbers. In the original study, most languages showed the same
direction under both calculations. Spanish and, later, Bengali were exceptions,
their overall bias direction flipped between the simple and weighted average. This
is worth checking for your language too.

## Common issues you may run into

- **Session disconnects during training**: Colab sessions can disconnect,
  especially on unstable networks or for very large corpora. Consider splitting
  training into smaller chunks with checkpointing (see the Newspaper Workbook for a
  worked example of this).
- **Words with multiple spellings or variant forms**: some languages have more
  spelling variation than others. Check your word counts carefully before assuming
  a word is genuinely absent from the corpus.
- **A very low PCA reliability gap**: this does not necessarily mean your language
  has no gender bias, it may mean the defining set does not translate as cleanly
  into your language, or that this specific corpus register does not suit the
  method well. Document this clearly rather than reporting the results as
  confirmed findings.

## What to do with your results

Once you have all your results, you can store them here in this repository, under a folder named for your language.
