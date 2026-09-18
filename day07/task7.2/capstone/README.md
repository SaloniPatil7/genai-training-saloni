## What it does

NovaTrust is a banking customer-service assistant. It classifies each request, routes balance, statement, and card actions to deterministic tools, answers supported FAQ and UPI questions from the knowledge base, and escalates unsafe or unsupported requests to a human agent. It keeps one validated account reference in process-local session memory for the REPL.

## How to run it (from a fresh clone)

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
printf 'OPENROUTER_API_KEY=your-key-here\n' > .env
python day07/task7.2/capstone/evals/run_evals.py
python day07/task7.2/capstone/graph/bot.py
```

The eval command is offline and checks routing, deterministic tools, refusal, escalation, and the adversarial cases. The interactive bot and RAG index require a working OpenRouter API key. From the repository root, refresh the index with `python day07/task7.2/capstone/build_index.py`.

## Architecture

```text
START
  |
  v
classify -- low confidence / out_of_scope --> escalate --> END
  |
  +-- balance_enquiry / card_hotlist / statement_request --> tools --> END
  |
  +-- upi_issue / small_talk --> rag --> END

classify applies the deterministic injection and sensitive-data gate.
rag retrieves Chroma documents and asks the guarded chat model to answer
only from the retrieved context with source filenames.
```

## Eval results

The checked-in suite contains 12 cases covering four KB-answerable requests, two unanswerable requests, three transactional tool calls, and three adversarial inputs. The current offline result is 12/12 passed (100%). Reproduce it with `python day07/task7.2/capstone/evals/run_evals.py`.

## Known limitations

- Classification, embeddings, and RAG responses depend on OpenRouter availability, model behavior, rate limits, and a valid API key.
- Session memory is process-local, stores only one account reference, and is not durable or multi-user safe.
- The injection gate uses known text patterns, so paraphrased prompt injections may still reach the classifier.
- Mock tools use fictional data and do not provide real authentication, authorization, or banking execution.
- There is no production audit log, observability pipeline, retry policy, or integrated human handoff service.