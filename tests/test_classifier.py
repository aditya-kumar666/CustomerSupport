import pytest

from enterprise_support.classifier import ClassificationError, ComplaintClassifier
from enterprise_support.models import ComplaintClassification


class FakeChatModel:
    def __init__(self, responses):
        self.responses = iter(responses)

    def classify(self, _complaint):
        response = next(self.responses)
        if isinstance(response, Exception):
            raise response
        if isinstance(response, dict):
            return ComplaintClassification.model_validate(response)
        return response


@pytest.mark.parametrize(
    ("complaint", "expected"),
    [
        (
            "My payment was deducted twice, but I received only one order.",
            {
                "category": "Payment",
                "priority": "High",
                "customer_intent": "Duplicate payment complaint",
                "requires_investigation": True,
            },
        ),
        (
            "My package is two weeks late and has not moved.",
            {
                "category": "Delivery",
                "priority": "High",
                "customer_intent": "Delayed delivery complaint",
                "requires_investigation": True,
            },
        ),
        (
            "I want a refund for a damaged headset.",
            {
                "category": "Refund",
                "priority": "Medium",
                "customer_intent": "Refund request for damaged product",
                "requires_investigation": True,
            },
        ),
        (
            "I cannot access my account after resetting the password.",
            {
                "category": "Account",
                "priority": "Medium",
                "customer_intent": "Account access problem",
                "requires_investigation": True,
            },
        ),
        (
            "The button fell off my new jacket after the first use.",
            {
                "category": "Product",
                "priority": "Medium",
                "customer_intent": "Report defective product",
                "requires_investigation": True,
            },
        ),
    ],
)
def test_classifies_complaint(complaint, expected):
    llm = FakeChatModel([expected])
    result = ComplaintClassifier(llm).classify(complaint)

    assert result == ComplaintClassification.model_validate(expected)


def test_retries_invalid_response():
    llm = FakeChatModel(
        [
            {"category": "Unknown", "priority": "Medium", "customer_intent": "Bad", "requires_investigation": True},
            {
                "category": "Delivery",
                "priority": "Low",
                "customer_intent": "Track an existing order",
                "requires_investigation": False,
            },
        ]
    )

    result = ComplaintClassifier(llm, max_attempts=2).classify("Where is my order?")

    assert result.category == "Delivery"


def test_invalid_response_raises_controlled_error():
    llm = FakeChatModel(
        [
            {"category": "Unknown", "priority": "Medium", "customer_intent": "Bad", "requires_investigation": True},
            {"category": "Unknown", "priority": "Medium", "customer_intent": "Bad", "requires_investigation": True},
        ]
    )

    with pytest.raises(ClassificationError, match="Could not produce a valid classification"):
        ComplaintClassifier(llm, max_attempts=2).classify("I need help")


def test_empty_complaint_raises_controlled_error():
    llm = FakeChatModel([])

    with pytest.raises(ClassificationError, match="cannot be empty"):
        ComplaintClassifier(llm).classify("   ")
