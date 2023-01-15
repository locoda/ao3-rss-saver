import os
import sys
import tomli
import feedparser
import requests
from datetime import datetime

FOLDER = "exports"
FORMATS = ["html", "epub"]

def saveFiles(export_dir, id, title, author):
    sys.stdout.write(f"saving work {id}, {title} by {author}\r\n")
    for format in FORMATS:
        os.makedirs(os.path.join(export_dir, format), exist_ok = True)
        download_url = f"https://archiveofourown.org/downloads/{id}/{id}.{format}" 
        downlad_filename = f"{id}_{title}_{author}.{format}".replace('/', '_')
        r = requests.get(download_url)
        with open(os.path.join(export_dir, format, downlad_filename), 'wb') as f:
            f.write(r.content)

def parse(feed):
    sys.stdout.write(f"parsing feed {feed['name']}: {feed['url']}\r\n")
    d = feedparser.parse(feed['url'])
    # Grab feed name and make folder
    export_dir = os.path.join(FOLDER, feed['name'])
    os.makedirs(export_dir, exist_ok = True)
    # Grab last update time from feed
    updated = datetime.fromisoformat(d['feed']['updated'][:-1])
    last_updated = datetime.min
    snapshot_path = os.path.join(export_dir, 'snapshot.atom')
    if (os.path.exists(snapshot_path)):
        snapshot = feedparser.parse(snapshot_path)
        last_updated = datetime.fromisoformat(snapshot['feed']['updated'][:-1])
        if (updated <= last_updated):
            # No new item is found
            return
    # Save New Items
    for entry in d.entries:
        if (datetime.fromisoformat(entry.updated[:-1]) > last_updated):
            id = entry.id.split('Work/')[1]
            title = entry.title
            author = entry.author
            saveFiles(export_dir, id, title, author)
    # Save feed snapshot
    r = requests.get(feed['url'])  
    with open(os.path.join(export_dir, 'snapshot.atom'), 'wb') as f:
        f.write(r.content)

if __name__ == "__main__":
    with open("config.toml", "rb") as f:
        config = tomli.load(f)
    
    for feed in config['feeds']:
        parse(feed)
