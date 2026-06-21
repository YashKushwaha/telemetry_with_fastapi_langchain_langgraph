from typing import Any, Dict


class PrivacyProcessor:
    def process(self, span: Dict[str, Any]) -> Dict[str, Any]:
        redacted = {key: value for key, value in span.items() if key not in {"password", "credit_card", "email"}}
        return redacted


class CostProcessor:
    def process(self, span: Dict[str, Any]) -> Dict[str, Any]:
        span = dict(span)
        span["estimated_cost"] = 0.0001
        return span
