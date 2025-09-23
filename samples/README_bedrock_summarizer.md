# Bedrock Document Summarizer

A comprehensive Python script to test Amazon Bedrock LLM for document summarization with support for multiple models and summary types.

## Features

- **Multiple Model Support**: Claude, Titan, and Llama models
- **Summary Types**: Concise, detailed, and bullet-point summaries
- **Batch Processing**: Summarize multiple documents at once
- **Model Comparison**: Compare summaries from different models
- **Interactive Mode**: Real-time text summarization
- **Flexible Input**: File input, direct text, or interactive mode

## Prerequisites

1. AWS CLI configured with appropriate credentials
2. Access to Amazon Bedrock models in your AWS account
3. Python 3.7 or higher

## Installation

```bash
pip install -r requirements.txt
```

## Usage Examples

### Basic Usage
```bash
# Summarize a single document with Claude
python bedrock_document_summarizer.py -f sample_document.txt

# Use different model
python bedrock_document_summarizer.py -f sample_document.txt -m titan

# Different summary type
python bedrock_document_summarizer.py -f sample_document.txt -t detailed
```

### Advanced Usage
```bash
# Compare all models
python bedrock_document_summarizer.py -f sample_document.txt -c

# Batch process multiple files
python bedrock_document_summarizer.py -b doc1.txt doc2.txt doc3.txt -m claude

# Direct text input
python bedrock_document_summarizer.py --text "Your text here" -t bullet

# Specify AWS region
python bedrock_document_summarizer.py -f sample_document.txt -r us-west-2
```

### Interactive Mode
```bash
# Run without arguments for interactive mode
python bedrock_document_summarizer.py
```

## Command Line Arguments

- `-f, --file`: Path to document file
- `-m, --model`: Model to use (claude, titan, llama)
- `-t, --type`: Summary type (concise, detailed, bullet)
- `-r, --region`: AWS region (default: us-east-1)
- `-b, --batch`: Multiple files for batch processing
- `-c, --compare`: Compare all models
- `--text`: Direct text input

## Model Information

- **Claude**: Anthropic Claude 3 Sonnet - Best for nuanced understanding
- **Titan**: Amazon Titan Text Express - AWS native model
- **Llama**: Meta Llama 2 70B Chat - Open-source alternative

## AWS Permissions Required

Ensure your AWS credentials have the following permissions:
- `bedrock:InvokeModel`
- Access to the specific Bedrock models you want to use

## Testing

Test with the provided sample document:
```bash
python bedrock_document_summarizer.py -f sample_document.txt -c
```