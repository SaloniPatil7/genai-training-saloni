# Day 04 — Knowledge Base & Indexing

## 1. Objective

The objective of this task was to build a knowledge base from multiple documents, split the documents into smaller chunks, generate embeddings for those chunks, and store/index them for later retrieval.

I experimented with two different `chunk_size` values:

* `chunk_size = 500`
* `chunk_size = 100`

The purpose was to observe how chunk size affects the number of chunks, embedding time, and indexing process.

---

## 2. Experiment 1 — `chunk_size = 500`

### Result

* Documents loaded: **10**
* Chunks created: **20**
* Chunks indexed: **20**
* Embedding completed successfully.

The program successfully generated embeddings for all 20 chunks.

### Output Summary

```text
Loaded 10 documents.
Created 20 chunks.

Embedding chunk 1/20...
...
Embedding chunk 20/20...

Indexed 20 chunks from 10 documents.
```

### Observation

With a chunk size of 500, the 10 documents were divided into only 20 chunks. Therefore, fewer embeddings had to be generated.

The complete indexing process finished successfully.

---

## 3. Experiment 2 — `chunk_size = 100`

### Result

* Documents loaded: **10**
* Chunks created: **96**
* Embedding started but encountered a **429 Rate Limit** error.

### Output Summary

```text
Loaded 10 documents.
Created 96 chunks.

Embedding chunk 1/96...
Rate limited (429). Waiting 10 seconds...
Rate limited (429). Waiting 20 seconds...
```

### Observation

Reducing the chunk size from 500 to 100 significantly increased the number of chunks:

**20 chunks → 96 chunks**

This means the embedding system had to process many more individual chunks.

Because of the larger number of embedding requests, the API encountered a **429 Rate Limit**.

The process therefore became much slower and did not complete during the experiment.

---

## 4. Comparison

| Parameter            | `chunk_size=500` | `chunk_size=100` |
| -------------------- | ---------------: | ---------------: |
| Documents            |               10 |               10 |
| Chunks               |               20 |               96 |
| Embedding requests   |               20 |               96 |
| Indexing             |        Completed |     Rate limited |
| Processing           |           Faster |           Slower |
| API rate-limit issue |               No |              Yes |

---

## 5. What I Learned

### Larger chunk size

A larger chunk size produces fewer chunks.

For example:

```text
chunk_size = 500
10 documents → 20 chunks
```

This means fewer embedding operations are required, making the indexing process faster and reducing the chance of hitting API rate limits.

### Smaller chunk size

A smaller chunk size produces more chunks.

```text
chunk_size = 100
10 documents → 96 chunks
```

More chunks can provide more granular pieces of information for retrieval, but they also require more embedding operations.

In this experiment, the increased number of chunks resulted in API rate limiting.

---

## 6. Important Trade-off

Chunk size is a trade-off between **retrieval granularity** and **processing efficiency**.

### Larger chunks

**Advantages:**

* Fewer chunks
* Fewer embedding requests
* Faster indexing
* Lower chance of rate limiting

**Disadvantages:**

* Each chunk contains more information
* Retrieval may return more unrelated information along with the relevant information

### Smaller chunks

**Advantages:**

* More focused pieces of information
* More granular retrieval
* Potentially better precision for specific questions

**Disadvantages:**

* Many more chunks
* More embedding requests
* Slower indexing
* Higher possibility of API rate limits

---

## 7. Experiment Conclusion

From my experiment:

```text
chunk_size=500
10 documents → 20 chunks → indexing completed successfully

chunk_size=100
10 documents → 96 chunks → rate limited (429)
```

Therefore, a smaller chunk size does not automatically mean a better RAG system.

The chunk size should be selected based on the type of documents, the retrieval requirements, embedding cost, processing speed, and API limitations.

For this experiment, **`chunk_size=500` was more efficient because the indexing completed successfully with significantly fewer embedding requests.**

---

## 8. Key Takeaway

> **Chunking controls how documents are divided before embedding. Smaller chunks provide finer-grained retrieval but increase the number of embeddings required. Larger chunks reduce processing overhead but may contain more information than necessary for a specific query.**

The goal is to find a **balanced chunk size** that provides useful retrieval without creating unnecessary embedding requests.
