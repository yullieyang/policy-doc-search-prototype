"""Streamlit UI for the policy-document search prototype.

Run locally:
    streamlit run app.py

The app loads every `*.md` file under `documents/`, splits each into
heading-anchored chunks, builds a TF-IDF index in memory, and serves
queries against it. There is no LLM call. There is no API key.

The UI shows: the top matching snippets with their source, an optional
sourced "draft answer" stitched from leading sentences of those
snippets, and the standing reviewer checklist.
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from src.citation_utils import render_full_block
from src.load_documents import chunks_summary, load_documents
from src.review_utils import (
    NO_SUFFICIENT_ANSWER, build_draft_answer, render_checklist,
)
from src.search_utils import DocumentSearcher, found_anything


PROJECT_ROOT = Path(__file__).resolve().parent
DOCUMENTS_DIR = PROJECT_ROOT / "documents"


# --- Page setup --------------------------------------------------------------

st.set_page_config(
    page_title="Policy Doc Search Prototype",
    page_icon="🔎",
    layout="centered",
)

st.title("Policy Doc Search Prototype")
st.caption(
    "Portfolio-style prototype for source-grounded document search. "
    "Local TF-IDF over Markdown files. No LLM API. No API key. "
    "Outputs are drafts for human review."
)


# --- Index ------------------------------------------------------------------

@st.cache_resource(show_spinner=False)
def _build_index(docs_dir: Path):
    chunks = load_documents(docs_dir)
    searcher = DocumentSearcher(chunks)
    return chunks, searcher


if not DOCUMENTS_DIR.exists() or not any(DOCUMENTS_DIR.glob("*.md")):
    st.error(
        f"No documents found under `{DOCUMENTS_DIR.relative_to(PROJECT_ROOT)}`. "
        "Add Markdown files to that directory and reload."
    )
    st.stop()

chunks, searcher = _build_index(DOCUMENTS_DIR)


# --- Sidebar ----------------------------------------------------------------

with st.sidebar:
    st.header("Corpus")
    summary = chunks_summary(chunks)
    st.write(f"**{len(chunks)} chunks** across **{len(summary)} documents**:")
    for doc_id, count in sorted(summary.items()):
        st.write(f"- `{doc_id}.md` ({count} sections)")

    st.divider()
    st.header("Search settings")
    top_k = st.slider("Top-K results", min_value=1, max_value=10, value=5)
    show_draft = st.checkbox(
        "Assemble a sourced draft answer from retrieved snippets", value=True
    )

    st.divider()
    st.caption(
        "All snippets shown in this app come directly from the Markdown "
        "files under `documents/`. The app does not call any external "
        "model or service."
    )


# --- Query ------------------------------------------------------------------

st.subheader("Query")
query = st.text_input(
    "Ask a question about the documents:",
    placeholder="e.g. how are data-quality issues escalated?",
)

if not query.strip():
    st.info(
        "Enter a query above to search the corpus. Examples:\n\n"
        "- *how are data-quality issues escalated?*\n"
        "- *what does a model documentation note need to contain?*\n"
        "- *who signs off on model approvals?*"
    )
    st.stop()


# --- Results ----------------------------------------------------------------

hits = searcher.search(query, top_k=top_k)

if not found_anything(hits):
    st.warning(NO_SUFFICIENT_ANSWER)
    st.markdown(
        "The query did not match any document section above the configured "
        "relevance threshold. Try rephrasing, or check the corpus list in "
        "the sidebar to confirm the topic is covered."
    )
    st.stop()


st.subheader(f"Top {len(hits)} matching snippet(s)")
for i, hit in enumerate(hits, start=1):
    st.markdown(f"#### Result {i}")
    st.markdown(render_full_block(hit))
    st.markdown("")  # spacing


if show_draft:
    st.divider()
    st.subheader("Sourced draft answer")
    st.markdown(build_draft_answer(hits))


st.divider()
st.markdown(render_checklist())

st.caption(
    "This prototype performs deterministic retrieval only. It does not "
    "generate prose beyond what is present in the source documents. "
    "Any answer used downstream must be reviewed by a named human."
)
