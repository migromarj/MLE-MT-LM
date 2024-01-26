import re
import markdown

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