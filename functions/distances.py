import re
from functions.models import request_to_bard, request_to_bing
from functions.utils import calculate_distance, get_percentage
from contexto.comparacion import Similitud, Distancia, DiferenciaStrings
from contexto.vectorizacion import VectorizadorFrecuencias, VectorizadorHash

def similarity_fill_mask(response1, response2):
    total_elements = len(response1)
    total_distance = 0

    for element1 in response1:
        hash_element = False
        for element2 in response2:
            if element1['token_str'].strip() == element2['token_str'].strip():
                prob_element1 = element1['score']
                prob_element2 = element2['score']
                distance_between_indices = calculate_distance(element1, element2)
                total_distance += (distance_between_indices * abs(prob_element1 - prob_element2)) / (total_elements - 1)
                hash_element = True
                break

        if not hash_element:
            total_distance += 1


    return 1 - (total_distance/5)

async def get_distance_answers(input1,input2,mode = 0, iteration = 0):
    if (mode == 0):
        response_bing = await request_to_bing(input1,input2,type="compare")
        if (len(re.findall(r'\d+%', response_bing)) > 0):
            #response_bard = request_to_bard(input,input2, "compare")
            return get_percentage(response_bing)
            #percentage_bard = get_percentage(response_bard)
            #mean = (percentage_bing + percentage_bard) / 2
        else:
            if iteration < 5:
                return await get_distance_answers(input1,input2,mode,iteration + 1)
        return 0
    else:
        
        # Similarity
        v_bow =  VectorizadorFrecuencias()
        v_tf =  VectorizadorFrecuencias(tipo='tfidf', idf=False)
        v_tfidf = VectorizadorFrecuencias(tipo='tfidf')
        v_hashing = VectorizadorHash() 
        test_texts = [input1,input2]
        v_bow.fit(test_texts)
        v_tf.fit(test_texts)
        v_tfidf.fit(test_texts)

        vectors = {}
        keys = ['bow', 'tf', 'tfidf', 'hash']
        for i, v in enumerate([v_bow, v_tf, v_tfidf, v_hashing]):
            vectors[keys[i]] = v.vectorizar(test_texts)

        s_bow = Similitud(v_bow)
        s_tf = Similitud(v_tf)
        s_tfidf = Similitud(v_tfidf)
        s_hashing = Similitud(v_hashing)

        cosine_bow = s_bow.coseno(test_texts)
        percentage_bow = cosine_bow[0][1] * 100
        cosine_tf = s_tf.coseno(test_texts)
        percentage_tf = cosine_tf[0][1] * 100
        cosine_hashing = s_hashing.coseno(test_texts)
        percentage_hashing = cosine_hashing[0][1] * 100
        cosine_tfidf = s_tfidf.coseno(test_texts)
        percentage_tfidf = cosine_tfidf[0][1] * 100

        # Difference
        d_hashing = Distancia(v_hashing)
        hamming_hashing = 1- d_hashing.hamming(test_texts)[0][1]

        # dictionary of "Difference"
        difference = {'hash': hamming_hashing}
        similarity = {'bow': percentage_bow, 'tf': percentage_tf, 'tfidf': percentage_tfidf, 'hash': percentage_hashing}
        return similarity['hash']