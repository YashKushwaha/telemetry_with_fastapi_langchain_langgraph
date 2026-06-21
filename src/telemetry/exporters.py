import logging
from typing import Any, Dict

logger = logging.getLogger("telemetry.exporter")


def console_export(event: str, payload: Dict[str, Any]) -> None:
    logger.info("export %s %s", event, payload)
