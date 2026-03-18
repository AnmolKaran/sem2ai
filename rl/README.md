# Reinforcement Learning

A reinforcement learning framework built on top of graph-based environments.

## How it works

- **`rlsetup.py`** — defines the environment: parses a graph DSL (similar to `graphs/gw2.py`) to create states, transitions, and rewards. Supports vertex blocking (`B`), edge creation, and reward assignment.
- **`rl1.py`** — implements the learning agent: runs episodes on the graph environment, updates a value/policy estimate (Q-learning style), and converges toward an optimal policy.

The agent explores the graph, collects rewards at designated vertices, and learns which actions to take at each state.

## How to run

```bash
python rl1.py
```

The graph environment is defined at the bottom of the file (or piped via stdin using the same DSL as `graphs/`). Learned policy and episode rewards are printed as training progresses.
