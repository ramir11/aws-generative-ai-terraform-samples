#!/usr/bin/env python3
"""
Bedrock Document Summarizer
A comprehensive script to test Amazon Bedrock LLM for document summarization.
"""

import boto3
import json
import argparse
import sys
from pathlib import Path
from typing import Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BedrockDocumentSummarizer:
    """Amazon Bedrock document summarizer with multiple model support."""
    
    def __init__(self, region: str = 'us-east-1'):
        """Initialize Bedrock client."""
        try:
            self.bedrock = boto3.client('bedrock-runtime', region_name=region)
            self.region = region
            logger.info(f"Initialized Bedrock client in region: {region}")
        except Exception as e:
            logger.error(f"Failed to initialize Bedrock client: {e}")
            sys.exit(1)
    
    def read_document(self, file_path: str) -> str:
        """Read document content from file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            logger.info(f"Successfully read document: {file_path}")
            return content
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return ""
    
    def summarize_with_claude(self, text: str, summary_type: str = "concise") -> str:
        """Summarize text using Claude model."""
        prompts = {
            "concise": f"Provide a concise summary of the following document:\n\n{text}",
            "detailed": f"Provide a detailed summary with key points of the following document:\n\n{text}",
            "bullet": f"Summarize the following document in bullet points:\n\n{text}"
        }
        
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": prompts.get(summary_type, prompts["concise"])
                }
            ]
        }
        
        try:
            response = self.bedrock.invoke_model(
                modelId='anthropic.claude-3-sonnet-20240229-v1:0',
                body=json.dumps(body)
            )
            
            result = json.loads(response['body'].read())
            return result['content'][0]['text']
        except Exception as e:
            logger.error(f"Error with Claude model: {e}")
            return f"Error: {e}"
    
    def summarize_with_titan(self, text: str, summary_type: str = "concise") -> str:
        """Summarize text using Amazon Titan model."""
        prompts = {
            "concise": f"Summarize this document concisely:\n\n{text}",
            "detailed": f"Provide a comprehensive summary of this document:\n\n{text}",
            "bullet": f"Create a bullet-point summary of this document:\n\n{text}"
        }
        
        body = {
            "inputText": prompts.get(summary_type, prompts["concise"]),
            "textGenerationConfig": {
                "maxTokenCount": 1000,
                "temperature": 0.3,
                "topP": 0.9
            }
        }
        
        try:
            response = self.bedrock.invoke_model(
                modelId='amazon.titan-text-express-v1',
                body=json.dumps(body)
            )
            
            result = json.loads(response['body'].read())
            return result['results'][0]['outputText']
        except Exception as e:
            logger.error(f"Error with Titan model: {e}")
            return f"Error: {e}"
    
    def summarize_with_llama(self, text: str, summary_type: str = "concise") -> str:
        """Summarize text using Meta Llama model."""
        prompts = {
            "concise": f"<s>[INST] Provide a concise summary of this document: {text} [/INST]",
            "detailed": f"<s>[INST] Provide a detailed summary with main points of this document: {text} [/INST]",
            "bullet": f"<s>[INST] Create a bullet-point summary of this document: {text} [/INST]"
        }
        
        body = {
            "prompt": prompts.get(summary_type, prompts["concise"]),
            "max_gen_len": 1000,
            "temperature": 0.3,
            "top_p": 0.9
        }
        
        try:
            response = self.bedrock.invoke_model(
                modelId='meta.llama2-70b-chat-v1',
                body=json.dumps(body)
            )
            
            result = json.loads(response['body'].read())
            return result['generation']
        except Exception as e:
            logger.error(f"Error with Llama model: {e}")
            return f"Error: {e}"
    
    def batch_summarize(self, documents: list, model: str = "claude", summary_type: str = "concise") -> Dict[str, str]:
        """Summarize multiple documents."""
        results = {}
        
        for doc_path in documents:
            if not Path(doc_path).exists():
                logger.warning(f"Document not found: {doc_path}")
                continue
                
            content = self.read_document(doc_path)
            if not content:
                continue
                
            logger.info(f"Summarizing: {doc_path}")
            
            if model.lower() == "claude":
                summary = self.summarize_with_claude(content, summary_type)
            elif model.lower() == "titan":
                summary = self.summarize_with_titan(content, summary_type)
            elif model.lower() == "llama":
                summary = self.summarize_with_llama(content, summary_type)
            else:
                logger.error(f"Unsupported model: {model}")
                continue
                
            results[doc_path] = summary
            
        return results
    
    def compare_models(self, text: str, summary_type: str = "concise") -> Dict[str, str]:
        """Compare summaries from different models."""
        results = {}
        
        models = {
            "Claude": self.summarize_with_claude,
            "Titan": self.summarize_with_titan,
            "Llama": self.summarize_with_llama
        }
        
        for model_name, summarize_func in models.items():
            logger.info(f"Getting summary from {model_name}")
            results[model_name] = summarize_func(text, summary_type)
            
        return results

def main():
    """Main function to run the document summarizer."""
    parser = argparse.ArgumentParser(description="Test Bedrock LLM for document summarization")
    parser.add_argument("--file", "-f", help="Path to document file")
    parser.add_argument("--model", "-m", choices=["claude", "titan", "llama"], 
                       default="claude", help="Model to use for summarization")
    parser.add_argument("--type", "-t", choices=["concise", "detailed", "bullet"], 
                       default="concise", help="Type of summary")
    parser.add_argument("--region", "-r", default="us-east-1", help="AWS region")
    parser.add_argument("--batch", "-b", nargs="+", help="Multiple files for batch processing")
    parser.add_argument("--compare", "-c", action="store_true", help="Compare all models")
    parser.add_argument("--text", help="Direct text input for summarization")
    
    args = parser.parse_args()
    
    # Initialize summarizer
    summarizer = BedrockDocumentSummarizer(region=args.region)
    
    # Handle different input modes
    if args.text:
        # Direct text input
        if args.compare:
            results = summarizer.compare_models(args.text, args.type)
            for model, summary in results.items():
                print(f"\n{'='*50}")
                print(f"SUMMARY FROM {model.upper()}")
                print(f"{'='*50}")
                print(summary)
        else:
            if args.model == "claude":
                summary = summarizer.summarize_with_claude(args.text, args.type)
            elif args.model == "titan":
                summary = summarizer.summarize_with_titan(args.text, args.type)
            elif args.model == "llama":
                summary = summarizer.summarize_with_llama(args.text, args.type)
            
            print(f"\nSUMMARY ({args.model.upper()}):")
            print("="*50)
            print(summary)
    
    elif args.batch:
        # Batch processing
        results = summarizer.batch_summarize(args.batch, args.model, args.type)
        for doc_path, summary in results.items():
            print(f"\n{'='*50}")
            print(f"SUMMARY FOR: {doc_path}")
            print(f"{'='*50}")
            print(summary)
    
    elif args.file:
        # Single file processing
        content = summarizer.read_document(args.file)
        if not content:
            print("Failed to read document")
            return
        
        if args.compare:
            results = summarizer.compare_models(content, args.type)
            for model, summary in results.items():
                print(f"\n{'='*50}")
                print(f"SUMMARY FROM {model.upper()}")
                print(f"{'='*50}")
                print(summary)
        else:
            if args.model == "claude":
                summary = summarizer.summarize_with_claude(content, args.type)
            elif args.model == "titan":
                summary = summarizer.summarize_with_titan(content, args.type)
            elif args.model == "llama":
                summary = summarizer.summarize_with_llama(content, args.type)
            
            print(f"\nSUMMARY ({args.model.upper()}):")
            print("="*50)
            print(summary)
    
    else:
        # Interactive mode
        print("Bedrock Document Summarizer - Interactive Mode")
        print("Enter text to summarize (type 'quit' to exit):")
        
        while True:
            text = input("\nEnter text: ")
            if text.lower() == 'quit':
                break
                
            summary = summarizer.summarize_with_claude(text, "concise")
            print(f"\nSUMMARY:")
            print("="*30)
            print(summary)

if __name__ == "__main__":
    main()