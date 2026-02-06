# Truth Serum 🧪

**Domain:** Counter-Intelligence  
**Description:** Filters deepfakes, misinformation, and botnets.

## Overview

The Truth Serum module verifies the authenticity and credibility of information. It analyzes sources, content patterns, and cross-references to detect misinformation.

## Features

- **Source Profiling**: Maintains trust scores for known domains
- **Content Analysis**: Detects sensationalism, manipulation patterns
- **False Claim Matching**: Checks against known debunked claims
- **Credibility Scoring**: Multi-factor credibility assessment
- **Threat Classification**: Identifies type of information threat

## Credibility Levels

- `verified` - Highly credible, trusted source
- `likely_authentic` - Appears genuine, minor concerns
- `uncertain` - Needs additional verification
- `suspicious` - Multiple red flags detected
- `likely_false` - Strong indicators of falsehood
- `debunked` - Matches known false information

## Threat Types

- `none` - No threats detected
- `misinformation` - Unintentionally false information
- `disinformation` - Deliberately false information
- `deepfake` - Synthetic media (future capability)
- `bot_amplification` - Artificial engagement (future capability)
- `coordinated_campaign` - Organized information operation

## Usage

```python
from src.truth_serum import TruthSerum

ts = TruthSerum()

content = {
    "title": "Breaking news about technology",
    "snippet": "Experts report new developments...",
    "link": "https://reuters.com/article",
    "timestamp": "2024-01-15T10:00:00"
}

result = ts.verify(content)

print(f"Credibility: {result.credibility.value}")
print(f"Confidence: {result.confidence:.0%}")
print(f"Red Flags: {result.red_flags}")
```

## Source Trust Database

Pre-configured trust scores for major sources:
- Reuters, AP News: 0.95 (highest trust)
- BBC, NYT, WSJ: 0.85-0.90
- .gov, .edu domains: 0.80-0.85
- Social media: 0.25-0.35
- Known problematic sources: < 0.10

## Red Flag Detection

The module detects:
- Sensationalist language ("SHOCKING", "URGENT", etc.)
- Excessive capitalization
- Known false claim patterns
- Emotional manipulation indicators
- Lack of specific verifiable details
- Unknown or suspicious domains
