import re
import sys,os
print(sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))))
from imageGenration import image_API
def promt(text):
# Regular expression pattern to find the placeholder and the text inside quotes
    pattern = r'##promt##\s*"([^"]+)"'

    # Replace all occurrences using a lambda function that calls image_API for each prompt
    new_text = re.sub(pattern, lambda m: str(image_API.get_image(m.group(1))), text)

    return new_text
