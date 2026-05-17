# policy-doc-search-prototype

## Tagline

A local document search prototype for source-grounded policy review
and human validation — deterministic TF-IDF retrieval, citation-bound
snippets, and an explicit unsupported-answer fallback.

## Project overview

This is a portfolio-style prototype for source-grounded review of
policy and methodology notes. Given a folder of Markdown documents,
the app splits each document into heading-anchored chunks, indexes
them with TF-IDF, and serves queries against the index. Every result
is returned with its source document and section. An optional
"sourced draft answer" stitches together the leading sentence of each
top hit, each line labeled with its source — the app does not
generate prose beyond what is present in the source documents.

The prototype is intentionally scoped to the retrieval and
source-attribution layer so the deterministic, citation-bound behavior
can be reviewed and tested on its own. A generation layer (a
controlled LLM call against the retrieved snippets) is treated as a
documented future extension, not part of the current scope.

## Why this matters

Most failure modes in document-grounded review happen at the
retrieval and attribution layer, not the generation layer: the wrong
section is cited, the version is stale, a downstream summary
confidently restates a passage that doesn't actually say what it
claims to. A small, deterministic prototype that exposes exactly what
was retrieved — and only that — makes those failure modes visible and
lets a reviewer audit them on their own terms, before any generation
layer is added.

## What this project demonstrates

- Designing a source-grounded retrieval workflow whose behavior is
  fully reviewable on its own — no generation layer in the runtime.
- Splitting Markdown documents into heading-anchored chunks so every
  snippet has a citable section.
- Building a small, in-memory TF-IDF index over the chunks with a
  configurable relevance threshold.
- Returning an explicit "no sufficiently supported answer" message
  when no chunk crosses the threshold, instead of fabricating an
  answer.
- Surfacing a standing reviewer checklist next to every result so
  human review is the default, not an afterthought.

## Repository structure

```
policy-doc-search-prototype/
├── README.md
├── .gitignore
├── requirements.txt
├── app.py                          # Streamlit entry point
├── documents/                      # Sample fictional documents
│   ├── sample_policy_doc_1.md      # Data quality reporting / escalation
│   ├── sample_policy_doc_2.md      # Model review and approval process
│   └── sample_methodology_note.md  # Model documentation expectations
├── src/
│   ├── __init__.py
│   ├── load_documents.py           # Markdown → heading-anchored chunks
│   ├── search_utils.py             # TF-IDF index + cosine search
│   ├── citation_utils.py           # Source / snippet rendering
│   └── review_utils.py             # Draft answer + reviewer checklist
└── outputs/                        # Local downloads / saved results
```

## Workflow

1. **Load.** Every `*.md` file under `documents/` is read and split
   into chunks by Markdown heading (`#`, `##`, `###`, `####`). Each
   chunk carries a back-reference to its source document and the
   nearest heading.
2. **Index.** A TF-IDF vectorizer is fit over the chunk corpus
   (English stop words, 1–2 grams, `min_df = 1`).
3. **Search.** The user enters a query. The query is vectorized and
   scored against every chunk by cosine similarity. Hits below a
   small score threshold are discarded.
4. **Render.** Each surviving hit is rendered with its source
   citation, a bounded-length snippet, and its similarity score.
5. **Optional draft.** If "Assemble a sourced draft answer" is
   checked, the app stitches together the leading sentence of each
   top hit, each line prefixed with its source. The draft is
   explicitly labeled as draft and as sourced from the retrieved
   snippets only.
6. **Reviewer checklist.** The standing reviewer checklist is shown
   below every result so a human reviewer can audit before sharing
   anything downstream.

## Data / inputs

Inputs are **synthetic and fictional**. The three sample documents
under `documents/` are fictional policy and methodology notes shaped
like the kind of internal documentation a research-support workflow
might consult. Document IDs (e.g. `POL-DQ-001`), version numbers,
review dates, and owners are illustrative. No real organization's
policy, methodology, or proprietary content is involved.

The corpus is intentionally small (three documents, ~28 chunks) so
the prototype is easy to inspect and reason about. Add your own
Markdown files to `documents/` to extend it.

