# Crossword Puzzle Generator

Generates valid crossword puzzles using constraint satisfaction and backtracking.

## How it works

1. **Block placement** — places `#` squares on the grid using heuristics to avoid clumping and ensure all white cells stay connected (verified with DFS)
2. **Word placement** — fills words from a dictionary via backtracking (`bF()`); falls back to greedy horizontal placement if backtracking exceeds ~28 seconds
3. Constraint propagation narrows candidate words at each position before searching

Two dictionaries are available: `dct20k.txt` (20k words, faster) and `dctLarge.txt` (full dictionary, better fill).

`crossword2.py` is the latest version; `crossword1.py` is an earlier, simpler iteration.

## How to run

```bash
python crossword2.py <height>x<width> <numBlocks> [dictionary.txt] [seedWords...]
```

| Argument | Format | Description |
|----------|--------|-------------|
| Dictionary | `dct20k.txt` | Path to a `.txt` word list |
| Grid size | `7x7` | Height × width (required) |
| Block count | `15` | Number of `#` squares |
| Seed words | `V2x3HELLO` | Pre-placed words — `V`/`H` + row×col + word |

Example:
```bash
python crossword2.py 7x7 12 dct20k.txt
```
