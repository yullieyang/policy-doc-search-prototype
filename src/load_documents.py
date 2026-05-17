"""Load Markdown documents from `documents/` and split them into sections.

The chunking strategy is deliberately simple: split each document on
Markdown headings (`#`, `##`) so each chunk is a coherent passage with a
local title. The chunk keeps a back-reference to its source document and
its heading so any downstream consumer (the search index, the UI)
can cite where a snippet came from.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
import re


@dataclass
class Chunk:
    """A chunk of a source document: heading-anchored passage of text."""
    doc_id: str         # filename without extension
    doc_title: str      # first level-1 heading of the source document
    section: str        # nearest heading text for this chunk
    section_level: int  # 1 for `#`, 2 for `##`, 3 for `###`, etc.
    text: str           # the chunk body (heading line excluded)

    @property
    def display_source(self) -> str:
        """Citation string shown next to a result, e.g. POL-DQ-001 §3."""
        return f"{self.doc_id} — {self.section}"


HEADING_RE = re.compile(r"^(#{1,4})\s+(.+?)\s*$")


def _split_into_sections(text: str) -> list[tuple[int, str, str]]:
    """Walk the document, emitting (heading_level, heading_text, body) per section.

    The first chunk before any heading is captured under heading "Preamble".
    """
    sections: list[tuple[int, str, str]] = []
    current_level = 0
    current_heading = "Preamble"
    current_body: list[str] = []

    for line in text.splitlines():
        m = HEADING_RE.match(line)
        if m:
            # flush the previous section
            body = "\n".join(current_body).strip()
            if body:
                sections.append((current_level, current_heading, body))
            current_level = len(m.group(1))
            current_heading = m.group(2).strip()
            current_body = []
        else:
            current_body.append(line)
    # flush the last section
    body = "\n".join(current_body).strip()
    if body:
        sections.append((current_level, current_heading, body))
    return sections


def _doc_title(text: str) -> str:
    """First H1 in the document, or the empty string."""
    for line in text.splitlines():
        m = HEADING_RE.match(line)
        if m and len(m.group(1)) == 1:
            return m.group(2).strip()
    return ""


def load_documents(documents_dir: Path) -> list[Chunk]:
    """Load every `*.md` file under `documents_dir` as a list of `Chunk`s."""
    chunks: list[Chunk] = []
    for md_path in sorted(documents_dir.glob("*.md")):
        text = md_path.read_text(encoding="utf-8")
        doc_id = md_path.stem
        title = _doc_title(text) or doc_id
        for level, heading, body in _split_into_sections(text):
            chunks.append(Chunk(
                doc_id=doc_id,
                doc_title=title,
                section=heading,
                section_level=level,
                text=body,
            ))
    return chunks


def chunks_summary(chunks: Iterable[Chunk]) -> dict[str, int]:
    """Tiny diagnostic: how many chunks per document."""
    out: dict[str, int] = {}
    for c in chunks:
        out[c.doc_id] = out.get(c.doc_id, 0) + 1
    return out
