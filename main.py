#!/usr/bin/env python3
"""
API Key Checker - Validate and test API keys for multiple providers
Supports batch processing and detailed validation reports
"""

import argparse
import json
import sys
from pathlib import Path
from api_validators import (
    OpenAIValidator,
    GitHubValidator,
    GoogleValidator,
    AWSValidator,
    HuggingFaceValidator,
)
from utils import load_keys_from_file, print_report


def get_validator(api_type):
    """Return validator instance for the given API type"""
    validators = {
        "openai": OpenAIValidator(),
        "github": GitHubValidator(),
        "google": GoogleValidator(),
        "aws": AWSValidator(),
        "huggingface": HuggingFaceValidator(),
    }
    return validators.get(api_type.lower())


def validate_single_key(key, api_type):
    """Validate and test a single API key"""
    validator = get_validator(api_type)

    if not validator:
        print(f"❌ Unknown API type: {api_type}")
        print(f"   Supported types: {', '.join(['openai', 'github', 'google', 'aws', 'huggingface'])}")
        return None

    result = {
        "api_type": api_type,
        "key_preview": key[:10] + "***" if len(key) > 10 else "***",
        "format_valid": validator.validate_format(key),
        "is_active": False,
        "status": "Invalid format",
        "error": None,
    }

    if result["format_valid"]:
        is_active, error = validator.test_key(key)
        result["is_active"] = is_active
        result["error"] = error
        if is_active:
            result["status"] = "✅ Valid and Active"
        else:
            result["status"] = f"❌ Invalid/Inactive - {error}"
    else:
        result["status"] = "❌ Invalid format"

    return result


def validate_batch_keys(keys_data, api_type):
    """Validate multiple keys from a list or file"""
    results = []

    if isinstance(keys_data, str) and Path(keys_data).exists():
        keys = load_keys_from_file(keys_data)
    elif isinstance(keys_data, list):
        keys = keys_data
    else:
        keys = [keys_data]

    for key in keys:
        if key.strip():
            result = validate_single_key(key.strip(), api_type)
            if result:
                results.append(result)

    return results


def main():
    parser = argparse.ArgumentParser(
        description="🔑 API Key Checker - Validate and test API keys",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check a single key
  python main.py openai "sk-..."
  
  # Check multiple keys from a file
  python main.py openai keys.txt
  
  # Test GitHub key
  python main.py github "ghp_..."
  
  # Check and save report
  python main.py openai keys.txt --output report.json
        """,
    )

    parser.add_argument("api_type", help="API type to check (openai, github, google, aws, huggingface)")
    parser.add_argument("key", help="API key or path to file with keys (one per line)")
    parser.add_argument("--output", "-o", help="Save report to JSON file")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    print("\n🔍 Checking API Key(s)...\n")

    # Check if input is a file
    if Path(args.key).exists():
        results = validate_batch_keys(args.key, args.api_type)
        print(f"📊 Batch validation of {len(results)} key(s)\n")
    else:
        results = validate_batch_keys([args.key], args.api_type)
        print(f"🔑 Single key validation\n")

    # Print results
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print_report(results)

    # Save to file if requested
    if args.output:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\n✅ Report saved to {args.output}")

    # Exit with appropriate code
    valid_count = sum(1 for r in results if r["is_active"])
    if valid_count == 0 and results:
        sys.exit(1)


if __name__ == "__main__":
    main()
