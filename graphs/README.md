# Graph World (gw2)

An ASCII graph environment with a mini DSL for defining graphs, setting rewards, and finding optimal paths.

## How it works

Graphs are defined via a simple command language parsed by `gw2.py`:

| Command | Effect |
|---------|--------|
| `G N` | Create a graph with N vertices (grid or general) |
| `V i` | Block vertex i (removes its edges) |
| `E i j` | Add/remove/toggle edges between vertices |
| `R` | Set a reward at a vertex or edge |

Once a graph is set up:
- `shortestPathToRwd()` finds the shortest path to the nearest reward
- `showAllRwds()` computes and displays the reward policy across the whole graph
- The grid is rendered as ASCII art with directional arrows (`^`, `v`, `<`, `>`) showing the optimal policy

`gw2.py` is the current version; `graph1.py` and `oldgw2.py` are earlier iterations.

## How to run

```bash
python gw2.py
```

Graph commands can be passed via stdin or hardcoded at the bottom of the file. See `gw2Test.txt` for example inputs and outputs.
