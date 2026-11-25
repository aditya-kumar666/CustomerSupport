from typing import Any, Protocol, TypedDict

from pydantic import ValidationError

from langgraph.graph import END, StateGraph

from .models import ComplaintClassification


SYSTEM_PROMPT = """You are a customer support complaint classifier.

Choose the most specific category and priority:
- category: Payment, Delivery, Refund, Product, Account, or General
- priority: Low, Medium, High, or Critical
- customer_intent: a short summary of what the customer wants
- requires_investigation: true when customer, order, payment, or account records must be checked

Do not invent customer details. Return only the structured classification."""


class ClassificationError(RuntimeError):
    """Raised when a complaint cannot be converted to a valid classification."""


class StructuredChatModel(Protocol):
    def classify(self, complaint: str) -> ComplaintClassification:
        """Return a validated classification."""


class ComplaintState(TypedDict, total=False):
    complaint: str
    attempts: int
    classification: ComplaintClassification | None
    error: str | None


class ComplaintClassifier:
    def __init__(self, llm: StructuredChatModel, max_attempts: int = 3) -> None:
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")

        self.llm = llm
        self.max_attempts = max_attempts
        self.graph = self._build_graph()

    def _build_graph(self) -> Any:
        graph = StateGraph(ComplaintState)
        graph.add_node("validate", self._validate)
        graph.add_node("classify", self._classify)
        graph.set_entry_point("validate")
        graph.add_conditional_edges(
            "validate",
            self._route_after_validation,
            {"classify": "classify", "end": END},
        )
        graph.add_conditional_edges(
            "classify",
            self._route_after_classification,
            {"classify": "classify", "end": END},
        )
        return graph.compile()

    def _validate(self, state: ComplaintState) -> ComplaintState:
        complaint = state["complaint"].strip()
        if not complaint:
            return {"complaint": "", "attempts": 0, "classification": None, "error": "Complaint text cannot be empty"}
        return {"complaint": complaint, "attempts": 0, "classification": None, "error": None}

    def _route_after_validation(self, state: ComplaintState) -> str:
        return "end" if state["error"] else "classify"

    def _classify(self, state: ComplaintState) -> ComplaintState:
        attempts = state["attempts"] + 1
        try:
            classification = self.llm.classify(state["complaint"])
            if not isinstance(classification, ComplaintClassification):
                classification = ComplaintClassification.model_validate(classification)
            return {
                "complaint": state["complaint"],
                "attempts": attempts,
                "classification": classification,
                "error": None,
            }
        except (ValidationError, ValueError, TypeError) as exc:
            return {
                "complaint": state["complaint"],
                "attempts": attempts,
                "classification": None,
                "error": str(exc),
            }
        except Exception as exc:
            return {
                "complaint": state["complaint"],
                "attempts": attempts,
                "classification": None,
                "error": str(exc),
            }

    def _route_after_classification(self, state: ComplaintState) -> str:
        if state["classification"] is not None:
            return "end"
        if state["attempts"] >= self.max_attempts:
            return "end"
        return "classify"

    def classify(self, complaint: str) -> ComplaintClassification:
        state = self.graph.invoke(
            {
                "complaint": complaint,
                "attempts": 0,
                "classification": None,
                "error": None,
            }
        )
        if state["classification"] is not None:
            return state["classification"]
        error = state["error"] or "Unknown classification failure"
        if error == "Complaint text cannot be empty":
            raise ClassificationError(error)
        raise ClassificationError(
            f"Could not produce a valid classification after {self.max_attempts} attempts"
        )
