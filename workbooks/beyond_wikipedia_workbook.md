# Beyond Wikipedia Workbook

This workbook walks through measuring gender bias using a corpus other than Wikipedia. It covers two paths: building a corpus from a **newspaper archive**, and
building a corpus from a **literary source like Wikisource**. It generalizes the steps used for a Bengali newspaper corpus and a Bengali literary corpus, and should
apply to other languages and other non-Wikipedia sources, such as government documents or social media data.

Read the [Wikipedia Workbook](wikipedia_workbook.md) first. Once you have a corpus built, either from a newspaper or from a literary source, the remaining steps
(tokenizing, training a Word2Vec model, building a gender direction, calculating bias scores) are identical to the Wikipedia workbook. This workbook covers what is
different: finding and preparing a non-Wikipedia corpus in the first place.

## Why use a corpus other than Wikipedia

Prior work has shown that gender bias measured in word embeddings is not always consistent across different types of text within the same language. A study of
English found that bias differs across news, social media, biomedical text, and Wikipedia. A similar study of Arabic compared Wikipedia against newspaper archives. For Bengali, comparing Wikipedia against both a newspaper corpus and a literary corpus revealed that a distinctive pattern found in Wikipedia did not appear in the
newspaper corpus, and that the literary corpus's older, more stylistically varied language actually broke down the reliability of the measurement method itself. If
you have already measured bias using Wikipedia for your language, comparing it against a second, different type of corpus is a natural next step, and may reveal
whether your Wikipedia results reflect the language generally, or something
specific to Wikipedia's writing style.
-

# Section 1: Newspaper

## Step 1: Find a corpus

Options to consider, roughly in order of ease of access:

- **A dataset already published for NLP research**, for example on Kaggle or
  HuggingFace Datasets. Search for your language plus "news corpus" or "newspaper
  dataset."
- **A newspaper's own public archive**, if one exists and allows bulk access.

Whichever source you use, check its licensing terms before using it in published
research.

## Step 2: Inspect the data before processing all of it

Before writing code to process an entire dataset, load just one small piece first
and check its actual structure.

```python
import pandas as pd
df = pd.read_csv("one_file_from_your_dataset.csv")
print(df.shape)
print(df.columns.tolist())
df.head(3)
```

Identify which column actually contains the article text (it may be called `body`,
`content`, `text`, or something else), and whether there is a status column you
need to filter on (for example, to exclude unpublished drafts).

## Step 3: Combine all files into one corpus

If your dataset is split across many files (for example, one file per month), loop
through all of them:

```python
import pandas as pd
import glob
import re

def clean_text(text):
    if pd.isna(text):
        return ""
    text = re.sub(r'\s+', ' ', str(text))
    return text.strip()

data_files = sorted(glob.glob("your_data_folder/*.csv"))
count = 0
with open("corpus.txt", "w", encoding="utf-8") as f_out:
    for filepath in data_files:
        df = pd.read_csv(filepath)
        for _, row in df.iterrows():
            if row.get('status') == 'published':  # adjust to your actual column
                body = clean_text(row.get('body'))  # adjust to your actual column
                if len(body) > 20:
                    f_out.write(body + "\n")
                    count += 1

print(f"Total articles written: {count}")
```

## Step 4: If your corpus is large, plan for interrupted training

Newspaper corpora can be significantly larger than a Wikipedia dump for the same
language. A Bengali newspaper corpus of just under one million articles was roughly
four times the size of the corresponding Wikipedia corpus. Training a Word2Vec
model on a very large corpus in a single continuous run increases the risk of
losing hours of progress to a disconnected Colab session or an unstable network
connection.

If your corpus is large, split it into chunks and train incrementally, saving a
checkpoint after each chunk.

```python
# Split the corpus into chunks of a manageable size
!split -l 60000 corpus.txt chunk_ --numeric-suffixes=1 --additional-suffix=.txt
```

```python
import os, glob
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

checkpoint_path = f"{DRIVE_DIR}/word2vec_progress.model"
progress_file = f"{DRIVE_DIR}/last_completed_chunk.txt"

if os.path.exists(progress_file):
    with open(progress_file) as f:
        last_done = int(f.read().strip())
    model = Word2Vec.load(checkpoint_path)
else:
    last_done = 0
    model = None

chunks = sorted(glob.glob("chunk_*_tokenized.txt"))

for i, chunk_path in enumerate(chunks, start=1):
    if i <= last_done:
        continue

    sentences = LineSentence(chunk_path)
    if model is None:
        model = Word2Vec(vector_size=300, window=5, min_count=5, workers=2, sg=1, epochs=5)
        model.build_vocab(sentences)
    else:
        model.build_vocab(sentences, update=True)

    model.train(sentences, total_examples=model.corpus_count, epochs=model.epochs)
    model.save(checkpoint_path)
    with open(progress_file, "w") as f:
        f.write(str(i))
    print(f"Chunk {i}/{len(chunks)} done and saved.")

model.save(f"{DRIVE_DIR}/word2vec_FINAL.model")
```

