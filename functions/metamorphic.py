from functions.readDatasets import choose_random_data, read_dataset
from functions.models import request_to_model, request_to_bing
from functions.distances import similarity_fill_mask, get_distance_answers
import time
import inspect


def input_equivalence_mrt(model,original_input, perturbed_input):
    if (model[0] != 'toxic' and model[0] != 'spam'):
        return "This model is not supported for this test"

    original_output = request_to_model(model, original_input)[0][0]['label']
    perturbed_output = request_to_model(model, perturbed_input)[0][0]['label']        
    return original_output == perturbed_output

async def equivalence_set_mrt(model, input1):
    
    original_output = request_to_model(model, input1)[0][0]['label']    
    llms_outputs = []

    if (model[0] == 'toxic'):
        
        if original_output == "neutral":
            original_output = "no"
        elif original_output == "non-toxic":
            original_output = "no"
        elif original_output == "toxic":
            original_output = "yes"
        
        bing_output = await request_to_bing(input1, type="toxic")
        #bard_output = request_to_bard(input1, "toxic")
        llms_outputs.append(bing_output.lower())
        #llms_outputs.append(bard_output.lower())
        
    elif (model[0] == 'spam'):
        
        if original_output == "No spam":
            original_output = "no"
        elif original_output == "Ham":
            original_output = "no"
        elif original_output == "Spam":
            original_output = "yes"
        
        bing_output = await request_to_bing(input1, type="spam")
        #bard_output = request_to_bard(input1, "spam")
        llms_outputs.append(bing_output.lower())
        #llms_outputs.append(bard_output.lower())
        
    else: 
        return "This model is not supported for this test"

    for llm_output in llms_outputs:
        if original_output != llm_output:
            return False
        
    return True

    
async def distance_set_mrt(model, original_input, perturbance,threshold=70):
    
    if (model[0] == 'fillmask'):
        ouput_1 = request_to_model(model, original_input)
        output_2 = await request_to_bing(original_input, type="fillmask")
        
        similarity_metric_1_2 = similarity_fill_mask(ouput_1, output_2) * 10
        return similarity_metric_1_2 > threshold
     
    elif (model[0] == 'translate' or model[0] == 'summarize' or model[0] == 'q&a'):
        output_1 = request_to_model(model, original_input)
        output_2 = await request_to_bing(original_input, type=perturbance)

        similarity_metric_1_2 = await get_distance_answers(output_1, output_2, 0)
        return similarity_metric_1_2 > threshold



def input_discrepancy_mrt(model,original_imput, perturbed_input):
    
    if (model[0] != 'toxic' and model[0] != 'spam'):
        return "This model is not supported for this test"
     
    original_output = request_to_model(model, original_imput)[0][0]['label']
    perturbed_output = request_to_model(model, perturbed_input)[0][0]['label']   
    
    return original_output != perturbed_output

async def input_distance_mrt(model, original_input, perturbed_input, threshold = 50):
    
    if (model[0] == 'fillmask'):
        ouput_1 = request_to_model(model, original_input)
        ouput_2 = request_to_model(model, perturbed_input)
        similarity_metric_1_2 = similarity_fill_mask(ouput_1, ouput_2) * 10
        return similarity_metric_1_2 > threshold 
    elif (model[0] == 'translate' or model[0] == 'summarize' or model[0] == 'q&a'):
        output_1 = request_to_model(model, original_input)
        output_2 = request_to_model(model, perturbed_input)
        
        similarity_metric_1_2 = await get_distance_answers(output_1, output_2, 1)
        return similarity_metric_1_2 > threshold
    
async def prompt_distance_mrt(model, original_prompt, perturbed_prompt, original_input, threshold = 70):
    
    if (model == 'bing'): 
        output_original_prompt = await request_to_bing(original_input,type="personalised", prompt = original_prompt)
        output_perturbed_prompt = await request_to_bing(original_input,type="personalised", prompt = perturbed_prompt)

        return await get_distance_answers(output_original_prompt, output_perturbed_prompt, 0) > threshold
    else:
        return "This model is not supported for this test"
    
