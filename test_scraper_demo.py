import asyncio
from typing import List
from pathlib import Path

# Core imports from crawl4ai
from crawl4ai import (
    AsyncWebCrawler, CrawlResult,
    BrowserConfig, CrawlerRunConfig,
    LLMConfig, PruningContentFilter,
    DefaultMarkdownGenerator,
    JsonCssExtractionStrategy, LLMExtractionStrategy,
    BFSDeepCrawlStrategy, DomainFilter, FilterChain
)
from crawl4ai.proxy_strategy import ProxyConfig
from crawl4ai import RoundRobinProxyStrategy

# Set current directory
__cur_dir__ = Path(__file__).parent


async def demo_basic_crawl():
    """Basic web crawling example with markdown output."""
    print("\n***1. Basic Web Crawling***")
    
    async with AsyncWebCrawler() as crawler:
        results: List[CrawlResult] = await crawler.arun(
            url="https://news.ycombinator.com"
        )

        for i, res in enumerate(results):
            print(f"\nResult {i + 1}:")
            print(f"Success: {res.success}")
            
            if res.success:
                print(f"Markdown length: {len(res.markdown.raw_markdown)} chars")
                print(f"First 100 characters: {res.markdown.raw_markdown[:100]}...")
            else:
                print("Failed to crawl the URL.")


async def main():
    """Run all demo functions sequentially."""
    print("***Comprehensive Crawl4AI Demo***")
    print("Note: Some examples may require API keys or config setups.")

    await demo_basic_crawl()
    # You can add more demos here as needed.

    print("\n***Demo Complete***")
    print("Check for any generated files (screenshots, PDFs, etc.) in the current directory.")

    # Cleanup any temp files that may have been created
    for file in __cur_dir__.glob("*.tmp"):
        file.unlink(missing_ok=True)


if __name__ == "__main__":
    asyncio.run(main())
