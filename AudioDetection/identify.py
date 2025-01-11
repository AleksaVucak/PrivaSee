import os
import spacy
from spacy.matcher import Matcher
import scispacy
from scispacy.linking import EntityLinker
import string
from typing import List, Tuple

def load_models():
    nlp = spacy.load("en_core_web_md")
    biomed_nlp = spacy.load("en_core_sci_md")
    biomed_nlp.add_pipe("scispacy_linker", config={
        "resolve_abbreviations": True,
        "linker_name": "umls"
    })
    return nlp, biomed_nlp

def setup_matcher(nlp) -> Matcher:
    matcher = Matcher(nlp.vocab)
    age_patterns = [
        [{"LIKE_NUM": True}, {"LOWER": {"IN": ["years", "year", "yrs", "yr"]}}, {"LOWER": "old"}],
        [{"LIKE_NUM": True}, {"TEXT": "-"}, {"LOWER": {"IN": ["year", "yr"]}}, {"TEXT": "-"}, {"LOWER": "old"}],
        [{"LIKE_NUM": True, "TEXT": {"REGEX": "^[0-9]{1,3}$"}}],
        [{"LOWER": "age"}, {"LIKE_NUM": True}],
        [{"LIKE_NUM": True}, {"LOWER": {"IN": ["y.o.", "yo", "y/o"]}}]
    ]
    matcher.add("AGE", age_patterns)
    return matcher

def get_entity_spans(doc) -> List[Tuple[int, int, str]]:
    spans = []
    for ent in doc.ents:
        spans.append((ent.start_char, ent.end_char, ent.text))
    return spans

def is_overlapping(entity: Tuple[int, int, str], scispacy_spans: List[Tuple[int, int, str]], label: str) -> bool:
    if label in {"LOC", "GPE", "ORG"}:
        return False
    start, end, _ = entity
    for sci_start, sci_end, _ in scispacy_spans:
        if not (end <= sci_start or start >= sci_end):
            return True
    return False

def find_entity_timestamps(entity_text: str, words: List[str], timestamps: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    entity_words = entity_text.split()
    occurrences = []
    for i in range(len(words) - len(entity_words) + 1):
        if words[i:i + len(entity_words)] == entity_words:
            start_idx = i
            end_idx = i + len(entity_words) - 1
            occurrences.append((timestamps[start_idx][0], timestamps[end_idx][1]))
    return occurrences

def find_phi(file_name: str) -> None:
    nlp, biomed_nlp = load_models()
    matcher = setup_matcher(nlp)
    PHI_LABELS = {"PERSON", "DATE", "GPE", "ORG", "NORP", "LOC", "AGE"}
    NON_ENTITIES = {"alright", "which", "okay"}
    base_name = os.path.splitext(os.path.basename(file_name))[0]
    spacy_phi_entities = []
    with open(f"transcripts/{base_name}_transcript.txt", 'r') as file:
        words = []
        timestamps = []
        for line in file:
            if ": " in line:
                word, times = line.strip().split(": ")
                word = word.strip(string.punctuation + " ")
                if not word:
                    continue
                try:
                    start_time, end_time = map(float, times.strip().split(" - "))
                    words.append(word)
                    timestamps.append((start_time, end_time))
                except ValueError:
                    print(f"Warning: Invalid timestamp format in line: {line}")
                    continue
    text = " ".join(words)
    doc = nlp(text)
    biomed_doc = biomed_nlp(text)
    scispacy_spans = get_entity_spans(biomed_doc)
    for ent in doc.ents:
        if ent.text.lower() in NON_ENTITIES:
            continue
        if ent.label_ in {"ORG", "PERSON"} and not ent.text[0].isupper():
            continue
        if ent.label_ in PHI_LABELS and not is_overlapping((ent.start_char, ent.end_char, ent.text), scispacy_spans, ent.label_):
            for start_time, end_time in find_entity_timestamps(ent.text, words, timestamps):
                spacy_phi_entities.append((ent.text, ent.label_, start_time, end_time))
    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        if not is_overlapping((span.start_char, span.end_char, span.text), scispacy_spans, "AGE"):
            for start_time, end_time in find_entity_timestamps(span.text, words, timestamps):
                spacy_phi_entities.append((span.text, "AGE", start_time, end_time))
    spacy_phi_entities.sort(key=lambda x: (x[2], x[3]))
    output_file_path = os.path.join("phi", f"{base_name}_phi.txt")
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    with open(output_file_path, 'w') as output_file:
        for entity_text, label, start_time, end_time in spacy_phi_entities:
            output_file.write(f"Entity: {entity_text}, Label: {label}, Start: {start_time:.2f}s, End: {end_time:.2f}s\n")
    print(f"SpaCy PHI information saved to {output_file_path}")
    print(f"Found {len(spacy_phi_entities)} PHI entities")
