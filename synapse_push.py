#!/usr/bin/env python

import synapseclient
import yaml
import os
import re
import cgi
import json

PROJECT_ID = "syn2786217"
WIKI_BASE  = "74384"
SECTION_BASE = "3.5"


def html_encode_code_blocks(txt):
    pieces = txt.split("```")
    results = []
    for i,piece in enumerate(pieces):
        ## if we're inside a code block, HTML encode the content
        if i % 2 == 1:
            results.append(cgi.escape(piece))
        else:
            results.append(piece)
    return "```".join(results)


def markdown_clean(txt, encoding="utf-8"):
    """
    Escape characters used in Synapse markdown. Input string should be either an
    ascii string (str) or a unicode string.
    """

    ## make an effort to coerce the string into a unicode string
    try:
        txt = unicode(txt)
    except UnicodeDecodeError:
        try:
            txt = unicode(txt, encoding="UTF-8", errors="replace")
        except UnicodeDecodeError:
            pass

    ## Synapse uses # and ## rather than ==== and ---- for headings
    txt = re.sub(r"^(.*?)\n(=)+$", r"# \1", txt, flags=re.MULTILINE)
    txt = re.sub(r"^(.*?)\n(-)+$", r"## \1", txt, flags=re.MULTILINE)

    txt = html_encode_code_blocks(txt)

    return txt.encode(encoding)


def load_doc(page):
    print "loading", page
    page_path = os.path.join("docs", page)
    with open(page_path) as handle:
        markdown = handle.read()
    new_text = markdown_clean(markdown)
    return new_text

if __name__ == "__main__":
    syn = synapseclient.Synapse()
    syn.login()
    wiki_set = syn.getWikiHeaders(PROJECT_ID)
    child_pages = {}
    for c in wiki_set:
        if c.get('parentId', '') == WIKI_BASE:
            child_pages[c['title']] = c['id']

    print child_pages

    with open('mkdocs.yml') as handle:
        doc_config = yaml.load(handle.read())

    index = doc_config['pages'][0][0]
    index_title = "%s - %s" % (SECTION_BASE, doc_config['pages'][0][1])
    src = {
         index_title : {
            'doc' : load_doc(doc_config['pages'][0][0]),
            'wiki_id' : WIKI_BASE
        }
    }

    sections = []
    for page_num, page in enumerate(doc_config['pages'][1:]):
        if page[1] not in sections:
            sections.append(page[1])

    section_numbers = {}
    for i, s in enumerate(sections):
        section_numbers[s] = i

    #Load/Update other pages
    for page_num, page in enumerate(doc_config['pages'][1:]):
        page_title = "%s.%s.%s - %s" % (SECTION_BASE, section_numbers[page[1]], page_num, page[2])
        src[page_title] = {
            'doc' : load_doc(page[0]),
            'wiki_id' : child_pages.get(page_title, None)
        }

    #print json.dumps(src, indent=4)
    for title, entry in src.items():
        if entry['wiki_id'] is None:
            print "creating new Page:", title
            wiki = synapseclient.wiki.Wiki(title=title,
                owner=PROJECT_ID,
                parentWikiId=WIKI_BASE,
                markdown=entry['doc'])
            syn.store(wiki)
        else:
            wiki = syn.getWiki(PROJECT_ID, entry['wiki_id'])
            if entry['doc'] != wiki.markdown:
                print "Updating Page", title
                wiki.markdown = entry['doc']
                syn.store(wiki)
            else:
                print "Skipping Page Update", title
