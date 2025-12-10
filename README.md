# Presidential-Actions-Quantified (WIP)
Explorations & visualisations of Presidential Actions

## Named Entity Recognition (NER)

### Interactive Person Topic River
Try it out [here!](https://storage.googleapis.com/web-visualisations/Presidential-Actions-Quantified/NER/person_topic_river_online.html)

### Notes & Observations
- I need to refine my data cleansing methodology. In the meantime, playing with new controls starts to tell stories. I added controls for
   - manually adding stop words
   - manually selecting top-k entities
   - toggle for normalizing area chart to 100%
- POC visualisation of **entity_type: PEOPLE**
  - Displays appearance of entities in monthly buckets
  - Defaults to **top-k = 25** (total PEOPLE entities: **n=1008**)
- Interesting observations
   - Bursts of names at the start, as POTUS delegated roles
   - Spike in mentions of a certain MAGA-aligned polemicist assassinated in September
   - Excluding POTUS & key staff/spouses, **Joe Biden** is virtually the only entity consistently mentioned in every single time bucket.
