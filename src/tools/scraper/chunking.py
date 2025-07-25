"""
Chunking utilities for grouping text content based on token budgets.
"""

import logging
from typing import List, Dict, Optional
import tiktoken


class TextChunker:
    """
    Utility for chunking text content based on token budgets using OpenAI's tiktoken.
    """
    
    def __init__(self, model_name: str = "text-embedding-3-small"):
        """
        Initialize the chunker with a specific OpenAI model.
        
        Args:
            model_name: Name of the OpenAI model to use for tokenization
        """
        self.logger = logging.getLogger(__name__)
        try:
            self.encoding = tiktoken.encoding_for_model(model_name)
            self.model_name = model_name
        except Exception as e:
            self.logger.warning(f"Failed to load tiktoken for model {model_name}: {e}")
            # Fallback to a simple character-based approach
            self.encoding = None
            self.model_name = "simple"
    
    def count_tokens(self, text: str) -> int:
        """
        Count tokens in text using tiktoken.
        
        Args:
            text: Text to count tokens for
            
        Returns:
            Number of tokens
        """
        if self.encoding is None:
            # Fallback: approximate tokens as characters / 4
            return len(text) // 4
        
        try:
            return len(self.encoding.encode(text))
        except Exception as e:
            self.logger.warning(f"Token counting failed: {e}")
            return len(text) // 4
    
    def chunk_paragraphs(self, paragraphs: List[str], max_tokens: int = 512) -> List[str]:
        """
        Group paragraphs into chunks based on token budget.
        
        Args:
            paragraphs: List of paragraphs to chunk
            max_tokens: Maximum tokens per chunk
            
        Returns:
            List of text chunks
        """
        if not paragraphs:
            return []
        
        chunks = []
        current_chunk = []
        current_tokens = 0
        
        for paragraph in paragraphs:
            # Skip empty paragraphs
            if not paragraph.strip():
                continue
                
            paragraph_tokens = self.count_tokens(paragraph)
            
            # If adding this paragraph would exceed the limit, start a new chunk
            if current_tokens + paragraph_tokens > max_tokens and current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = [paragraph]
                current_tokens = paragraph_tokens
            else:
                current_chunk.append(paragraph)
                current_tokens += paragraph_tokens
        
        # Add the last chunk if it has content
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks
    
    def chunk_text(self, text: str, max_tokens: int = 512) -> List[str]:
        """
        Chunk a single text string into smaller pieces.
        
        Args:
            text: Text to chunk
            max_tokens: Maximum tokens per chunk
            
        Returns:
            List of text chunks
        """
        if not text:
            return []
        
        # Simple approach: split by sentences and then group
        import re
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        chunks = []
        current_chunk = []
        current_tokens = 0
        
        for sentence in sentences:
            sentence_tokens = self.count_tokens(sentence)
            
            if current_tokens + sentence_tokens > max_tokens and current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = [sentence]
                current_tokens = sentence_tokens
            else:
                current_chunk.append(sentence)
                current_tokens += sentence_tokens
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks


# Global chunker instances for different models
_chunkers = {}


def get_chunker(model_name: str = "text-embedding-3-small") -> TextChunker:
    """
    Get a chunker instance for the specified model.
    
    Args:
        model_name: Name of the OpenAI model
        
    Returns:
        TextChunker instance
    """
    global _chunkers
    if model_name not in _chunkers:
        _chunkers[model_name] = TextChunker(model_name)
    return _chunkers[model_name]


def chunk_paragraphs(paragraphs: List[str], max_tokens: int = 512, 
                    model_name: str = "text-embedding-3-small") -> List[str]:
    """
    Convenience function to chunk paragraphs.
    
    Args:
        paragraphs: List of paragraphs to chunk
        max_tokens: Maximum tokens per chunk
        model_name: Name of the OpenAI model
        
    Returns:
        List of text chunks
    """
    chunker = get_chunker(model_name)
    return chunker.chunk_paragraphs(paragraphs, max_tokens)


def chunk_text(text: str, max_tokens: int = 512, 
               model_name: str = "text-embedding-3-small") -> List[str]:
    """
    Convenience function to chunk text.
    
    Args:
        text: Text to chunk
        max_tokens: Maximum tokens per chunk
        model_name: Name of the OpenAI model
        
    Returns:
        List of text chunks
    """
    chunker = get_chunker(model_name)
    return chunker.chunk_text(text, max_tokens) 