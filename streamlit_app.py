import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
import random

# Custom headers to mimic a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

def scrape_url(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text
        text = soup.get_text()
        
        # Break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text
    except Exception as e:
        return f"Error scraping {url}: {str(e)}"

st.title("Web Scraper")

# Text area for user to input URLs
urls_input = st.text_area("Enter URLs (one per line):", height=200)

if st.button("Scrape"):
    if urls_input:
        urls = urls_input.split('\n')
        urls = [url.strip() for url in urls if url.strip()]
        
        if urls:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            scraped_content = ""
            for i, url in enumerate(urls):
                status_text.text(f"Scraping URL {i+1}/{len(urls)}: {url}")
                content = scrape_url(url)
                scraped_content += f"--- Content from {url} ---\n\n{content}\n\n"
                
                # Update progress bar
                progress_bar.progress((i + 1) / len(urls))
                
                # Add a random delay between requests to be polite
                time.sleep(random.uniform(1, 3))
            
            st.text_area("Scraped Content:", value=scraped_content, height=400)
            st.success("Scraping complete!")
        else:
            st.warning("Please enter at least one valid URL.")
    else:
        st.warning("Please enter some URLs to scrape.")
