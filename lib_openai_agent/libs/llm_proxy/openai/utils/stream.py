"""
Stream related utilities.
"""
import re
import json
import uuid

'''

id: 8741e60e-4ab7-4dc9-b172-3000fb9ca8ee
data: {"index": 0, "type": "text", "text": {"annotations": null, "value": " \ud83d\ude0a"}, "is_error": "false", "isLast": "false", "typing": "true"}

id: 52691622-d5a4-4f3f-8658-c72c8c6b0d87
data: {"isLast": "true", "typing": "false", "is_error": "false", "thread_id": "thread_gf8wrho6rotPjNKf4GrjYOy8"}
'''


def process_message(message, is_last, thread_id):
    if is_last:
        end_message = {
            "isLast": "true",
            "typing": "false",
            "is_error": "false",
            "thread_id": thread_id
        }
        return f"id: {uuid.uuid4()}\ndata: {json.dumps(end_message)}\n\n"
    else:
        json_data = message
        if hasattr(message, 'model_dump_json'):
            json_data = message.model_dump_json()

        if isinstance(json_data, str) and json_data.startswith('data:'):
            return json_data
        else:
            json_data = json.loads(json_data)
            json_data["is_error"] = "false"
            json_data["isLast"] = "false"
            json_data["typing"] = "true"
            # Remove file annotation
            if json_data.get('text', {}).get('annotations') is not None:
                json_data['text']['annotations'] = []
                json_data['text']['value'] = re.sub(
                    r'【.*?】', '', json_data['text']['value'])
            return f"id: {uuid.uuid4()}\ndata: {json.dumps(json_data)}\n\n"
