# NER Runner (spaCy en_core_web_trf)

This folder includes:
- `run_ner_from_csv.py` — runs NER over `presidential_actions.xlsx` using spaCy's transformer model.
- `requirements.txt` — minimal dependencies.

## Steps (CPU)

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_trf
python run_ner_locally.py
```

## Output
`ner_presidential_actions_YYYY-MM-DD.csv` with columns:
`doc_id, title, type, date, entity_text, entity_type, canonical_entity`

- Entities kept: PERSON, ORG, GPE, NORP, LOC, FAC, LAW, WORK_OF_ART
- Dedupe within each doc by `(canonical_entity, entity_type)`

## Notes
- If you prefer a non-transformer pipeline for speed, replace `en_core_web_trf` with `en_core_web_md` in the script.
- `canonical_entity` applies simple alias merges (e.g., US/USA/U.S. → United States) and smart title casing.
