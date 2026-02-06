"""
API Validators for different API providers
Each validator implements format validation and live key testing
"""

import re
import requests
from abc import ABC, abstractmethod


class BaseValidator(ABC):
    """Base class for all API validators"""

    @abstractmethod
    def validate_format(self, key):
        """Check if key format is valid"""
        pass

    @abstractmethod
    def test_key(self, key):
        """Test if key is active, returns (is_active: bool, error: str)"""
        pass


class OpenAIValidator(BaseValidator):
    """Validator for OpenAI API keys"""

    FORMAT_PATTERN = r"^sk-[A-Za-z0-9\-]{20,}$"

    def validate_format(self, key):
        return bool(re.match(self.FORMAT_PATTERN, key))

    def test_key(self, key):
        try:
            headers = {"Authorization": f"Bearer {key}"}
            response = requests.get(
                "https://api.openai.com/v1/models",
                headers=headers,
                timeout=5,
            )
            if response.status_code == 200:
                return True, None
            elif response.status_code == 401:
                return False, "Unauthorized - invalid key"
            else:
                return False, f"HTTP {response.status_code}"
        except requests.RequestException as e:
            return False, str(e)


class GitHubValidator(BaseValidator):
    """Validator for GitHub Personal Access Tokens"""

    FORMAT_PATTERN = r"^(ghp_|github_pat_)[A-Za-z0-9_]{36,}$"

    def validate_format(self, key):
        return bool(re.match(self.FORMAT_PATTERN, key))

    def test_key(self, key):
        try:
            headers = {"Authorization": f"token {key}"}
            response = requests.get(
                "https://api.github.com/user",
                headers=headers,
                timeout=5,
            )
            if response.status_code == 200:
                return True, None
            elif response.status_code == 401:
                return False, "Unauthorized - invalid token"
            else:
                return False, f"HTTP {response.status_code}"
        except requests.RequestException as e:
            return False, str(e)


class GoogleValidator(BaseValidator):
    """Validator for Google API keys"""

    FORMAT_PATTERN = r"^AIza[0-9A-Za-z\-_]{35}$"

    def validate_format(self, key):
        return bool(re.match(self.FORMAT_PATTERN, key))

    def test_key(self, key):
        try:
            # Test with Google Geocoding API (free tier)
            response = requests.get(
                "https://maps.googleapis.com/maps/api/geocode/json",
                params={"address": "1600 Amphitheatre Parkway, Mountain View, CA", "key": key},
                timeout=5,
            )
            data = response.json()

            if response.status_code == 200:
                if "error_message" not in data:
                    return True, None
                else:
                    return False, data.get("error_message", "API returned error")
            else:
                return False, f"HTTP {response.status_code}"
        except requests.RequestException as e:
            return False, str(e)


class AWSValidator(BaseValidator):
    """Validator for AWS Access Keys"""

    FORMAT_PATTERN = r"^AKIA[0-9A-Z]{16}$"

    def validate_format(self, key):
        return bool(re.match(self.FORMAT_PATTERN, key))

    def test_key(self, key):
        try:
            # AWS keys need both access key and secret key
            # For format validation only without secret key
            import boto3

            # Create STS client with the key
            # Note: This requires AWS_SECRET_ACCESS_KEY environment variable or credentials file
            sts = boto3.client("sts", aws_access_key_id=key)
            sts.get_caller_identity()
            return True, None
        except Exception as e:
            error_msg = str(e)
            if "InvalidClientTokenId" in error_msg or "SignatureDoesNotMatch" in error_msg:
                return False, "Invalid credentials"
            elif "NoCredentialsError" in error_msg:
                return False, "AWS credentials not configured properly"
            else:
                return False, error_msg


class HuggingFaceValidator(BaseValidator):
    """Validator for Hugging Face API tokens"""

    FORMAT_PATTERN = r"^hf_[A-Za-z0-9_]{34,}$"

    def validate_format(self, key):
        return bool(re.match(self.FORMAT_PATTERN, key))

    def test_key(self, key):
        try:
            headers = {"Authorization": f"Bearer {key}"}
            response = requests.get(
                "https://huggingface.co/api/whoami",
                headers=headers,
                timeout=5,
            )
            if response.status_code == 200:
                return True, None
            elif response.status_code == 401:
                return False, "Unauthorized - invalid token"
            else:
                return False, f"HTTP {response.status_code}"
        except requests.RequestException as e:
            return False, str(e)


class ClaudeValidator(BaseValidator):
    """Validator for Claude (Anthropic) API keys"""

    FORMAT_PATTERN = r"^sk-ant-[A-Za-z0-9\-_]{70,}$"

    def validate_format(self, key):
        return bool(re.match(self.FORMAT_PATTERN, key))

    def test_key(self, key):
        try:
            headers = {
                "x-api-key": key,
                "anthropic-version": "2023-06-01",
            }
            response = requests.get(
                "https://api.anthropic.com/v1/models",
                headers=headers,
                timeout=5,
            )
            if response.status_code == 200:
                return True, None
            elif response.status_code == 401:
                return False, "Unauthorized - invalid API key"
            else:
                return False, f"HTTP {response.status_code}"
        except requests.RequestException as e:
            return False, str(e)


