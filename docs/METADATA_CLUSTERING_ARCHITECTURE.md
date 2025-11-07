# Metadata Clustering Architecture

## Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     INPUT: Financial Documents                  │
│                                                                 │
│  • "JPMorgan Chase & Co. 2023 Annual Report - Finance Sector"  │
│  • "Apple Inc. 2023 Annual Report - Technology Sector"         │
│  • "Goldman Sachs Group Inc. 2023 Report - Finance"            │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│              STEP 1: Chunking & Metadata Extraction             │
│                     (FinancialChunker)                          │
│                                                                 │
│  For each document:                                             │
│  1. Split into chunks (1000 chars, 200 overlap)                │
│  2. Extract metadata using regex:                              │
│     - Year: \b(19\d{2}|20\d{2})\b                              │
│     - Company: patterns for Inc/Corp/Ltd/LLC                   │
│     - Sector: keyword matching                                 │
│  3. Attach metadata to each chunk                              │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    STEP 2: Create Embeddings                    │
│                    (OpenAIEmbeddingModel)                       │
│                                                                 │
│  • Model: text-embedding-3-small                               │
│  • Dimension: 1536                                             │
│  • Batch size: 100 chunks at a time                            │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│         STEP 3: Metadata Grouping (Two-Stage Clustering)        │
│                     (RAPTORClustering)                          │
│                                                                 │
│  Stage 1: Group by Metadata Tuple                              │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ (finance, JPMorgan, 2023)    → [chunk1, chunk2, ...]  │    │
│  │ (technology, Apple, 2023)    → [chunk3, chunk4, ...]  │    │
│  │ (finance, Goldman Sachs, 2023) → [chunk5, chunk6, ...]│    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                 │
│  Stage 2: Sub-Clustering Within Each Group                     │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ For each metadata group with > 3 nodes:                │    │
│  │   1. Apply UMAP (reduce to 10 dimensions)              │    │
│  │   2. Apply GMM (find optimal clusters)                 │    │
│  │   3. Create sub-clusters based on embeddings           │    │
│  │                                                         │    │
│  │ For groups with ≤ 3 nodes:                             │    │
│  │   - Keep as single cluster                             │    │
│  └────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                STEP 4: Build RAPTOR Tree (Level 0)              │
│                      (RAPTORTree)                               │
│                                                                 │
│  Level 0 (Leaf nodes):                                         │
│  ┌──────────────────────────────────────────────────────┐      │
│  │ JPMorgan/Finance/2023 Group:                         │      │
│  │   ├─ Cluster 1: [Revenue chunks]                     │      │
│  │   ├─ Cluster 2: [Banking chunks]                     │      │
│  │   └─ Cluster 3: [Risk management chunks]             │      │
│  │                                                       │      │
│  │ Apple/Technology/2023 Group:                         │      │
│  │   ├─ Cluster 1: [iPhone chunks]                      │      │
│  │   └─ Cluster 2: [Services chunks]                    │      │
│  └──────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│            STEP 5: Summarize & Build Higher Levels              │
│                   (GPT-3.5-turbo for summaries)                 │
│                                                                 │
│  For each cluster:                                              │
│  1. Concatenate all chunk texts                                │
│  2. Generate summary using LLM                                 │
│  3. Create parent node with summary                            │
│  4. Repeat clustering & summarization for next level           │
│                                                                 │
│  Level 1 (Summaries of Level 0):                               │
│  ┌──────────────────────────────────────────────────────┐      │
│  │ • JPMorgan 2023 Financial Performance Summary        │      │
│  │ • Apple 2023 Product & Services Summary              │      │
│  │ • Goldman Sachs 2023 Investment Banking Summary      │      │
│  └──────────────────────────────────────────────────────┘      │
│                                                                 │
│  Level 2 (Higher level summaries):                             │
│  ┌──────────────────────────────────────────────────────┐      │
│  │ • Finance Sector 2023 Overview                       │      │
│  │ • Technology Sector 2023 Overview                    │      │
│  └──────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   STEP 6: Query & Retrieval                     │
│                     (RAPTORRetriever)                           │
│                                                                 │
│  Query: "What were JPMorgan's 2023 earnings?"                  │
│                                                                 │
│  1. Create query embedding                                     │
│  2. Tree Traversal Method:                                     │
│     ┌────────────────────────────────────────────────────┐     │
│     │ Start at root → Find most relevant nodes          │     │
│     │ Traverse down → Get more specific chunks          │     │
│     │ Returns: Hierarchical context                     │     │
│     └────────────────────────────────────────────────────┘     │
│                                                                 │
│  3. Collapsed Tree Method (alternative):                       │
│     ┌────────────────────────────────────────────────────┐     │
│     │ Search all layers simultaneously                  │     │
│     │ Return top-k most similar nodes                   │     │
│     └────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                  STEP 7: Generate Answer (QA)                   │
│                      (GPT-4-turbo-preview)                      │
│                                                                 │
│  Input:                                                         │
│  • Retrieved context from tree                                 │
│  • User question                                               │
│                                                                 │
│  Output:                                                        │
│  • Generated answer with citations                             │
│  • Source attribution                                          │
└─────────────────────────────────────────────────────────────────┘
```

## Comparison: Standard vs Metadata Clustering

### Standard Clustering (Without Metadata)

```
All Chunks → UMAP → GMM → Clusters
    ↓
Mixed clusters (JPM + Apple + Goldman all together)
```

### Metadata Clustering (With Metadata)

```
All Chunks → Group by (sector, company, year) → Sub-cluster each group
    ↓
