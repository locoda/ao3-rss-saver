import os
import sys
import tomli
from bs4 import BeautifulSoup
import requests
import json
import time

FOLDER = "exports"
FORMAT = "html"


def saveFiles(export_dir, id, title, author):
    sys.stdout.write(f"saving work {id}, {title} by {author}\r\n")
    download_url = f"https://archiveofourown.org/downloads/{id}/{id}.{FORMAT}?updated_at={int(time.time())}"
    downlad_filename = f"{id}_{title}_{author}.{FORMAT}".replace('/', '_')
    r = requests.get(download_url)
    with open(os.path.join(export_dir, downlad_filename), 'wb') as f:
        f.write(r.content)


def parse(feed):
    sys.stdout.write(f"parsing feed {feed['name']}: {feed['url']}\r\n")

    # Grab feed name and make folder
    export_dir = os.path.join(FOLDER, feed['name'])
    os.makedirs(export_dir, exist_ok=True)

    # Grab last metadata if exist
    if os.path.exists(os.path.join(export_dir, 'meta.json')):
        with open(os.path.join(export_dir, 'meta.json'), "r") as f:
            old_metadata = json.load(f)
    else:
        old_metadata = {}

    # Grab current webpage
    soup = BeautifulSoup(requests.get(feed['url']).content, "html.parser")
    entries = soup.select("ol.work.index.group > li")
    metadata = {}
    for entry in entries:
        title = entry.select('h4 > a')[0].get_text()
        try:
            author = entry.select('h4 > a')[1].get_text()
        except IndexError:
            author = "Anonymous"  # No link on author
        id = entry.attrs['id'].lstrip('work_')
        try:
            words = int(entry.select_one('dd.words').text.replace(',', ''))
        except ValueError:
            words = 0 # No words - Seems like AO3 Bug 
        metadata[id] = words
        if old_metadata.get(id) != words:
            # Download if old metadata doesn't match current word
            saveFiles(export_dir, id, title, author)

    # Save Metadata for next crawl
    with open(os.path.join(export_dir, 'meta.json'), "w") as f:
        json.dump(metadata, f)


if __name__ == "__main__":
    with open("config.toml", "rb") as f:
        config = tomli.load(f)

    for feed in config['feeds']:
        parse(feed)
