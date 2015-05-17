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

def find_attachments(doc):
    tmp = re.findall(r'\${image\?fileName=([^}]+)}', doc)
    return tmp

def load_doc(page):
    print "loading", page
    page_path = os.path.join("docs", page)
    with open(page_path) as handle:
        markdown = handle.read()
    new_text = markdown_clean(markdown)
    attachments = find_attachments(new_text)
    return new_text, attachments

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
    doc, attachments = load_doc(doc_config['pages'][0][0])
    src = {
         index_title : {
            'doc' : doc,
            'attachments' : attachments,
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
        page_title = "%s.%s - %s" % (SECTION_BASE, page_num, page[2])
        doc, attachments = load_doc(page[0])
        src[page_title] = {
            'doc' : doc,
            'attachments' : attachments,
            'wiki_id' : child_pages.get(page_title, None)
        }

    #https://github.com/Sage-Bionetworks/synapsePythonClient/blob/develop/synapseclient/client.py#L2822

    #print json.dumps(src, indent=4)
    for title, entry in src.items():
        if entry['wiki_id'] is None:
            print "creating new Page:", title
            wiki = synapseclient.wiki.Wiki(title=title,
                owner=PROJECT_ID,
                parentWikiId=WIKI_BASE,
                markdown=entry['doc'])
            wiki = syn.store(wiki)
        else:
            wiki = syn.getWiki(PROJECT_ID, entry['wiki_id'])
            if entry['doc'] != wiki.markdown:
                print "Updating Page", title
                wiki.markdown = entry['doc']
                wiki = syn.store(wiki)
            else:
                print "Skipping Page Update", title
        #scan attachments
        uri = "/entity/%s/wiki/%s/attachmenthandles" % (wiki.ownerId, wiki.id)
        attachments = syn.restGET(uri)
        for a in entry['attachments']:
            found = False
            for elem in attachments['list']:
                if elem['fileName'] == a: # could also put an md5 check here as well
                    found = True
            #find it
            if not found:
                print "Uploading Attachment", a
                wiki.update({'attachments':[os.path.join("images", a)]})
                syn.store(wiki)
            #syn._getFileHandle and syn.chunkedFileUpload.
            print a
