#!/usr/bin/env python

import synapseclient
import yaml
import os
import re
import cgi

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


if __name__ == "__main__":
    syn = synapseclient.Synapse()
    syn.login()
    wiki_set = syn.getWikiHeaders(PROJECT_ID)
    child_pages = {}
    for c in wiki_set:
        if c.get('parentId', '') == WIKI_BASE:
            child_pages[c['title']] = c['id']

    with open('mkdocs.yml') as handle:
        doc_config = yaml.load(handle.read())

    #load the index
    index_path = os.path.join("docs", doc_config['pages'][0][0])
    with open(index_path) as handle:
        markdown = handle.read()
    new_text = markdown_clean(markdown)
    #compare to what is online
    wiki = syn.getWiki(PROJECT_ID, WIKI_BASE)
    if new_text != wiki.markdown:
        wiki.markdown = new_text
        syn.store(wiki)
    else:
        print "Skipping Page Update"

    #Load/Update other pages
    for page_num, page in enumerate(doc_config['pages'][1:]):
        page_path = os.path.join("docs", page[0])
        with open(page_path) as handle:
            markdown = handle.read()
        new_text = markdown_clean(markdown)
        title = page[1]
        page_title = "%s.%s - %s" % (SECTION_BASE, page_num, title)
        if page_title not in child_pages:
            print "creating new Page:", page_title
            wiki = synapseclient.wiki.Wiki(title=page_title,
                owner=PROJECT_ID,
                parentWikiId=WIKI_BASE,
                markdown=new_text)
            syn.store(wiki)
        else:
            wiki = syn.getWiki(PROJECT_ID, child_pages[page_title])
            print page
            if new_text != wiki.markdown:
                print "Updating Page", page
                wiki.markdown = new_text
                syn.store(wiki)
            else:
                print "Skipping Page Update", page