class GeminiValidator(BaseValidator):
    """Validator for Google Gemini API keys"""

    FORMAT_PATTERN = r"^AIza[0-9A-Za-z\-_]{35}$|^[A-Za-z0-9_\-]{40,}$"

    def validate_format(self, key):
        return bool(re.match(self.FORMAT_PATTERN, key))

    def test_key(self, key):
        try:
            response = requests.get(
                "https://generativelanguage.googleapis.com/v1beta/models",
                params={"key": key},
                timeout=5,
            )
            if response.status_code == 200:
                return True, None
            elif response.status_code == 400:
                return False, "Invalid API key format"
            elif response.status_code == 403:
                return False, "Forbidden - API not enabled or key invalid"
            else:
                return False, f"HTTP {response.status_code}"
        except requests.RequestException as e:
            return False, str(e)


class GrokValidator(BaseValidator):
    """Validator for Grok (xAI) API keys"""

    FORMAT_PATTERN = r"^xai-[A-Za-z0-9\-_]{20,}$"

    def validate_format(self, key):
        return bool(re.match(self.FORMAT_PATTERN, key))

    def test_key(self, key):
        try:
            headers = {"Authorization": f"Bearer {key}"}
            response = requests.get(
                "https://api.x.ai/v1/models",
                headers=headers,
                timeout=5,
            )
            if response.status_code == 200:
                return True, None
            elif response.status_code == 401:
                return False, "Unauthorized - invalid API key"
            else:
                return False, f"HTTP {response.status_code}"
        except requests.RequestException as e:
            return False, str(e)


class CohereValidator(BaseValidator):
    """Validator for Cohere API keys"""

    FORMAT_PATTERN = r"^[a-z0-9\-]{36}$"

    def validate_format(self, key):
        return bool(re.match(self.FORMAT_PATTERN, key))

    def test_key(self, key):
        try:
            headers = {"Authorization": f"Bearer {key}"}
            response = requests.post(
                "https://api.cohere.com/v1/check-api-key",
                headers=headers,
                timeout=5,
            )
            if response.status_code == 200:
                return True, None
            elif response.status_code == 401:
                return False, "Unauthorized - invalid API key"
            else:
                return False, f"HTTP {response.status_code}"
        except requests.RequestException as e:
            return False, str(e)


class PerplexityValidator(BaseValidator):
    """Validator for Perplexity API keys"""

    FORMAT_PATTERN = r"^pplx-[A-Za-z0-9\-_]{40,}$"

    def validate_format(self, key):
        return bool(re.match(self.FORMAT_PATTERN, key))

    def test_key(self, key):
        try:
            headers = {"Authorization": f"Bearer {key}"}
            response = requests.get(
                "https://api.perplexity.ai/models",
                headers=headers,
                timeout=5,
            )
            if response.status_code == 200:
                return True, None
            elif response.status_code == 401:
                return False, "Unauthorized - invalid API key"
            else:
                return False, f"HTTP {response.status_code}"
        except requests.RequestException as e:
            return False, str(e)


class ReplicateValidator(BaseValidator):
    """Validator for Replicate API tokens"""

    FORMAT_PATTERN = r"^[a-z0-9]{40}$"

    def validate_format(self, key):
        return bool(re.match(self.FORMAT_PATTERN, key))

    def test_key(self, key):
        try:
            headers = {"Authorization": f"Token {key}"}
            response = requests.get(
                "https://api.replicate.com/v1/account",
                headers=headers,
                timeout=5,
            )
            if response.status_code == 200:
                return True, None
            elif response.status_code == 401:
                return False, "Unauthorized - invalid token"
            else:
                return False, f"HTTP {response.status_code}"
        except requests.RequestException as e:
            return False, str(e)


class TogetherAIValidator(BaseValidator):
    """Validator for Together AI API keys"""

    FORMAT_PATTERN = r"^[a-z0-9]{40}$"

    def validate_format(self, key):
        return bool(re.match(self.FORMAT_PATTERN, key))

    def test_key(self, key):
        try:
            headers = {"Authorization": f"Bearer {key}"}
            response = requests.get(
                "https://api.together.xyz/v1/models",
                headers=headers,
                timeout=5,
            )
            if response.status_code == 200:
                return True, None
            elif response.status_code == 401:
                return False, "Unauthorized - invalid API key"
            else:
                return False, f"HTTP {response.status_code}"
        except requests.RequestException as e:
            return False, str(e)


class AnthropicValidator(BaseValidator):
    """Validator for Anthropic API keys (alternative format)"""

    FORMAT_PATTERN = r"^sk-ant-[A-Za-z0-9\-_]{60,}$"

    def validate_format(self, key):
        return bool(re.match(self.FORMAT_PATTERN, key))

    def test_key(self, key):
        try:
            headers = {
                "x-api-key": key,
                "anthropic-version": "2023-06-01",
            }
            response = requests.get(
                "https://api.anthropic.com/v1/models",
                headers=headers,
                timeout=5,
            )
            if response.status_code == 200:
                return True, None
            elif response.status_code == 401:
                return False, "Unauthorized - invalid API key"
            else:
                return False, f"HTTP {response.status_code}"
        except requests.RequestException as e:
            return False, str(e)
