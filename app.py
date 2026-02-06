"""
API Key Checker Web Application
Flask-based web interface for validating API keys
"""

from flask import Flask, render_template, request, jsonify
import json
from api_validators import (
    OpenAIValidator,
    GitHubValidator,
    GoogleValidator,
    AWSValidator,
    HuggingFaceValidator,
    ClaudeValidator,
    GeminiValidator,
    GrokValidator,
    CohereValidator,
    PerplexityValidator,
    ReplicateValidator,
    TogetherAIValidator,
    AnthropicValidator,
)

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Initialize validators
validators = {
    "openai": OpenAIValidator(),
    "github": GitHubValidator(),
    "google": GoogleValidator(),
    "aws": AWSValidator(),
    "huggingface": HuggingFaceValidator(),
    "claude": ClaudeValidator(),
    "gemini": GeminiValidator(),
    "grok": GrokValidator(),
    "cohere": CohereValidator(),
    "perplexity": PerplexityValidator(),
    "replicate": ReplicateValidator(),
    "togetherai": TogetherAIValidator(),
}


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/api/validate', methods=['POST'])
def validate_key():
    """API endpoint to validate a single key"""
    data = request.json
    api_type = data.get('api_type', '').lower()
    key = data.get('key', '').strip()

    if not api_type or not key:
        return jsonify({'error': 'Missing api_type or key'}), 400

    if api_type not in validators:
        return jsonify({
            'error': f'Unknown API type. Supported: {", ".join(validators.keys())}'
        }), 400

    validator = validators[api_type]

    # Validate format
    format_valid = validator.validate_format(key)

    result = {
        'api_type': api_type,
        'key_preview': key[:10] + '***' if len(key) > 10 else '***',
        'format_valid': format_valid,
        'is_active': False,
        'status': 'Invalid format',
        'error': None,
    }

    if format_valid:
        # Test if key is active
        is_active, error = validator.test_key(key)
        result['is_active'] = is_active
        result['error'] = error
        if is_active:
            result['status'] = 'Valid and Active ✅'
        else:
            result['status'] = f'Invalid/Inactive - {error}'
    else:
        result['status'] = 'Invalid format'

    return jsonify(result)


@app.route('/api/batch-validate', methods=['POST'])
def batch_validate():
    """API endpoint to validate multiple keys"""
    data = request.json
    api_type = data.get('api_type', '').lower()
    keys = data.get('keys', [])

    if not api_type or not keys:
        return jsonify({'error': 'Missing api_type or keys'}), 400

    if api_type not in validators:
        return jsonify({
            'error': f'Unknown API type. Supported: {", ".join(validators.keys())}'
        }), 400

    results = []
    for key in keys:
        if key.strip():
            # Make a request to the single validate endpoint
            validator = validators[api_type]

            format_valid = validator.validate_format(key.strip())
            result = {
                'api_type': api_type,
                'key_preview': key.strip()[:10] + '***' if len(key.strip()) > 10 else '***',
                'format_valid': format_valid,
                'is_active': False,
                'status': 'Invalid format',
                'error': None,
            }

            if format_valid:
                is_active, error = validator.test_key(key.strip())
                result['is_active'] = is_active
                result['error'] = error
                if is_active:
                    result['status'] = 'Valid and Active ✅'
                else:
                    result['status'] = f'Invalid/Inactive - {error}'

            results.append(result)

    return jsonify({'results': results})


@app.route('/api/supported-apis', methods=['GET'])
def supported_apis():
    """Get list of supported API types"""
    return jsonify({
        'apis': [
            {'name': 'OpenAI', 'type': 'openai', 'description': 'OpenAI API keys (sk-*)'},
            {'name': 'Claude', 'type': 'claude', 'description': 'Anthropic Claude API keys'},
            {'name': 'Gemini', 'type': 'gemini', 'description': 'Google Gemini API keys'},
            {'name': 'Grok', 'type': 'grok', 'description': 'xAI Grok API keys'},
            {'name': 'Cohere', 'type': 'cohere', 'description': 'Cohere API keys'},
            {'name': 'Perplexity', 'type': 'perplexity', 'description': 'Perplexity API keys'},
            {'name': 'Replicate', 'type': 'replicate', 'description': 'Replicate API tokens'},
            {'name': 'Together AI', 'type': 'togetherai', 'description': 'Together AI API keys'},
            {'name': 'GitHub', 'type': 'github', 'description': 'GitHub Personal Access Tokens'},
            {'name': 'Google Cloud', 'type': 'google', 'description': 'Google Cloud API keys'},
            {'name': 'AWS', 'type': 'aws', 'description': 'AWS Access Keys'},
            {'name': 'Hugging Face', 'type': 'huggingface', 'description': 'Hugging Face tokens'},
        ]
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
