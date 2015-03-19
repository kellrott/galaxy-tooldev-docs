#!/usr/bin/env python

import yaml
import subprocess
import os
import string

handle = open("mkdocs.yml")
meta = yaml.load(handle.read())

text = {}
for src, dst in meta['imports']:
    cmd = "pandoc --from=rst --to=markdown %s " % (src)
    print "Exec", cmd
    process = subprocess.Popen(cmd, shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)

    out, err = process.communicate()
    text[dst] = out

for name in meta['templates']:
    with open(os.path.join('templates', name)) as handle:
        template = string.Template(handle.read())

    with open(os.path.join('docs', name), "w") as handle:
        handle.write(template.substitute(text))
