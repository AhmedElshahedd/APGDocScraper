# APGDocScraper

### **Overview**

`APGDocScraper` is a Python-based web scraping tool designed to extract document information from the APG (Austrian Power Grid) Document Hub. It uses Selenium to navigate through the website and scrape data such as document names, publication dates, document types, and legal bases from multiple pages. The scraped data is then saved in a CSV format for easy access and further analysis.

### **Features**

- Scrapes documents from Document Hub.
- Handles pagination automatically.
- Extracts details like Document Name, Publication Date, Document Type, and Legal Bases.
- Saves the extracted data to a CSV file.
  
### **Requirements**

To run this project, the following Python libraries are required:

- **Selenium**: For automating browser interactions.
- **Webdriver Manager**: For managing the Chrome WebDriver automatically.
- **Pandas**: For creating and saving data in CSV format.

You can install the required libraries by running:

```bash
pip install selenium webdriver-manager pandas
