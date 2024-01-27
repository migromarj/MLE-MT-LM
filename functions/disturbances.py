import random
import string

from functions.utils import get_only_answer_bing, request_to_bing


def replace_characters(input, level):
    if level < 1 or level > 10:
       return "Level must be between 1 and 10."
    
    caracteres = list(input)
    indices_a_sustituir = [i for i in range(len(caracteres)) if caracteres[i] in string.ascii_letters]
    num_caracteres_a_sustituir = int(len(indices_a_sustituir) * level / 20)
    indices_a_sustituir = random.sample(indices_a_sustituir, num_caracteres_a_sustituir)
    
    for indice in indices_a_sustituir:
        caracteres[indice] = random.choice(string.ascii_letters)
    
    return ''.join(caracteres)

def add_characters(input, level):
    if level < 1 or level > 10:
        return "Level must be between 1 and 10."
    
    characters = list(input)
    num_characters_to_add = int(len(characters) * level / 20)
    
    for _ in range(num_characters_to_add):
        index = random.randint(0, len(characters))
        characters.insert(index, random.choice(string.ascii_letters))
    
    return ''.join(characters)

async def add_random_words(input):
    response = await request_to_bing(input, type="add_random_words")
    return response

async def remplace_named_entities(input):
    response = await request_to_bing(input, type="remplace_named_entities")
    return get_only_answer_bing(response)

async def change_order(input):
    response = await request_to_bing(input, type="change_order")
    return get_only_answer_bing(response)

async def use_negation(input):
    response = await request_to_bing(input, type="use_negation")
    return get_only_answer_bing(response)

async def introducce_demografic_context(input):
    response = await request_to_bing(input, type="introducce_demografic_context")
    return response