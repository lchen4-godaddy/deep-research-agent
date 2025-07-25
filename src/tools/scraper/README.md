# Web Scraping Tools

This directory contains modular web scraping tools with chunking capabilities.

## File Structure

### Core Scrapers
- **`simple_scraper.py`**: Original bulk URL scraper
- **`page_scraper.py`**: Individual page scraper with enhanced content extraction

### Chunking Utilities
- **`chunking.py`**: Text chunking utilities with OpenAI tiktoken
- **`chunked_scraper.py`**: Combined scraping and chunking functionality

## Usage Examples

### Basic Page Scraping
```python
from src.tools.scraper.page_scraper import scrape_single_page

# Scrape a single page
result = await scrape_single_page("https://example.com")
print(f"Title: {result['title']}")
print(f"Content: {result['content'][:200]}...")
print(f"Paragraphs: {result['paragraph_count']}")
```

### Text Chunking
```python
from src.tools.scraper.chunking import chunk_paragraphs, chunk_text

# Chunk paragraphs
paragraphs = ["Paragraph 1...", "Paragraph 2...", "Paragraph 3..."]
chunks = chunk_paragraphs(paragraphs, max_tokens=512)

# Chunk text
text = "Long text content..."
chunks = chunk_text(text, max_tokens=512)
```

### Combined Scraping and Chunking
```python
from src.tools.scraper.chunked_scraper import scrape_and_chunk_page

# Scrape and chunk in one step
result = await scrape_and_chunk_page("https://example.com", max_tokens=512)
print(f"Chunks: {result['chunk_count']}")
print(f"First chunk: {result['chunked_paragraphs'][0]}")
```

### Multiple Pages with Analysis
```python
from src.tools.scraper.chunked_scraper import scrape_and_chunk_multiple_pages, scrape_with_analysis

# Scrape multiple pages
urls = ["https://example1.com", "https://example2.com"]
results = await scrape_and_chunk_multiple_pages(urls, max_tokens=512)

# Scrape with analysis
result = await scrape_with_analysis("https://example.com", max_tokens=512)
analysis = result['analysis']
print(f"Average chunk length: {analysis['avg_chunk_length']}")
```

## Features

### Page Scraper
- ✅ **Enhanced content extraction** with fast lxml HTML parsing
- ✅ **Paragraph extraction** for structured content
- ✅ **Error handling** for network issues and invalid URLs
- ✅ **Async support** for concurrent scraping

### Chunking Utilities
- ✅ **Token-based chunking** using OpenAI's tiktoken
- ✅ **Multiple model support** (text-embedding-3-small, text-embedding-3-large, etc.)
- ✅ **Fallback mechanism** for when tiktoken isn't available
- ✅ **Flexible chunk sizes** based on token budgets

### Combined Functionality
- ✅ **One-step scraping and chunking**
- ✅ **Multiple page processing** with concurrent execution
- ✅ **Analysis and statistics** for chunk quality
- ✅ **Error resilience** with graceful failure handling

## Configuration

### OpenAI Models
The chunking utilities support various OpenAI models:
- `text-embedding-3-small` (default)
- `text-embedding-3-large`
- `gpt-4`
- `gpt-3.5-turbo`
- Any model supported by tiktoken

### Chunk Sizes
- **Small chunks** (256 tokens): Good for precise analysis
- **Medium chunks** (512 tokens): Balanced for most use cases
- **Large chunks** (1024 tokens): Good for context preservation

## Error Handling

All scrapers handle common errors gracefully:
- **Network timeouts**: Retry with exponential backoff
- **Invalid URLs**: Return error status with details
- **Missing content**: Provide empty results with error messages
- **Tiktoken failures**: Fall back to character-based chunking

## Performance

- **Concurrent scraping**: Multiple pages processed simultaneously
- **Efficient parsing**: Fast HTML parsing with BeautifulSoup + lxml
- **Memory management**: Content length limits to prevent memory issues
- **Caching**: Global instances for encodings and scrapers 