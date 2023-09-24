import json
import logging

########### FUNCTION DEFINITIONS ############

# Function to retrieve the JSON string containing the product schema from the html of an item page
def getProductSchema(item_html):
    """
    This function extracts product information from HTML code in JSON-LD format.
    
    :param item_html: It is a string containing the HTML code of a webpage that contains information
    about a product
    :return: a dictionary containing information about a product, extracted from the input HTML using
    the schema.org markup format. If no such information is found, the function returns None.
    """
    scripts = item_html.find_all('script', {'type': 'application/ld+json'})
    if scripts is None or len(scripts) == 0:
        return None
    
    product_info = None

    for script in scripts:
        try:
            data = json.loads(script.string)
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and item.get("@type") == "Product":
                            product_info = item
                            break
            elif isinstance(data, dict) and data.get("@type") == "Product":
                product_info = data
        except json.JSONDecodeError:
                continue
    return product_info


def extractSchemaFields(product_schema):
    """
    The function extracts specific fields from a product schema dictionary and returns them in a new
    dictionary.
    
    :param product_schema: The input parameter is a dictionary representing a product schema, which
    contains information about a product such as its name, brand, price, color, and gender
    :return: a dictionary containing the extracted fields from the input product schema. If the input
    product schema is None, the function returns None and logs a warning message.
    """
    if product_schema is None:
        logging.warning('Invalid or empty product schema.')
        return None

    # Initialize an empty dictionary to hold the extracted fields
    extracted_fields = {"TITLE": None, "BRAND": None, "TYPE": None, "PRICE": None, "COLOR": None, "GENDER": None}

    # Extract 'PRODUCT_TYPE', 'PRICE', 'COLOR', and 'BRAND'
    if "name" in product_schema:
        extracted_fields["TITLE"] = product_schema["name"]
    
    if "offers" in product_schema and "price" in product_schema["offers"]:
        extracted_fields["PRICE"] = product_schema["offers"]["price"]

    if "brand" in product_schema and "name" in product_schema["brand"]:
        extracted_fields["BRAND"] = product_schema["brand"]["name"]

    if "color" in product_schema:
        extracted_fields["COLOR"] = product_schema["color"]
    
    if "gender" in product_schema:
        extracted_fields["GENDER"] = product_schema["gender"]

    return extracted_fields


#If product schema is not present, extract the product headings from the meta tags
def extractFromTags(html):
    """
    The function extracts product attributes from HTML tags and returns it in a dictionary format.
    
    :param html: The HTML code of a webpage that contains information about a product
    :return: a dictionary containing information extracted from the input HTML. The dictionary has keys
    for "TITLE", "BRAND", "PRICE", "COLOR", "GENDER", and "Type". The values for these keys are
    extracted from the HTML using various methods such as finding specific HTML tags or attributes. If
    any of the information cannot be extracted, the corresponding value in the dictionary will be None
    """
    if html is None:
        logging.warning('Invalid or empty HTML.')
        return None

    extracted_info = {"TITLE": None, "BRAND": None,"Type": None, "PRICE": None, "COLOR": None, "GENDER": None}

    product_name = html.find("meta", {"name": "title"}) or html.find("meta", {"property": "og:title"})
    extracted_info["TITLE"] = product_name.get("content") if product_name else html.find("title").text

    brand = html.find("meta", {"property": "og:site_name"}) or html.find("div", {"class": "brand-name"})
    extracted_info["BRAND"] = brand.get("content") if brand else None

    price = html.find("meta", {"name": "twitter:data1"}) 
    if price is None:
        price = html.find(lambda tag: tag.name in ['div', 'span'] and 
                        'product-price' in tag.get('class', ''))
    extracted_info["PRICE"] = price.get("content") if price and price.name == 'meta' else price.text.strip() if price else None


    color = html.find("span", {"class": "product-color"})
    extracted_info["COLOR"] = color.text if color else None

    gender = html.find("span", {"class": "product-gender"})
    extracted_info["GENDER"] = gender.text if gender else None

    return extracted_info
