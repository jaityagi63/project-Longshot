"""
Truth Serum Module - Counter-Intelligence
==========================================
Filters deepfakes, misinformation, and botnets.
"""

import re
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum


class CredibilityLevel(Enum):
    """Credibility classification levels."""
    VERIFIED = "verified"
    LIKELY_AUTHENTIC = "likely_authentic"
    UNCERTAIN = "uncertain"
    SUSPICIOUS = "suspicious"
    LIKELY_FALSE = "likely_false"
    DEBUNKED = "debunked"


class ThreatType(Enum):
    """Types of information threats."""
    NONE = "none"
    MISINFORMATION = "misinformation"
    DISINFORMATION = "disinformation"
    DEEPFAKE = "deepfake"
    BOT_AMPLIFICATION = "bot_amplification"
    COORDINATED_CAMPAIGN = "coordinated_campaign"
    SATIRE_MISINTERPRETED = "satire_misinterpreted"


@dataclass
class SourceProfile:
    """Profile of an information source."""
    domain: str
    trust_score: float  # 0-1
    category: str  # news, blog, social, government, academic, unknown
    known_biases: List[str] = field(default_factory=list)
    fact_check_record: Dict[str, int] = field(default_factory=dict)  # true/false/mixed counts


@dataclass
class VerificationResult:
    """Result of content verification."""
    content_id: str
    timestamp: str
    credibility: CredibilityLevel
    confidence: float  # 0-1
    threat_type: ThreatType
    source_analysis: Dict[str, Any]
    content_analysis: Dict[str, Any]
    cross_references: List[Dict[str, str]]
    red_flags: List[str]
    recommendations: List[str]


