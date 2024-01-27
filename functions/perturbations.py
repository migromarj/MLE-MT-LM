import random
import string
from functions.models import request_to_bing
from functions.utils import get_only_answer_bing
import nltk

##########################################################################
#############      Perturbaciones a nivel de caracteres      #############
##########################################################################

# Borrado de caracteres

def delete_characters(input, level=2):
    if level < 1 or level > 10:
        return "Level must be between 1 and 10."

    characters = list(input)
    indexes_to_delete = [i for i in range(len(characters)) if characters[i] in string.ascii_letters]
    num_characters_to_delete = int(len(indexes_to_delete) * level / 20)
    indexes_to_delete = random.sample(indexes_to_delete, num_characters_to_delete)

    for i in sorted(indexes_to_delete, reverse=True):
        del characters[i]

    return ''.join(characters)

# Remplazo de carácteres

def replace_characters(input, level=2):
    if level < 1 or level > 10:
       return "Level must be between 1 and 10."
    
    caracteres = list(input)
    indices_a_sustituir = [i for i in range(len(caracteres)) if caracteres[i] in string.ascii_letters]
    num_caracteres_a_sustituir = int(len(indices_a_sustituir) * level / 20)
    indices_a_sustituir = random.sample(indices_a_sustituir, num_caracteres_a_sustituir)
    
    for indice in indices_a_sustituir:
        caracteres[indice] = random.choice(string.ascii_letters)
    
    return ''.join(caracteres)

# Añadir carácteres aleatorios

def add_characters(input, level=2):
    if level < 1 or level > 10:
        return "Level must be between 1 and 10."
    
    characters = list(input)
    num_characters_to_add = int(len(characters) * level / 20)
    
    for _ in range(num_characters_to_add):
        index = random.randint(0, len(characters))
        characters.insert(index, random.choice(string.ascii_letters))
    
    return ''.join(characters)

##########################################################################
#############       Perturbaciones a nivel de palabras       #############
##########################################################################

# Reemplazo de palabras por sinónimos

async def replace_words_with_synonyms(input, iterations=0):
    try:
        response = await request_to_bing(input, "replace_word_synonyms")
        response = response.split(':')[1].strip().replace('"', '').replace("'", '')
    except Exception as exception:
        print(exception)
        if iterations < 5:
            response = await replace_words_with_synonyms(input, iterations + 1)
        else:
            response = "Error"
    return response

# Reemplazo de palabras por antónimos

async def replace_words_with_antonyms(input, iterations=0):
    try:
        response = await request_to_bing(input, "replace_word_antonyms")
        response = response.split(':')[1].strip().replace('"', '').replace("'", '')
    except Exception as exception:
        print(exception)
        if iterations < 5:
            response = await replace_words_with_antonyms(input, iterations + 1)
        else:
            response = "Error"
    return response

# Añadir palabras aleatorias

async def add_random_words(input):
    response = await request_to_bing(input, type="add_random_words")
    return response

# Reemplazo de nombres propios

async def remplace_named_entities(input):
    response = await request_to_bing(input, type="remplace_named_entities")
    return get_only_answer_bing(response)

##########################################################################
#############      Perturbaciones a nivel de oraciones       #############
##########################################################################

# Reemplazo de oraciones

async def replace_sentences(input):
    response = await request_to_bing(input, "replace_sentences")
    response = response.split('{')[1].strip().replace('}', '')
    return response

# Eliminación de oraciones

def delete_sentences(input_text, level):
    if level < 1 or level > 10:
        return "El nivel debe estar entre 1 y 10."

    sentences = nltk.sent_tokenize(input_text)
    num_sentences_to_delete = int(len(sentences) * level / 20)

    if num_sentences_to_delete >= len(sentences):
        return "The level is too high and the text would be empty. Try a lower level."

    indexes_to_delete = random.sample(range(len(sentences)), num_sentences_to_delete)
    sentences_to_keep = [sentences[i] for i in range(len(sentences)) if i not in indexes_to_delete]
    
    res = ' '.join(sentences_to_keep)

    return res

# Uso de doble negación

async def use_double_negative(input):
    response = await request_to_bing(input, "double_negative")
    response = response.split('{')[1].strip().replace('}', '')
    return response

# Prompt injection

async def inject_prompt(input, prompt):
    response = await request_to_bing(input, "personalised", prompt)
    return response

# Cambio de orden de las palabras

async def change_order(input):
    response = await request_to_bing(input, type="change_order")
    return get_only_answer_bing(response)

# Uso de negación

async def use_negation(input):
    response = await request_to_bing(input, type="use_negation")
    return get_only_answer_bing(response)

# Introducir contexto demográfico

async def introducce_demografic_context(input):
    response = await request_to_bing(input, type="introducce_demografic_context")
    return response