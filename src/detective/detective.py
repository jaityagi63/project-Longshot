import sys
import warnings
import random
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Handle the import for duckduckgo_search which might be renamed to ddgs
try:
    from duckduckgo_search import DDGS
except ImportError:
    try:
        from ddgs import DDGS
    except ImportError:
        print("❌ Critical Error: 'duckduckgo-search' library not found.")
        sys.exit(1)

try:
    from googlesearch import search as google_search
    HAS_GOOGLE = True
except ImportError:
    HAS_GOOGLE = False

# Suppress warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)


class NewsSimulator:
    """Generates realistic simulated news for demonstration purposes."""
    
    # Major news sources with their URL patterns
    NEWS_SOURCES = [
        {"name": "Reuters", "domain": "reuters.com", "path": "/world/", "trust": 0.95},
        {"name": "AP News", "domain": "apnews.com", "path": "/article/", "trust": 0.95},
        {"name": "BBC News", "domain": "bbc.com", "path": "/news/", "trust": 0.90},
        {"name": "The New York Times", "domain": "nytimes.com", "path": "/2026/02/", "trust": 0.88},
        {"name": "The Wall Street Journal", "domain": "wsj.com", "path": "/articles/", "trust": 0.88},
        {"name": "Bloomberg", "domain": "bloomberg.com", "path": "/news/articles/", "trust": 0.87},
        {"name": "Financial Times", "domain": "ft.com", "path": "/content/", "trust": 0.88},
        {"name": "The Guardian", "domain": "theguardian.com", "path": "/world/", "trust": 0.82},
        {"name": "CNN", "domain": "cnn.com", "path": "/2026/02/06/", "trust": 0.78},
        {"name": "CNBC", "domain": "cnbc.com", "path": "/2026/02/06/", "trust": 0.80},
        {"name": "TechCrunch", "domain": "techcrunch.com", "path": "/2026/02/06/", "trust": 0.75},
        {"name": "Ars Technica", "domain": "arstechnica.com", "path": "/", "trust": 0.80},
    ]
    
    # Topic-specific news templates
    TOPIC_TEMPLATES = {
        "ai": [
            {"title": "Major AI Breakthrough: {topic} Advances Transform Industry", 
             "snippet": "Leading researchers announce significant progress in {topic}, with implications for healthcare, finance, and autonomous systems. Experts predict widespread adoption within 18 months."},
            {"title": "OpenAI, Google, and Anthropic Collaborate on {topic} Safety Standards",
             "snippet": "Tech giants unite to establish new safety protocols for {topic} development. The initiative aims to address concerns about alignment and control of advanced AI systems."},
            {"title": "{topic} Regulation: EU Proposes New Framework",
             "snippet": "European Union lawmakers unveil comprehensive regulations for {topic} deployment. Companies must comply with transparency and accountability requirements by 2027."},
            {"title": "Investment Surge: VC Funding for {topic} Startups Hits Record $50B",
             "snippet": "Venture capital firms pour unprecedented funding into {topic} ventures. Analysts cite breakthrough applications and enterprise demand as key drivers."},
        ],
        "supply_chain": [
            {"title": "Global Supply Chain Alert: {topic} Disruption Affects Major Industries",
             "snippet": "Manufacturing and logistics sectors face significant challenges as {topic} impacts international trade routes. Companies scramble to secure alternative suppliers."},
            {"title": "Semiconductor Shortage Intensifies Amid {topic} Concerns",
             "snippet": "Chip manufacturers warn of extended lead times as {topic} compounds existing production constraints. Automotive and electronics sectors most affected."},
            {"title": "Shipping Giants Reroute Vessels Due to {topic}",
             "snippet": "Major shipping companies announce route changes and delays following {topic}. Freight costs expected to rise 15-20% in coming weeks."},
            {"title": "Supply Chain Resilience: Companies Stockpile Inventory After {topic}",
             "snippet": "Businesses increase safety stock levels in response to {topic}. Just-in-time manufacturing practices under renewed scrutiny."},
        ],
        "cybersecurity": [
            {"title": "Critical Vulnerability: {topic} Exposes Enterprise Systems",
             "snippet": "Security researchers discover major flaw affecting millions of systems worldwide. Organizations urged to patch immediately as exploitation attempts detected."},
            {"title": "State-Sponsored Hackers Target {topic} Infrastructure",
             "snippet": "Intelligence agencies warn of sophisticated attacks on critical infrastructure related to {topic}. Multiple countries coordinating defensive response."},
            {"title": "Data Breach: {topic} Incident Affects Millions of Users",
             "snippet": "Company discloses unauthorized access to customer data following {topic} security incident. Affected users advised to monitor accounts and reset credentials."},
            {"title": "Ransomware Attack Disrupts {topic} Operations",
             "snippet": "Cybercriminal group claims responsibility for attack on {topic} systems. Recovery efforts underway as negotiations continue."},
        ],
        "finance": [
            {"title": "Markets React: {topic} Triggers Sharp Movements",
             "snippet": "Global markets experience volatility as investors assess impact of {topic}. Analysts recommend diversification amid uncertainty."},
            {"title": "Federal Reserve Monitors {topic} Economic Implications",
             "snippet": "Central bank officials express concern over potential {topic} effects on inflation and employment. Policy response under consideration."},
            {"title": "Banking Sector: {topic} Impacts Credit Conditions",
             "snippet": "Major financial institutions adjust lending practices following {topic}. Small business loans and mortgages may face stricter requirements."},
            {"title": "Crypto Markets: {topic} Drives Digital Asset Volatility",
             "snippet": "Cryptocurrency prices swing dramatically as traders react to {topic}. Bitcoin and Ethereum see significant volume increases."},
        ],
        "general": [
            {"title": "Breaking: {topic} - What You Need to Know",
             "snippet": "Comprehensive analysis of {topic} and its potential implications. Experts weigh in on short-term and long-term impacts."},
            {"title": "Industry Analysis: How {topic} Reshapes Market Dynamics",
             "snippet": "Deep dive into the effects of {topic} on global business landscape. Winners and losers emerge as companies adapt to new realities."},
            {"title": "{topic}: Global Leaders Respond to Emerging Situation",
             "snippet": "World leaders and industry executives address {topic} concerns. Coordinated international response taking shape."},
            {"title": "Expert Opinion: Navigating {topic} Challenges",
             "snippet": "Leading analysts provide guidance on managing {topic} risks and opportunities. Key strategies for businesses and individuals."},
            {"title": "Timeline: Key Developments in {topic}",
             "snippet": "Chronological overview of significant events related to {topic}. From initial reports to current situation assessment."},
        ],
    }
    
    # Unrelated trending news (always included for variety)
    TRENDING_NEWS = [
        {"title": "Climate Summit 2026: Nations Pledge Accelerated Emissions Cuts",
         "snippet": "World leaders commit to ambitious new targets at global climate conference. Developing nations secure increased financing for green transition.",
         "category": "environment"},
        {"title": "SpaceX Successfully Launches Starship to Mars Orbit",
         "snippet": "Historic mission marks humanity's first crewed spacecraft to enter Mars orbit. Crew of six astronauts begins orbital operations ahead of landing attempt.",
         "category": "space"},
        {"title": "Breakthrough in Cancer Treatment: mRNA Therapy Shows 90% Success Rate",
         "snippet": "Clinical trials demonstrate unprecedented effectiveness of personalized mRNA cancer vaccines. FDA fast-tracks approval process.",
         "category": "health"},
        {"title": "Global Chip Shortage Eases as New Fabs Come Online",
         "snippet": "New semiconductor manufacturing facilities in US, Europe, and Asia begin production. Industry analysts predict normalized supply by Q3 2026.",
         "category": "technology"},
        {"title": "Electric Vehicle Sales Surpass Gas Cars in Europe for First Time",
         "snippet": "February 2026 marks historic milestone as EV registrations exceed traditional vehicles. Charging infrastructure expansion accelerates.",
         "category": "automotive"},
        {"title": "Major Central Banks Announce Coordinated Interest Rate Decision",
         "snippet": "Federal Reserve, ECB, and Bank of Japan align monetary policy in rare coordinated move. Markets stabilize following announcement.",
         "category": "finance"},
        {"title": "Quantum Computing Milestone: Google Achieves Error-Corrected Qubits",
         "snippet": "Breakthrough in quantum error correction brings practical quantum computing closer. Commercial applications expected within 5 years.",
         "category": "technology"},
        {"title": "UN Report: Global Food Prices Stabilize After Two-Year Surge",
         "snippet": "World Food Programme reports easing of supply pressures. Agricultural innovation and favorable weather credited for improvement.",
         "category": "economy"},
    ]
    
    @classmethod
    def _detect_topic_category(cls, query: str) -> str:
        """Detect the topic category from the query."""
        query_lower = query.lower()
        
        ai_keywords = ["ai", "artificial intelligence", "openai", "gpt", "llm", "machine learning", 
                       "neural", "chatbot", "anthropic", "google ai", "deepmind", "model", "training"]
        supply_keywords = ["supply chain", "supplier", "manufacturing", "logistics", "shipping", 
                          "semiconductor", "chip", "shortage", "disruption", "factory"]
        cyber_keywords = ["cyber", "hack", "breach", "ransomware", "security", "vulnerability", 
                         "malware", "attack", "data leak", "encryption"]
        finance_keywords = ["market", "stock", "finance", "bank", "investment", "crypto", "bitcoin",
                           "inflation", "recession", "fed", "interest rate", "economy"]
        
        if any(kw in query_lower for kw in ai_keywords):
            return "ai"
        elif any(kw in query_lower for kw in supply_keywords):
            return "supply_chain"
        elif any(kw in query_lower for kw in cyber_keywords):
            return "cybersecurity"
        elif any(kw in query_lower for kw in finance_keywords):
            return "finance"
        else:
            return "general"
    
    @classmethod
    def _generate_article_id(cls, title: str) -> str:
        """Generate a realistic-looking article ID from title."""
        hash_input = title + str(datetime.now().timestamp())
        return hashlib.md5(hash_input.encode()).hexdigest()[:12]
    
    @classmethod
    def _format_url_slug(cls, title: str) -> str:
        """Convert title to URL-friendly slug."""
        slug = "".join(c if c.isalnum() or c.isspace() else "" for c in title.lower())
        slug = "-".join(slug.split())[:60]
        return slug
    
    @classmethod
    def generate_news(cls, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Generate realistic simulated news articles.
        
        Args:
            query: The search query
            max_results: Maximum number of results
            
        Returns:
            List of simulated news articles
        """
        results = []
        category = cls._detect_topic_category(query)
        templates = cls.TOPIC_TEMPLATES.get(category, cls.TOPIC_TEMPLATES["general"])
        
        # Shuffle sources and templates for variety
        sources = random.sample(cls.NEWS_SOURCES, min(len(cls.NEWS_SOURCES), max_results + 2))
        random.shuffle(templates)
        
        # Generate related news (based on query)
        num_related = min(max_results - 1, len(templates))
        for i in range(num_related):
            template = templates[i % len(templates)]
            source = sources[i % len(sources)]
            
            # Format the title and snippet with the query topic
            topic_words = query.title()
            title = template["title"].format(topic=topic_words)
            snippet = template["snippet"].format(topic=query)
            
            # Generate realistic URL
            slug = cls._format_url_slug(title)
            article_id = cls._generate_article_id(title)
            url = f"https://www.{source['domain']}{source['path']}{slug}-{article_id}"
            
            # Random timestamp within last 24 hours
            hours_ago = random.randint(1, 24)
            timestamp = (datetime.now() - timedelta(hours=hours_ago)).isoformat()
            
            results.append({
                "title": f"[{source['name']}] {title}",
                "link": url,
                "snippet": snippet,
                "timestamp": timestamp,
                "source": source["name"],
                "trust_score": source["trust"],
                "simulated": True,
                "category": category,
            })
        
        # Add 1-2 trending/unrelated news for variety
        num_trending = min(2, max_results - num_related)
        trending_sample = random.sample(cls.TRENDING_NEWS, num_trending)
        
        for news in trending_sample:
            source = random.choice(sources)
            slug = cls._format_url_slug(news["title"])
            article_id = cls._generate_article_id(news["title"])
            url = f"https://www.{source['domain']}{source['path']}{slug}-{article_id}"
            
            hours_ago = random.randint(1, 12)
            timestamp = (datetime.now() - timedelta(hours=hours_ago)).isoformat()
            
            results.append({
                "title": f"[{source['name']}] {news['title']}",
                "link": url,
                "snippet": news["snippet"],
                "timestamp": timestamp,
                "source": source["name"],
                "trust_score": source["trust"],
                "simulated": True,
                "category": news["category"],
                "trending": True,
            })
        
        # Sort by timestamp (most recent first)
        results.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return results[:max_results]


class Detective:
    """
    The Detective module: Intelligence.
    Searches the web for facts and news related to a specific keyword or event.
    """

    def __init__(self, simulation_mode: bool = False):
        """
        Initialize the Detective.
        
        Args:
            simulation_mode: If True, always use simulated news (for demos/testing)
        """
        self.simulation_mode = simulation_mode
        self.simulator = NewsSimulator()
        try:
            self.ddgs = DDGS()
        except Exception:
            self.ddgs = None

    def investigate(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Searches the web for the given query.

        Args:
            query (str): The keyword or sentence to search for.
            max_results (int): Maximum number of results to return.

        Returns:
            list: A list of dictionaries containing title, href, and body of results.
        """
        print(f"🕵️  Detective is investigating: '{query}'...")
        
        # If simulation mode is forced, skip real search
        if self.simulation_mode:
            print("📡 Running in SIMULATION MODE...")
            return self._get_simulated_results(query, max_results)
        
        results = []
        max_retries = 3
        
        import time
        
        # List of backends to try in order
        backends = ['auto', 'html', 'lite']
        
        for attempt in range(max_retries):
            current_backend = backends[attempt % len(backends)]
            
            try:
                print(f"   (Attempt {attempt + 1} using backend: '{current_backend}')")
                search_generator = self.ddgs.text(query, max_results=max_results, backend=current_backend)
                
                found_new = False
                if search_generator:
                    for result in search_generator:
                        results.append({
                            "title": result.get("title"),
                            "link": result.get("href"),
                            "snippet": result.get("body"),
                            "timestamp": datetime.now().isoformat(),
                            "simulated": False,
                        })
                        found_new = True
                
                if found_new:
                    break
                else:
                    print(f"⚠️  Attempt {attempt + 1}: No results returned. Retrying...")
            
            except Exception as e:
                print(f"⚠️  Attempt {attempt + 1} Error ({current_backend}): {e}")
            
            if attempt < max_retries - 1:
                time.sleep(2)
        
        # Fallback to Google Search if enabled
        if not results and HAS_GOOGLE:
            print("\n⚠️  DuckDuckGo failed. Attempting fallback to Google Search...")
            try:
                g_results = google_search(query, num_results=max_results, advanced=True)
                for res in g_results:
                    results.append({
                        "title": getattr(res, 'title', res.url if hasattr(res, 'url') else str(res)),
                        "link": getattr(res, 'url', str(res)) if hasattr(res, 'url') else str(res),
                        "snippet": getattr(res, 'description', "No description available."),
                        "timestamp": datetime.now().isoformat(),
                        "simulated": False,
                    })
                
                if results:
                    print(f"✅  Google Search found {len(results)} clues.")
                    
            except Exception as e:
                print(f"❌  Google Search fallback also failed: {e}")

        # Final fallback: Simulation mode
        if not results:
            print("❌  Detective failed to find any clues after retries and fallback.")
            return self._get_simulated_results(query, max_results)

        print(f"✅  Detective found {len(results)} clues.")
        return results
    
    def _get_simulated_results(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Generate simulated news results."""
        print("\n📡 Engaging ADVANCED SIMULATION MODE...")
        print("   (Generating realistic news articles from major sources)")
        
        results = self.simulator.generate_news(query, max_results)
        
        print(f"\n✅  Detective generated {len(results)} simulated articles:")
        for i, r in enumerate(results, 1):
            is_trending = "🔥 TRENDING" if r.get("trending") else f"📰 {r.get('category', 'news').upper()}"
            print(f"   {i}. {is_trending}: {r['source']}")
        
        return results


if __name__ == "__main__":
    # Test the Detective
    d = Detective()
    
    # Use command line arguments if provided
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = "artificial intelligence developments 2026"
        
    clues = d.investigate(query, max_results=5)
    
    print("\n" + "=" * 70)
    print("📋 DETECTIVE REPORT")
    print("=" * 70)
    
    for i, clue in enumerate(clues, 1):
        print(f"\n{i}. {clue.get('title', 'No Title')}")
        print(f"   🔗 {clue.get('link', 'No Link')}")
        print(f"   📝 {clue.get('snippet', 'No Snippet')[:150]}...")
        if clue.get('simulated'):
            print(f"   ⚠️  [SIMULATED - Source: {clue.get('source', 'Unknown')}]")
