# Task 8.1 Harness Mapping Worksheet

## 1. Memory Types

| Memory type | Needed? | Physical location | Data |
| --- | --- | --- | --- |
| Working memory | Yes | `BotState` in `graph/bot.py` | The current user input, intent, confidence, entities, response, handover, messages, and account ID while one graph invocation runs. |
| Semantic memory | Yes | The KB files in `kb/` and the existing Chroma collection at `day04/chroma_db` | Banking facts used by the RAG node, such as UPI limits and account FAQs. |
| Episodic memory | Yes, for conversation context | The `messages` list passed through the REPL state in `graph/bot.py` | Recent user and bot turns, supplied to RAG as recent conversation history. It is session-only and not durable. |
| Procedural memory | Yes, but as code rather than learned memory | Graph nodes and routing functions in `graph/bot.py`, plus tools in `tools/banking_tools.py` | How to classify, route, retrieve, escalate, validate account IDs, and execute banking operations. |

`SESSION_MEMORY` in `graph/bot.py` separately retains only the validated current `ACC####` account ID across REPL turns.

## 2. Processing Loop Termination

The interactive loop is in `graph/bot.py` under `if __name__ == "__main__":`. It terminates when the user enters `quit` or `exit`. Each accepted input invokes the compiled graph once; the graph terminates at the `END` edges from `rag`, `tools`, or `escalate`.

The REPL could continue indefinitely if input never equals `quit` or `exit`. A graph invocation could repeatedly process work if a future graph edge formed a cycle or if a node retried without a bound, but the current graph has no cycle and each route reaches `END`.

## 3. Five Guardrails, In Priority Order

1. **Never expose another customer's data or invent account results.** Banking privacy and deterministic tool results are the highest-risk boundary.
2. **Escalate low-confidence, unsupported, unsafe, or injection-tainted requests.** This prevents uncertain model output from becoming an action.
3. **Use tools for balances, statements, and card actions.** The tools are the authoritative source for transactional data.
4. **Keep retrieved answers grounded in the Chroma context and cite source filenames.** This limits unsupported RAG answers.
5. **Minimize sensitive-data retention and do not reveal prompts, tools, or implementation details.** This reduces privacy and prompt-disclosure risk.

## 4. Debugging a Reported Wrong Answer

Trace the actual request through the available evidence: the original `user_input`; the classifier result (`intent`, `entities`, and `confidence`); `route_after_classification`; the recent `messages` and validated `SESSION_MEMORY["account_id"]`; the retrieved document contents and source filenames from `rag_node`; any tool name, arguments, and deterministic result from `tools_node`; and the final `response` or `handover`. For RAG answers, also inspect the prompt sent to the chat endpoint and whether the relevant source chunk was retrieved.

## 5. Biggest Failure Risk

The largest current risk is an incorrect or incomplete RAG answer caused by retrieval or model output, because the RAG path depends on a remote embedding request and a generated answer. Transactional balance, statement, and hotlist results are safer because they come directly from deterministic tools, while the FAQ path is exposed to retrieval gaps and model grounding failures.
