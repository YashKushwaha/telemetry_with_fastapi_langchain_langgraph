import asyncio
import random
from typing import Any, Dict, List


class MockSQLDatabase:
    async def query(self, sql: str) -> List[Dict[str, Any]]:
        latency = random.choice([0.05, 0.5, 2.0])
        await asyncio.sleep(latency)
        return [
            {"id": 1, "name": "Alice", "status": "active"},
            {"id": 2, "name": "Bob", "status": "inactive"},
        ]


    async def execute(self, sql: str) -> Dict[str, Any]:
        latency = random.choice([0.05, 0.5, 2.0])
        await asyncio.sleep(latency)
        return {"status": "ok", "statement": sql}
