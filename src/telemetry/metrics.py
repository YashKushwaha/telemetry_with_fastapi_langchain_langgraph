from collections import Counter
from typing import Dict, List, Optional
from uuid import uuid4

_request_counts: Counter[str] = Counter()
_request_latencies: List[float] = []
_failed_requests = 0
_feedback_store: List[Dict[str, Optional[str]]] = []


def record_request(path: str, latency_ms: float, failed: bool = False) -> None:
    global _failed_requests
    _request_counts[path] += 1
    _request_latencies.append(latency_ms)
    if failed:
        _failed_requests += 1


def add_feedback(user_id: Optional[str], rating: int, comment: Optional[str]) -> str:
    feedback_id = f"fb-{uuid4().hex[:8]}"
    _feedback_store.append(
        {"feedback_id": feedback_id, "user_id": user_id, "rating": rating, "comment": comment}
    )
    return feedback_id


def get_metrics_snapshot() -> Dict[str, object]:
    average_latency = float(sum(_request_latencies) / len(_request_latencies)) if _request_latencies else 0.0
    return {
        "requests": sum(_request_counts.values()),
        "failed_requests": _failed_requests,
        "average_latency_ms": round(average_latency, 1),
        "requests_by_path": dict(_request_counts),
        "feedback_count": len(_feedback_store),
    }
