#!/usr/bin/env python3

# Code to automatically scrape ADS, and identify recent Dunlap publications and highlight authors.
# Written by Bryan Gaensler for Dunlap Hack Day, 4 June 2019

# Enter your ADS token here
# See https://github.com/adsabs/adsabs-dev-api#access
token = 'your token here'

# Enter your department here
affil = 'your department here'

# Enter output path
outpath = '/output/path'

# Number of papers to return
num = 5

# Max number of authors to list explicitly
maxauth = 5

import ads
import datetime
import unidecode
import requests
from itertools import groupby


# Query ADS
# Uses https://ads.readthedocs.io/en/latest/

ads.config.token = token
papers = list(ads.SearchQuery(q="aff:"+affil, sort="pubdate", rows=num))


authstr = ['' for x in range(num)]
pdate = ['' for x in range(num)]
title = ['' for x in range(num)]
bib = ['' for x in range(num)]
finalstr = ['' for x in range(num)]

for n,paper in enumerate(papers):
    for i in range(len(paper.author)):
        # Make authors in bold
        if affil in paper.aff[i]:
            paper.author[i] = "<strong>"+paper.author[i]+"</strong>"
        # Remove long author lists
        elif (i > maxauth):
            paper.author[i] = "..."
#   Eliminate multiple ellipses
    authstr[n] = ", ".join([x[0] for x in groupby(paper.author)])
    
    pdate[n] = datetime.datetime.strptime(paper.pubdate[0:7], "%Y-%m").strftime('%b %Y')
    title[n] = unidecode.unidecode(paper.title[0])
    bib[n] = paper.bibcode 
    finalstr[n] = '<a href="https://ui.adsabs.harvard.edu/abs/'+bib[n]+'" target="_blank">'+authstr[n]+', '+title[n]+', '+pdate[n]+'</a> <p>'


# Now write output to WWW

f = open(outpath+"/publication_list.html","w")

f.write('<h3>Recent '+affil+' Publications</h3>'+'\n')
for n in range(num):
     f.write(str(n+1)+'. '+finalstr[n]+'\n')

f.write('<p><a href="https://ui.adsabs.harvard.edu/#search/q=aff%3A%22'+affil+'%22&sort=date%20desc" target="_blank">Complete list >></a></p>')
f.close()


