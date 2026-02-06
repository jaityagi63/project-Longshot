"""
Market Analyzer Module - Company Impact Analysis
=================================================
Analyzes news to determine impact on specific companies,
calculating potential monetary gains or losses.
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum


class ImpactType(Enum):
    """Type of impact on a company."""
    POSITIVE = "positive"  # Gain
    NEGATIVE = "negative"  # Loss
    NEUTRAL = "neutral"
    MIXED = "mixed"


class Sector(Enum):
    """Industry sectors."""
    TECHNOLOGY = "Technology"
    FINANCE = "Finance"
    HEALTHCARE = "Healthcare"
    ENERGY = "Energy"
    RETAIL = "Retail"
    MANUFACTURING = "Manufacturing"
    AUTOMOTIVE = "Automotive"
    TELECOMMUNICATIONS = "Telecommunications"
    DEFENSE = "Defense"
    ENTERTAINMENT = "Entertainment"


@dataclass
class Company:
    """Represents a company in the market."""
    ticker: str
    name: str
    sector: Sector
    market_cap_billions: float
    stock_price: float
    daily_volume_millions: float
    keywords: List[str] = field(default_factory=list)
    competitors: List[str] = field(default_factory=list)
    suppliers: List[str] = field(default_factory=list)


@dataclass
class CompanyImpact:
    """Analysis of impact on a specific company."""
    company: Company
    impact_type: ImpactType
    relevance_score: float  # 0-1, how relevant the news is
    monetary_impact: float  # Positive = gain, Negative = loss
    percentage_change: float  # Expected stock price change
    reasoning: str
    related_keywords: List[str]
    confidence: float


@dataclass
class MarketAnalysis:
    """Complete market analysis from news."""
    news_summary: str
    timestamp: str
    sector_impacts: Dict[str, ImpactType]
    affected_companies: List[CompanyImpact]
    total_market_impact: float
    top_gainers: List[CompanyImpact]
    top_losers: List[CompanyImpact]
    market_sentiment: str  # "bullish", "bearish", "neutral"
    key_insights: List[str]


class MarketAnalyzer:
    """
    Analyzes news to determine company impacts and monetary effects.
    """

    def __init__(self):
        """Initialize the Market Analyzer with company database."""
        self.companies = self._load_companies()
        self.sector_keywords = self._load_sector_keywords()
        print("📈 Market Analyzer initialized with company database.")
    
    def _load_companies(self) -> List[Company]:
        """Load company database."""
        return [
            # Technology
            Company("AAPL", "Apple Inc.", Sector.TECHNOLOGY, 2800, 185.50, 65,
                   ["iphone", "apple", "ios", "mac", "vision pro", "ai"],
                   ["GOOGL", "MSFT", "SAMSUNG"], ["TSM", "FOXCONN"]),
            Company("MSFT", "Microsoft Corp.", Sector.TECHNOLOGY, 2900, 390.25, 25,
                   ["microsoft", "windows", "azure", "openai", "copilot", "ai", "cloud"],
                   ["GOOGL", "AMZN", "AAPL"], []),
            Company("GOOGL", "Alphabet Inc.", Sector.TECHNOLOGY, 1750, 142.80, 28,
                   ["google", "alphabet", "android", "gemini", "ai", "search", "youtube"],
                   ["MSFT", "META", "AAPL"], []),
            Company("META", "Meta Platforms", Sector.TECHNOLOGY, 950, 380.50, 18,
                   ["meta", "facebook", "instagram", "whatsapp", "metaverse", "llama"],
                   ["GOOGL", "SNAP", "PINS"], []),
            Company("NVDA", "NVIDIA Corp.", Sector.TECHNOLOGY, 1200, 485.50, 45,
                   ["nvidia", "gpu", "ai", "chips", "semiconductor", "cuda", "data center"],
                   ["AMD", "INTC"], ["TSM"]),
            Company("AMD", "Advanced Micro Devices", Sector.TECHNOLOGY, 220, 135.20, 55,
                   ["amd", "ryzen", "radeon", "cpu", "gpu", "chips", "semiconductor"],
                   ["NVDA", "INTC"], ["TSM", "GFS"]),
            Company("TSM", "Taiwan Semiconductor", Sector.TECHNOLOGY, 480, 95.30, 12,
                   ["tsmc", "taiwan", "semiconductor", "chips", "fabrication", "foundry"],
                   ["INTC", "SAMSUNG"], []),
            Company("INTC", "Intel Corp.", Sector.TECHNOLOGY, 180, 42.50, 38,
                   ["intel", "cpu", "chips", "semiconductor", "foundry", "data center"],
                   ["AMD", "NVDA", "TSM"], []),
            
            # AI Companies
            Company("OPENAI", "OpenAI (Private)", Sector.TECHNOLOGY, 80, 0, 0,
                   ["openai", "chatgpt", "gpt", "gpt-4", "gpt-5", "dall-e", "sora"],
                   ["GOOGL", "ANTHROPIC"], ["MSFT", "NVDA"]),
            Company("ANTHROPIC", "Anthropic (Private)", Sector.TECHNOLOGY, 15, 0, 0,
                   ["anthropic", "claude", "constitutional ai", "safety"],
                   ["OPENAI", "GOOGL"], ["GOOGL", "AMZN"]),
            
            # Finance
            Company("JPM", "JPMorgan Chase", Sector.FINANCE, 420, 145.80, 12,
                   ["jpmorgan", "chase", "banking", "investment", "finance"],
                   ["BAC", "GS", "MS"], []),
            Company("GS", "Goldman Sachs", Sector.FINANCE, 120, 365.20, 3,
                   ["goldman", "sachs", "investment", "banking", "trading"],
                   ["JPM", "MS"], []),
            Company("V", "Visa Inc.", Sector.FINANCE, 500, 260.40, 8,
                   ["visa", "payment", "credit card", "digital payment"],
                   ["MA", "PYPL"], []),
            
            # Healthcare
            Company("JNJ", "Johnson & Johnson", Sector.HEALTHCARE, 380, 160.50, 7,
                   ["johnson", "pharmaceutical", "medical", "vaccine", "drug"],
                   ["PFE", "MRK"], []),
            Company("PFE", "Pfizer Inc.", Sector.HEALTHCARE, 160, 28.50, 35,
                   ["pfizer", "vaccine", "pharmaceutical", "drug", "mrna"],
                   ["JNJ", "MRNA", "BNTX"], []),
            Company("MRNA", "Moderna Inc.", Sector.HEALTHCARE, 35, 92.30, 8,
                   ["moderna", "mrna", "vaccine", "biotechnology", "cancer"],
                   ["PFE", "BNTX"], []),
            
            # Automotive
            Company("TSLA", "Tesla Inc.", Sector.AUTOMOTIVE, 580, 185.20, 95,
                   ["tesla", "electric vehicle", "ev", "musk", "self-driving", "battery"],
                   ["F", "GM", "RIVN"], ["PANASONIC", "LG"]),
            Company("F", "Ford Motor Co.", Sector.AUTOMOTIVE, 48, 12.10, 45,
                   ["ford", "automotive", "ev", "f-150", "mustang"],
                   ["GM", "TSLA"], []),
            Company("GM", "General Motors", Sector.AUTOMOTIVE, 52, 38.50, 15,
                   ["gm", "general motors", "chevrolet", "ev", "cruise"],
                   ["F", "TSLA"], []),
            
            # Energy
            Company("XOM", "Exxon Mobil", Sector.ENERGY, 450, 105.80, 18,
                   ["exxon", "oil", "gas", "energy", "petroleum", "drilling"],
                   ["CVX", "BP", "SHEL"], []),
            Company("CVX", "Chevron Corp.", Sector.ENERGY, 280, 148.20, 8,
                   ["chevron", "oil", "gas", "energy", "refinery"],
                   ["XOM", "BP"], []),
            
            # Retail
            Company("AMZN", "Amazon.com Inc.", Sector.RETAIL, 1550, 150.80, 45,
                   ["amazon", "aws", "ecommerce", "cloud", "alexa", "prime"],
                   ["WMT", "MSFT", "GOOGL"], []),
            Company("WMT", "Walmart Inc.", Sector.RETAIL, 420, 155.30, 8,
                   ["walmart", "retail", "grocery", "ecommerce"],
                   ["AMZN", "TGT", "COST"], []),
            
            # Defense
            Company("LMT", "Lockheed Martin", Sector.DEFENSE, 110, 425.50, 1.2,
                   ["lockheed", "defense", "military", "f-35", "missile", "aerospace"],
                   ["RTX", "NOC", "BA"], []),
            Company("RTX", "RTX Corporation", Sector.DEFENSE, 135, 92.30, 5,
                   ["raytheon", "rtx", "defense", "missile", "pratt whitney"],
                   ["LMT", "NOC"], []),
        ]
    
    def _load_sector_keywords(self) -> Dict[Sector, List[str]]:
        """Load sector-related keywords."""
        return {
            Sector.TECHNOLOGY: ["tech", "software", "ai", "cloud", "semiconductor", "chip", "data", "cyber"],
            Sector.FINANCE: ["bank", "finance", "investment", "trading", "crypto", "interest rate", "fed"],
            Sector.HEALTHCARE: ["health", "medical", "pharma", "drug", "vaccine", "fda", "clinical"],
            Sector.ENERGY: ["oil", "gas", "energy", "renewable", "solar", "wind", "drilling"],
            Sector.RETAIL: ["retail", "ecommerce", "consumer", "shopping", "sales"],
            Sector.MANUFACTURING: ["manufacturing", "factory", "production", "supply chain"],
            Sector.AUTOMOTIVE: ["automotive", "car", "vehicle", "ev", "electric", "self-driving"],
            Sector.TELECOMMUNICATIONS: ["telecom", "5g", "wireless", "network", "broadband"],
            Sector.DEFENSE: ["defense", "military", "weapon", "missile", "security", "government"],
            Sector.ENTERTAINMENT: ["entertainment", "streaming", "movie", "gaming", "media"],
        }
    
    def analyze_news(self, news_items: List[Dict[str, Any]]) -> MarketAnalysis:
        """
        Analyze a list of news items for company impacts.
        
        Args:
            news_items: List of news articles with title, snippet, link
            
        Returns:
            MarketAnalysis with company impacts and monetary effects
        """
        print("📊 Market Analyzer: Analyzing news for company impacts...")
        
        # Combine all news text for analysis
        combined_text = " ".join([
            f"{item.get('title', '')} {item.get('snippet', '')}"
            for item in news_items
        ]).lower()
        
        news_summary = news_items[0].get("title", "News Analysis") if news_items else "No news"
        
        # Detect affected sectors
        sector_impacts = self._analyze_sector_impacts(combined_text)
        
        # Find and analyze affected companies
        affected_companies = self._find_affected_companies(combined_text, news_items)
        
        # Sort into gainers and losers
        gainers = sorted(
            [c for c in affected_companies if c.monetary_impact > 0],
            key=lambda x: x.monetary_impact,
            reverse=True
        )[:5]
        
        losers = sorted(
            [c for c in affected_companies if c.monetary_impact < 0],
            key=lambda x: x.monetary_impact
        )[:5]
        
        # Calculate total market impact
        total_impact = sum(c.monetary_impact for c in affected_companies)
        
        # Determine market sentiment
        if total_impact > 1_000_000_000:
            sentiment = "bullish"
        elif total_impact < -1_000_000_000:
            sentiment = "bearish"
        else:
            sentiment = "neutral"
        
        # Generate key insights
        insights = self._generate_insights(affected_companies, sector_impacts, news_items)
        
        analysis = MarketAnalysis(
            news_summary=news_summary,
            timestamp=datetime.now().isoformat(),
            sector_impacts=sector_impacts,
            affected_companies=affected_companies,
            total_market_impact=total_impact,
            top_gainers=gainers,
            top_losers=losers,
            market_sentiment=sentiment,
            key_insights=insights,
        )
        
        print(f"✅ Analyzed impact on {len(affected_companies)} companies.")
        print(f"   Market sentiment: {sentiment.upper()}")
        
        return analysis
    
    def _analyze_sector_impacts(self, text: str) -> Dict[str, ImpactType]:
        """Determine which sectors are affected and how."""
        impacts = {}
        
        # Positive and negative indicators
        positive_words = ["growth", "surge", "gain", "profit", "success", "breakthrough", 
                         "innovation", "partnership", "expansion", "bullish", "record"]
        negative_words = ["loss", "crash", "fail", "breach", "lawsuit", "decline", 
                         "shortage", "disruption", "layoff", "bearish", "investigation"]
        
        for sector, keywords in self.sector_keywords.items():
            sector_mentioned = any(kw in text for kw in keywords)
            
            if sector_mentioned:
                pos_count = sum(1 for w in positive_words if w in text)
                neg_count = sum(1 for w in negative_words if w in text)
                
                if pos_count > neg_count:
                    impacts[sector.value] = ImpactType.POSITIVE
                elif neg_count > pos_count:
                    impacts[sector.value] = ImpactType.NEGATIVE
                else:
                    impacts[sector.value] = ImpactType.NEUTRAL
        
        return impacts
    
    def _find_affected_companies(self, text: str, news_items: List[Dict]) -> List[CompanyImpact]:
        """Find companies mentioned or affected by the news."""
        affected = []
        
        # Sentiment indicators
        positive_context = ["growth", "surge", "gain", "profit", "success", "breakthrough", 
                          "innovation", "partnership", "expansion", "launch", "record", "beat"]
        negative_context = ["loss", "crash", "fail", "breach", "lawsuit", "decline", 
                          "shortage", "disruption", "layoff", "investigation", "hack", "miss"]
        
        for company in self.companies:
            # Check if company is mentioned
            relevance = 0.0
            matched_keywords = []
            
            # Direct mention by name or ticker
            if company.name.lower() in text or company.ticker.lower() in text:
                relevance = 0.95
                matched_keywords.append(company.name)
            
            # Keyword matches
            for keyword in company.keywords:
                if keyword.lower() in text:
                    relevance = max(relevance, 0.6 + random.uniform(0, 0.3))
                    matched_keywords.append(keyword)
            
            # Sector-level impact (indirect effect)
            sector_kws = self.sector_keywords.get(company.sector, [])
            sector_match = any(kw in text for kw in sector_kws)
            if sector_match and relevance < 0.3:
                relevance = 0.2 + random.uniform(0, 0.2)
            
            # Skip if not relevant enough
            if relevance < 0.15:
                continue
            
            # Determine impact type based on context
            pos_score = sum(1 for w in positive_context if w in text)
            neg_score = sum(1 for w in negative_context if w in text)
            
            # Check if company is competitor of affected company (inverse impact)
            is_competitor_benefit = False
            for other_company in self.companies:
                if company.ticker in other_company.competitors:
                    if other_company.name.lower() in text or other_company.ticker.lower() in text:
                        if neg_score > pos_score:
                            is_competitor_benefit = True
                            break
            
            if is_competitor_benefit:
                impact_type = ImpactType.POSITIVE
                pos_score, neg_score = neg_score, pos_score  # Invert for monetary calc
            elif pos_score > neg_score:
                impact_type = ImpactType.POSITIVE
            elif neg_score > pos_score:
                impact_type = ImpactType.NEGATIVE
            else:
                impact_type = ImpactType.NEUTRAL
            
            # Calculate monetary impact based on market cap and relevance
            base_impact = company.market_cap_billions * 1_000_000_000 * 0.001  # 0.1% baseline
            severity_multiplier = (pos_score - neg_score) * 0.005  # Each sentiment word = 0.5%
            
            # Apply relevance factor
            monetary_impact = base_impact * relevance * (1 + severity_multiplier)
            
            if impact_type == ImpactType.NEGATIVE:
                monetary_impact = -abs(monetary_impact)
            elif impact_type == ImpactType.NEUTRAL:
                monetary_impact = monetary_impact * random.uniform(-0.2, 0.2)
            
            # Add some randomness for realism
            monetary_impact *= random.uniform(0.7, 1.3)
            
            # Calculate percentage change
            if company.stock_price > 0:
                percentage_change = (monetary_impact / (company.market_cap_billions * 1_000_000_000)) * 100
            else:
                percentage_change = random.uniform(-5, 5)
            
            # Generate reasoning
            reasoning = self._generate_reasoning(company, impact_type, matched_keywords, news_items)
            
            affected.append(CompanyImpact(
                company=company,
                impact_type=impact_type,
                relevance_score=relevance,
                monetary_impact=monetary_impact,
                percentage_change=percentage_change,
                reasoning=reasoning,
                related_keywords=matched_keywords[:5],
                confidence=min(0.95, relevance + random.uniform(0, 0.15)),
            ))
        
        # Sort by absolute monetary impact
        affected.sort(key=lambda x: abs(x.monetary_impact), reverse=True)
        
        return affected[:15]  # Return top 15 most impacted
    
    def _generate_reasoning(self, company: Company, impact: ImpactType, 
                           keywords: List[str], news_items: List[Dict]) -> str:
        """Generate reasoning for the company impact."""
        impact_word = "benefit" if impact == ImpactType.POSITIVE else "risk" if impact == ImpactType.NEGATIVE else "exposure"
        
        if keywords:
            return f"{company.name} may {impact_word} from news related to {', '.join(keywords[:3])}. " \
                   f"As a {company.sector.value} company, market dynamics could affect valuation."
        else:
            return f"{company.name} ({company.sector.value} sector) has indirect {impact_word} exposure."
    
    def _generate_insights(self, companies: List[CompanyImpact], 
                          sector_impacts: Dict, news_items: List[Dict]) -> List[str]:
        """Generate key insights from the analysis."""
        insights = []
        
        # Sector insight
        positive_sectors = [s for s, i in sector_impacts.items() if i == ImpactType.POSITIVE]
        negative_sectors = [s for s, i in sector_impacts.items() if i == ImpactType.NEGATIVE]
        
        if positive_sectors:
            insights.append(f"📈 Bullish signal for: {', '.join(positive_sectors)}")
        if negative_sectors:
            insights.append(f"📉 Bearish signal for: {', '.join(negative_sectors)}")
        
        # Top mover insight
        if companies:
            top = max(companies, key=lambda x: abs(x.monetary_impact))
            direction = "gain" if top.monetary_impact > 0 else "lose"
            insights.append(f"💰 {top.company.ticker} expected to {direction} ${abs(top.monetary_impact)/1e6:.1f}M")
        
        # Competitor dynamics
        gainers = [c for c in companies if c.impact_type == ImpactType.POSITIVE]
        losers = [c for c in companies if c.impact_type == ImpactType.NEGATIVE]
        if gainers and losers:
            insights.append(f"🔄 Market shift: {len(gainers)} gainers vs {len(losers)} losers")
        
        return insights[:5]
    
    def get_analysis_report(self, analysis: MarketAnalysis) -> str:
        """Generate a detailed text report of the analysis."""
        lines = [
            "📊 MARKET IMPACT ANALYSIS REPORT",
            "=" * 60,
            f"Analysis Time: {analysis.timestamp}",
            f"News: {analysis.news_summary[:60]}...",
            f"Market Sentiment: {analysis.market_sentiment.upper()}",
            f"Total Market Impact: ${analysis.total_market_impact:,.0f}",
            "",
        ]
        
        if analysis.top_gainers:
            lines.append("📈 TOP GAINERS:")
            for c in analysis.top_gainers[:5]:
                lines.append(f"  {c.company.ticker}: +${c.monetary_impact/1e6:.2f}M ({c.percentage_change:+.2f}%)")
        
        if analysis.top_losers:
            lines.append("\n📉 TOP LOSERS:")
            for c in analysis.top_losers[:5]:
                lines.append(f"  {c.company.ticker}: ${c.monetary_impact/1e6:.2f}M ({c.percentage_change:+.2f}%)")
        
        lines.append("\n💡 KEY INSIGHTS:")
        for insight in analysis.key_insights:
            lines.append(f"  • {insight}")
        
        return "\n".join(lines)


if __name__ == "__main__":
    # Test the Market Analyzer
    analyzer = MarketAnalyzer()
    
    test_news = [
        {
            "title": "OpenAI Announces GPT-5 With Revolutionary Reasoning Capabilities",
            "snippet": "The new AI model shows breakthrough performance in complex reasoning tasks, potentially disrupting enterprise software market.",
            "link": "https://example.com/news"
        },
        {
            "title": "NVIDIA Reports Record Demand for AI Chips",
            "snippet": "GPU giant sees unprecedented orders from cloud providers and AI companies.",
            "link": "https://example.com/news2"
        }
    ]
    
    analysis = analyzer.analyze_news(test_news)
    print("\n" + analyzer.get_analysis_report(analysis))