If a disconnect happens partway through, simply reconnect, remount Google Drive,
and re-run this same code. It will automatically detect the last completed chunk
and resume from there, rather than starting over.

If chunks of 240,000 lines or similar prove too large and still risk losing
significant progress to a disconnect, reduce the chunk size, for example to 60,000
lines, so that each individual chunk represents a smaller amount of lost work in
the worst case.

## Step 5: Counting word frequencies and multi-word phrases in a large corpus

For a very large corpus file, avoid loading the entire file into memory at once,
this can crash your session. Read it one line at a time instead:

```python
def count_phrase_streaming(filepath, phrase):
    count = 0
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            count += line.count(phrase)
    return count
```

This same line-by-line approach applies to counting individual word frequencies
across a large corpus as well.

## Newspaper: common issues you may run into

- **A very large word-count or model file**: GitHub's web upload interface has a
  25MB limit even though GitHub itself allows files up to 100MB. Files between
  25MB and 100MB can still be pushed using git from the command line, they just
  cannot be uploaded through the website's upload button.
- **Missing words**: some modern profession words may simply not appear in an
  older archive, or vice versa. This is expected and worth reporting.

---

# Section 2: Literature

## Step 1: Find a literary source

**Wikisource** is generally the most accessible option if your language has a
Wikisource edition, since it is structured similarly to Wikipedia and hosts
public-domain literary works. Other options include a national library's digital
archive, or a published literary dataset if one exists for your language.

## Step 2: Understand that Wikisource stores content differently from Wikipedia

If you are using Wikisource, be aware that it stores its content very differently
from Wikipedia. The reading-view page for a work is often just a set of references
pointing to a separate part of the site (the "Page" namespace) where individual
scanned pages have been transcribed and quality-checked by volunteers. Standard
extraction tools built for Wikipedia's structure will not resolve these references,
and using them directly on a Wikisource dump will likely yield almost no usable
text.

## Step 3: Download the full-history dump and extract the Page namespace

To extract real text from Wikisource, download the full-history dump (not the
standard articles-only dump), and parse it directly for pages in namespace 104
(the Page namespace), keeping only pages marked with a quality level of proofread
or validated.

```python
import bz2, re, html

def clean_wikisource_text(raw_text):
    text = html.unescape(raw_text)
    text = re.sub(r'<noinclude>.*?</noinclude>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()

def get_quality_level(raw_text):
    unescaped = html.unescape(raw_text)
    match = re.search(r'pagequality level="(\d)"', unescaped)
    return int(match.group(1)) if match else None
```

Loop through the dump, keep only namespace 104 pages with a quality level of 3
(proofread) or 4 (validated), clean each page's text, and write it to your corpus
file.

## Step 4: Be cautious about publication dates

Filenames on Wikisource sometimes reflect the year of a later reprint or
collected-works edition rather than the work's original publication date.
Cross-check against independent sources, especially when a filename year seems
implausibly late relative to what is known about the author, for example, a
filename year that falls after the author's known date of death.

## Literature: common issues you may run into

- **Very little usable text on a first attempt**: if a standard extraction tool
  yields almost no text, this is very likely the Page namespace issue described in
  Step 2 and 3 above, not a problem with your code.
- **A near-uniform, one-sided bias result**: if almost every measured word comes
  back leaning the same direction regardless of what the word actually means, this
  is more likely a sign that the gender direction failed to isolate gender
  specifically (check your PCA reliability gap) than a genuine finding that the
  corpus is extremely biased. Older, more stylistically varied or poetic language
  can degrade the reliability of this method. Report this as a methodological
  limitation rather than a confirmed result.
- **Missing words**: an older literary corpus may simply not contain modern
  profession words at all (for example, "analyst" or "astronaut"). This is
  expected and worth reporting, not a bug to fix.

---

## Comparing against your Wikipedia results

Once you have bias scores from both a Wikipedia corpus and a second corpus (whether
newspaper, literary, or both) for the same language, compare:

1:- Whether the overall simple and weighted averages point in the same direction in
  both corpora, or flip.
2:- Whether individual profession words reverse direction between the two corpora.
3:- Whether the PCA reliability gap is meaningfully different between the two
  corpora, this can help explain differences you observe, or flag when a result
  should not be trusted.

Once you have all your results, you can store them here in this repository.
