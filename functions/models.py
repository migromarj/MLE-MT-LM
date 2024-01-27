import os
import requests
import time
from sydney import SydneyClient
from functions.utils import convert_to_plain_text
from bardapi import BardCookies

def request_to_model(model, input, iterations=0):

    BASE_URL = "https://api-inference.huggingface.co/models/"
    headers = {"Authorization": f"Bearer {os.getenv('HUGGING_FACE_API_KEY')}"}
    new_input = input
    parameters = {}

    if model[0] == 'fillmask':
        new_input = input.replace('<mask>', model[2])
    elif model[0] == 'translate':
        parameters = {"src_lang": "en_XX", "tgt_lang": "tgt_XX"}

    query = {"inputs": new_input, "wait_for_model": True, "parameters":parameters}

    try:
        response = requests.post(BASE_URL + model[1], json=query, headers=headers)
    except Exception as exception:
        print(exception)

    if response.status_code != 200 and iterations < 5: # 503 (Service loading) or 429 (Too many requests)
        time.sleep(10)
        request_to_model(model, input, iterations + 1)

    return response.json()

async def request_to_bing(question, type="q&a", prompt = ""):

    if (type == "q&a"):
        prompt = "Answer me the following question in plain text without using quotes: "
    elif (type == "change_order"):
        prompt = "Change the order of the next sentence: "
    elif (type == "replace_word_synonyms"):
        prompt = "Use synonyms to change the words in the sentence, without changing the meaning. Give me back just one sentence: "
    elif (type == "replace_word_antonyms"):
        prompt = "Use antonyms to change the words in the sentence, and meaning of the sentence. Give me back just one sentence: "
    elif (type == "replace_sentences"):    
        prompt = "Replace one of the sentences with another sentence that has nothing to do with the context. Return me as a result what the text would look like after the transformation. Give me back the result between {}: "
    elif (type == "double_negative"):
        prompt = "Add double negatives without changing the meaning of the sentence. Make use of double negations even if it is incorrect in the use of language. Give me back just one sentence between {}: "
    async with SydneyClient() as sydney:
        request = prompt + question
        response = await sydney.ask(request, citations=False)
        response = convert_to_plain_text(response)
        return response
    
def request_to_bard(question):

    cookie_dict = {
        "__Secure-1PSID": os.getenv('SECURE_1PSID'),
        "__Secure-1PSIDTS": os.getenv('SECURE_1PSIDTS'),
        "__Secure-1PSIDCC": os.getenv('SECURE_1PSIDCC'),
    }

    bard = BardCookies(cookie_dict=cookie_dict)
    response = bard.get_answer(question)['content']
    return response