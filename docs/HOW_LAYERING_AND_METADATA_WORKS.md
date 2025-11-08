# How Layering and Metadata Work in FinRAG RAPTOR Tree

## Complete Process Overview

```
Documents → Layer 0 → Layer 1 → Layer 2 → ... → Root
           (chunks)  (summaries) (summaries)
```

---

## 📊 Layer 0 Creation (Leaf Nodes)

### Location: `tree.py` → `build_tree()` method (lines 66-76)

**Process**:
1. Each document chunk becomes a **leaf node**
2. Metadata is directly copied from the chunk

**Code**:
```python
for idx, (chunk, embedding) in enumerate(zip(chunks, chunk_embeddings)):
    node = ClusterNode(
        node_id=f"leaf_{idx}",
        text=chunk["text"],           # Original chunk text
        embedding=embedding,           # Chunk embedding
        children=[],                   # No children (it's a leaf)
        level=0,                       # Layer 0
        metadata=chunk                 # DIRECT COPY of chunk metadata
    )
```

**Metadata Source**: Extracted from document text using regex patterns in `FinancialChunker.extract_metadata()`
- Year: `\b(19\d{2}|20\d{2})\b` (finds 2023, 2022, etc.)
- Company: Patterns for Inc/Corp/Ltd/LLC
- Sector: Keyword matching (technology, finance, healthcare, etc.)

**Result**: Layer 0 nodes have real metadata from documents

---

## 🌳 Layer 1+ Creation (Summary Nodes)

### Location: `tree.py` → `_build_level()` method (lines 138-207)

This method is called **recursively** for each layer.

### Step-by-Step Process:

### **Step 1: Clustering** (Line 156)
```python
# Get embeddings for current nodes
embeddings = np.array([node.embedding for node in nodes])

# Perform clustering with metadata awareness
clusters = self.clustering.perform_clustering_with_nodes(nodes, embeddings)
```

**What happens**:
- If **metadata clustering enabled** (default):
  - Groups nodes by (sector, company, year) first → `extract_metadata_groups()`
  - Then performs UMAP + GMM clustering **within each metadata group**
- If **metadata clustering disabled**:
  - Standard UMAP + GMM clustering on all nodes together

**Result**: List of clusters, where each cluster = array of node indices

---

### **Step 2: For Each Cluster, Create Parent Node**

#### **2a. Summarize Cluster** (Lines 177-180)
```python
cluster_texts = [node.text for node in cluster_nodes]
summary = self.summarization_model.summarize(
    cluster_texts,
    max_tokens=self.config.summarization_length
)
```

**Method**: Uses GPT-3.5-turbo to create a concise summary of all child texts

---

#### **2b. Create Summary Embedding** (Line 183)
```python
summary_embedding = self.embedding_model.create_embedding(summary)
```

**Method**: Uses text-embedding-3-small to embed the summary

---

#### **2c. Inherit Metadata from Children** (Line 186) ⭐
```python
inherited_metadata = self._inherit_metadata_from_children(cluster_nodes)
```

**This is the KEY method!** Let me show you exactly how it works:

---

## 🔄 Metadata Inheritance Method

### Location: `tree.py` → `_inherit_metadata_from_children()` (lines 105-133)

### Algorithm: **Majority Vote**

```python
def _inherit_metadata_from_children(self, children: List[ClusterNode]) -> Dict[str, Any]:
    """
    Inherit metadata from children nodes.
    Takes the most common value for each metadata field.
    """
    if not children:
        return {}
    
    metadata_fields = ['sector', 'company', 'year']
    inherited = {}
    
    for field in metadata_fields:
        # Step 1: Collect all valid values for this field
        values = []
        for child in children:
            if hasattr(child, 'metadata') and child.metadata:
                value = child.metadata.get(field)
                if value and value != 'unknown':
                    values.append(value)
        
        if values:
            # Step 2: Use MOST COMMON value (majority vote)
            from collections import Counter
            most_common = Counter(values).most_common(1)[0][0]
            inherited[field] = most_common
    
    return inherited
```

### Example Scenarios:

#### **Scenario 1: All Children Have Same Metadata** (Most Common)
```
Children:
  - Child 1: sector='technology', company='Apple Inc', year='2023'
  - Child 2: sector='technology', company='Apple Inc', year='2023'
  - Child 3: sector='technology', company='Apple Inc', year='2023'

Parent Metadata:
  → sector='technology'  (3 votes)
  → company='Apple Inc'  (3 votes)
  → year='2023'          (3 votes)
```

#### **Scenario 2: Mixed Metadata** (Majority Wins)
```
Children:
  - Child 1: sector='technology', company='Apple Inc', year='2023'
  - Child 2: sector='technology', company='Apple Inc', year='2023'
  - Child 3: sector='finance', company='JPMorgan', year='2023'

Parent Metadata:
  → sector='technology'  (2 votes > 1 vote)
  → company='Apple Inc'  (2 votes > 1 vote)
  → year='2023'          (3 votes)
```

#### **Scenario 3: Some Children Missing Metadata**
```
Children:
  - Child 1: sector='technology', company='Apple Inc', year='2023'
  - Child 2: sector='unknown', company='unknown', year='2023'
  - Child 3: sector='technology', company='Apple Inc', year='2023'

Parent Metadata:
  → sector='technology'  (2 valid votes, 'unknown' ignored)
  → company='Apple Inc'  (2 valid votes, 'unknown' ignored)
  → year='2023'          (3 votes)
```

---

