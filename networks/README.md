# Network Generator

Generates random graphs and analyzes their degree distributions.

## How it works

Two construction methods, selected via command-line:

- **Connected (C)** — randomly adds edges while keeping the graph connected (Chvátal-style)
- **Incremental (I)** — grows the graph by adding nodes one at a time, connecting each new node to existing ones with preferential attachment

After construction, prints the degree distribution as `degree:count` pairs.

## How to run

```bash
python networks.py <avgDeg> <constructionType> <nodeCt>
```

Example — 100-node graph with average degree 4, built incrementally:
```bash
python networks.py 4 I 100
```
