# Detective 🕵️

**Domain:** Intelligence  
**Description:** Searches the web for facts and news related to a specific keyword or event.

## Overview

The Detective module is the intelligence-gathering component of Project Longshot. It performs web searches using multiple backends (DuckDuckGo, Google) with automatic fallback and retry logic.

## Features

- **Multi-backend search**: Uses DuckDuckGo as primary, Google as fallback
- **Automatic retry**: Handles rate limiting and temporary failures
- **Simulation mode**: Provides mock data when network is unavailable
- **Structured results**: Returns consistent data format for downstream processing

## Usage

### As a Module

```python
from src.detective import Detective

detective = Detective()
clues = detective.investigate("semiconductor shortage 2024", max_results=5)

for clue in clues:
    print(f"Title: {clue['title']}")
    print(f"Link: {clue['link']}")
    print(f"Snippet: {clue['snippet']}")
```

### From Command Line

```bash
python -m src.detective.detective "your search query"
```

## Prerequisites

```bash
pip install duckduckgo-search googlesearch-python
```

## Output Format

Each result contains:
- `title`: The title of the search result
- `link`: URL to the source
- `snippet`: Brief description/excerpt
- `timestamp`: When the search was performed

## Configuration

The Detective uses the following configuration options from `config.py`:
- `DETECTIVE_MAX_RESULTS`: Maximum results to return (default: 5)
- `DETECTIVE_RETRY_ATTEMPTS`: Number of retry attempts (default: 3)

## Notes

- Uses anonymous search to avoid tracking
- Respects rate limits with exponential backoff
- Network-blocked environments will receive simulated results
- Results should be verified using the Truth Serum module
