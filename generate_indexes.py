from yattag import Doc
import os

def generate_index(dir):
    index_file = os.path.join(dir, 'index.html')
    title = dir.split('/')[-1]
    doc, tag, text, line = Doc().ttl()
    doc.asis('<!DOCTYPE html>')
    with tag('html'):
        doc.attr(title=title)
        with tag('head'):
            doc.stag('meta', charset='utf-8')
            doc.stag('meta', name="viewport", content="width=device-width, initial-scale=1")
            doc.stag('link', rel='stylesheet', href='https://unpkg.com/@picocss/pico@latest/css/pico.min.css')
        with tag('title'):
          text(title)
        with tag('body'):
            with tag('main', klass="container"):
                with tag('h1'):
                    text(f"{title}")
                with tag('p'):
                    with tag('a', href='..'):
                        text('..')
                directories = [d for d in os.listdir(dir) if os.path.isdir(os.path.join(dir, d))]
                files = sorted([d for d in os.listdir(dir) if os.path.isfile(os.path.join(dir, d))], reverse=True)
                for item in directories + files:
                    if (item == 'index.html'): 
                        continue
                    if (item == 'snapshot.atom'): 
                        continue
                    if (item.startswith('.')):
                        continue
                    with tag('p'):
                        with tag('a', href=item):
                            text(item)
                    

    with open(index_file, 'w') as f:
        f.write(doc.getvalue())
    
    for item in directories:
        generate_index(os.path.join(dir, item))

if __name__ == "__main__":
    generate_index('exports')