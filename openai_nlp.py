#Set your OPENAI_API_KEY environment variable by adding the following line into your shell initialization 
#script (e.g. .bashrc, zshrc, etc.) or running it in the command line before the fine-tuning command:
    #export OPENAI_API_KEY="<OPENAI_API_KEY>"
import config
import openai

def updateWithNLP(extracted_info):
    """
    The function takes extracted information, generates NLP output, parses it, and returns updated
    information.
    
    :param extracted_info: It is a variable that contains information extracted from a source, such as a
    text document or a database. This information can be in the form of text, numbers, or other data
    types. The function "updateWithNLP" takes this extracted information as input and uses natural
    language processing (NLP
    :return: the updated information after processing it with NLP.
    """
    # Generate NLP output
    string_response = nlpOutput(extracted_info)

    # Parse and update extracted info
    updated_info = parseOutput(extracted_info, string_response)

    return updated_info

def nlpOutput(extracted_fields):
    """
    This function takes in extracted fields from a product description and uses OpenAI's
    text-davinci-003 engine to generate a prompt asking for details about the product, returning the
    generated response.
    
    :param extracted_fields: The parameter extracted_fields is a dictionary containing the extracted
    fields from a product description. It is used to retrieve the product title, which is then used as
    input for the NLP model to identify the product details
    :return: The function `nlpOutput` takes in a dictionary `extracted_fields` as input and returns a
    string that contains the product details extracted from the given product title using OpenAI's GPT-3
    language model. If the product title is None, the function returns the string 'No product title
    found'.
    """

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

    openai.api_key = config.OPENAI_KEY

    response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    temperature=0.5,
    max_tokens=100
    )
    return response.choices[0].text.strip()

def parseOutput(extracted_info, string_response):
    """
    The function parses a response string and updates a dictionary with extracted information.
    
    :param extracted_info: The `extracted_info` parameter is a dictionary containing information that
    has already been extracted from a response string. The keys of the dictionary represent the type of
    information (e.g. "Title", "Brand", "Type") and the values represent the extracted
    information for each key. If a key
    :param string_response: The string response is a string containing information that needs to be
    parsed and matched with keys in a dictionary
    :return: the updated `extracted_info` dictionary with new key-value pairs added based on the
    `string_response` input. The function also prints the number of keys that were updated.
    """
    keys_updated = 0
    # Parse response string
    for line in string_response.split('\n'):
        if ' - ' in line:
            key, value = [item.strip() for item in line.split(' - ')]
            key = key.upper()  # Make key uppercase to match dictionary keys
            # Check for the key in the dictionary in a case-insensitive manner
            for info_key in extracted_info:
                if info_key.upper() == key and extracted_info[info_key] is None and value.lower() != 'not specified':
                    extracted_info[info_key] = value
                    keys_updated += 1
                    break
    print(f'Updated {keys_updated} keys')
    return extracted_info
