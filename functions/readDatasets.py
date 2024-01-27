import json
import random
import pandas as pd

def read_dataset(dataset_type):
    if dataset_type == "IMdb":
        path = "./data/IMdb.csv"
        df = pd.read_csv(path)
        df = df[['Overview']]
        return df
    elif dataset_type == "toxic":
        path = "./data/toxic.csv"
        df = pd.read_csv(path)
        df = df[['comment_text', 'toxic']]
        df['comment_text'] = df['comment_text'].str.replace('\n', ' ')
        return df
    elif dataset_type == "spam":
        path = "./data/YoutubeSPAM.csv"
        df = pd.read_csv(path, encoding='latin-1')
        df = df[['CONTENT', 'CLASS']]
        return df
    elif dataset_type == "squad":
        path = "./data/SQuAD2.0.json"
        with open(path, 'r', encoding='utf-8') as file:
            squad_data = json.load(file)
        
        data_list = []
        for entry in squad_data['data']:
            title = entry['title']
            for paragraph in entry['paragraphs']:
                for qa in paragraph['qas']:
                    question = qa['question']
                    answer_text = qa['answers'][0]['text'] if qa['answers'] else None
                    data_list.append({'title': title, 'question': question, 'answer': answer_text})
        
        df = pd.DataFrame(data_list)
        return df
    else:
        raise ValueError("Unsupported dataset type")

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
