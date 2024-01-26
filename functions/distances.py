from functions.utils import calculate_distance

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