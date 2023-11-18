import sqlite3
import json
from datetime import datetime

def create_table(cursor, table_name):
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (title TEXT, message TEXT, author TEXT, timestamp TEXT)")

def insert_data(cursor, table_name, title, message, author, timestamp):
    cursor.execute(f"INSERT INTO {table_name} (title, message, author, timestamp) VALUES (?, ?, ?, ?)", (title, message, author, timestamp))

def json_to_sqlite(json_file_path, db_file_path, table_name):
    with open(json_file_path, 'r') as f:
        json_data = json.load(f)

    conn = sqlite3.connect(db_file_path)
    c = conn.cursor()

    # Create table
    create_table(c, table_name)

    # Insert data
    for entry in json_data:
        title = entry.get('title', 'N/A')
        create_time = entry.get('create_time', None)
        if create_time:
            timestamp = datetime.fromtimestamp(create_time).strftime('%Y-%m-%d %H:%M:%S')
        else:
            timestamp = 'N/A'

        mapping = entry.get('mapping', {})
        for key, value in mapping.items():
            message_data = value.get('message') if value else None
            if message_data:
                author_data = message_data.get('author', {})
                author = author_data.get('role', 'N/A')
                content_data = message_data.get('content', {})
                parts = content_data.get('parts', [])
                message = ' '.join(parts)  # Assuming parts is a list of strings
                insert_data(c, table_name, title, message, author, timestamp)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    json_file_path = 'conversations.json'
    db_file_path = 'conversations.json.db'
    table_name = 'message'
    json_to_sqlite(json_file_path, db_file_path, table_name)
