"""Reviewer-checklist and draft-answer scaffolding.

The prototype intentionally does not generate prose answers. Where a
"draft answer" appears in the UI, it is constructed by concatenating
the leading sentences of the top hits, each labeled with its source.
That keeps every line in the answer traceable to a snippet a human
reviewer can audit. There is no LLM call anywhere.
"""

from __future__ import annotations

from typing import Iterable

from .search_utils import SearchHit


NO_SUFFICIENT_ANSWER = (
    "No sufficiently supported answer found in the available documents."
)


def first_sentence(text: str) -> str:
    """Return the first sentence-ish slice of a chunk for the draft answer."""
    text = text.strip()
    for sep in (". ", "? ", "! "):
        idx = text.find(sep)
        if 0 < idx < 220:
            return text[: idx + 1].strip()
    return text[:220].strip() + ("…" if len(text) > 220 else "")


def build_draft_answer(hits: Iterable[SearchHit]) -> str:
    """Stitch the leading sentences of the top hits into a labeled draft.

    Each line is prefixed with the source so the reviewer can see where
    the sentence came from. The function adds no original prose.
    """
    hits = list(hits)
    if not hits:
        return NO_SUFFICIENT_ANSWER
    lines = []
    for h in hits:
        sent = first_sentence(h.chunk.text)
        lines.append(f"- ({h.chunk.doc_id} §{h.chunk.section}) {sent}")
    return (
        "**Draft answer — assembled from retrieved snippets only:**\n\n"
        + "\n".join(lines)
        + "\n\n_Every line above is sourced. A human reviewer must "
          "verify each sentence against the linked source before using "
          "this draft in any downstream document._"
    )


REVIEW_CHECKLIST = [
    "Does each retrieved snippet support the answer it appears under?",
    "Are there sections of the documents that conflict with the retrieved snippets?",
    "Is the cited source the current version of the policy or methodology?",
    "Does the answer require additional context that the retrieved snippets do not provide?",
    "Has the answer been read and edited by a named human reviewer before sharing?",
]


def render_checklist() -> str:
    """Markdown rendering of the standing reviewer checklist."""
    items = "\n".join(f"- [ ] {item}" for item in REVIEW_CHECKLIST)
    return f"### Reviewer checklist\n\n{items}"
