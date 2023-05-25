#Set your OPENAI_API_KEY environment variable by adding the following line into your shell initialization 
#script (e.g. .bashrc, zshrc, etc.) or running it in the command line before the fine-tuning command:
    #export OPENAI_API_KEY="<OPENAI_API_KEY>"
import openai

current_description = "Loose Fit Jacquard-weave Resort Shirt, Beige/red striped"

prompt = """
I am an AI model trained to identify details about a product from a given description. Here are a few examples:

Description: "Loose Fit Jacquard-weave Resort Shirt, Beige/red striped"
Details: 
Brand - Not specified
Color - Beige and red
Type - Shirt
Material - Jacquard
Fit - Loose
Gender - Not specified

Description: "NIKE Air Force 1 Low LV8 1-Womens 7.5 CW0984-100"
Details: 
Brand - Nike
Color - White
Type - Shoe
Material - Not specified
Fit - Not specified
Gender - Women

Description: "Eyelet Corset Peplum Top"
Details: 
Brand - Not specified
Color - Not Specified
Type - Top
Material - Not specified
Fit - Not specified
Gender - Women

Now, for the following description, please identify the product details:

Description: {current_description}
"""

openai.api_key = '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'

response = openai.Completion.create(
  engine="text-davinci-003",
  prompt=prompt,
  temperature=0.5,
  max_tokens=100
)

print(response.choices[0].text.strip())