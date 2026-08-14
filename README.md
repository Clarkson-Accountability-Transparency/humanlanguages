# Human Languages: Gender Bias in NLP

This repository is a resource for anyone who wants to measure gender bias in word
embeddings for a language, or a type of text, not yet covered by this research.

Word embedding models learn to represent words as vectors based on how those words
are used in text, and in doing so, they pick up the social biases present in that
text, including gender bias. This repository documents a method for measuring that
bias, called DirectBias, and applies it across different languages and different
types of text.

Check out our research papers on this topic [here](https://lin-web.clarkson.edu/~jmatthew/HumanLanguages/) as well.

## What has already been done

This methodology has already been applied to nine languages: English, Chinese,
Spanish, Arabic, German, French, Farsi, Urdu, and Wolof. In every case, the corpus
used was Wikipedia.

Since then, it has been extended to two more languages, Bengali and Hindi, and to
two additional types of text beyond Wikipedia for Bengali. Bengali has been measured
using Wikipedia, a literary corpus, and a newspaper corpus; Hindi has been measured
using Wikipedia. Nepali is currently in progress.

## What this repository is for

If you want to apply this same methodology to a language that hasn't been covered
yet, or to a different type of text such as a newspaper archive instead of
Wikipedia, this repository gives you two step-by-step guides to start from:

- **[Wikipedia Workbook](workbooks/wikipedia_workbook.md)** — walks through building
  a corpus and measuring gender bias using Wikipedia, for any language that has a
  Wikipedia edition.
- **[Beyond Wikipedia Workbook](workbooks/beyond_wikipedia_workbook.md)** — walks through doing
  the same using a newspaper archive, a literary corpus, or another non-Wikipedia
  source of text.

  Each workbook is written to be language-agnostic, so you can follow it for whichever
language you are working with.

You can also find other related materials including:
- **[Defining Sets ](yamls)** — suggested defining set pairs and neutral words for a variety of languages in yaml
- **[Other Scripts](script) and [Figures](figures)** related to our work



## Where this comes from

This work builds on the original gender bias measurement method introduced by Bolukbasi et al. (2016) for English, later extended to eight additional languages, and is now being extended to more languages and corpus types beyond that.
