# 🔑 API Key Checker

A modern web-based application to validate and test API keys for multiple providers. Features a beautiful UI, real-time validation, batch processing, and instant feedback.

## Features

✅ **Multi-Provider Support**
- OpenAI (sk-* keys)
- GitHub (Personal Access Tokens)
- Google Cloud (API keys)
- AWS (Access Keys)
- Hugging Face (Tokens)

✅ **Dual Validation**
- Format validation (checks key pattern)
- Live testing (verifies key is active with actual API calls)

✅ **Batch Processing**
- Check single keys via command line
- Process multiple keys from a file
- Generate JSON reports

✅ **Flexible Output**
- Beautiful formatted table
- JSON export
- Save reports to file

## Installation

1. Clone or download this project
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run the web server:
```bash
python app.py
```
4. Open your browser and go to: **http://localhost:5000**

## Usage

### Single Key Validation
1. Select an API type from the dropdown (OpenAI, GitHub, Google, AWS, Hugging Face)
2. Paste your API key in the input field
3. Click "Validate Key"
4. View instant results with validation status and details

### Batch Processing
1. Switch to "Batch Upload" mode
2. Select the API type
3. Paste multiple keys (one per line)
4. Click "Validate All"
5. View summary statistics and individual results

### Features
- ✅ **Real-time Validation** - Instant format and live key testing
- ✅ **Security** - Keys are never stored or logged
- ✅ **Beautiful UI** - Modern, responsive interface
- ✅ **Batch Processing** - Check multiple keys at once
- ✅ **Keyboard Shortcuts** - Ctrl+Enter to validate

## Supported API Types

| API Type | Key Format | Example |
|----------|-----------|---------|
| `openai` | sk-* | sk-proj-abc123... |
| `github` | ghp_* or github_pat_* | ghp_abc123... |
| `google` | AIza* | AIzaSyD... |
| `aws` | AKIA* | AKIAIOSFODNN7EXAMPLE |
| `huggingface` | hf_* | hf_abcdef123456... |

## Output Examples

### Single Key Result
```
Status: ✅ Valid and Active
API Type: OpenAI
Key Preview: sk-***
Format Valid: ✅ Yes
Key Active: ✅ Yes
```

### Batch Results
```
Valid & Active: 2
Invalid/Inactive: 1
Format Errors: 0

#1: ✅ Valid and Active [sk-***]
#2: ❌ Invalid/Inactive [sk-***] - Error: Unauthorized
#3: ❌ Invalid format [sk-***]
```

## Exit Codes

- `0` - Server running successfully
- `1` - Server error or port already in use

## Running on Different Ports

To run on a different port:
```bash
# Edit app.py and change:
app.run(debug=True, host='0.0.0.0', port=8000)
```

## Requirements

- Python 3.7+
- requests (HTTP library)
- tabulate (table formatting)
- boto3 (AWS SDK, optional for AWS keys)

## File Format for Batch Processing

Create a text file with one API key per line:
```
sk-abc123...
sk-def456...
sk-ghi789...
```

## Notes

- Keys are not stored or logged permanently
- Sensitive key information is masked in output
- Live testing makes actual API calls to validate keys
- Some providers may rate-limit validation attempts
- AWS validation requires credentials configuration

## Limitations

- AWS validation requires `AWS_SECRET_ACCESS_KEY` to be configured
- Google API testing uses free Geocoding API
- Rate limits may affect batch processing of large key sets

## Error Handling

The tool handles common errors:
- Invalid format detection
- Network timeouts
- API rate limiting
- Unauthorized/invalid credentials
- File not found errors

## License

MIT
