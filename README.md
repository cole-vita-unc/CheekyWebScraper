# Cheeky Web Scraper

## Description 

This project is a web scraping tool designed to extract product information from web pages in a structured format. It aims to fetch detailed product information like product name, brand, price, color, and gender from a given webpage using Python.

The primary goal of this tool is to leverage the structured data present in the form of JSON-LD scripts and HTML tags on the webpage. If the JSON-LD format is present, it will try to extract the product schema from it; otherwise, it resorts to the extraction from HTML tags.

The tool makes use of Selenium with the Chrome WebDriver for web scraping and BeautifulSoup for parsing the HTML content.

This program uses Natural Language Processing (NLP) capabilities of OpenAI's GPT-3 model to refine and enhance the product information extracted. The function updateWithNLP() is responsible for generating NLP output and parsing it to return the updated product information.

### Prerequisites
In order to use the OpenAI API, you will need to set your OpenAI API key in the environment variables. You can do this by adding the following line to your shell initialization script (e.g., .bashrc, zshrc, etc.) or by running it in the command line before the fine-tuning command:

export OPENAI_API_KEY="<OPENAI_API_KEY>"

Make sure to replace <OPENAI_API_KEY> with your actual OpenAI API key.


## Current Success Rates 
Out of 55 tested websites, the program succesfully captured the HTML of 52 of them (92.7%). 
For the 51 websites where the HTML was recovered, the program retrieved the following attributes expressed as a percent: 

- Product Title: 100% 
- Product Brand: 94.1%
- Product Type: 100%
- Product Price: 43.1%
- Product Color: 35.2% 
- Product Gender: 66.7%

- Average number of attributes updated by NLP: 2.2 

## Possible Improvements 

- Improve efficiency of HTML retrieval 

Using Selenium to retrieve the html of websites was much more consistent than Beautiful Soup, however it makes the runtime longer. 
By creating a function to identify whether Beautiful Soup is adequate to retrieve the html, the amount of times Selenium is used can be lowered.

- Revisit attribute retrieval 

The scraper can expand to attempt to capture other attributes such as fit, material, and category.
More cases can also be added to the current attribute retrieval methods by examining common html patterns.

- Fine tune an NLP designed for attribute detection 

There are costs associated with using GPT3 which may be large when the program is scaled to millions of items. Fine tuning an NLP with no associated costs would help bring down the price.

- Use an NLP to determine the category of clothing

Categories are not necessarily objective (i.e. how do you determine if a product is "vintage", by the date it was made or its look), but manually determining the category for millions of products is infeasable




