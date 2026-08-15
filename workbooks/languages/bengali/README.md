# Bengali

Bengali gender bias measurement, following the general methodology in
[../../workbooks/wikipedia_workbook.md](../../workbooks/wikipedia_workbook.md) and
[../../workbooks/beyond_wikipedia_workbook.md](../../workbooks/beyond_wikipedia_workbook.md).

Measured using three corpora: Wikipedia, a literary corpus built from Bengali
Wikisource, and a newspaper corpus built from Prothom Alo.

## Defining Set (7 pairs)

| English | Bengali |
|---|---|
| woman - man | নারী - পুরুষ |
| daughter - son | কন্যা - পুত্র |
| mother - father | মা - বাবা |
| girl - boy | মেয়ে - ছেলে |
| queen - king | রানী - রাজা |
| wife - husband | স্ত্রী - স্বামী |
| madam - sir | ম্যাডাম - স্যার |

## Profession Set (32 words)

Bengali largely lacks grammatical gender, but 5 profession words retain vestigial
masculine/feminine forms (teacher, actor, writer, nurse, student); 6 professions
have borrowed-English vs. native-Bengali variants (engineer, manager, driver, chef,
governor, worker); 2 are multi-word phrases (filmmaker, comedian).

## Corpus Statistics

| Corpus | Size | Articles/Pages | Sentences |
|---|---|---|---|
| Wikipedia | 1.2 GB | 187,772 | 1,791,600 |
| Literature (Wikisource) | 267 MB | 96,365 proofread pages | 739,073 |
| Newspaper (Prothom Alo) | 4.6 GB | 949,036 | Not computed |

## Gender Direction Reliability (PCA gap)

| Corpus | PCA Gap |
|---|---|
| Wikipedia | 0.134 |
| Newspaper | 0.101 |
| Literature | 0.049 (flagged unreliable, below the 0.06 benchmark) |

## Corpus-Level Bias

| Corpus | Simple Average | Weighted Average |
|---|---|---|
| Wikipedia | -0.0022 | +0.0268 (flips female-leaning) |
| Newspaper | -0.0139 | -0.0427 (stays male-leaning) |
| Literature | -0.1193 | Not reported (unreliable) |

## Key Findings

- Wikipedia's bias direction flips between simple and weighted averaging; the
  newspaper corpus does not replicate this flip.
- Several professions (teacher, nurse, governor, scientist, and others) reverse
  direction entirely between Wikipedia and newspaper.
- The literary corpus produces a near-uniform, unreliable result (21 of 22
  measurable professions male-leaning), interpreted as a breakdown of the
  measurement method on archaic, poetic language rather than a genuine finding.

## Notes and Translation Challenges

- Wikisource stores literary text in a separate "Page" namespace, not resolved by
  standard extraction tools; a custom parser was required.
- Several Wikisource filenames reflect a later reprint/collected-works edition year
  rather than the original publication date; original dates were verified against
  independent sources.
- Full results, per-profession breakdowns, and paper draft available in the
  [bengali-gender-bias](https://github.com/Ashikahamedpranto/bengali-gender-bias)
  repository.
