#!/usr/bin/env python3
"""
Run NER with spaCy (en_core_web_trf) over a CSV file.

Expected input file (same folder as this script):
  presidential_actions.csv

Required columns (case-insensitive accepted, will be normalized):
  doc_id, title, type, date, text_clean

Output:
  ner_presidential_actions_<YYYY-MM-DD>.csv with columns:
  doc_id, title, type, date, entity_text, entity_type, canonical_entity
"""
import sys, re
from pathlib import Path
from datetime import date
import pandas as pd
import spacy
from spacy.util import is_package

INPUT = Path("presidential_actions.csv")
ALLOWED = {"PERSON","ORG","GPE","NORP","LOC","FAC","LAW","WORK_OF_ART"}
OUT_CSV = Path(f"ner_presidential_actions_{date.today().isoformat()}.csv")

def canonicalize(text: str, label: str) -> str:
    t = str(text).strip()
    t = re.sub(r'^[\"' + "'" + r'“”‘’\[\(\{]+', '', t)
    t = re.sub(r'[\"' + "'" + r'“”‘’\]\)\}]+$', '', t)
    t = re.sub(r'\s+', ' ', t).strip()
    repl = {
        "u.s.": "United States",
        "us": "United States",
        "u.s.a.": "United States",
        "usa": "United States",
        "united states of america": "United States",
        "u.k.": "United Kingdom",
        "uk": "United Kingdom",
        "u.a.e.": "United Arab Emirates",
        "uae": "United Arab Emirates",
        "eu": "European Union"
    }
    low = t.lower()
    if low in repl:
        return repl[low]
    if label in {"ORG","FAC","LAW","WORK_OF_ART"} and low.startswith("the "):
        t = t[4:]
    if t.isupper() and 2 <= len(t) <= 6:
        return t
    small = {"of","the","and","in","for","on","at","to","by","with","de","la"}
    parts = re.split(r'(\s+)', t)
    out = []
    for w in parts:
        if w.isspace(): out.append(w); continue
        lw = w.lower()
        out.append(lw if lw in small else (w[:1].upper() + w[1:]))
    return ''.join(out)

def main():
    if not INPUT.exists():
        sys.exit(f"Couldn't find {INPUT}.\nMeaning of \"put next to\": place this script and the CSV in the SAME FOLDER (same directory).")

    df = pd.read_csv(INPUT)
    needed = {"doc_id","title","type","date","text_clean"}
    lower = {c.lower(): c for c in df.columns}
    missing = needed - set(lower)
    if missing:
        sys.exit(f"Missing required columns in CSV: {missing}. Found columns: {list(df.columns)}")
    if any(lower[x] != x for x in needed):
        df = df.rename(columns={lower[x]: x for x in needed})
    df["text_clean"] = df["text_clean"].astype(str).fillna("")

    if not is_package("en_core_web_trf"):
        sys.exit("spaCy model 'en_core_web_trf' not installed. Run: python -m spacy download en_core_web_trf")
    nlp = spacy.load("en_core_web_trf", disable=["lemmatizer"])

    records = []
    texts = df["text_clean"].tolist()
    docs = nlp.pipe(texts, batch_size=8)
    for (doc_id, title, typ, dt, text), doc in zip(df[["doc_id","title","type","date","text_clean"]].itertuples(index=False, name=None), docs):
        seen = set()
        for ent in doc.ents:
            if ent.label_ not in ALLOWED:
                continue
            etext = ent.text.strip()
            canon = canonicalize(etext, ent.label_)
            key = (canon, ent.label_)
            if key in seen:
                continue
            seen.add(key)
            records.append({
                "doc_id": doc_id,
                "title": title,
                "type": typ,
                "date": dt,
                "entity_text": etext,
                "entity_type": ent.label_,
                "canonical_entity": canon
            })

    out_df = pd.DataFrame.from_records(records, columns=["doc_id","title","type","date","entity_text","entity_type","canonical_entity"])
    out_df.to_csv(OUT_CSV, index=False)
    print(f"Wrote {OUT_CSV} with {len(out_df)} rows")

if __name__ == "__main__":
    main()
