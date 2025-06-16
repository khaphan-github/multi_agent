import json
import re

def detect_json_from_string(input_string):
    """
    Detects and extracts JSON from a given string.

    Parameters:
        input_string (str): The string to check for JSON content.

    Returns:
        dict or list: The parsed JSON object if valid JSON is found.
        None: If no valid JSON is found.
    """
    try:
        # Use regex to find a potential JSON object or array in the string
        match = re.search(r'({.*}|\[.*\])', input_string)
        if match:
            # Try to parse the matched JSON substring
            return json.loads(match.group(0))
    except json.JSONDecodeError:
        pass
    return None