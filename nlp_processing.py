from transformers import pipeline
import json
import os

sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
toxicity_classifier = pipeline("text-classification", model="unitary/toxic-bert")
ner_tagger = pipeline("ner", grouped_entities=True)

input_path = "data/latest_data.json"
output_path = "data/processed_data.json"

if not os.path.exists(input_path):
    raise FileNotFoundError("Run data_ingestion.py first.")

with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

for entry in data:
    text = entry["content"]
    try:
        entry["sentiment"] = sentiment_analyzer(text[:512])[0]
    except:
        entry["sentiment"] = {"label": "ERROR", "score": 0}
    try:
        entry["toxicity"] = toxicity_classifier(text[:512])[0]
    except:
        entry["toxicity"] = {"label": "ERROR", "score": 0}
    try:
        entry["entities"] = [e["word"] for e in ner_tagger(text[:512])]
    except:
        entry["entities"] = []

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"Processed {len(data)} entries.")