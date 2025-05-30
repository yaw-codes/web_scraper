import asyncio
import base64
import os
from typing import List
from crawl4ai import AsyncWebCrawler, CrawlResult, CacheMode
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai import LLMConfig,PruningContentFilter
from crawl4ai import DefaultMarkdownGenerator
from crawl4ai.proxy_strategy import ProxyConfig
from crawl4ai import RoundRobinProxyStrategy
from crawl4ai import JsonCssExtractionStrategy,LLMExtractionStrategy
from crawl4ai import BFSDeepCrawlStrategy,DomainFilter, FilterChain
from pathlib import Path
import json

__cur_dir__ = Path(__file__)


async def demo_basic_crawl():
    """Basic web crawling example with markdown output."""
    print("\n***1. Basic Web Crawling***")
    
    async with AsyncWebCrawler() as crawler:
        results: List[CrawlResult] = await crawler.arun(
            url="https://news.ycombinator.com",
    
            )

        for i, res in enumerate(results):
            print(f"Result {i + 1}:")
            print(f"Success: {res.success}")
            
            if res.success:
                print(f"Markdown length: {len(res.markdown.raw_markdown)} chars")
                print(f"First 100 characters: {res.markdown.raw_markdown[:100]}...")
            else:
                print("Failed to crawl the URL.")


async def demo_parrallel_crawl():
    """Crawl multiple URLs in parallel."""
    print("\n***2. Parallel Web Crawling***")
    urls: List[str] = [
        "https://news.ycombinator.com",
        "https://www.wikipedia.org",
        "https://www.python.org"
    ]

    async with AsyncWebCrawler() as crawler:

        results: List[CrawlResult] = await crawler.arun_many(
            urls=urls,
                                                             )

        print(f"Crawled {len(results)} URLs in parallel.")
        for i, res in enumerate(results):
            print(
                f"{i + 1}. {urls[i]} - {'Success' if res.success else 'Failed'} "
            )

async def demo_fit_markdown():
    """Generate focused markdown with LLM content filter"""
    print("\n***3. Fit Markdown with LLM content filter***")
    
    async with AsyncWebCrawler() as crawler:
        results:CrawlResult = await crawler.arun(
            url = "http://en.wikipedia.org/wiki/Python_(programming_language)",
            config = CrawlerRunConfig(
                markdown_generator=DefaultMarkdownGenerator(
                    content_filter=PruningContentFilter(
                    )
            )
        )
        )

        print(f"Raw: {len(results.markdown.raw_markdown)} chars")
        print(f"Fit: {len(results.markdown.fit_markdown)} chars")

async def demo_media_and_links():
    """Extract media and links from a webpage."""
    print("\n***4. Media and Links Extraction***")

    async with AsyncWebCrawler() as crawler:
        results: List[CrawlResult] = await crawler.arun(
            url="https://en.wikipedia.org/wiki/Main_Page"
        )

        for i, res in enumerate(results):
            # Extract and save all images
            images = res.media.get("images", [])
            print(f"Found {len(images)} images")

            # Extract and save all links (internal and external)
            internal_links = res.links.get("internal", [])
            external_links = res.links.get("external", [])
            print(f"Found {len(internal_links)} internal links")
            print(f"Found {len(external_links)} external links")

            # Print a few images and links
            for image in images[:3]:
                print(f"image: {image['src']}")
            for link in internal_links[:3]:
                print(f"internal link: {link['href']}")
            for link in external_links[:3]:
                print(f"external link: {link['href']}")

            # # Save to files
            # with open("images.json", "w") as f:
            #     json.dump(images, f, indent=2)

            # with open("links.json", "w") as f:
            #     json.dump({
            #         "internal": internal_links,
            #         "external": external_links
            #     }, f, indent=2)




async def demo_screenshot_and_pdf():
    pass()



async def main():
    """Run all demo fuctions sequentially."""

    print("***Comprehensive Crawl4AI Demo***")
    print("Note: Some examples require API keys or other configurations.")


    # Run all demos

    # await demo_basic_crawl()
    # await demo_parrallel_crawl()
    # await demo_fit_markdown()
  
    await demo_media_and_links()
    # Add more demo functions here as needed



    print("\n***Demo Complete***")
    print("Check for any generated files (screenshots, PDFs, etc.) in the current directory.")

    #clean up any tem files that may have been created
if __name__ == "__main__":
    asyncio.run(main())
    #clean up any tem files that may have been created
    for file in __cur_dir__.parent.glob("*.tmp"):
        file.unlink(missing_ok=True)