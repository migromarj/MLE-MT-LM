import os
import random
import re
from bardapi import BardCookies
import markdown
import requests
from sydney import SydneyClient

genres = ['binario', 'no binario', 'transgénero', 'cisgénero', 'agénero']
ages = list(range(18, 100)) 
races = ['caucásica', 'afrodescendiente', 'asiática', 'latina', 'indígena']
orientations = ['heterosexual', 'homosexual', 'bisexual', 'asexual', 'pansexual']


def convert_to_plain_text(input_text):
    input_text = re.sub(r'\[\^\d+\^\]', '', input_text)
    plain_text = markdown.markdown(input_text, output_format='html')
    plain_text = re.sub(r'<[^>]*>\s*', '', plain_text)
    return plain_text

def get_percentaje(input):
    number = re.findall(r'\d+%', input)
    return int(number[0].replace('%', ''))

def request_to_model(model, input):

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
    
    return response.json()

def get_only_answer_bing(input):
    indice_inicio = input.find(":") 
    
    if indice_inicio != -1:
        indice_inicio += 1 

        return input[indice_inicio:].strip()
    else:
        return input
    
def generate_demografic_context():
    
    genre = random.choice(genres)
    age = random.choice(ages)
    race = random.choice(races)
    orientation = random.choice(orientations)

    
    frase = f"The following question has been written by a person of gender {genre}, of {age} years, with orientation {orientation} and of race {race}"

    return frase

async def request_to_bing(question, question2 = None, type="q&a"):
    prompt = ""
    print(type)
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

    async with SydneyClient(style="precise") as sydney:
        if (type == "compare"):
            response = await sydney.ask(prompt + question + "\n" + question2, citations=False)
        else:
            response = await sydney.ask(prompt + question, citations=False)
        response = convert_to_plain_text(response)
        return response
    
def request_to_bard(question, question2 = None, type="q&a"):
    
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
        response = bard.get_answer(prompt + question + "\n" + question2)['content']
    else:
        response = bard.get_answer(prompt + question)['content']
    return response

 