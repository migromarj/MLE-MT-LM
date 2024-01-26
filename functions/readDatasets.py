import json
import random
import pandas as pd

# Prompt Injection

def choose_random_data(dataset):

    if dataset == "jailbreaks":
        return get_random_jailbreak()
    elif dataset == "questions":
        return get_random_question()

def read_jailbreaks():
    
    jailbreaks = []
    path = './data/prompt_injection/jailbreaks.json'

    with open(path) as json_file:
        data = json.load(json_file)

        for p in data['jailbreak']:
            jailbreaks.append(p)

    return jailbreaks

def get_random_jailbreak():
    jailbreaks = read_jailbreaks()

    res = random.choice(jailbreaks)
    while "[INSERT PROMPT HERE]" not in res:
        res = random.choice(jailbreaks)

    return res

def read_questions():
    
    csv_path = './data/prompt_injection/do_not_answer_en.csv'

    df = pd.read_csv(csv_path)

    return df['question'].tolist()

def get_random_question():

    questions = read_questions()

    return random.choice(questions)