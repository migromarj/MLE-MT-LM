from functions.models import request_to_model
from functions.utils import agregate_index
from functions.distances import similarity_fill_mask
from functions.models import request_to_bing

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