## 📝 Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    LAYER 0 (Leaf Nodes)                         │
│                                                                 │
│  Metadata Source: Direct from document chunks                  │
│  Method: FinancialChunker.extract_metadata() - regex patterns  │
│                                                                 │
│  Node 1: text="Apple revenue...", metadata={                   │
│            sector='technology',                                 │
│            company='Apple Inc',                                 │
│            year='2023'                                          │
│          }                                                      │
│  Node 2: text="Apple iPhone...", metadata={...}                │
│  ...                                                            │
└─────────────────────────────────────────────────────────────────┘
                           ↓
                    _build_level(level=1)
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│              STEP 1: CLUSTERING (with metadata)                 │
│                                                                 │
│  Method: clustering.perform_clustering_with_nodes()            │
│                                                                 │
│  1. Extract metadata groups:                                   │
│     Group 1: (technology, Apple Inc, 2023) → [Node1, Node2]   │
│     Group 2: (finance, JPMorgan, 2023) → [Node10, Node11]     │
│                                                                 │
│  2. Within each group, cluster by embeddings (UMAP + GMM)     │
│                                                                 │
│  Result: clusters = [[0,1,2], [3,4], ...]                     │
└─────────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│         STEP 2: FOR EACH CLUSTER, CREATE PARENT NODE           │
│                                                                 │
│  For cluster [0,1,2]:                                          │
│                                                                 │
│  A. Summarize:                                                 │
│     texts = [node0.text, node1.text, node2.text]              │
│     summary = GPT-3.5("Summarize: " + texts)                  │
│     → "Apple Inc reported strong 2023 results..."             │
│                                                                 │
│  B. Embed summary:                                             │
│     embedding = text-embedding-3-small(summary)                │
│                                                                 │
│  C. Inherit metadata (MAJORITY VOTE):                          │
│     _inherit_metadata_from_children([node0, node1, node2])    │
│                                                                 │
│     Children values:                                           │
│       node0: sector='technology', company='Apple', year='2023' │
│       node1: sector='technology', company='Apple', year='2023' │
│       node2: sector='technology', company='Apple', year='2023' │
│                                                                 │
│     Most common:                                               │
│       sector → 'technology' (3 votes)                          │
│       company → 'Apple Inc' (3 votes)                          │
│       year → '2023' (3 votes)                                  │
│                                                                 │
│     inherited_metadata = {                                     │
│       'sector': 'technology',                                  │
│       'company': 'Apple Inc',                                  │
│       'year': '2023'                                           │
│     }                                                          │
│                                                                 │
│  D. Add extra metadata:                                        │
│     inherited_metadata.update({                                │
│       'num_children': 3,                                       │
│       'cluster_idx': 0                                         │
│     })                                                         │
│                                                                 │
│  E. Create parent node:                                        │
│     parent = ClusterNode(                                      │
│       node_id="level_1_cluster_0",                            │
│       text=summary,                                            │
│       embedding=summary_embedding,                             │
│       children=[node0, node1, node2],                         │
│       level=1,                                                 │
│       metadata=inherited_metadata                              │
│     )                                                          │
└─────────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                    LAYER 1 (Summary Nodes)                      │
│                                                                 │
│  Metadata Source: Inherited from Layer 0 children              │
│  Method: _inherit_metadata_from_children() - majority vote     │
│                                                                 │
│  Node: text="Apple Inc reported strong 2023 results...",      │
│        metadata={                                              │
│          sector='technology',      ← Inherited!                │
│          company='Apple Inc',      ← Inherited!                │
│          year='2023',              ← Inherited!                │
│          num_children=3,                                       │
│          cluster_idx=0                                         │
│        }                                                       │
└─────────────────────────────────────────────────────────────────┘
                           ↓
              Repeat _build_level(level=2)
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                    LAYER 2 (Higher Summary)                     │
│                                                                 │
│  Metadata Source: Inherited from Layer 1 children              │
│  Method: Same - majority vote from children                    │
│                                                                 │
│  Continues until max_depth or only 1 node remains             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Summary: Methods Used

| Aspect | Layer 0 | Layer 1+ |
|--------|---------|----------|
| **Text** | Original chunk | GPT-3.5-turbo summary |
| **Embedding** | From chunk | text-embedding-3-small on summary |
| **Metadata** | Regex extraction from document | **Majority vote from children** |
| **Clustering** | Groups formed by metadata + embeddings | Same process recursively |

---

## 🔑 Key Methods

1. **`build_tree()`** - Main orchestrator, creates Layer 0 and calls `_build_level()` recursively

2. **`_build_level()`** - Creates one layer:
   - Clusters nodes
   - Summarizes each cluster
   - Creates parent nodes with inherited metadata

3. **`_inherit_metadata_from_children()`** - **Metadata propagation**:
   - Collects values from children
   - Filters out `None` and `'unknown'`
   - Returns most common value for each field (sector, company, year)

4. **`perform_clustering_with_nodes()`** - Clustering logic:
   - If metadata clustering enabled: group by metadata first
   - Then UMAP + GMM within groups

---

## 🧪 Why This Matters

**Without metadata inheritance** (before the fix):
- Layer 0: ✅ `technology/Apple Inc/2023`
- Layer 1: ❌ `unknown/unknown/unknown`
- Layer 2: ❌ `unknown/unknown/unknown`

**With metadata inheritance** (after the fix):
- Layer 0: ✅ `technology/Apple Inc/2023`
- Layer 1: ✅ `technology/Apple Inc/2023` (inherited via majority vote)
- Layer 2: ✅ `technology/Apple Inc/2023` (inherited via majority vote)

This maintains **business context** throughout the tree hierarchy! 🎉
