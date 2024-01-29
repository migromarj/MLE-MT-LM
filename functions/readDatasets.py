import json
import random
import pandas as pd

# Read datasets

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
    
    elif dataset_type == "fill_mask":
        path = "./data/fill_mask.csv"
        df = pd.read_csv(path, encoding='utf-8')
        return df
    elif dataset_type == "jailbreaks":
        jailbreaks = []
        path = "./data/jailbreaks.json"

        with open(path) as json_file:
            data = json.load(json_file)

            for p in data['jailbreak']:
                jailbreaks.append(p)

        return jailbreaks
    elif dataset_type == "questions":
        csv_path = './data/do_not_answer_en.csv'

        df = pd.read_csv(csv_path)

        return df['question'].tolist()

    else:
        raise ValueError("Unsupported dataset type")

# Get random data

def choose_random_data(dataset):

    if dataset == "jailbreaks":
        return get_random_jailbreak()
    elif dataset == "questions":
        return get_random_question()
    elif dataset == "squad":
        return get_random_squad()
    elif dataset == "IMdb":
        return get_random_IMdb()
    elif dataset == "toxic":
        return get_random_toxic()
    elif dataset == "spam":
        return get_random_spam()
    elif dataset == "fill_mask":
        return get_random_fill_mask()
    
def get_random_squad():
    squad = read_dataset("squad")
    return random.choice(squad['question'].tolist())

def get_random_IMdb():
    IMdb = read_dataset("IMdb")
    return random.choice(IMdb['Overview'].tolist())

def get_random_toxic():
    toxic = read_dataset("toxic")
    return random.choice(toxic['comment_text'].tolist())

def get_random_spam():
    spam = read_dataset("spam")
    return random.choice(spam['CONTENT'].tolist())

def get_random_fill_mask():
    fill_mask = read_dataset("fill_mask")
    return random.choice(fill_mask['input'].tolist())

def get_random_jailbreak():
    jailbreaks = read_dataset("jailbreaks")

    res = random.choice(jailbreaks)
    while "[INSERT PROMPT HERE]" not in res:
        res = random.choice(jailbreaks)

    return res

def get_random_question():

    questions = read_dataset("questions")

    return random.choice(questions)
