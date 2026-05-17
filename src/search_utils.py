"""TF-IDF search over loaded document chunks.

The search is deterministic. There is no LLM call anywhere. Given a
query string, the function returns the top-K chunks ranked by cosine
similarity against a TF-IDF vector. If no chunk scores above a small
threshold, the function returns an empty list — which the UI uses to
trigger the explicit "no sufficiently supported answer" message.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .load_documents import Chunk


# Below this score, treat as "no relevant result". Calibrated on the
# sample documents — short, focused queries that match a section
# heading-ish topic score well above 0.10; off-topic queries score
# well below it.
MIN_SCORE_THRESHOLD = 0.10


@dataclass
class SearchHit:
    """One result of the search: a chunk plus its similarity score."""
    chunk: Chunk
    score: float


class DocumentSearcher:
    """Wraps a TF-IDF vectorizer fit over a chunk corpus."""

    def __init__(self, chunks: list[Chunk]) -> None:
        self.chunks = chunks
        self._vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2),
            min_df=1,
        )
        corpus = [c.text for c in chunks]
        self._matrix = self._vectorizer.fit_transform(corpus) if corpus else None

    def search(self, query: str, top_k: int = 5) -> list[SearchHit]:
        """Return the top-K hits for `query` ranked by cosine similarity."""
        if self._matrix is None or not query.strip():
            return []
        q_vec = self._vectorizer.transform([query])
        sims = cosine_similarity(q_vec, self._matrix).ravel()
        order = sims.argsort()[::-1]

        hits: list[SearchHit] = []
        for idx in order[:top_k]:
            score = float(sims[idx])
            if score < MIN_SCORE_THRESHOLD:
                break
            hits.append(SearchHit(chunk=self.chunks[idx], score=score))
        return hits

    @property
    def vocabulary_size(self) -> int:
        return len(self._vectorizer.vocabulary_) if self._matrix is not None else 0


def found_anything(hits: Iterable[SearchHit]) -> bool:
    """Convenience: True when the search produced at least one hit."""
    hits = list(hits)
    return len(hits) > 0
