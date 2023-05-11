import markdown
import argparse 
import glob
from mdutils import to_unicode, utf8, clean_list

def get_title_summary_by_md_file(file):
    with open(file) as f:
        source = f.read()

        md1 = markdown.Markdown(extensions=["markdown.extensions.meta"])
        md1.convert(source)
        md_meta = getattr(md1, "Meta")
        return md_meta["title"][0], md_meta["summary"][0]
    

def parse_all_posts(folder):
    # here we parse all posts
    if folder=="":
        return ""
    
    links = [] 
    for file in glob.glob(f"{folder}/*"):

        title, summary = get_title_summary_by_md_file(file)
        file = file[len(folder):]
        links.append((file[1:-2]+"html", title, summary))
    
    content = ""
    for l in links:
        content += "\n <div class='pages'>"
        content += f"\n <h2><a href='{l[0]}'>{l[1]}</a></h2>"
        content += f"\n <p> {l[2]}</p>"
        content += "\n<div>"

    return content 


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", help="folder to read post from", required=True)
    parser.add_argument("--template", help="template", required=True)
    parser.add_argument("--output", help="output file", required=True)

    args = parser.parse_args()

    content = parse_all_posts(args.folder)
    with open(args.template, "r") as f:
        _tpl = f.read()
        _tpl = to_unicode(_tpl)

    html = _tpl.format(content=content)
    html = utf8(html)
    with open(args.output, "wb") as f:
            f.write(html)


   