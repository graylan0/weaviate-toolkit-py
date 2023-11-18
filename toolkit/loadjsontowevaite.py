import weaviate
import json

# Initialize Weaviate client
client = weaviate.Client("http://localhost:8080")

# Define the schema for ChatGPTHistory
schema = {
    "classes": [
        {
            "class": "ChatGPTHistory",
            "properties": [
                {"name": "title", "dataType": ["string"]},
                {"name": "create_time", "dataType": ["number"]},
                {"name": "update_time", "dataType": ["number"]},
                {"name": "mapping", "dataType": ["text"]}
            ]
        }
    ]
}

# Create the schema in Weaviate
client.schema.create(schema)

# Load JSON data
with open('conversations.json', 'r') as file:
    data = json.load(file)

# Insert data into Weaviate
for item in data:
    client.data_object.create(item, "ChatGPTHistory")