#!/usr/bin/env python3

# Code to automatically scrape ADS, and identify recent Dunlap publications and highlight authors.
# Written by Bryan Gaensler for Dunlap Hack Day, 4 June 2019

import warnings
warnings.filterwarnings("ignore")

# Enter your ADS token here
# See https://github.com/adsabs/adsabs-dev-api#access
token = 'your token here'

# Enter your department here
affil = 'your department here'

# Enter output path
outpath = '/output/path/here/publications.html'

# Number of papers to return
num = 20

# Max number of authors to list explicitly
maxauth = 5

import ads
import codecs
import datetime
import unidecode
import requests
from itertools import groupby

import html.entities
table = {k: '&{};'.format(v) for k, v in html.entities.codepoint2name.items()}

# Query ADS
# Uses https://ads.readthedocs.io/en/latest/

ads.config.token = token

# All papers associated with affil
papers = list(ads.SearchQuery(q="aff:"+affil, sort="date desc, bibcode desc", rows=num))

# Only first author papers associated with affil
#papers = list(ads.SearchQuery(q="pos(aff:\""+affil+"\",1)", sort="date desc, bibcode desc", rows=num))

authstr = ['' for x in range(num)]
pdate = ['' for x in range(num)]
title = ['' for x in range(num)]
bib = ['' for x in range(num)]
finalstr = ['' for x in range(num)]

for n,paper in enumerate(papers):
    for i in range(len(paper.author)):
        # Fix accents
        paper.author[i] = paper.author[i].translate(table)
        # Make authors in bold
        if affil in paper.aff[i]:
            paper.author[i] = "<strong>"+paper.author[i]+"</strong>"
        # Remove long author lists
        elif (i > maxauth):
            paper.author[i] = "..."
#   Eliminate multiple ellipses
    authstr[n] = ", ".join([x[0] for x in groupby(paper.author)])
    
#   Format date correctly, even if in the form 2019-00
    try:
        pdate[n] = datetime.datetime.strptime(paper.pubdate[0:7], "%Y-%m").strftime('%b %Y')
    except:
        pdate[n] = datetime.datetime.strptime(paper.pubdate[0:4], "%Y").strftime('%Y')
    title[n] = unidecode.unidecode(paper.title[0])
    bib[n] = paper.bibcode 
    finalstr[n] = '<a href="https://ui.adsabs.harvard.edu/abs/'+bib[n]+'" target="_blank">'+authstr[n]+', '+title[n]+', '+pdate[n]+'</a> <p>'


# Now write output to WWW

f = codecs.open(outpath,'w','utf-8')

f.write('<h3>Recent '+affil+' Publications ('+datetime.datetime.now().strftime("%b %d, %Y")+')</h3>'+'\n') 

for n in range(num):
    f.write(str(n+1)+'. '+finalstr[n]+'\n')
      
# All papers associated with affil
f.write('<p><a href="https://ui.adsabs.harvard.edu/#search/q=aff%3A%22'+affil+'%22&sort=date%20desc" target="_blank">Complete list >></a></p>')

# Only first author papers associated with affil
#f.write('<p><a href="https://ui.adsabs.harvard.edu/search/q=pos(aff%3A%22'+affil+'%22%2C1)&sort=date%20desc%2C%20bibcode%20desc" target="_blank">Complete list >></a></p>')

f.close()