## Methods

The prototype is deterministic. **No LLM API call** happens anywhere.
No API key is required. The dependencies are limited to `streamlit`
and `scikit-learn`.

- **Chunking.** Heading-anchored split of each Markdown file. The
  chunk size is whatever fits between two headings; on these sample
  documents that is between roughly 60 and 320 characters per chunk.
- **Indexing.** `sklearn.feature_extraction.text.TfidfVectorizer`
  with English stop words, 1–2 grams, and `min_df = 1`. The matrix
  is held in memory.
- **Scoring.** Cosine similarity (`sklearn.metrics.pairwise.cosine_similarity`)
  between the query vector and the chunk matrix.
- **Thresholding.** Hits below a small minimum similarity score
  (default 0.10) are discarded, so off-topic queries return zero
  hits rather than weakly-related ones.
- **Draft answer.** The optional draft answer concatenates the
  leading sentence of each top hit, each line labeled with the
  source. No paraphrasing, no new prose.

AI coding tools may support scaffolding, documentation review, and
consistency checks during development, but the retrieval logic,
thresholding, citation rendering, and the unsupported-answer policy
are analyst-owned and independently verified. The runtime app does
**not** call any external AI service.

## Outputs

- An interactive Streamlit UI with the corpus summary, search input,
  and reviewer checklist.
- Top-K matching snippets, each rendered with its source citation
  and similarity score.
- An optional sourced draft answer assembled from the leading
  sentences of the top hits.
- An explicit "No sufficiently supported answer found in the
  available documents." message when no chunk crosses the relevance
  threshold.

## How to run

```bash
pip install -r requirements.txt
streamlit run app.py
```

The Streamlit app opens at `http://localhost:8501` by default.

Try these queries against the bundled sample documents:

- *how are data-quality issues escalated?*
- *what does a methodology note need to contain?*
- *who signs off on model approvals?*
- *how do I bake a cake?* — should return the "no sufficiently
  supported answer" message.

## Reviewability and documentation

- Every snippet is rendered with its source document and section, so
  a reviewer can trace any claim back to the originating chunk.
- The draft answer adds no prose; every line is sourced.
- The reviewer checklist is rendered after every result and is also
  available in `src/review_utils.py` as a Python constant for reuse
  in other artifacts.
- The retrieval threshold is configurable in `src/search_utils.py`
  (`MIN_SCORE_THRESHOLD`) — a reviewer can tighten it if the corpus
  grows.
- The codebase is small (~250 lines across four modules + the
  Streamlit app) and easy to review in a single sitting.

## Responsible use

- The app does not generate answers beyond the retrieved snippets.
  Where a draft answer appears, it is explicitly labeled as a draft
  and as sourced.
- The "No sufficiently supported answer" message is a feature, not
  a bug. The app refuses to fabricate when retrieval does not
  produce a confident hit.
- The reviewer checklist on every page exists so human review is
  the default before any answer is shared downstream.
- No external AI or LLM service is contacted. No API key is
  required.
- The bundled documents are fictional. Replace them with your own
  Markdown files to extend the corpus; do not paste confidential or
  non-public material into a copy of this app that runs on a shared
  or hosted environment without confirming the hosting context is
  appropriate for the data classification.

## Portfolio Context

This project translates recurring patterns from analytical work —
source-grounded document review, citation discipline, retrieval
workflows, and human-in-the-loop validation — into a public, synthetic
portfolio prototype. The sample documents are fictional and the
retrieval is local and deterministic; nothing in this repository
replicates any internal or proprietary system. The goal is to
demonstrate reproducible, reviewable workflow design at the retrieval-
and-attribution layer, so a generation layer can later be added under
controlled, documented conditions.

## What this project does not do

- It does **not** call any external LLM, AI, or generation service.
- It does **not** require any API key or cloud credential.
- It does **not** generate prose beyond what is present in the
  retrieved snippets.
- It does **not** assert correctness of the source documents.
- It does **not** version, fetch, or refresh documents — the corpus
  is whatever sits in `documents/` at app startup.
