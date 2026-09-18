# Day 10 Retro

1. I would define the evaluation contract and fresh-clone installation path before building the final graph, so missing manifests and empty eval files could not survive until demo day.
2. I would replace process-local account memory with authenticated, durable session storage and explicit authorization checks before exposing account data.
3. I would add structured tracing, adversarial regression cases, and failure injection for model, embedding, and tool outages before calling the system production-ready.