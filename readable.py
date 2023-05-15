import json
import sys
from datetime import datetime
import html
import os


def main(filename):
    with open(filename, "r") as f:
        posts = []
        for line in f:
            try:
                post = json.loads(line)
                posts.append(post)
            except:
                continue

    html_output = "<html><head><title>Posts</title></head><body>"

    for post in posts:
        title = post['title']
        author = post['author']
        permalink = f"https://reddit.com{post['permalink']}"
        created_utc = int(post['created_utc'])  # Convert to integer
        created_date = datetime.utcfromtimestamp(created_utc).strftime('%d/%m/%Y')
        selftext = post['selftext']
        selftext = html.unescape(selftext).replace('&#x200B;', '')
        selftext = html.unescape(selftext).replace('**', '')

        html_content = f"<h2>{title}</h2>"
        url = post.get('url')
        if url is not None and selftext != "[deleted]" and "comments" not in url:
            html_content += f"<img src='{url}' loading='lazy'><br><br>"

        html_content += f"<p>Author: {author}<br>Created Date: {created_date}<br>Permalink: <a href='{permalink}'>{permalink}</a></p><p>{selftext}</p>"
        html_output += html_content

    html_output += "</body></html>"

    # Get the base name of the input file
    base_filename = os.path.splitext(os.path.basename(filename))[0]
    output_filename = f"{base_filename}.html"

    with open(output_filename, "w") as f:
        f.write(html_output)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        main(filename)
    else:
        print("Usage: python your_program.py filename")