- It does **not** ship a production RAG pipeline. It is a
  retrieval-and-attribution prototype intended to be reviewable
  before an LLM layer is added.
- It does **not** replace analyst, reviewer, or domain-expert
  judgment.

## Limitations

- **TF-IDF is lexical.** Synonym matches and semantic equivalents
  are not found unless they share vocabulary. A real production
  retriever would mix TF-IDF (BM25) with a learned embedding model.
- **Heading-anchored chunking is coarse.** A long section becomes a
  single chunk; a very short one might score weakly even when
  relevant.
- **The relevance threshold is hand-tuned** on the sample corpus.
  Different corpora will need different thresholds; the constant
  lives in `src/search_utils.py`.
- **No conversation memory.** Each query is independent. There is no
  follow-up handling.
- **No document refresh.** Documents are read once at startup and
  cached. Editing a file under `documents/` requires restarting the
  app.
- **No deduplication.** Two near-identical sections in different
  documents both surface as separate hits.

## Future improvements

- Add a BM25 ranker (`rank_bm25`) alongside TF-IDF and compare
  results.
- Add an embeddings-based retriever (e.g. `sentence-transformers`)
  as an offline alternative to a hosted model.
- Add a "compare to prior version" mode so a reviewer can see how
  retrieved snippets changed between two corpus versions.
- Add a small `pytest` suite that asserts the search returns the
  expected source for a curated set of canonical queries.
- Document a path for adding a controlled LLM layer (provider-specific
  API, prompt template, draft-only output policy, audit log) without
  changing the retrieval-and-attribution core.

## Skills demonstrated

- Designing a source-grounded retrieval workflow with retrieval and
  attribution as the load-bearing layer.
- Implementing a small, deterministic search prototype in Python
  with `scikit-learn` and `streamlit`.
- Translating recurring reviewer concerns (source attribution,
  draft labeling, "I don't know" handling) into product behavior.
- Scoping the prototype to retrieval and attribution and documenting
  how a generation layer could be added later under controlled
  conditions.
- Documentation discipline — "what this project does not do" and
  limitations are front-of-README, not buried.

## Project summary

A local TF-IDF search prototype over Markdown policy and methodology
notes that returns source-grounded snippets, refuses to answer when
retrieval is weak, and surfaces a reviewer checklist next to every
result — no LLM API.

### Workflow summary

A prototype for the *retrieval and attribution* layer of a
source-grounded review workflow. Three sample Markdown documents are
split into heading-anchored chunks, indexed with TF-IDF, and served
behind a Streamlit UI. Every hit shows its source document and
section. An optional draft answer stitches the leading sentence of
each top hit together, each line sourced — no paraphrasing.
Off-topic queries return "no sufficiently supported answer" rather
than fabricating. The intent is to make the retrieval-and-attribution
layer reviewable on its own, before any generation layer is added.

### Design rationale

- **It is the right layer to scope.** Most failure modes in
  document-grounded review happen at retrieval and attribution, not
  at generation. A deterministic prototype at this layer can be
  reviewed and tested independently, which makes any future
  generation layer easier to evaluate.
- **It refuses to fabricate.** Off-topic queries return an explicit
  "no sufficiently supported answer" message. The draft answer adds
  no prose beyond what is present in the snippets; every line carries
  its source.
- **The reviewer is the default, not the exception.** The standing
  reviewer checklist is rendered after every result. The
  responsible-use language in the README is concrete — it names the
  LLM API not used, the API key not required, the data classification
  considerations for hosted deployments.

### Honest limitations

- TF-IDF is lexical only. Synonyms and semantic equivalents are
  missed unless they share vocabulary. A real retriever would mix
  BM25 with a learned embedding model.
- The relevance threshold is hand-tuned on the sample corpus and
  would need recalibration on a different document set.
- The corpus is loaded once at startup and cached; editing a document
  does not refresh the index without an app restart.

## GitHub description

> Local document search prototype for source-grounded policy
> review and human validation.

(95 chars.)
