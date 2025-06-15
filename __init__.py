# app/__init__.py
"""LLM Search Backend Application"""

__version__ = "1.0.0"
__author__ = "Your Name"
__description__ = "AI-powered search backend with intelligent content analysis"

# app/config/__init__.py
"""Configuration module"""

from .settings import settings

__all__ = ["settings"]

# app/core/__init__.py
"""Core application logic"""

from .pipeline import SearchPipeline
from .exceptions import (
    PipelineException,
    QueryEnhancementException,
    SearchEngineException,
    ContentFetchException,
    LLMAnalysisException,
    CacheException,
    RateLimitException,
    ValidationException,
    ServiceUnavailableException
)

__all__ = [
    "SearchPipeline",
    "PipelineException",
    "QueryEnhancementException", 
    "SearchEngineException",
    "ContentFetchException",
    "LLMAnalysisException",
    "CacheException",
    "RateLimitException",
    "ValidationException",
    "ServiceUnavailableException"
]

# app/services/__init__.py
"""Service layer modules"""

from .query_enhancer import QueryEnhancementService
from .search_engine import MultiSearchEngine
from .content_fetcher import ZenRowsContentFetcher
from .llm_analyzer import LLMAnalysisService
from .cache_service import CacheService
from .cost_tracker import CostTracker

__all__ = [
    "QueryEnhancementService",
    "MultiSearchEngine", 
    "ZenRowsContentFetcher",
    "LLMAnalysisService",
    "CacheService",
    "CostTracker"
]

# app/models/__init__.py
"""Data models"""

from .requests import SearchRequest
from .responses import SearchResponse, HealthResponse, ErrorResponse
from .internal import (
    ContentSource,
    SearchResult,
    ContentData,
    QueryEnhancement
)

__all__ = [
    "SearchRequest",
    "SearchResponse",
    "HealthResponse", 
    "ErrorResponse",
    "ContentSource",
    "SearchResult",
    "ContentData",
    "QueryEnhancement"
]

# app/api/__init__.py
"""API layer"""

# app/api/endpoints/__init__.py
"""API endpoints"""

from . import search, health

__all__ = ["search", "health"]

# app/utils/__init__.py
"""Utility functions"""

# scripts/check_api_keys.py
"""Script to validate API keys"""

import asyncio
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

async def check_brave_api():
    """Test Brave Search API"""
    api_key = os.getenv("BRAVE_SEARCH_API_KEY")
    if not api_key:
        return False, "API key not found"
    
    try:
        async with aiohttp.ClientSession() as session:
            url = "https://api.search.brave.com/res/v1/web/search"
            headers = {
                "Accept": "application/json",
                "X-Subscription-Token": api_key
            }
            params = {"q": "test", "count": 1}
            
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    return True, "OK"
                else:
                    return False, f"HTTP {response.status}"
    except Exception as e:
        return False, str(e)

async def check_bing_api():
    """Test Bing Search API"""
    api_key = os.getenv("BING_SEARCH_API_KEY")
    if not api_key:
        return False, "API key not found"
    
    try:
        async with aiohttp.ClientSession() as session:
            url = "https://api.bing.microsoft.com/v7.0/search"
            headers = {"Ocp-Apim-Subscription-Key": api_key}
            params = {"q": "test", "count": 1}
            
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    return True, "OK"
                else:
                    return False, f"HTTP {response.status}"
    except Exception as e:
        return False, str(e)

async def check_zenrows_api():
    """Test ZenRows API"""
    api_key = os.getenv("ZENROWS_API_KEY")
    if not api_key:
        return False, "API key not found"
    
    try:
        async with aiohttp.ClientSession() as session:
            url = "https://api.zenrows.com/v1/"
            params = {
                "url": "https://httpbin.org/html",
                "apikey": api_key
            }
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    return True, "OK"
                else:
                    return False, f"HTTP {response.status}"
    except Exception as e:
        return False, str(e)

async def check_ollama():
    """Test Ollama connection"""
    ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{ollama_host}/api/tags") as response:
                if response.status == 200:
                    data = await response.json()
                    models = [model["name"] for model in data.get("models", [])]
                    return True, f"Available models: {models}"
                else:
                    return False, f"HTTP {response.status}"
    except Exception as e:
        return False, str(e)

async def main():
    """Check all API connections"""
    print("🔍 Checking API Keys and Connections...\n")
    
    checks = [
        ("Brave Search API", check_brave_api()),
        ("Bing Search API", check_bing_api()),
        ("ZenRows API", check_zenrows_api()),
        ("Ollama Service", check_ollama())
    ]
    
    results = await asyncio.gather(*[check[1] for check in checks])
    
    for i, (name, _) in enumerate(checks):
        success, message = results[i]
        status = "✅" if success else "❌"
        print(f"{status} {name}: {message}")
    
    all_good = all(result[0] for result in results)
    
    print(f"\n{'🎉 All APIs are working!' if all_good else '⚠️  Some APIs need attention'}")
    
    if not all_good:
        print("\n💡 Tips:")
        print("- Check your .env file for correct API keys")
        print("- Ensure Ollama is running: ollama serve")
        print("- Pull required model: ollama pull llama2:7b")

if __name__ == "__main__":
    asyncio.run(main())

# scripts/setup_ollama.py
"""Script to setup Ollama and download models"""

import subprocess
import sys
import time
import requests

def run_command(command, description):
    """Run a shell command"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def check_ollama_running():
    """Check if Ollama service is running"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    """Setup Ollama and download models"""
    print("🚀 Setting up Ollama for LLM Search Backend\n")
    
    # Check if Ollama is already installed
    if run_command("ollama --version", "Checking Ollama installation"):
        print("✅ Ollama is already installed")
    else:
        print("📥 Installing Ollama...")
        if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
            if not run_command("curl -fsSL https://ollama.ai/install.sh | sh", "Installing Ollama"):
                print("❌ Failed to install Ollama")
                return
        else:
            print("🪟 On Windows, please download Ollama from https://ollama.ai/download")
            return
    
    # Start Ollama service
    if not check_ollama_running():
        print("🔄 Starting Ollama service...")
        # Start Ollama in background
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Wait for service to start
        for i in range(30):  # Wait up to 30 seconds
            if check_ollama_running():
                print("✅ Ollama service started")
                break
            time.sleep(1)
        else:
            print("❌ Failed to start Ollama service")
            return
    else:
        print("✅ Ollama service is already running")
    
    # Download required models
    models_to_download = [
        "llama2:7b",  # Default model
        # "mistral:7b",  # Alternative model
        # "codellama:7b"  # Code-focused model
    ]
    
    for model in models_to_download:
        if run_command(f"ollama pull {model}", f"Downloading {model}"):
            print(f"✅ Model {model} downloaded successfully")
        else:
            print(f"❌ Failed to download {model}")
    
    # List available models
    if run_command("ollama list", "Listing available models"):
        pass
    
    print("\n🎉 Ollama setup completed!")
    print("💡 You can now start the search backend with: make dev")

if __name__ == "__main__":
    main()
