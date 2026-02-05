# Detective 🕵️

**Domain:** Intelligence
**Description:** Searches the web for facts and news related to a specific keyword or event.

## Usage

The Detective module is a Python script that uses the `duckduckgo-search` library to find information.

### Prerequisites

```bash
pip install -r requirements.txt
```

### Running the Detective

You can run the detective from the command line:

```bash
python detective.py "your query here"
```

Example:

```bash
python detective.py "latest advancements in quantum computing"
```

### Code Structure

- `detective.py`: Main class `Detective` with `investigate(query)` method.

## Notes

- The module uses `duckduckgo_search` (or `ddgs`) to perform anonymous searches.
- If you encounter "No results" or timeouts, check your internet connection or try again later as you might be rate-limited.
