#Set your OPENAI_API_KEY environment variable by adding the following line into your shell initialization 
#script (e.g. .bashrc, zshrc, etc.) or running it in the command line before the fine-tuning command:
    #export OPENAI_API_KEY="<OPENAI_API_KEY>"
import openai
import json

def nlpOutput(extracted_fields):

    product_title = extracted_fields['TITLE']

    if product_title is None:
        return 'No product title found'

    prompt = f"""
    I am an AI model trained to identify details about a product from a given description. Here are a few examples:

    Description: "Buy Blue & Grey Handbags for Women by BAGGIT Online | Ajio.com"
    Details: 
    Brand - Aijo
    Color - Blue and Grey
    Type - Handbag
    Material - Not Specified
    Fit - Not Specified 
    Gender - Women

    Description: "NIKE Air Force 1 Low LV8 1-Womens 7.5 CW0984-100"
    Details: 
    Brand - Nike
    Color - White
    Type - Shoe
    Material - Not specified
    Fit - Not specified
    Gender - Women

    Description: "Amazon.com: Swarovski Attract Trilogy Drop Pierced Earrings with White Crystals on a Rhodium Plated Setting with Hinged Closure, 1 1/8 inches: Clothing, Shoes & Jewelry"
    Details: 
    Brand - Swarovski
    Color - White
    Type - Jewelry
    Material - Crystals
    Fit - Not specified
    Gender - Women

    You can assume products like skirts, corsets, and dresses have the gender attribute "Women"

    Now, for the following description, please identify the product details:

    Description: {product_title}
    """

    openai.api_key = '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'

    response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    temperature=0.5,
    max_tokens=100
    )
    return response.choices[0].text.strip()
    
#TODO: Consolidate these two functions

def parseOutput(extracted_info, string_response):
    keys_updated = 0
    # Parse response string
    for line in string_response.split('\n'):
        if ' - ' in line:
            key, value = [item.strip() for item in line.split(' - ')]
            key = key.upper()  # Make key uppercase to match dictionary keys
            # Check for the key in the dictionary in a case-insensitive manner
            for info_key in extracted_info:
                if info_key.upper() == key and extracted_info[info_key] is None and value != 'Not specified':
                    extracted_info[info_key] = value
                    keys_updated += 1
                    break
    print(f'Updated {keys_updated} keys')
    return extracted_info