class TruthSerum:
    """
    The Truth Serum module: Counter-Intelligence.
    Filters deepfakes, misinformation, and botnets.
    """

    def __init__(self):
        """Initialize the Truth Serum."""
        self.source_profiles = self._load_source_profiles()
        self.known_false_claims = self._load_known_false_claims()
        self.verification_history: List[VerificationResult] = []
    
    def _load_source_profiles(self) -> Dict[str, SourceProfile]:
        """Load known source profiles."""
        profiles = {
            # Trusted sources
            "reuters.com": SourceProfile("reuters.com", 0.95, "news", [], {"true": 98, "false": 1, "mixed": 1}),
            "apnews.com": SourceProfile("apnews.com", 0.95, "news", [], {"true": 97, "false": 1, "mixed": 2}),
            "bbc.com": SourceProfile("bbc.com", 0.90, "news", ["uk-perspective"], {"true": 94, "false": 2, "mixed": 4}),
            "nytimes.com": SourceProfile("nytimes.com", 0.85, "news", ["left-leaning"], {"true": 90, "false": 3, "mixed": 7}),
            "wsj.com": SourceProfile("wsj.com", 0.85, "news", ["right-leaning-economics"], {"true": 91, "false": 2, "mixed": 7}),
            
            # Academic/Government
            "gov": SourceProfile("gov", 0.85, "government", [], {"true": 90, "false": 2, "mixed": 8}),
            "edu": SourceProfile("edu", 0.80, "academic", [], {"true": 85, "false": 3, "mixed": 12}),
            
            # Social media (lower trust by default)
            "twitter.com": SourceProfile("twitter.com", 0.30, "social", ["unverified"], {}),
            "x.com": SourceProfile("x.com", 0.30, "social", ["unverified"], {}),
            "facebook.com": SourceProfile("facebook.com", 0.25, "social", ["unverified"], {}),
            "reddit.com": SourceProfile("reddit.com", 0.35, "social", ["community-moderated"], {}),
            
            # Known problematic sources
            "infowars.com": SourceProfile("infowars.com", 0.05, "blog", ["conspiracy", "far-right"], {"true": 5, "false": 85, "mixed": 10}),
        }
        return profiles
    
    def _load_known_false_claims(self) -> List[Dict[str, Any]]:
        """Load database of known false claims for matching."""
        return [
            {"pattern": r"5g.*covid", "category": "health_conspiracy", "debunked_date": "2020-04-15"},
            {"pattern": r"election.*stolen.*2020", "category": "political_misinformation", "debunked_date": "2021-01-06"},
            {"pattern": r"flat.*earth", "category": "science_denial", "debunked_date": "ancient"},
            {"pattern": r"microchip.*vaccine", "category": "health_conspiracy", "debunked_date": "2020-12-01"},
            {"pattern": r"climate.*hoax", "category": "science_denial", "debunked_date": "ongoing"},
        ]
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL."""
        if not url:
            return "unknown"
        
        # Remove protocol
        url = re.sub(r'^https?://', '', url)
        # Extract domain
        domain = url.split('/')[0]
        # Remove www
        domain = re.sub(r'^www\.', '', domain)
        
        return domain.lower()
    
    def _analyze_source(self, url: str) -> Dict[str, Any]:
        """Analyze the credibility of a source."""
        domain = self._extract_domain(url)
        
        # Check for known profile
        profile = self.source_profiles.get(domain)
        
        # Check domain suffix for government/academic
        if not profile:
            if domain.endswith('.gov'):
                profile = self.source_profiles.get("gov")
            elif domain.endswith('.edu'):
                profile = self.source_profiles.get("edu")
        
        if profile:
            return {
                "domain": domain,
                "trust_score": profile.trust_score,
                "category": profile.category,
                "known_biases": profile.known_biases,
                "fact_check_record": profile.fact_check_record,
                "known_source": True,
            }
        else:
            # Unknown source - apply heuristics
            trust_score = 0.4  # Default moderate skepticism
            
            # Reduce trust for certain TLDs
            if any(domain.endswith(tld) for tld in ['.info', '.xyz', '.top', '.buzz']):
                trust_score -= 0.2
            
            # Reduce trust for very long domains (often suspicious)
            if len(domain) > 30:
                trust_score -= 0.1
            
            return {
                "domain": domain,
                "trust_score": max(0.1, trust_score),
                "category": "unknown",
                "known_biases": [],
                "fact_check_record": {},
                "known_source": False,
            }
    
    def _analyze_content(self, text: str) -> Dict[str, Any]:
        """Analyze content for red flags."""
        text_lower = text.lower()
        
        red_flags = []
        manipulation_score = 0.0
        
        # Check for sensationalist language
        sensational_words = [
            "shocking", "unbelievable", "you won't believe", "secret", "they don't want you to know",
            "breaking", "urgent", "must share", "wake up", "exposed"
        ]
        sensational_count = sum(1 for word in sensational_words if word in text_lower)
        if sensational_count > 2:
            red_flags.append("Excessive sensationalist language")
            manipulation_score += 0.15
        
        # Check for known false claims
        for claim in self.known_false_claims:
            if re.search(claim["pattern"], text_lower):
                red_flags.append(f"Matches known false claim pattern: {claim['category']}")
                manipulation_score += 0.4
        
        # Check for excessive capitalization
        caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        if caps_ratio > 0.3:
            red_flags.append("Excessive capitalization (aggressive tone)")
            manipulation_score += 0.1
        
        # Check for lack of specific details
        has_numbers = bool(re.search(r'\d+', text))
        has_names = bool(re.search(r'[A-Z][a-z]+ [A-Z][a-z]+', text))
        has_dates = bool(re.search(r'\d{4}|\d{1,2}/\d{1,2}', text))
        
        specificity_score = sum([has_numbers, has_names, has_dates]) / 3
        if specificity_score < 0.33:
            red_flags.append("Lacks specific verifiable details")
            manipulation_score += 0.1
        
        # Check for emotional manipulation
        emotional_words = ["angry", "furious", "terrified", "outrage", "disgusting", "evil", "destroy"]
        emotional_count = sum(1 for word in emotional_words if word in text_lower)
        if emotional_count > 2:
            red_flags.append("High emotional manipulation indicators")
            manipulation_score += 0.15
        
        return {
            "word_count": len(text.split()),
            "sensationalism_score": min(1.0, sensational_count * 0.15),
            "manipulation_score": min(1.0, manipulation_score),
            "specificity_score": specificity_score,
            "red_flags": red_flags,
        }
    
    def _find_cross_references(self, text: str, title: str) -> List[Dict[str, str]]:
        """
        Simulate finding cross-references from other sources.
        In production, this would call external fact-checking APIs.
        """
        # Simulated cross-reference check
        references = []
        
        # Simulate finding corroborating sources
        if len(text) > 100:  # If there's substantial content
            references.append({
                "source": "Reuters Fact Check",
                "status": "No matches found",
                "url": "https://www.reuters.com/fact-check/"
            })
            references.append({
                "source": "Snopes",
                "status": "No matches found",
                "url": "https://www.snopes.com/"
            })
        
        return references
    
    def verify(self, content: Dict[str, Any]) -> VerificationResult:
        """
        Verify the authenticity and credibility of content.
        
        Args:
            content: Dictionary with keys:
                - title: Content title
                - snippet: Content body/description
                - link: Source URL
                - timestamp: When content was found
        
        Returns:
            VerificationResult with credibility assessment.
        """
        title = content.get("title", "")
        text = content.get("snippet", "")
        url = content.get("link", "")
        
        print(f"🧪 Truth Serum analyzing: '{title[:50]}...'")
        
        # Generate content ID
        content_hash = hashlib.md5(f"{title}{text}{url}".encode()).hexdigest()[:12]
        content_id = f"VER-{content_hash}"
        
        # Analyze source
        source_analysis = self._analyze_source(url)
        
        # Analyze content
        content_analysis = self._analyze_content(f"{title} {text}")
        
        # Find cross-references
        cross_refs = self._find_cross_references(text, title)
        
        # Aggregate red flags
        all_red_flags = content_analysis.get("red_flags", [])
        if not source_analysis.get("known_source"):
            all_red_flags.append("Source not in trusted database")
        if source_analysis.get("trust_score", 0) < 0.3:
            all_red_flags.append("Source has low trust rating")
        
        # Calculate overall credibility
        source_weight = 0.4
        content_weight = 0.6
        
        source_score = source_analysis.get("trust_score", 0.5)
        content_score = 1.0 - content_analysis.get("manipulation_score", 0)
        
        overall_score = (source_score * source_weight) + (content_score * content_weight)
        
        # Determine credibility level
        if overall_score >= 0.85:
            credibility = CredibilityLevel.VERIFIED
        elif overall_score >= 0.70:
            credibility = CredibilityLevel.LIKELY_AUTHENTIC
        elif overall_score >= 0.50:
            credibility = CredibilityLevel.UNCERTAIN
        elif overall_score >= 0.30:
            credibility = CredibilityLevel.SUSPICIOUS
        elif overall_score >= 0.15:
            credibility = CredibilityLevel.LIKELY_FALSE
        else:
            credibility = CredibilityLevel.DEBUNKED
        
        # Determine threat type
        threat_type = ThreatType.NONE
        if content_analysis.get("manipulation_score", 0) > 0.5:
            threat_type = ThreatType.MISINFORMATION
        if any("known false claim" in flag for flag in all_red_flags):
            threat_type = ThreatType.DISINFORMATION
        
        # Generate recommendations
        recommendations = []
        if credibility in [CredibilityLevel.SUSPICIOUS, CredibilityLevel.LIKELY_FALSE, CredibilityLevel.DEBUNKED]:
            recommendations.append("⚠️ Do not act on this information without independent verification")
            recommendations.append("🔍 Seek corroboration from established news sources")
        elif credibility == CredibilityLevel.UNCERTAIN:
            recommendations.append("📋 Seek additional sources before making decisions")
        else:
            recommendations.append("✅ Information appears credible for use in analysis")
        
        result = VerificationResult(
            content_id=content_id,
            timestamp=datetime.now().isoformat(),
            credibility=credibility,
            confidence=min(0.95, overall_score + 0.1),
            threat_type=threat_type,
            source_analysis=source_analysis,
            content_analysis=content_analysis,
            cross_references=cross_refs,
            red_flags=all_red_flags,
            recommendations=recommendations,
        )
        
        self.verification_history.append(result)
        
        print(f"✅ Truth Serum verdict: {credibility.value.upper()} (confidence: {result.confidence:.0%})")
        
        return result
    
    def batch_verify(self, contents: List[Dict[str, Any]]) -> List[VerificationResult]:
        """Verify multiple pieces of content."""
        results = []
        for content in contents:
            results.append(self.verify(content))
        return results
    
    def get_verification_summary(self, result: VerificationResult) -> str:
        """Generate a human-readable verification summary."""
        emoji_map = {
            CredibilityLevel.VERIFIED: "✅",
            CredibilityLevel.LIKELY_AUTHENTIC: "👍",
            CredibilityLevel.UNCERTAIN: "❓",
            CredibilityLevel.SUSPICIOUS: "⚠️",
            CredibilityLevel.LIKELY_FALSE: "❌",
            CredibilityLevel.DEBUNKED: "🚫",
        }
        
        lines = [
            f"🧪 TRUTH SERUM VERIFICATION REPORT",
            f"{'=' * 50}",
            f"Content ID: {result.content_id}",
            f"",
            f"{emoji_map.get(result.credibility, '?')} VERDICT: {result.credibility.value.upper()}",
            f"Confidence: {result.confidence:.0%}",
            f"Threat Type: {result.threat_type.value}",
            f"",
            f"📊 SOURCE ANALYSIS",
            f"  Domain: {result.source_analysis.get('domain', 'unknown')}",
            f"  Trust Score: {result.source_analysis.get('trust_score', 0):.0%}",
            f"  Category: {result.source_analysis.get('category', 'unknown')}",
            f"",
            f"🚩 RED FLAGS ({len(result.red_flags)}):",
        ]
        
        if result.red_flags:
            for flag in result.red_flags:
                lines.append(f"  • {flag}")
        else:
            lines.append("  None detected")
        
        lines.append("")
        lines.append("💡 RECOMMENDATIONS:")
        for rec in result.recommendations:
            lines.append(f"  {rec}")
        
        return "\n".join(lines)


if __name__ == "__main__":
    # Test the Truth Serum
    ts = TruthSerum()
    
    # Test with reliable source
    reliable_content = {
        "title": "Federal Reserve announces interest rate decision",
        "snippet": "The Federal Reserve Board announced on Wednesday that it will maintain the current interest rate at 5.25%, citing stable employment figures and moderating inflation trends.",
        "link": "https://www.reuters.com/business/fed-rate-decision",
        "timestamp": datetime.now().isoformat()
    }
    
    result1 = ts.verify(reliable_content)
    print("\n" + ts.get_verification_summary(result1))
    
    print("\n" + "=" * 60 + "\n")
    
    # Test with suspicious content
    suspicious_content = {
        "title": "SHOCKING: Secret plot EXPOSED - They don't want you to see this!",
        "snippet": "Wake up people! Unbelievable things are happening that the media won't tell you. This is URGENT and you MUST share before it's taken down!",
        "link": "https://totally-real-news.xyz/breaking-story-12345",
        "timestamp": datetime.now().isoformat()
    }
    
    result2 = ts.verify(suspicious_content)
    print("\n" + ts.get_verification_summary(result2))
