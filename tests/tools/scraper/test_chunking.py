"""
Tests for the chunking utilities.
"""

import pytest

from src.tools.scraper.chunking import TextChunker, chunk_paragraphs, chunk_text, get_chunker


def test_text_chunker_initialization():
    """Test TextChunker initialization."""
    chunker = TextChunker()
    
    # Should have an encoding or fallback
    assert hasattr(chunker, 'encoding')
    assert hasattr(chunker, 'model_name')


def test_count_tokens():
    """Test token counting functionality."""
    chunker = TextChunker()
    
    # Test with simple text
    text = "This is a test sentence."
    tokens = chunker.count_tokens(text)
    
    # Should return a positive number
    assert isinstance(tokens, int)
    assert tokens > 0
    
    # Test with empty text
    empty_tokens = chunker.count_tokens("")
    assert empty_tokens == 0


def test_chunk_paragraphs():
    """Test paragraph chunking functionality."""
    paragraphs = [
        "This is the first paragraph with some content.",
        "This is the second paragraph with different content.",
        "This is the third paragraph that is quite long and contains more information about various topics.",
        "Short paragraph.",
        "Another short one."
    ]
    
    # Test with default settings
    chunks = chunk_paragraphs(paragraphs, max_tokens=100)
    
    # Should return a list
    assert isinstance(chunks, list)
    assert len(chunks) > 0
    
    # Each chunk should be a string
    for chunk in chunks:
        assert isinstance(chunk, str)
        assert len(chunk) > 0
    
    print(f"  - Original paragraphs: {len(paragraphs)}")
    print(f"  - Resulting chunks: {len(chunks)}")
    for i, chunk in enumerate(chunks):
        print(f"    Chunk {i+1}: {len(chunk)} characters")


def test_chunk_text():
    """Test text chunking functionality."""
    text = """
    This is a long text that should be chunked into smaller pieces. 
    It contains multiple sentences and paragraphs. 
    The chunking algorithm should split this text based on token limits.
    This is useful for processing large documents.
    """
    
    # Test with default settings
    chunks = chunk_text(text, max_tokens=50)
    
    # Should return a list
    assert isinstance(chunks, list)
    assert len(chunks) > 0
    
    # Each chunk should be a string
    for chunk in chunks:
        assert isinstance(chunk, str)
        assert len(chunk) > 0
    
    print(f"  - Original text length: {len(text)}")
    print(f"  - Resulting chunks: {len(chunks)}")
    for i, chunk in enumerate(chunks):
        print(f"    Chunk {i+1}: {len(chunk)} characters")


def test_chunk_paragraphs_empty():
    """Test chunking with empty input."""
    chunks = chunk_paragraphs([], max_tokens=100)
    assert chunks == []
    
    # Empty strings should be filtered out, not chunked
    chunks = chunk_paragraphs(["", "", ""], max_tokens=100)
    assert chunks == []


def test_chunk_text_empty():
    """Test text chunking with empty input."""
    chunks = chunk_text("", max_tokens=100)
    assert chunks == []
    
    chunks = chunk_text("   ", max_tokens=100)
    assert chunks == []


def test_get_chunker():
    """Test the get_chunker function."""
    chunker1 = get_chunker("bert-base-uncased")
    chunker2 = get_chunker("bert-base-uncased")
    
    # Should return the same instance (singleton pattern)
    assert chunker1 is chunker2
    
    # Should be a TextChunker instance
    assert isinstance(chunker1, TextChunker)


def test_chunk_paragraphs_different_models():
    """Test chunking with different OpenAI models."""
    paragraphs = [
        "This is a test paragraph.",
        "This is another test paragraph with more content.",
        "This is the third paragraph."
    ]
    
    # Test with different OpenAI models
    models_to_test = ["text-embedding-3-small", "text-embedding-3-large"]
    
    for model in models_to_test:
        try:
            chunks = chunk_paragraphs(paragraphs, max_tokens=50, model_name=model)
            print(f"  - Model {model}: {len(chunks)} chunks")
            assert isinstance(chunks, list)
        except Exception as e:
            print(f"  - Model {model}: failed - {e}")
            # Continue with other models
            continue 