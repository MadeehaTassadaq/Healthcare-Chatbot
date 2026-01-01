#!/usr/bin/env python3
"""
Text extraction and vector loading for the Physical AI and Humanoid Robotics book.
Extracts content from https://agreeable-sand-0efbb301e.4.azurestaticapps.net/ and loads into Qdrant.
"""
import logging
import os
import re
import time
from typing import Any, Dict, List
from urllib.parse import urljoin, urlparse

import cohere
import requests
from bs4 import BeautifulSoup
from qdrant_client import QdrantClient
from qdrant_client.http import models


class WebExtractor:
    """Extracts content from the target website."""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        )

    def get_page_content(self, url: str) -> str:
        """Fetch HTML content from a URL."""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logging.error(f"Failed to fetch {url}: {e}")
            return ""

    def extract_all_pages(self) -> List[Dict[str, Any]]:
        """Extract content from all pages on the site."""
        # For now, we'll just process the main URL - in a real implementation
        # you'd want to crawl all pages on the site
        content = self.get_page_content(self.base_url)
        if not content:
            return []

        soup = BeautifulSoup(content, "html.parser")

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        return [
            {
                "url": self.base_url,
                "title": soup.title.string.strip() if soup.title and soup.title.string else "No Title",
                "content": soup.get_text(),
                "html": str(soup),
            }
        ]


class ContentParser:
    """Parses HTML content and extracts structured text."""

    def parse_content(self, html: str, url: str) -> List[Dict[str, Any]]:
        """Parse HTML and extract content by headers."""
        soup = BeautifulSoup(html, "html.parser")

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Find all headers (h1, h2, h3)
        headers = soup.find_all(["h1", "h2", "h3"])

        chunks = []

        if not headers:
            # If no headers found, use the entire content as one chunk
            text_content = soup.get_text(separator=" ", strip=True)
            if text_content:
                chunks.append(
                    {
                        "url": url,
                        "header": "Main Content",
                        "content": text_content,
                        "header_type": "none",
                    }
                )
        else:
            # Process content under each header
            for i, header in enumerate(headers):
                header_text = header.get_text(strip=True)
                header_type = header.name

                # Find the next header to determine content boundaries
                next_header = None
                if i + 1 < len(headers):
                    next_header = headers[i + 1]

                # Get content between this header and the next
                content_elements = []
                current = header.next_sibling

                while current:
                    if current == next_header:
                        break
                    if hasattr(current, "name") and current.name in ["h1", "h2", "h3"]:
                        break
                    if hasattr(current, "get_text"):
                        content_elements.append(
                            current.get_text(separator=" ", strip=True)
                        )
                    elif isinstance(current, str) and current.strip():
                        content_elements.append(current.strip())
                    current = current.next_sibling

                content = " ".join(content_elements).strip()

                # Combine header text with content
                full_content = f"{header_text} {content}".strip()

                if full_content:
                    chunks.append(
                        {
                            "url": url,
                            "header": header_text,
                            "content": full_content,
                            "header_type": header_type,
                        }
                    )

        return chunks


class Chunker:
    """Chunks content based on header hierarchy."""

    def chunk_content(self, pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process pages and create content chunks."""
        all_chunks = []

        for page in pages:
            parser = ContentParser()
            chunks = parser.parse_content(page.get("html", ""), page.get("url", ""))
            all_chunks.extend(chunks)

        return all_chunks


class EmbeddingService:
    """Generates embeddings using Cohere API."""

    def __init__(self, api_key: str):
        self.client = cohere.Client(api_key)
        self.model = "embed-english-v3.0"

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts."""
        try:
            response = self.client.embed(
                texts=texts, model=self.model, input_type="search_document"
            )
            return response.embeddings
        except Exception as e:
            logging.error(f"Failed to generate embeddings: {e}")
            return [[] for _ in texts]


class VectorStore:
    """Manages storage in Qdrant."""

    def __init__(self, url: str, api_key: str, collection_name: str = "humanoid_robotics_docs"):
        self.client = QdrantClient(url=url, api_key=api_key, prefer_grpc=False)
        self.collection_name = collection_name

    def create_collection(self):
        """Create the collection if it doesn't exist."""
        try:
            # Check if collection exists
            collection_info = self.client.get_collection(self.collection_name)
            print(f"Collection '{self.collection_name}' already exists.")
        except Exception as e:
            # Collection doesn't exist, create it
            print(f"Collection '{self.collection_name}' does not exist. Creating it...")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=1024,  # Cohere embed-english-v3.0 produces 1024-dim vectors
                    distance=models.Distance.COSINE,
                ),
            )
            print(f"Collection '{self.collection_name}' created successfully.")

    def store_chunks(self, chunks: List[Dict[str, Any]], embeddings: List[List[float]]):
        """Store chunks with embeddings in Qdrant."""
        points = []

        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            if not embedding:  # Skip chunks that failed to embed
                continue

            point = models.PointStruct(
                id=i,
                vector=embedding,
                payload={
                    "url": chunk["url"],
                    "header": chunk["header"],
                    "content": chunk["content"][:10000],  # Limit content size
                    "header_type": chunk["header_type"],
                    "module": "humanoid_robotics",
                    "content_type": "documentation",
                },
            )
            points.append(point)

        if points:
            self.client.upsert(collection_name=self.collection_name, points=points)


def main():
    """Main ingestion pipeline."""
    logging.basicConfig(level=logging.INFO)

    # Configuration - in a real app, these would come from environment variables
    BASE_URL = os.getenv(
        "BASE_URL", "https://agreeable-sand-0efbb301e.4.azurestaticapps.net/"
    )
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")
    QDRANT_URL = os.getenv("QDRANT_URL")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

    if not all([COHERE_API_KEY, QDRANT_URL, QDRANT_API_KEY]):
        raise ValueError(
            "Missing required environment variables: COHERE_API_KEY, QDRANT_URL, QDRANT_API_KEY"
        )

    # Initialize components
    extractor = WebExtractor(BASE_URL)
    chunker = Chunker()
    embedding_service = EmbeddingService(COHERE_API_KEY)
    vector_store = VectorStore(QDRANT_URL, QDRANT_API_KEY)

    logging.info("Starting content extraction...")
    pages = extractor.extract_all_pages()

    if not pages:
        logging.error("No pages extracted, exiting.")
        return

    logging.info(f"Extracted {len(pages)} pages")

    logging.info("Chunking content...")
    chunks = chunker.chunk_content(pages)
    logging.info(f"Created {len(chunks)} content chunks")

    # Prepare texts for embedding (limit the number to avoid rate limits)
    texts = [chunk["content"] for chunk in chunks]

    # Batch process to avoid rate limits
    batch_size = 96  # Cohere's max batch size is 96
    all_embeddings = []

    logging.info("Generating embeddings...")
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i : i + batch_size]
        batch_embeddings = embedding_service.generate_embeddings(batch_texts)
        all_embeddings.extend(batch_embeddings)

        # Add a small delay to respect rate limits
        time.sleep(1)

    logging.info("Creating Qdrant collection...")
    vector_store.create_collection()

    logging.info("Storing embeddings in Qdrant...")
    vector_store.store_chunks(chunks, all_embeddings)

    logging.info("Ingestion pipeline completed successfully!")


if __name__ == "__main__":
    main()