#!/usr/bin/env python
# coding=utf-8
"""
mdtree, convert markdown to html with TOC(table of contents) tree. https://github.com/menduo/mdtree
"""
import sys, os
import glob
import markdown
from mdutils import PY3, clean_list, parse_title, to_bool, to_unicode, utf8, ImageCheckPattern
from mdparser import gen_html, prepare_static_files, parse_static_files, adjust_ext_list

_d_static_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

__all__ = ["MdTree", "convert_from_file"]


class MdTree(object):
    """
    Python markdown tree tool
    """

    def __init__(self, **kwargs):
        """
        :param kwargs:
        """
        self.ext_list = [
            "markdown.extensions.meta",
            "markdown.extensions.headerid",
            "markdown.extensions.tables",
            "markdown.extensions.toc",
            "markdown.extensions.fenced_code",
            "markdown.extensions.codehilite",
        ]

        self.title = kwargs.get("title", "")
        self._html = ""
        self.template = kwargs.get("template")
        if self.template== "":
            self.template= os.path.join(_d_static_path, "html/template.html")
        # print(f"template {self.template}", kwargs)

        self.js_list = kwargs.get("js", [])
        self.css_list = kwargs.get("css", [])
        self.ext_list.extend(kwargs.get("exts", []))
        self.ext_list = list(set(self.ext_list))

        self.by = "text"
        self.filepath = kwargs.get("filepath", None)
        self.base_dir = kwargs.get("base_dir", None)
        self.to64 = kwargs.get("to64", False)

    def adjust_config(self, meta):
        ext_list = meta.get("exts", [])
        css_list = meta.get("css", [])
        js_list = meta.get("js", [])

        self.ext_list = clean_list(list(set(self.ext_list + ext_list)))
        self.ext_list = adjust_ext_list(self.ext_list, ext_list)

        self.css_list = clean_list(list(set(self.css_list + css_list)))
        self.js_list = clean_list(list(set(self.js_list + js_list)))

        self.base_dir = meta.get("base_dir", [None])[0]
        to64_v_list = clean_list(meta.get("to64", [False]))[0]
        self.to64 = self.to64 or to_bool(to64_v_list)

        if self.by == "file" and not self.base_dir:
            self.base_dir = os.path.split(self.filepath)[0]

        self.title = self.title or meta.get("title", [""])[0]

    def parse_md_config(self, source):
        """
        parse exts config from markdown file and update the markdown object

        exts source: https://pythonhosted.org/Markdown/extensions/
        :return:
        """
        md1 = markdown.Markdown(extensions=["markdown.extensions.meta"])
        md1.convert(source)
        md_meta = getattr(md1, "Meta")

        # recreate an instance of Markdown object
        md2 = markdown.Markdown(extensions=self.ext_list)
        if self.to64:
            if not self.base_dir:
                raise ValueError(
                    "base dir is required while convert from text and enable convert local image to base64")
            md2.inlinePatterns["image_link"] = ImageCheckPattern(self.base_dir, md2)
        return md2, md_meta

    def convert(self, source, all_post_content):
        """
        convert markdown to html with TOC
        :param str source: contents of markdown file
        :return:
        """
        source = to_unicode(source)

        # parse meta、exts config
        md, md_meta = self.parse_md_config(source)
        self.adjust_config(md_meta)

        md_html = md.convert(source)
        toc = getattr(md, "toc", "")

        # prepare the basic static files
        # Umang:remove
        # css_base, js_base = prepare_static_files()
        css_base, js_base = "", ""
        # get title from init、meta、markdown source
        title = self.title or parse_title(source)

        # try to get more static files from markdown source
        css_more, js_more = parse_static_files(md_meta, self.css_list, self.js_list)

        template = self.template
        # print(css_more)

        params = {
            "title": title,
            "content": md_html,
            "css_base": css_base,
            "js_base": js_base,
            "css_more": css_more,
            "js_more": js_more,
            "toc": toc,
            "template": template,
            "all_post_content": all_post_content
        }

        self._html = gen_html(params)
        return self._html

    def convert_file(self, spath, all_post_content):
        """
        convert markdown to html with TOC
        :param str spath: path of source file
        """
        self.by = "file"
        self.filepath = os.path.expanduser(spath)
        self.base_dir = os.path.split(self.filepath)[0]

        with open(spath) as f:
            mdstring = f.read()

        return self.convert(mdstring, all_post_content)

    def save_file(self, tpath):
        """
        write to file
        :param str tpath: path of target file
        :return:
        """
        # print(self._html)
        with open(tpath, "wb") as f:
            f.write(self._html)
        return tpath


# Exported Funcs
def convert_from_file(**kwargs):
    """
    :param dict kwargs:
    :return:
    """
    source = kwargs["source"] or ""
    target = kwargs.get("target") or ""
    # print(kwargs)
    mdtree = MdTree(**kwargs)
    all_post_content = parse_all_posts(kwargs.get("md_folder"))
    html = mdtree.convert_file(source, all_post_content)
    html = utf8(html)
    if target:
        mdtree.save_file(target)
    else:
        if PY3:
            sys.stdout.buffer.write(html)
        else:
            sys.stdout.write(html)
    return html


def get_title_by_md_file(file):
    with open(file) as f:
        source = f.read()

        md1 = markdown.Markdown(extensions=["markdown.extensions.meta"])
        md1.convert(source)
        md_meta = getattr(md1, "Meta")
        return md_meta["title"][0]

def parse_all_posts(folder):
    # here we parse all posts
    if folder=="":
        return ""
    
    links = [] 
    for file in glob.glob(f"{folder}/*"):

        title = get_title_by_md_file(file)
        file = file[len(folder):]
        links.append((file[1:-2]+"html", title))
    
    content = "<ul class='posts'>"
    for l in links:
        content += f"\n <li><a href='{l[0]}'>{l[1]}</a>"

    content += "\n </ul>"

    return content 