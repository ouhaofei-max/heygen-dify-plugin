from typing import Any
import re

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class HeygenDifyPluginProvider(ToolProvider):
    """Provider class for HeyGen Dify plugin.

    Validates the provided credentials for the tool. Currently it verifies that
    the `heygen_api_key` value exists, is a non-empty string and roughly matches
    the expected API key pattern (alphanumeric + dashes, length sanity check).
    """

    API_KEY_RE = re.compile(r"^[A-Za-z0-9\-]{16,128}$")

    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            if not isinstance(credentials, dict):
                raise ValueError("credentials must be a dict")

            api_key = credentials.get("heygen_api_key")
            if not api_key or not isinstance(api_key, str):
                raise ValueError("heygen_api_key is required and must be a string")

            # Basic sanity check of key format; exact format may vary by HeyGen.
            if not self.API_KEY_RE.match(api_key):
                # We don't reject immediately on a strict mismatch, but warn via error.
                raise ValueError("heygen_api_key format looks invalid")

        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))

