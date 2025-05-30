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

__cur_dir__ = Path(__file__).parent.resolve()
# Ensure the tmp directory exists
(__cur_dir__ / "tmp").mkdir(exist_ok=True)

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
    """Take screenshots and generate PDFs of a webpage."""
    print("\n***5. Screenshot and PDF Generation***")

    async with AsyncWebCrawler() as crawler:
        results: List[CrawlResult] = await crawler.arun(
            #url = "https://www.example.com",
            url="https://en.wikipedia.org/wiki/Giant_anteater",
            config=CrawlerRunConfig(
                screenshot=True,
                pdf=True
            )
        )

        for i, res in enumerate(results):

            if res.screenshot:
                # Save screenshot
                scrnshot_path = f"{__cur_dir__}/tmp/example_screenshot_{i + 1}.png"
                with open(scrnshot_path, "wb") as f:
                    f.write(base64.b64decode(res.screenshot))
                print(f"Screenshot saved to {scrnshot_path}")

            if res.pdf:
                # Save PDF
                pdf_path = f"{__cur_dir__}/tmp/example_pdf_{i + 1}.pdf"
                with open(pdf_path, "wb") as f:
                    f.write(res.pdf)
                print(f"PDF saved to {pdf_path}")




async def main():
    """Run all demo fuctions sequentially."""

    print("***Comprehensive Crawl4AI Demo***")
    print("Note: Some examples require API keys or other configurations.")


    # Run all demos

    # await demo_basic_crawl()
    # await demo_parrallel_crawl()
    # await demo_fit_markdown()
  
    # await demo_media_and_links()


    await demo_screenshot_and_pdf()
    # Add more demo functions here as needed



    print("\n***Demo Complete***")
    print("Check for any generated files (screenshots, PDFs, etc.) in the current directory.")

    #clean up any tem files that may have been created
if __name__ == "__main__":
    asyncio.run(main())
    #clean up any tem files that may have been created
    for file in __cur_dir__.parent.glob("*.tmp"):
        file.unlink(missing_ok=True)