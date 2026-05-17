"""Citation rendering for the UI.

Every snippet returned by the search must show its source so a reviewer
can trace the claim back to the document. These helpers format a
citation block consistently and produce a snippet preview of bounded
length.
"""

from __future__ import annotations

from typing import Iterable

from .search_utils import SearchHit


SNIPPET_MAX_CHARS = 320


def shorten(text: str, max_chars: int = SNIPPET_MAX_CHARS) -> str:
    """Return the first `max_chars` characters with an ellipsis if truncated."""
    text = text.strip()
    if len(text) <= max_chars:
        return text
    # Try to break at a sentence boundary near the limit
    cut = text.rfind(". ", 0, max_chars)
    if cut > max_chars * 0.5:
        return text[: cut + 1] + " …"
    return text[: max_chars - 1].rstrip() + "…"


def render_citation(hit: SearchHit) -> str:
    """Human-readable citation: source filename + section + score."""
    c = hit.chunk
    return f"**{c.doc_id}.md** — §{c.section}  ·  similarity {hit.score:.3f}"


def render_snippet(hit: SearchHit) -> str:
    """The snippet text shown under a citation."""
    return shorten(hit.chunk.text)


def render_full_block(hit: SearchHit) -> str:
    """Combined citation + snippet block, Markdown-ready."""
    return f"{render_citation(hit)}\n\n> {render_snippet(hit)}"


def render_results(hits: Iterable[SearchHit]) -> str:
    """Render a list of hits as a Markdown block."""
    hits = list(hits)
    if not hits:
        return ""
    return "\n\n---\n\n".join(render_full_block(h) for h in hits)
