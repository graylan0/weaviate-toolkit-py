import weaviate
import json

# Increase the timeout value (e.g., 120 seconds)
client = weaviate.Client("http://localhost:8080", timeout_config=(72000, 72000))

with open('conversations.json', 'r') as file:
    data = json.load(file)

for item in data:
    if 'id' in item:
        item['message_id'] = item.pop('id')

    if 'mapping' in item and isinstance(item['mapping'], dict):
        item['mapping'] = json.dumps(item['mapping'])

    if 'moderation_results' in item and isinstance(item['moderation_results'], list):
        item['moderation_results'] = json.dumps(item['moderation_results'])

    client.data_object.create(item, "ChatGPTHistory")
