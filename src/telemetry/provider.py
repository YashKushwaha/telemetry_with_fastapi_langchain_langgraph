import logging
from contextlib import contextmanager
from typing import Dict, Optional

from telemetry.context import get_request_context_as_dict

logger = logging.getLogger("telemetry")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


@contextmanager
def trace_span(name: str, attributes: Optional[Dict[str, str]] = None):
    span_attrs = get_request_context_as_dict()
    if attributes:
        span_attrs.update(attributes)
    logger.info("span.start %s %s", name, span_attrs)
    try:
        yield
    except Exception:
        logger.exception("span.error %s %s", name, span_attrs)
        raise
    finally:
        logger.info("span.end %s %s", name, span_attrs)
