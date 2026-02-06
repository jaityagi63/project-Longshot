"""
Project Longshot - News Impact Analyzer
========================================
Collects news, shows gainers/losers with reasons, and regional effects.
"""

import sys
import argparse
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.detective import Detective
from src.market_analyzer import MarketAnalyzer, ImpactType

console = Console()


class NewsImpactAnalyzer:
    """Analyzes news for market impact on companies."""

    def __init__(self):
        """Initialize the analyzer."""
        console.print(Panel.fit(
            "[bold cyan]🎯 PROJECT LONGSHOT[/bold cyan]\n"
            "[dim]News Impact Analyzer[/dim]",
            border_style="cyan"
        ))
        
        self.detective = Detective()
        self.market_analyzer = MarketAnalyzer()
        
        console.print("[green]✅ Ready![/green]\n")
    
    def analyze(self, topic: str) -> Dict[str, Any]:
        """Analyze a news topic."""
        console.print(Panel(f"[bold]🔍 Topic: {topic}[/bold]", style="blue"))
        
        # Collect News
        console.print("\n[bold yellow]📰 COLLECTING NEWS...[/bold yellow]")
        news = self.detective.investigate(topic, max_results=5)
        
        if not news:
            console.print("[red]No news found.[/red]")
            return {}
        
        # Analyze Market Impact
        market = self.market_analyzer.analyze_news(news)
        
        # Display Results
        self._show_news(news)
        self._show_gainers_losers(market)
        self._show_regional_effects(market)
        self._show_cause_analysis(news, market)
        
        return {"news": news, "market": market}
    
    def _show_news(self, news: List[Dict]):
        """Display collected news."""
        console.print("\n" + "═" * 70)
        console.print("[bold magenta]📰 NEWS COLLECTED[/bold magenta]\n")
        
        for i, article in enumerate(news, 1):
            source = article.get("source", "News")
            title = article.get("title", "Unknown")
            link = article.get("link", "#")
            
            console.print(f"[cyan]{i}. {source}[/cyan]")
            console.print(f"   {title}")
            console.print(f"   [dim blue]{link}[/dim blue]\n")
    
    def _show_gainers_losers(self, market):
        """Show gainers and losers with reasons."""
        console.print("═" * 70)
        console.print("[bold green]📈 GAINERS[/bold green]\n")
        
        if market.top_gainers:
            for g in market.top_gainers[:5]:
                console.print(f"[bold green]{g.company.ticker}[/bold green] - {g.company.name}")
                console.print(f"   Gain: [green]+${g.monetary_impact/1e6:.1f}M[/green] ({g.percentage_change:+.2f}%)")
                console.print(f"   [dim]Reason: {g.reasoning}[/dim]\n")
        else:
            console.print("[dim]No gainers identified.[/dim]\n")
        
        console.print("[bold red]📉 LOSERS[/bold red]\n")
        
        if market.top_losers:
            for l in market.top_losers[:5]:
                console.print(f"[bold red]{l.company.ticker}[/bold red] - {l.company.name}")
                console.print(f"   Loss: [red]${l.monetary_impact/1e6:.1f}M[/red] ({l.percentage_change:+.2f}%)")
                console.print(f"   [dim]Reason: {l.reasoning}[/dim]\n")
        else:
            console.print("[dim]No losers identified.[/dim]\n")
    
    def _show_regional_effects(self, market):
        """Show regional effects."""
        console.print("═" * 70)
        console.print("[bold cyan]🌍 REGIONAL EFFECTS[/bold cyan]\n")
        
        # Calculate impact levels
        affected_count = len(market.affected_companies)
        
        regions = [
            ("🇺🇸 North America", "HIGH" if affected_count > 5 else "MODERATE" if affected_count > 2 else "LOW"),
            ("🇪🇺 Europe", "MODERATE" if affected_count > 3 else "LOW"),
            ("🌏 Asia-Pacific", "HIGH" if any(c.company.ticker in ["TSM", "SAMSUNG"] for c in market.affected_companies) else "MODERATE"),
            ("🌎 Latin America", "LOW"),
            ("🌍 Middle East & Africa", "LOW"),
        ]
        
        for region, impact in regions:
            if impact == "HIGH":
                style = "[bold red]HIGH IMPACT[/bold red]"
            elif impact == "MODERATE":
                style = "[yellow]MODERATE IMPACT[/yellow]"
            else:
                style = "[green]LOW IMPACT[/green]"
            
            console.print(f"   {region}: {style}")
        
        # Sector effects
        console.print("\n[bold]Sector Effects:[/bold]")
        for sector, impact in market.sector_impacts.items():
            if impact == ImpactType.POSITIVE:
                icon = "🟢 Bullish"
            elif impact == ImpactType.NEGATIVE:
                icon = "🔴 Bearish"
            else:
                icon = "🟡 Neutral"
            console.print(f"   {sector}: {icon}")
    
    def _show_cause_analysis(self, news, market):
        """Show cause and effect analysis."""
        console.print("\n" + "═" * 70)
        console.print("[bold yellow]⚡ CAUSE & EFFECT ANALYSIS[/bold yellow]\n")
        
        # Main cause (from news)
        main_news = news[0].get("title", "Unknown event")
        console.print(f"[bold]Primary Cause:[/bold]")
        console.print(f"   {main_news}\n")
        
        # Effects summary
        total_gain = sum(c.monetary_impact for c in market.affected_companies if c.monetary_impact > 0)
        total_loss = sum(c.monetary_impact for c in market.affected_companies if c.monetary_impact < 0)
        net = total_gain + total_loss
        
        console.print(f"[bold]Market Effects:[/bold]")
        console.print(f"   Total Gains:  [green]+${total_gain/1e6:,.1f}M[/green]")
        console.print(f"   Total Losses: [red]${total_loss/1e6:,.1f}M[/red]")
        
        if net > 0:
            console.print(f"   Net Impact:   [bold green]+${net/1e6:,.1f}M (POSITIVE)[/bold green]")
        else:
            console.print(f"   Net Impact:   [bold red]${net/1e6:,.1f}M (NEGATIVE)[/bold red]")
        
        # Market sentiment
        console.print(f"\n[bold]Market Sentiment:[/bold] {market.market_sentiment.upper()}")
        
        # Key insights
        if market.key_insights:
            console.print(f"\n[bold]Key Insights:[/bold]")
            for insight in market.key_insights:
                console.print(f"   • {insight}")
        
        console.print("\n" + "═" * 70 + "\n")
    
    def interactive(self):
        """Interactive mode."""
        console.print("[dim]Enter a topic to analyze, or 'quit' to exit.[/dim]")
        
        while True:
            try:
                topic = console.input("\n[bold cyan]📰 Topic:[/bold cyan] ")
                
                if topic.lower() in ['quit', 'exit', 'q']:
                    console.print("[dim]Goodbye![/dim]")
                    break
                
                if topic.strip():
                    self.analyze(topic)
                    
            except KeyboardInterrupt:
                console.print("\n[dim]Goodbye![/dim]")
                break


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="News Impact Analyzer")
    parser.add_argument("--query", "-q", type=str, help="Topic to analyze")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    
    args = parser.parse_args()
    
    analyzer = NewsImpactAnalyzer()
    
    if args.query:
        analyzer.analyze(args.query)
    else:
        analyzer.interactive()


if __name__ == "__main__":
    main()
