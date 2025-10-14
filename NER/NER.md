***

# NER
## Named Entity Recognition (spaCy)
- The script [run_ner_from_csv.py](/NER/run_ner_from_csv.py) uses **spaCy** with transformer models
  - Looks in its folder for a CSV file called [presidential_actions.csv](/NER/presidential_actions.CSV)
  - Discards numerical entities (e.g. DATE, TIME, PERCENT, MONEY, QUANTITY, ORDINAL, CARDINAL)
  - Generates a CSV file [ner_presidential_actions_YYYY-MM-DD](/NER/ner_presidential_actions_2025-10-14.csv)

***
