import re
from typing import Optional

from telemetry.provider import trace_span
from llm.mock_llm import generate_response


def _evaluate_math(expression: str) -> Optional[str]:
    digits = re.findall(r"[-+*/0-9.()]+", expression)
    if not digits:
        return None
    try:
        return str(eval("".join(digits)))
    except Exception:
        return None


async def run_agent_workflow(message: str) -> str:
    with trace_span("Planner", {"agent": "simple"}):
        tool_result = _evaluate_math(message)

    if tool_result is not None:
        with trace_span("Calculator", {"tool": "calculator"}):
            return f"Calculator result: {tool_result}"

    with trace_span("LLM", {"agent": "fallback"}):
        return await generate_response(message, [])
