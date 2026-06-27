import httpx
from backend.config import settings
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class OPAClient:
    def __init__(self):
        self.opa_url = str(settings.OPA_URL)

    async def evaluate_policy(self, policy_path: str, input_data: Dict[str, Any]) -> bool:
        url = f"{self.opa_url}/v1/data/{policy_path}"
        payload = {"input": input_data}
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, timeout=2.0)
                if response.status_code == 200:
                    result = response.json().get("result", False)
                    # OPA returns either a boolean or an object. If it's an allow rule, check result.allow
                    if isinstance(result, dict) and "allow" in result:
                        return result["allow"]
                    return bool(result)
                else:
                    logger.error(f"OPA returned status code {response.status_code}")
                    return False
        except Exception as e:
            logger.error(f"Failed to evaluate OPA policy: {e}")
            # Fail closed
            return False

opa_client = OPAClient()