async def calculate_M_ASR(model, disturbation_func, quality_attribute, perturbance, change_meaning = False, iterations = 5):
    fulfilled_relations = 0
    evaluated_relations = 0
    start = time.time()
    
    '''
    if (model == 'bing'):
        for _ in range(iterations):

            text = choose_random_data('squad')
            disturbed = disturbation_func(text)

            if (quality_attribute == 'Robustness'):
                question = choose_random_data('questions')
                fulfilled_relations += input_distance_mrt(model, text, disturbed) 
                evaluated_relations += 1

            elif (quality_attribute == 'Fairness'):
                

            elif (quality_attribute == 'Non-determinism'):
                
            elif (quality_attribute == 'Efficiency'):
                
            elif (quality_attribute == 'Attack-resistance'):
                prompt = choose_random_data('jailbreaks')
                prompt = prompt.replace("[INSERT PROMPT HERE]", "")
                fulfilled_relations += prompt_distance_mrt(model,"",prompt,question)
                evaluated_relations += 1
    '''
        
    if (model[0]=='fillmask'):

        for _ in range(iterations):
            text = choose_random_data('wikipedia')
            if inspect.iscoroutinefunction(disturbation_func):
                disturbed = await disturbation_func(text)
            else:
                disturbed = disturbation_func(text)
        
            if (quality_attribute == 'Robustness'):
                fulfilled_relations += await input_distance_mrt(model, text, disturbed) 
                evaluated_relations += 1
            
            elif (quality_attribute == 'Fairness' or quality_attribute == 'Non-determinism'):
                fulfilled_relations += await distance_set_mrt(model, text, perturbance)
                evaluated_relations += 1
            else:
                return "This quality attribute is not supported for this test"
    
    elif (model[0]=='translate'):
        for _ in range(iterations):

            text = choose_random_data('IMdb')
            if inspect.iscoroutinefunction(disturbation_func):
                disturbed = await disturbation_func(text)
            else:
                disturbed = disturbation_func(text)
        
            if (quality_attribute == 'Robustness'):
                fulfilled_relations += await input_distance_mrt(model, text, disturbed) 
                evaluated_relations += 1
            
            elif (quality_attribute == 'Fairness' or quality_attribute == 'Non-determinism'):
                fulfilled_relations += await distance_set_mrt(model, text, perturbance)
                evaluated_relations += 1
            else:
                return "This quality attribute is not supported for this test"


    elif (model[0]=='summarize'):
        for _ in range(iterations):

            text = choose_random_data('IMdb')
            if inspect.iscoroutinefunction(disturbation_func):
                disturbed = await disturbation_func(text)
            else:
                disturbed = disturbation_func(text)
            if (quality_attribute == 'Robustness'):
                fulfilled_relations += await input_distance_mrt(model, text, disturbed) 
                evaluated_relations += 1
            
            elif ( quality_attribute == 'Non-determinism'):
                fulfilled_relations += await distance_set_mrt(model, text, perturbance)
                evaluated_relations += 1
            else:
                return "This quality attribute is not supported for this test"
    
    elif(model[0]=='toxic' or model[0]=='spam'):
        
        for _ in range(iterations):
        
            text = choose_random_data('toxic') if model[0]=='toxic' else choose_random_data('spam')
            if inspect.iscoroutinefunction(disturbation_func):
                disturbed = await disturbation_func(text)
            else:
                disturbed = disturbation_func(text)
        
            if (quality_attribute == 'Robustness'):
                if change_meaning:
                    fulfilled_relations += input_discrepancy_mrt(model,text,disturbed)
                    evaluated_relations += 1
                else:
                    fulfilled_relations += input_equivalence_mrt(model,text,disturbed)
                    evaluated_relations += 1
            
            elif (quality_attribute == 'Fairness' or quality_attribute == 'Non-determinism'):
                fulfilled_relations += await equivalence_set_mrt(model,text)
                evaluated_relations += 1
    
    else:
        return "This model is not supported for this test"
    
        
    '''
    for text in texts:
        disturbed = disturbation_func(text)  
        
        if model[0] == 'q&a' or model[0] == 'translate' or model[0] == 'fillmask' or model[0] == 'summarize':
            fulfilled_relations += input_distance_mrt(model, text, disturbed) 
            evaluated_relations += 1
            if model[0] == 'q&a':
                fulfilled_relations += prompt_distance_mrt(model,text,disturbed,original_prompt,perturbed_prompt) 
                evaluated_relations += 1
        elif model[0] in ['toxic', 'spam']:
            fulfilled_relations += input_equivalence_mrt(model,text,disturbed)
            evaluated_relations += 1
        elif model[0] == 'q&a' or model[0] == 'spam':
            fulfilled_relations += input_discrepancy_mrt(model,text,disturbed)
            evaluated_relations += 1
        elif model[0] in ['spam', 'toxic']:
            fulfilled_relations += equivalence_set_mrt(model,text)
            evaluated_relations += 1
        elif model[0] == 'q&a' or model[0] == 'translate' or model[0] == 'fillmask' or model[0] == 'summarize':
            res_dict = distance_set_mrt(model, text, perturbance)
            res = any(res_dict.values())
            fulfilled_relations += res
            evaluated_relations += 1
    '''


    if evaluated_relations == 0:
        return 0 

    m_asr = fulfilled_relations / evaluated_relations
    return m_asr, time.time() - start