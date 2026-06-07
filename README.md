# Web Data Quality Auditor

An automated, pipeline-driven Python utility designed to evaluate the data quality, structural integrity, and search engine indexing relevance of web URLs. This project simulates core data quality workflows by leveraging **Regular Expressions (Regex)** for structural filtration and **BeautifulSoup** for semantic HTML metadata evaluation.

##  Key Features

* **Regex-Driven URL Parsing:** Utilizes optimized Regular Expression patterns to instantly isolate tracking parameters (`utm_`, `ref=`), infinite pagination loops, and malformed URL formatting.
* **Semantic HTML Audit:** Dynamically crawls target links using the `requests` library and parses essential SEO metadata tags (`<title>`, `<meta description>`, and structural `<h1>` tags) via BeautifulSoup.
* **Automated Curation Rules:** Features an internal, rule-based grading framework that subtracts data-quality penalties dynamically based on thin content, broken structural layouts, or parameters.
* **Structured Decision Logs:** Generates a clean, exportable `web_data_quality_report.csv` file mapping out final processing statuses (e.g., *Index/Keep*, *Optimize*, *Filter/Exclude*) accompanied by explicit technical justifications.

---

##  Technology Stack

* **Language:** Python 3.x
* **Core Libraries:** `re` (Regular Expressions), `urllib` (URL Parsing), `csv`, `json`
* **Third-Party Libraries:** `BeautifulSoup4` (HTML Parsing), `requests` (HTTP Client Library)

---



