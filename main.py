import os
import feedparser
import requests
from datetime import datetime

FOLDER = "exports"
FORMATS = ["html", "epub"]
FEEDS = [
  'https://archiveofourown.org/tags/16861914/feed.atom', # Generations from Exile Tribe (Band)
  'https://archiveofourown.org/tags/19984521/feed.atom', # The Rampage from Exile Tribe (Band)
  'https://archiveofourown.org/tags/40234885/feed.atom', # Fantastics from Exile Tribe (Band)
  'https://archiveofourown.org/tags/17343258/feed.atom', # EXILE (Japan Band)
  'https://archiveofourown.org/tags/12153406/feed.atom', # J Soul Brothers (Band)
  'https://archiveofourown.org/tags/65865229/feed.atom', # Sexy Zone (Band)
  'https://archiveofourown.org/tags/5650746/feed.atom', # SixTONES (Band)
  'https://archiveofourown.org/tags/65865400/feed.atom', # Hey! Say! JUMP (Band)
  'https://archiveofourown.org/tags/21592518/feed.atom', # HiGH&LOW: the Story of S.W.O.R.D. (TV)
  'https://archiveofourown.org/tags/21592494/feed.atom', # HiGH&LOW (Movies)
  'https://archiveofourown.org/tags/72641245/feed.atom', # Sato Taiki/Yamamoto Sekai
]

def saveFiles(export_dir, id, title, author):
    print(f"savign work {id}, {title} by {author}")
    for format in FORMATS:
        os.makedirs(os.path.join(export_dir, format), exist_ok = True)
        download_url = f"https://archiveofourown.org/downloads/{id}/{id}.{format}" 
        downlad_filename = f"{id}_{title}_{author}.{format}".replace('/', '_')
        r = requests.get(download_url)
        with open(os.path.join(export_dir, format, downlad_filename), 'wb') as f:
            f.write(r.content)

def parse(feed):
    print(f"parsing feed {feed}")
    d = feedparser.parse(feed)
    # Grab title from feed and make folder
    source = d['feed']['title']
    export_dir = os.path.join(FOLDER, source)
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
    r = requests.get(feed)  
    with open(os.path.join(export_dir, 'snapshot.atom'), 'wb') as f:
        f.write(r.content)

if __name__ == "__main__":
    for feed in FEEDS:
        parse(feed)
