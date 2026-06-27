import logging
from langfuse import Langfuse
from backend.config import settings

logger = logging.getLogger(__name__)

class LangfuseTracer:
    def __init__(self):
        self.langfuse = None
        if settings.LANGFUSE_PUBLIC_KEY and settings.LANGFUSE_SECRET_KEY:
            self.langfuse = Langfuse(
                public_key=settings.LANGFUSE_PUBLIC_KEY,
                secret_key=settings.LANGFUSE_SECRET_KEY.get_secret_value(),
                host=settings.LANGFUSE_HOST
            )
            logger.info("Langfuse Tracing Initialized")
        else:
            logger.warning("Langfuse keys not found. Tracing disabled.")

    def trace_workflow(self, trace_id: str, name: str, user_id: str, metadata: dict = None):
        if not self.langfuse:
            return None
            
        return self.langfuse.trace(
            id=trace_id,
            name=name,
            user_id=user_id,
            metadata=metadata or {}
        )

langfuse_tracer = LangfuseTracer()
