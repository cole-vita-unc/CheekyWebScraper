import json 

def extract_image_url(html_content):
    """
    Extracts the main product image URL from the provided HTML content.
    
    :param html_content: BeautifulSoup object of the HTML content of the product page.
    :return: URL of the main product image or None if not found.
    """
    # First, try to extract the image from the product schema
    scripts = html_content.find_all('script', {'type': 'application/ld+json'})
    for script in scripts:
        try:
            data = json.loads(script.string)
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and item.get("@type") == "Product":
                        if "image" in item:
                            return item["image"]
            elif isinstance(data, dict) and data.get("@type") == "Product":
                if "image" in data:
                    return data["image"]
        except json.JSONDecodeError:
            continue
    
    # If the image URL is not in the product schema, try to extract it from meta tags
    meta_image = html_content.find("meta", {"property": "og:image"})
    if meta_image:
        return meta_image.get("content")
    
    # If the above methods fail, add more methods or return None
    return None