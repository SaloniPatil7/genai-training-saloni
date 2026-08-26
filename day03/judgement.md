# Task 3.1 — Workflow or Agent?

## 1. Classify incoming customer emails into five categories

**Decision: Workflow**

The categories are fixed and the classification process is predictable, so a workflow is sufficient. The cost of errors can be controlled with validation, and a fixed workflow provides more predictability than giving an agent unnecessary freedom.

## 2. Resolve a customer's failed UPI transaction end-to-end across three internal systems, deciding the path as it goes

**Decision: Agent**

The agent needs to decide what to do based on information returned from different systems, so the path may change during the process. The cost of errors is high in banking, so the agent should still have strict tools and guardrails to maintain predictability.

## 3. Generate a monthly account-summary paragraph from a fixed data table

**Decision: Workflow**

The input and required output are well defined, so there is no need for an agent to make decisions about the process. A workflow gives better predictability and reduces the cost of errors for a routine task.

## 4. Answer product FAQs from a knowledge base

**Decision: Workflow**

The system can retrieve information from the knowledge base and generate an answer using a fixed sequence of steps. This gives predictable behavior and reduces the cost of errors by keeping answers grounded in the available information.

## 5. Research and compile a comparison of competitor credit-card offerings

**Decision: Agent**

This task can require multiple searches and decisions about which information to collect and compare. An agent is useful because the path is less predictable, although the cost of errors means the results should still be checked and grounded in reliable sources.

## 6. Route an incoming call to the right department

**Decision: Workflow**

The departments and routing rules are usually predefined, so a fixed workflow can classify the request and send it to the correct department. This provides high predictability and reduces the cost of routing errors.