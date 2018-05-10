#!/usr/bin/python
# -*- coding: UTF-8 -*-

import rdflib

g = rdflib.Graph()

# ... add some triples to g somehow ...
g.parse("engenhariaFlorestalRDF.owl")

qres = g.query(
    """SELECT DISTINCT ?cidade ?pais
       WHERE {
          ?cidade localizado_em: ?pais
       }""")

for row in qres:
    print("%s knows %s" % row)