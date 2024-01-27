from contexto.comparacion import Similitud, Distancia, DiferenciaStrings
from contexto.vectorizacion import *
from functions.utils import get_percentaje, request_to_bard, request_to_bing, request_to_model, agregate_index
from functions.models import request_to_model, request_to_bing
from functions.distances import similarity_fill_mask

def input_equivalence_mrt(model,original_imput, perturbed_input):
    
    if (model[0] != 'toxic' and model[0] != 'spam'):
        return "This model is not supported for this test"
     
    original_output = request_to_model(model, original_imput)[0][0]['label']
    perturbed_output = request_to_model(model, perturbed_input)[0][0]['label']        
    
    return original_output == perturbed_output

async def equivalence_set_mrt(model, input):
    
    original_output = request_to_model(model, input)[0][0]['label']    
    llms_outputs = []

    if (model[0] == 'toxic'):
        
        if original_output == "neutral":
            original_output = "no"
        elif original_output == "non-toxic":
            original_output = "no"
        elif original_output == "toxic":
            original_output = "yes"
        
        bing_output = await request_to_bing(input, "toxic")
        bard_output = request_to_bard(input, "toxic")
        llms_outputs.append(bing_output.lower())
        llms_outputs.append(bard_output.lower())
        
    elif (model[0] == 'spam'):
        
        if original_output == "No spam":
            original_output = "no"
        elif original_output == "Ham":
            original_output = "no"
        elif original_output == "Spam":
            original_output = "yes"
        
        bing_output = await request_to_bing(input, "spam")
        bard_output = request_to_bard(input, "spam")
        llms_outputs.append(bing_output.lower())
        llms_outputs.append(bard_output.lower())
        
    else: 
        return "This model is not supported for this test"

    for llm_output in llms_outputs:
        if original_output != llm_output:
            return False
        
    return True

async def get_distance_answers(input,input2,mode = 0):
    if (mode == 0):
        response_bing = await request_to_bing(input,input2,"compare")
        response_bard = request_to_bard(input,input2, "compare")
        percentaje_bing = get_percentaje(response_bing)
        percentaje_bard = get_percentaje(response_bard)
        mean = (percentaje_bing + percentaje_bard) / 2
        return mean
    else:
        
        # Similarity
        v_bow =  VectorizadorFrecuencias()
        v_tf =  VectorizadorFrecuencias(tipo='tfidf', idf=False)
        v_tfidf = VectorizadorFrecuencias(tipo='tfidf')
        v_hashing = VectorizadorHash()
        test_texts = [input,input2]
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
        return difference, similarity
    
async def distance_set_mrt(original_input, model='q&a', mode=0, threshold=70):
    
    if (model[0] == 'fillmask'):
        return "TODO" # TODO 
    elif (model[0] == 'translate' or model[0] == 'summarize' or model == 'q&a'):
        output_original_input = request_to_model(model, original_input)
        bing_output = await request_to_bing(original_input, model[0])
        bard_output = request_to_bard(original_input, model[0])
        output_original_input = next(iter(output_original_input[0].values()))
        if (mode == 0):
            similarity_bing_output = await get_distance_answers(output_original_input, bing_output, 0)
            similarity_bard_output = await get_distance_answers(output_original_input, bard_output, 0)
            return {"bing": similarity_bing_output > threshold, "bard": similarity_bard_output > threshold}
        else:
            similarity_other_bing = await get_distance_answers(output_original_input, bing_output, 1)
            similarity_other_bard = await get_distance_answers(output_original_input, bard_output, 1)
            return {"bing": similarity_other_bing > threshold, "bard": similarity_other_bard > threshold}

def calculate_M_ASR(model, disturbation_func, texts):
    fulfilled_relations = 0
    evaluated_relations = 0

    for text in texts:
        disturbed = disturbation_func(text)  
        
        if model[0] == 'q&a' or model[0] == 'translate' or model[0] == 'fillmask' or model[0] == 'summarize':
            fulfilled_relations += input_distance_mrt(disturbed) #TODO: Complete this function
            evaluated_relations += 1
            if model[0] == 'q&a':
                fulfilled_relations += prompt_distance_mrt(disturbed) #TODO: Complete this function
                evaluated_relations += 1
        elif model[0] in ['toxic', 'spam']:
            fulfilled_relations += input_equivalence_mrt(model,text,disturbed)
            evaluated_relations += 1
        elif model[0] == 'q&a' or model[0] == 'spam':
            fulfilled_relations += input_discrepancy_mrt(disturbed)
            evaluated_relations += 1
        elif model[0] in ['spam', 'toxic']:
            fulfilled_relations += equivalence_set_mrt(model,disturbed)
            evaluated_relations += 1
        elif model[0] == 'q&a' or model[0] == 'translate' or model[0] == 'fillmask' or model[0] == 'summarize':
            res_dict = distance_set_mrt(text, model=model[0])
            res = any(res_dict.values()) #TODO: check if this is correct
            fulfilled_relations += res
            evaluated_relations += 1


    if evaluated_relations == 0:
        return 0 

    m_asr = fulfilled_relations / evaluated_relations
    return m_asr

def input_discrepancy_mrt(model,original_imput, perturbed_input):
    
    if (model[0] != 'toxic' and model[0] != 'spam'):
        return "This model is not supported for this test"
     
    original_output = request_to_model(model, original_imput)[0][0]['label']
    perturbed_output = request_to_model(model, perturbed_input)[0][0]['label']
    print(original_output)
    print(perturbed_output)       
    
    return original_output != perturbed_output

def input_distance_mrt(model, original_prompt, original_input, perturbed_input, threshold = 0.5):
    
    if (model[0] == 'fillmask'):
        output_original_input = request_to_model(model, original_prompt + original_input)
        output_perturbed_input = request_to_model(model, original_prompt + perturbed_input)
        agregate_index(output_original_input)
        agregate_index(output_perturbed_input)

        print(output_original_input)
        print(output_perturbed_input)
        similarity_metric = similarity_fill_mask(output_original_input, output_perturbed_input)
        print(f'Distance between response1 and response2: {similarity_metric}')
        return similarity_metric > threshold
    else:
        return "This model is not supported for this test" # TODO: USE TOMÁS FUNCTION
    
def prompt_distance_mrt(model, original_prompt, perturbed_prompt, original_input, threshold = 0.5):
    
    if (model[0] == 'q&a'): 
        output_original_prompt = request_to_bing(original_input,"personalised", original_prompt)
        output_perturbed_prompt = request_to_bing(original_input,"personalised", perturbed_prompt)

        print(output_original_prompt)
        print(output_perturbed_prompt)

        # TODO: USE TOMÁS FUNCTION
    else:
        return "This model is not supported for this test"