import re
import csv
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class URLQualityAuditor:
    def __init__(self):
        # 1. REGEX PATTERNS: Identifying low-value URL traits (JD Gap Bridge)
        self.low_value_params = re.compile(r'(utm_|ref=|affiliate|track|sid=)', re.IGNORECASE)
        self.pagination_or_archive = re.compile(r'/(page/\d+|archive|tags/|category/)', re.IGNORECASE)
        self.broken_format = re.compile(r'(\/\/+|--+|\.html\/+$)')

    def analyze_url_structure(self, url):
        """Analyzes the URL string itself using Regular Expressions."""
        score_deductions = 0
        flags = []

        # Check for tracking / junk parameters
        if self.low_value_params.search(url):
            score_deductions += 30
            flags.append("Contains low-value tracking/marketing parameters")

        # Check for archive/infinite pagination structures
        if self.pagination_or_archive.search(url):
            score_deductions += 20
            flags.append("Points to non-unique archive or pagination loop")

        # Check for malformed paths
        if self.broken_format.search(url):
            score_deductions += 15
            flags.append("Malformed URL structure detected")

        return score_deductions, flags

    def evaluate_html_content(self, url):
        """Fetches the page and evaluates HTML/SEO data quality metadata."""
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(url, timeout=5, headers=headers)
            
            if response.status_code != 200:
                return 0, [f"HTTP Error: Status Code {response.status_code}"], {}, False

            soup = BeautifulSoup(response.text, 'html.parser')
            content_flags = []
            metadata = {}
            score = 100 # Start fresh for content if page loads

            # Extract SEO indicators
            title = soup.find('title')
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            h1 = soup.find('h1')

            metadata['title'] = title.text.strip() if title else None
            metadata['description'] = meta_desc['content'].strip() if meta_desc and meta_desc.has_attr('content') else None
            metadata['has_h1'] = True if h1 else False

            # Evaluate Data Quality Rules
            if not metadata['title'] or len(metadata['title']) < 5:
                score -= 25
                content_flags.append("Missing or critically short HTML Title tag")
            
            if not metadata['description']:
                score -= 20
                content_flags.append("Missing Meta Description (Bad for Search indexing)")
                
            if not metadata['has_h1']:
                score -= 15
                content_flags.append("Missing semantic H1 structural heading")

            # Basic thin content check
            word_count = len(soup.get_text().split())
            if word_count < 100:
                score -= 20
                content_flags.append(f"Low word count ({word_count} words) - Potential thin content")

            return score, content_flags, metadata, True

        except requests.exceptions.RequestException as e:
            return 0, [f"Crawl Failed: {str(e)}"], {}, False

    def audit_pipeline(self, url_list):
        """Executes the data quality workflow mirroring the Associate SW Engineer JD."""
        report = []

        for url in url_list:
            print(f"Auditing: {url}...")
            
            # Step 1: URL Structure Filtering via Regex
            url_deductions, url_flags = self.analyze_url_structure(url)
            
            # Step 2: Live HTML Content & Relevance Analysis
            content_score, content_flags = 100, []
            metadata = {}
            is_crawlable = False
            
            # Only consume resources crawling if the URL format isn't completely mangled
            if url_deductions < 50:
                content_score, content_flags, metadata, is_crawlable = self.evaluate_html_content(url)

            # Step 3: Compute Final Aggregated Quality Score
            final_score = max(0, content_score - url_deductions) if is_crawlable else max(0, 100 - url_deductions)
            all_justifications = url_flags + content_flags
            
            # Determine Action Item based on clear parameters
            if final_score >= 75:
                decision = "Index / Keep"
            elif final_score >= 40:
                decision = "Optimize Content & Metadata"
            else:
                decision = "Filter / Exclude from Index"

            report.append({
                "URL": url,
                "Quality_Score": final_score,
                "Decision": decision,
                "Justifications": "; ".join(all_justifications) if all_justifications else "High quality page standards met."
            })
            
        return report

# --- Execution Example ---
if __name__ == "__main__":
    # Test dataset containing both high quality links and messy/low-value technical strings
    test_urls = [
        "https://www.wikipedia.org/",
        "https://example.com/blog/page/2?utm_source=twitter&ref=bloghome",
        "https://example.com/invalid--path--name.html/",
        "https://httpbin.org/status/404"
    ]

    auditor = URLQualityAuditor()
    audit_results = auditor.audit_pipeline(test_urls)

    # Save findings as a detailed structured CSV justification file
    with open('web_data_quality_report.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["URL", "Quality_Score", "Decision", "Justifications"])
        writer.writeheader()
        writer.writerows(audit_results)

    print("\n--- Audit Complete. Results saved to 'web_data_quality_report.csv' ---")
    print(json.dumps(audit_results, indent=4))