Organized clusters (JPM chunks together, Apple chunks together)
```

## Key Benefits Visualization

```
┌─────────────────────────────────────────────────────────────────┐
│                    WITHOUT Metadata Clustering                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Cluster 1: [JPM Revenue, Apple iPhone, Goldman M&A]          │
│  Cluster 2: [JPM Banking, Tesla Production, Apple Services]    │
│  Cluster 3: [Goldman Trading, JPM Risk, Apple R&D]             │
│                                                                 │
│  ❌ Mixed companies in same cluster                            │
│  ❌ Harder to retrieve company-specific info                   │
│  ❌ Less organized structure                                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     WITH Metadata Clustering                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  JPMorgan/Finance/2023:                                        │
│    ├─ Cluster 1: [Revenue, Income, Performance]               │
│    └─ Cluster 2: [Banking, Trading, Risk]                     │
│                                                                 │
│  Apple/Technology/2023:                                        │
│    ├─ Cluster 1: [iPhone, Products]                           │
│    └─ Cluster 2: [Services, Subscriptions]                    │
│                                                                 │
│  ✅ Company-specific clusters                                  │
│  ✅ Better retrieval for targeted queries                      │
│  ✅ Organized by business context                              │
└─────────────────────────────────────────────────────────────────┘
```

## Code Flow

```python
# 1. Initialize
finrag = FinRAG()  # Metadata clustering enabled by default

# 2. Add documents (automatic metadata extraction)
finrag.add_documents([
    "JPMorgan Chase & Co. 2023 Annual Report - Finance Sector..."
])

# Internal flow:
#   → FinancialChunker.chunk_text_with_metadata()
#   → extract_metadata() for each document
#   → Attach metadata to chunks
#   → Create embeddings
#   → RAPTORClustering.perform_metadata_clustering()
#   → Build RAPTOR tree with metadata-aware clusters

# 3. Query
result = finrag.query("What were JPMorgan's 2023 earnings?")

# Internal flow:
#   → Create query embedding
#   → RAPTORRetriever.retrieve()
#   → Tree traversal (benefits from metadata organization)
#   → QA model generates answer
```

## File Interaction Map

```
┌──────────────────────────────────────────────────────────────┐
│                         finrag.py                            │
│                    (Main API Entry Point)                    │
└──────────────────────────────────────────────────────────────┘
                    ↓                ↓
        ┌───────────────┐   ┌──────────────────┐
        │   config.py   │   │   models.py      │
        │               │   │ FinancialChunker │
        │ use_metadata_ │   │ extract_metadata │
        │  clustering   │   │ chunk_text_with_ │
        │ metadata_keys │   │   metadata       │
        └───────────────┘   └──────────────────┘
                                    ↓
                          ┌──────────────────┐
                          │   tree.py        │
                          │   RAPTORTree     │
                          │  build_tree()    │
                          └──────────────────┘
                                    ↓
                          ┌──────────────────┐
                          │ clustering.py    │
                          │ RAPTORClustering │
                          │ • extract_       │
                          │   metadata_      │
                          │   groups()       │
                          │ • perform_       │
                          │   metadata_      │
                          │   clustering()   │
                          └──────────────────┘
```

## Data Structures

### ClusterNode

```python
ClusterNode(
    text="JPMorgan revenue reached $158.1 billion...",
    index=0,
    embedding=[0.12, -0.34, ...],  # 1536 dimensions
    children=[1, 2, 3],
    metadata={
        "sector": "finance",
        "company": "JPMorgan Chase & Co.",
        "year": "2023"
    }
)
```

### Metadata Groups

```python
{
    ("finance", "JPMorgan Chase & Co.", "2023"): [node1, node2, node3],
    ("technology", "Apple Inc.", "2023"): [node4, node5],
    ("finance", "Goldman Sachs", "2023"): [node6, node7, node8]
}
```

## Performance Characteristics

```
┌─────────────────────────────────────────────────────────┐
│                  Time Complexity                        │
├─────────────────────────────────────────────────────────┤
│ Metadata extraction:     O(n) - regex on each doc      │
│ Metadata grouping:       O(n) - single pass            │
│ UMAP per group:          O(m log m) - m = group size   │
│ GMM per group:           O(m × k × i) - k clusters     │
│                                                         │
│ Overall: Similar to standard clustering, often faster  │
│ (smaller groups cluster faster than one large group)   │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                  Space Complexity                       │
├─────────────────────────────────────────────────────────┤
│ Metadata per node:       ~100 bytes (3 strings)        │
│ For 1000 nodes:          ~100 KB (negligible)          │
│                                                         │
│ Overall: Minimal overhead                              │
└─────────────────────────────────────────────────────────┘
```

## Configuration Options

```python
┌──────────────────────────────────────────────────────────┐
│                  FinRAGConfig Options                    │
├──────────────────────────────────────────────────────────┤
│                                                          │
│ # Metadata clustering                                   │
│ use_metadata_clustering = True                          │
│ metadata_keys = ["sector", "company", "year"]           │
│                                                          │
│ # Clustering parameters                                 │
│ reduction_dimension = 10      # UMAP dimensions         │
│ max_clusters = 5              # Max GMM clusters        │
│ gaussian_random_state = 42    # Reproducibility         │
│                                                          │
│ # Retrieval                                             │
│ top_k = 10                    # Nodes to retrieve       │
│                                                          │
│ # Models                                                │
│ embedding_model = "text-embedding-3-small"              │
│ summarization_model = "gpt-3.5-turbo"                   │
│ qa_model = "gpt-4-turbo-preview"                        │
└──────────────────────────────────────────────────────────┘
```
