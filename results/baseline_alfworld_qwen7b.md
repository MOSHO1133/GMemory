# ALFWorld baseline: qwen2.5-7b, AutoGen, empty vs G-Memory

All 134 ALFWorld tasks, run once with each memory setting.

| Metric | empty (no memory) | g-memory |
|---|---|---|
| **Overall success** | **48/134 (35.8%)** | **37/134 (27.6%)** |
| put | 9/24 (37.5%) | 9/24 (37.5%) |
| clean | 7/31 (22.6%) | 9/31 (29.0%) |
| heat | 13/23 (56.5%) | 10/23 (43.5%) |
| cool | 12/21 (57.1%) | 7/21 (33.3%) |
| examine | 3/18 (16.7%) | 2/18 (11.1%) |
| puttwo | 4/17 (23.5%) | 0/17 (0.0%) |
| Prompt tokens | 7,078,487 | 12,995,340 |
| Completion tokens | 124,402 | 223,577 |
| Run time | 2838.16 s (47.3 min) | 5342.34 s (89.0 min) |
| Time per task | 21.2 s | 39.9 s |

G-Memory stored 36 insights by the end of the run.

## Setup

- **LLM:** `qwen2.5-7b` served by Ollama through its OpenAI-compatible API (`OPENAI_API_BASE=http://localhost:11434/v1`). It is a local model built from `qwen2.5:7b` with `num_ctx 8192`, running fully on an RTX 2060 Super 8 GB.
- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2`
- **Command:** `python tasks/run.py --task alfworld --reasoning io --mas_type autogen --max_trials 30 --model qwen2.5-7b --mas_memory {empty,g-memory}`
- **G-Memory parameters:** defaults (successful_topk 1, failed_topk 0, insights_topk 3, threshold 0.0, hop 1, no role projector)
- **Environment:** ALFWorld `AlfredTWEnv` with the oracle controller, run on WSL2 Ubuntu
- **Seed:** `random.seed(42)`. Each setting was run once, so the run-to-run spread is unknown.

## Notes

- The `price=` value in the run log uses hard-coded GPT-4o rates. It does not apply to a local model.
- Both runs used `TMPDIR` set to a folder on disk. ALFWorld's fast-downward wrapper copies a 31 MB `libdownward.so` into a new temp folder every time it loads a game, and those copies stay mapped. That filled the 7.8 GB `/tmp` tmpfs after about 125 tasks and crashed the first empty run.
- The first G-Memory run crashed at task 20, when `merge_insights` first runs: `FINCH() got an unexpected keyword argument 'metric'`. The cause was that `finch_clust` and `finchpy` both install the `finch` package, and `finch_clust` overwrote `finchpy`. The fix was to keep only `finchpy==0.0.1` (commit `a0a0b0c`).
- The reported runs both finished cleanly: 134/134 tasks, exit code 0, no tracebacks or API errors.
- With this 7B model, G-Memory scored 8.2 points **below** the no-memory baseline. It also used about 1.8× the tokens and 1.9× the time.
