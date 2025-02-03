import os
import google.generativeai as genai
import PIL.Image
from retreive import *
from constants import *


if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = api_key
genai.configure(api_key=api_key)


def gen_response(query):
    result = retreive_context(query)
    rel_context,images,faq_context = result

    prompt = f"""
    Your a Chat Assistant, you will understand the query and use the context to answer precisely
    Query : {query}
    Context : {rel_context}
    Also add a separate heading called FAQ under which create a 2 question for the {faq_context} and diaplay as question&answer
    """

    model = genai.GenerativeModel(model_name="gemini-1.5-flash")



    if images:
        image_ = PIL.Image.open(images[0])
        response = model.generate_content([prompt, image_])
    else:
        response = model.generate_content([prompt])
    

    return response