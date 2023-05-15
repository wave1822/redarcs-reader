import sys
import os
from datetime import datetime
import json
import html

def format_json(input_file, output_file):
    input_filename = os.path.splitext(input_file)[0]
    json_objects = {}

    # Read the JSON file line by line and parse each JSON object separately
    with open(input_file, 'r') as file:
        for line in file:
            try:
                json_data = json.loads(line)
                author = json_data.get("author")
                author_flair_text = json_data.get("author_flair_text")
                created_utc = json_data.get("created_utc")
                created_utc = datetime.fromtimestamp(int(created_utc))
                created_utc = created_utc.strftime("%d/%m/%Y")
                body = json_data.get("body")
                link_id = json_data.get("link_id")

                formatted_json = {
                    "author": author,
                    "created_utc": created_utc,
                    "Comment": body,
                }

                if author_flair_text is not None:
                    formatted_json["author_flair_text"] = author_flair_text

                if link_id not in json_objects:
                    json_objects[link_id] = []
                json_objects[link_id].append(formatted_json)

            except json.JSONDecodeError:
                # Ignore lines that do not contain valid JSON
                pass

    # Create the HTML output
    html_content = f'''
    <html>
    <head>
        <title>Comments</title>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 20px; }}
            h1 {{ font-size: 18px; margin-bottom: 5px; }}
            p {{ margin-top: 0; }}
            pre {{ background-color: #f4f4f4; padding: 10px; white-space: pre-wrap; }}
        </style>
    </head>
    <body>
        <h1>Comments</h1>
    '''

    # Iterate over the grouped JSON objects and add them to the HTML output
    for link_id, objects in json_objects.items():
        formatted_link_id = f"https://reddit.com/r/{json_data['subreddit']}/comments/{link_id[3:]}"
        html_content += f'''
        <h2>Permalink: {formatted_link_id}</h2>
        <div>
            <pre>{json.dumps(objects, indent=4).replace('"', '')}</pre>
        </div>
        '''

    html_content += '''
    </body>
    </html>
    '''

    # Write the HTML content to the output_file
    with open(output_file, 'w') as file:
        file.write(html_content)

# Check if the required arguments are provided
if len(sys.argv) < 2:
    print("Usage: python script.py <input_file>")
else:
    input_file = sys.argv[1]
    output_file = f"{os.path.splitext(input_file)[0]}.html"
    format_json(input_file, output_file)
