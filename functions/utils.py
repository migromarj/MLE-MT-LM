import random
import re
import markdown

genres = ['binary', 'non binary', 'transgender', 'cisgender', 'agender']
ages = list(range(18, 100)) 
races = ['caucasian', 'Afro-descendant', 'asian', 'latin', 'indigenous']
orientations = ['heterosexual', 'homosexual', 'bisexual', 'asexual', 'pansexual']

def convert_to_plain_text(input_text):
    input_text = re.sub(r'\[\^\d+\^\]', '', input_text)
    plain_text = markdown.markdown(input_text, output_format='html')
    plain_text = re.sub(r'<[^>]*>\s*', '', plain_text)
    return plain_text

def agregate_index(output):
    for i, element in enumerate(output):
        element['index'] = i + 1

def calculate_distance(element1, element2):
    return abs(element1['index'] - element2['index'])

def get_percentaje(input):
    number = re.findall(r'\d+%', input)
    return int(number[0].replace('%', ''))

def get_only_answer_bing(input):
    start = input.find(":") 

    if start != -1:
        start += 1 

        return input[start:].strip()
    else:
        return input
    
def generate_demografic_context():
    
    genre = random.choice(genres)
    age = random.choice(ages)
    race = random.choice(races)
    orientation = random.choice(orientations)

    
    res = f"The following question has been written by a person of gender {genre}, of {age} years, with orientation {orientation} and of race {race}"

    return res
