from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


ComplaintCategory = Literal["Payment", "Delivery", "Refund", "Product", "Account", "General"]
Priority = Literal["Low", "Medium", "High", "Critical"]


class ComplaintClassification(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category: ComplaintCategory = Field(description="Best complaint category")
    priority: Priority = Field(description="Urgency of the complaint")
    customer_intent: str = Field(min_length=3, description="Concise description of the customer's intent")
    requires_investigation: bool = Field(description="Whether customer or order records require investigation")
