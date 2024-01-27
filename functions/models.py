import os
import requests
import time
from sydney import SydneyClient
from functions.utils import convert_to_plain_text
from bardapi import BardCookies
from utils.utils import generate_demografic_context

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

async def request_to_bing(first_question, second_question = None, type="q&a", prompt = ""):

    if (type == "q&a"):
        prompt = "Answer me the following question in plain text without using quotes: "
    elif (type == "change_order"):
        prompt = "Change the order of the next sentence: "
    elif (type == "add_random_words"):
        prompt = "Add random words, do not replace, to the next sentence but don't let the phrase lose its meaning: "
    elif (type == "remplace_named_entities"):
        prompt = "Replace all named entities to alter the demographic context of the following sentence, give me only the new sentence: "
    elif (type == "use_negation"):
        prompt = "Modify the following sentence using the negation, give me only the new sentence: "
    elif (type == "introducce_demografic_context"):
        demografic_context = generate_demografic_context()
        prompt = prompt + demografic_context + "\n"
    elif (type == "toxic"):
        prompt = "Is the following sentence toxic? Say me only yes or no, i dont want anything else " + "\n"
    elif (type == "spam"):
        prompt = "Is the following sentence spam? Say me only yes or no, i dont want anything else " + "\n"
    elif (type == "compare"):
        prompt = "Compare the following sentences.Say me only the % number of similarity, i dont want anyting else: " + "\n"
    elif (type == "replace_word_synonyms"):
        prompt = "Use synonyms to change the words in the sentence, without changing the meaning. Give me back just one sentence: "
    elif (type == "replace_word_antonyms"):
        prompt = "Use antonyms to change the words in the sentence, and meaning of the sentence. Give me back just one sentence: "
    elif (type == "replace_sentences"):    
        prompt = "Replace one of the sentences with another sentence that has nothing to do with the context. Return me as a result what the text would look like after the transformation. Give me back the result between {}: "
    elif (type == "double_negative"):
        prompt = "Add double negatives without changing the meaning of the sentence. Make use of double negations even if it is incorrect in the use of language. Give me back just one sentence between {}: "
    async with SydneyClient() as sydney:
        if (type == "compare"):
            response = await sydney.ask(prompt + first_question + "\n" + second_question, citations=False)
        else:
            response = await sydney.ask(prompt + first_question, citations=False)
        response = convert_to_plain_text(response)
        return response
    
def request_to_bard(first_question, second_question = None, type="q&a", prompt = ""):

    cookie_dict = {
        "__Secure-1PSID": os.getenv('SECURE_1PSID'),
        "__Secure-1PSIDTS": os.getenv('SECURE_1PSIDTS'),
        "__Secure-1PSIDCC": os.getenv('SECURE_1PSIDCC'),
    }

    prompt = ""
    if (type == "q&a"):
        prompt = "Answer me the following question in plain text without using quotes: "
    elif (type == "toxic"):
        prompt = "Is the following sentence toxic? Say me only yes or no, i dont want anything else " + "\n"
    elif (type == "spam"):
        prompt = "Is the following sentence spam? Say me yes or no, i dont want anything else " + "\n"
    elif (type == "compare"):
        prompt = "Compare the following sentences and give me only the % number of similarity, i dont want anyting else: " + "\n"

    bard = BardCookies(cookie_dict=cookie_dict)
    if (type == "compare"):
        response = bard.get_answer(prompt + first_question + "\n" + second_question)['content']
    else:
        response = bard.get_answer(prompt + first_question)['content']
    return response