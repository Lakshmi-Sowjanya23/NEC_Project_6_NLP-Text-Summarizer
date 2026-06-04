from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re

# Load model only once
summarizer_model = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6"
)


def extract_keywords(text, top_n=5):

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=100
    )

    tfidf_matrix = vectorizer.fit_transform([text])

    scores = tfidf_matrix.toarray()[0]

    words = vectorizer.get_feature_names_out()

    ranked = np.argsort(scores)[::-1]

    keywords = [words[i] for i in ranked[:top_n]]

    return keywords


def get_statistics(original_text, summary_text):

    original_words = len(original_text.split())

    summary_words = len(summary_text.split())

    compression_ratio = round(
        (summary_words / original_words) * 100,
        2
    )

    sentence_count = len(
        re.findall(r'[.!?]+', original_text)
    )

    return {
        "original_words": original_words,
        "summary_words": summary_words,
        "compression_ratio": compression_ratio,
        "sentence_count": sentence_count
    }


def summarize_text(text):

    result = summarizer_model(
        text,
        max_length=150,
        min_length=40,
        do_sample=False
    )

    summary = result[0]["summary_text"]

    keywords = extract_keywords(text)

    stats = get_statistics(text, summary)

    return {
        "summary": summary,
        "keywords": keywords,
        "stats": stats
    }