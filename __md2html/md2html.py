#!/usr/bin/env python
# coding=utf-8
"""
Executable file for mdtree https://github.com/menduo/mdtree
"""
import argparse
import sys, os
from os.path import join

up_path = lambda _path, n: os.sep.join(_path.split(os.sep)[:-n])
_p_parent_dir = up_path(os.path.abspath(__file__), 2)
_path_of_mdtree_dir = join(up_path(os.path.abspath(__file__), 2), "mdtree")


def parse_args():
    """
    Define and parse `optparse` options for command-line usage.
    """
    usage = """mdtree [options] [source file]"""
    desc = "convert markdown to html with TOC(Table of contents) tree"

    parser = argparse.ArgumentParser(usage=usage, description=desc)
    parser.add_argument("source", default="", help="source file, markdown")
    parser.add_argument("-t", "--target", dest="target",
                        help="Write output to TARGET. Defaults to STDOUT.")

    parser.add_argument("--css", dest="css", default=[], nargs="*", help="more css, http/s links")
    parser.add_argument("--js", dest="js", default=[],  nargs="*", help="more js, http/s links")
    parser.add_argument("--title", dest="title", default="", help="title")
    parser.add_argument("--template", dest="template", default="", help="html template")
    parser.add_argument("--md_folder", dest="md_folder", default="", help="folder to read all posts from")
    
    parser.add_argument("--to64", dest="to64", default=False, action="store_true",
                        help="convert local image to base64?")

    return parser.parse_args()


def main(c_func):  # pragma: no cover
    """Run Markdown from the command line."""

    args = parse_args()

    if not args.source:
        return

    print(args)
    params = {
        "source": args.source,
        "target": args.target,
        "title": args.title,
        "template": args.template,
        "css" : args.css,
        "js": args.js,
        "md_folder": args.md_folder
    }
    if args.to64:
        params.update({"to64": args.to64})

    c_func(**params)



from main import convert_from_file

if __name__ == '__main__':
    main(convert_from_file)