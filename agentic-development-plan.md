# Enterprise Customer Support Agent

## Goal

Build one end-to-end agentic AI application while learning LangGraph, RAG, DeepEval, Ragas, Langfuse, and FastAPI.

The system will read customer complaints, look up customer and order information, retrieve relevant company policies, recommend resolutions, escalate complex cases for human approval, and record evaluations and traces.

## Technology Stack

- Python
- LangGraph
- ChromaDB
- DeepEval
- Ragas
- Langfuse
- FastAPI
- Pydantic
- pytest

## Final Architecture

```text
Customer Complaint API
        |
        v
LangGraph Supervisor
   |         |           |
   v         v           v
Customer   Policy     Resolution
Agent      Agent         Agent
   |         |           |
Customer   RAG         Reviewer
and Order  ChromaDB        |
Tools                       v
                 Human Approval
                        |
                        v
               Final Recommendation
```

Monitoring and evaluation cross-cut the application:

- Langfuse traces, latency, token usage, costs, and prompt versions
- DeepEval agent tests
- Ragas RAG tests

## Seven-Day Implementation Roadmap

### Day 1 - Build the Basic Classification Agent

Deliverables:

- Define a Pydantic response model.
- Classify complaints with an LLM.
- Return category, priority, customer intent, and investigation requirement.
- Handle invalid or malformed model responses.
- Add five complaint test cases.

Implementation scope:

- Complaint classification only
- No LangGraph orchestration
- No RAG
- No evaluation framework

Test input:

```text
My payment was deducted twice,
but I received only one order.
```

Expected response:

```json
{
  "category": "Payment",
  "priority": "High",
  "customer_intent": "Duplicate payment complaint",
  "requires_investigation": true
}
```

Acceptance criteria:

- Structured output is validated by Pydantic.
- Invalid model output produces a controlled error or retry.
- All five test cases pass.

### Day 2 - Build the Multi-Agent LangGraph Workflow

Deliverables:

- Add a Planner Agent.
- Add a Policy Research Agent.
- Add a Resolution Agent.
- Add a Reviewer Agent.
- Add customer and order lookup tools.
- Implement conditional routing and retry limits.

Workflow:

1. Planner extracts and organizes the complaint.
2. Customer and order tools gather supporting context.
3. Policy Research gathers relevant policy information.
4. Resolution proposes a recommendation.
5. Reviewer validates the result.
6. Rejected recommendations return to Resolution, subject to a retry limit.
7. Complex or high-risk cases route to human approval.

Acceptance criteria:

- The graph completes successfully for valid complaints.
- An incorrect recommendation is rejected.
- Rejection triggers another resolution attempt.
- The retry limit prevents infinite loops.

### Day 3 - Add RAG with ChromaDB

Deliverables:

- Upload company policy PDFs.
- Extract policy text.
- Chunk documents with an explicit strategy.
- Generate embeddings.
- Store documents and metadata in ChromaDB.
- Retrieve relevant policy sections.
- Connect retrieval to the Policy Research Agent.

Acceptance criteria:

- Refund, delivery, and payment questions retrieve relevant policy sections.
- Retrieved citations or document metadata are preserved.
- Policy answers can be traced to retrieved content.

### Day 4 - Integrate DeepEval

Deliverables:

- Automated answer relevancy tests.
- Automated faithfulness tests.
- Automated hallucination tests.
- Task-completion tests.
- Tool-correctness tests.
- A suite containing at least ten test cases.

Acceptance criteria:

- Failing test cases identify the responsible response or tool behavior.
- Evaluation configuration is repeatable through the test command.
- The suite distinguishes successful, marginal, and failing behavior.

### Day 5 - Integrate Ragas

Deliverables:

- Context precision metric.
- Context recall metric.
- Faithfulness metric.
- Answer relevancy metric.
- Retrieval comparison for Top K = 3 and Top K = 5.

Acceptance criteria:

- Ragas runs against a fixed evaluation dataset.
- Metrics are recorded for both retrieval configurations.
- The better configuration is identified with supporting metric values.

### Day 6 - Integrate Langfuse

Deliverables:

- Trace LangGraph execution.
- Trace LLM calls.
- Trace tool calls.
- Track token usage and latency.
- Track cost.
- Compare two prompt versions.

Acceptance criteria:

- Every test run contains a complete trace.
- The slowest workflow step is identifiable.
- The most expensive workflow step is identifiable.
- Prompt-version differences can be compared.

### Day 7 - Complete the Application

Deliverables:

- FastAPI complaint-processing endpoint.
- Human approval endpoint or approval state for escalations.
- Error handling and bounded retries.
- Unit and integration tests.
- Combined DeepEval, Ragas, and Langfuse pipeline.
- README with setup and run instructions.

Acceptance criteria:

- An API request receives a validated final recommendation.
- Escalations require an approval decision.
- Failures return structured errors.
- The combined evaluation pipeline runs consistently.
- A feature change can be implemented and verified within a 45-minute interview simulation.

## Suggested Project Structure

```text
enterprise_customer_support/
├── app/
│   ├── api/
│   ├── agents/
│   ├── graph/
│   ├── tools/
│   ├── rag/
│   ├── evaluators/
│   ├── models/
│   └── observability/
├── data/
│   ├── policies/
│   └── fixtures/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── deepeval/
│   └── ragas/
├── pyproject.toml
└── README.md
```

## Daily Working Method

For each day:

1. State the implementation requirement.
2. Identify the smallest project structure needed.
3. Implement one vertical slice.
4. Add focused tests.
5. Run the tests and fix failures.
6. Review the implementation.
7. Answer a few short interview questions based on the code.

## Day 1 Starting Task

Start by creating a minimal Python project and implementing the complaint classification agent.

Requirements:

- Use LangGraph for the classification workflow.
- Use Pydantic for structured output.
- Use Pydantic for structured output.
- Use an LLM-based classifier.
- Return a controlled error for invalid model output.
- Add five test cases.
- Do not add LangGraph yet.
